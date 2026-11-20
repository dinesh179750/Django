/* =====================================================================
   MelodyHub - player logic (plain JavaScript, no libraries)
   One audio element is the "master clock"; the muted video follows it,
   so pause / resume / seek / next always affect both together.
   ===================================================================== */
(() => {
  'use strict';

  /* ------------------------------------------------------------ helpers */
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmt = (t) => {
    if (!isFinite(t) || t < 0) t = 0;
    const m = Math.floor(t / 60), s = Math.floor(t % 60);
    return m + ':' + String(s).padStart(2, '0');
  };
  const store = {
    get(key, fallback) { try { const v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; } },
    set(key, val) { try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) { /* storage blocked */ } },
  };
  const EQ = '<span class="eq" aria-hidden="true"><i></i><i></i><i></i></span>';

  /* --------------------------------------------------------------- data */
  const songs = JSON.parse($('#songs-data').textContent);
  const defaultFavs = JSON.parse($('#default-favs').textContent);
  const byId = (id) => songs.find((s) => s.id === Number(id));

  const audio = $('#audio');
  const video = $('#video');

  const state = {
    index: 0,
    favs: store.get('mh_favs', defaultFavs).filter((id) => byId(id)),
    user: store.get('mh_user', null),
    scrubbing: false,
  };
  const current = () => songs[state.index];

  /* ------------------------------------------------------------- toast */
  let toastTimer;
  function toast(msg) {
    const el = $('#toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2200);
  }

  /* --------------------------------------------------------- rendering */
  function renderFavourites() {
    const cur = current();
    $('#fav-list').innerHTML = state.favs.map((id) => {
      const s = byId(id);
      return `<li class="fav-item${s.id === cur.id ? ' is-active' : ''}">
        <button type="button" class="fav-main" data-play="${s.id}" aria-label="Play ${esc(s.title)}">
          <img src="${s.image}" alt="" width="64" height="64" loading="lazy">
          <span class="meta"><b>${esc(s.title)}</b><small>${esc(s.singer)}</small><small>${esc(s.movie)}</small></span>
          ${EQ}
        </button>
        <button type="button" class="fav-remove" data-remove="${s.id}" aria-label="Remove ${esc(s.title)} from favourites" title="Remove">&times;</button>
      </li>`;
    }).join('');
    $('#fav-empty').hidden = state.favs.length > 0;
  }

  function similarTo(song) {
    const others = songs.filter((s) => s.id !== song.id);
    const same = others.filter((s) => s.genre === song.genre);
    const rest = others.filter((s) => s.genre !== song.genre);
    const k = rest.length ? song.id % rest.length : 0;           // rotate so lists differ per song
    return [...same, ...rest.slice(k), ...rest.slice(0, k)].slice(0, 4);
  }

  function renderSimilar() {
    $('#similar-list').innerHTML = similarTo(current()).map((s) => `<li>
      <button type="button" class="sim-item" data-play="${s.id}" aria-label="Play ${esc(s.title)}">
        <img src="${s.image}" alt="" width="52" height="52" loading="lazy">
        <span class="meta"><b>${esc(s.title)}</b><small>${esc(s.singer)} &middot; ${esc(s.genre)}</small></span>
      </button></li>`).join('');
  }

  function renderCurrent() {
    const s = current();
    // card 1
    const img = $('#now-img');
    img.src = s.image; img.alt = 'Cover of ' + s.title;
    $('#now-title').textContent = s.title;
    $('#now-details').innerHTML =
      `<li><b>${esc(s.singer)}</b></li><li>${esc(s.movie)}</li><li>${esc(s.genre)}</li><li>${s.year}</li>`;
    // video section 2
    $('#info-title').textContent = s.title;
    $('#info-singer').textContent = s.singer;
    $('#info-author').textContent = s.author;
    $('#info-movie').textContent = s.movie;
    $('#info-genre').textContent = s.genre;
    $('#info-year').textContent = s.year;
    // footer
    const f = $('#f-img'); f.src = s.image; f.alt = 'Cover of ' + s.title;
    $('#f-title').textContent = s.title;
    $('#f-artist').textContent = s.singer + ' \u00b7 ' + s.movie;

    renderFavourites();
    renderSimilar();
    renderFavButton();
    updatePlayUI();

    if ('mediaSession' in navigator && window.MediaMetadata) {
      try {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: s.title, artist: s.singer, album: s.movie,
          artwork: [{ src: s.image, sizes: '600x600', type: 'image/jpeg' }],
        });
      } catch (e) { /* ignore */ }
    }
  }

  function renderFavButton() {
    const on = state.favs.includes(current().id);
    const btn = $('#now-fav');
    btn.setAttribute('aria-pressed', String(on));
    $('.heart', btn).innerHTML = on ? '&#9829;' : '&#9825;';
    $('#now-fav-label').textContent = on ? 'In favourites' : 'Favourite';
  }

  /* --------------------------------------------------------- favourites */
  function toggleFav(id) {
    id = Number(id);
    const i = state.favs.indexOf(id);
    if (i >= 0) { state.favs.splice(i, 1); toast('Removed from favourites'); }
    else { state.favs.push(id); toast('Added to favourites'); }
    store.set('mh_favs', state.favs);
    renderFavourites();
    renderFavButton();
  }

  /* ---------------------------------------------------------- playback */
  async function play() {
    try { await audio.play(); }
    catch (e) { if (e.name !== 'AbortError') toast('Press play again to start the music'); }
  }
  const pause = () => audio.pause();
  const togglePlay = () => (audio.paused ? play() : pause());

  function setSong(i, { play: autoplay = false } = {}) {
    state.index = (i + songs.length) % songs.length;
    const s = current();
    audio.pause();
    audio.src = s.audio;
    video.src = s.video;
    video.poster = s.image;
    audio.currentTime = 0;
    store.set('mh_last', s.id);
    $('#seek').value = 0; setFill($('#seek'));
    $('#t-cur').textContent = '0:00'; $('#t-dur').textContent = '0:00';
    renderCurrent();
    if (autoplay) play();
  }
  const playSongById = (id) => {
    const idx = songs.findIndex((s) => s.id === Number(id));
    if (idx === state.index) { play(); return; }          // same song: just make sure it plays
    setSong(idx, { play: true });
  };
  const next = () => setSong(state.index + 1, { play: true });
  const prev = () => {
    if (audio.currentTime > 3) { audio.currentTime = 0; syncVideo(true); return; }
    setSong(state.index - 1, { play: true });
  };

  function updatePlayUI() {
    const playing = !audio.paused;
    document.body.classList.toggle('is-playing', playing);
    const b = $('#btn-play');
    // SVG elements have no .hidden property, so toggle the attribute instead
    $('.i-play', b).toggleAttribute('hidden', playing);
    $('.i-pause', b).toggleAttribute('hidden', !playing);
    b.setAttribute('aria-label', playing ? 'Pause' : 'Play');
    $('#now-play').textContent = playing ? 'Pause' : 'Play';
    document.title = (playing ? '\u25B6 ' : '') + current().title + ' - MelodyHub';
  }

  function syncVideo(force) {
    if (!isFinite(audio.currentTime)) return;
    if (force || Math.abs(video.currentTime - audio.currentTime) > 0.4) {
      try { video.currentTime = audio.currentTime; } catch (e) { /* video not ready yet */ }
    }
  }

  /* ------------------------------------------------------ progress bar */
  function setFill(input) {
    const min = Number(input.min || 0), max = Number(input.max || 100);
    input.style.setProperty('--p', ((input.value - min) / (max - min)) * 100 + '%');
  }

  audio.addEventListener('play', () => { video.play().catch(() => {}); updatePlayUI(); });
  audio.addEventListener('pause', () => { video.pause(); updatePlayUI(); });
  audio.addEventListener('ended', next);
  audio.addEventListener('seeked', () => syncVideo(true));
  audio.addEventListener('waiting', () => video.pause());
  audio.addEventListener('playing', () => { if (video.paused) video.play().catch(() => {}); });
  audio.addEventListener('loadedmetadata', () => { $('#t-dur').textContent = fmt(audio.duration); syncVideo(true); });
  audio.addEventListener('durationchange', () => { $('#t-dur').textContent = fmt(audio.duration); });
  audio.addEventListener('timeupdate', () => {
    if (!state.scrubbing && audio.duration) {
      $('#seek').value = (audio.currentTime / audio.duration) * 1000;
      setFill($('#seek'));
    }
    if (!state.scrubbing) $('#t-cur').textContent = fmt(audio.currentTime);
    if (!audio.paused) syncVideo(false);
  });
  audio.addEventListener('error', () => { if (audio.src) toast('Could not load this song'); });

  const seek = $('#seek');
  seek.addEventListener('pointerdown', () => { state.scrubbing = true; });
  seek.addEventListener('input', () => {
    setFill(seek);
    if (audio.duration) {
      const t = (seek.value / 1000) * audio.duration;
      $('#t-cur').textContent = fmt(t);
      audio.currentTime = t;
    }
  });
  const endScrub = () => { state.scrubbing = false; };
  seek.addEventListener('change', endScrub);
  seek.addEventListener('pointerup', endScrub);
  seek.addEventListener('keyup', endScrub);

  /* ------------------------------------------------------------ volume */
  const volume = $('#volume');
  const ICON_VOL = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4z" fill="currentColor"/>';
  const ICONS = {
    high: ICON_VOL + '<path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>',
    low: ICON_VOL + '<path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>',
    mute: ICON_VOL + '<path d="m16 9 5 6M21 9l-5 6"/></svg>',
  };
  function updateVolumeUI() {
    const muted = audio.muted || audio.volume === 0;
    volume.value = muted ? 0 : audio.volume;
    setFill(volume);
    const btn = $('#btn-mute');
    btn.innerHTML = muted ? ICONS.mute : audio.volume < 0.5 ? ICONS.low : ICONS.high;
    btn.setAttribute('aria-label', muted ? 'Unmute' : 'Mute');
  }
  volume.addEventListener('input', () => {
    audio.volume = Number(volume.value);
    audio.muted = audio.volume === 0;
    store.set('mh_vol', audio.volume);
    updateVolumeUI();
  });
  $('#btn-mute').addEventListener('click', () => {
    if (audio.muted || audio.volume === 0) {
      audio.muted = false;
      if (audio.volume === 0) audio.volume = store.get('mh_vol', 0.8) || 0.8;
    } else {
      audio.muted = true;
    }
    updateVolumeUI();
  });

  /* ------------------------------------------------------ click wiring */
  $('#btn-play').addEventListener('click', togglePlay);
  $('#btn-next').addEventListener('click', next);
  $('#btn-prev').addEventListener('click', prev);
  $('#video-toggle').addEventListener('click', togglePlay);
  $('#now-play').addEventListener('click', togglePlay);
  $('#now-fav').addEventListener('click', () => toggleFav(current().id));

  document.addEventListener('click', (e) => {
    const rm = e.target.closest('[data-remove]');
    if (rm) { toggleFav(rm.dataset.remove); return; }
    const pl = e.target.closest('[data-play]');
    if (pl) playSongById(pl.dataset.play);
  });

  document.addEventListener('keydown', (e) => {
    if (e.code !== 'Space') return;
    const t = e.target;
    if (t.closest('input, textarea, button, a, select, [role="dialog"]')) return;
    e.preventDefault();
    togglePlay();
  });

  if ('mediaSession' in navigator) {
    try {
      navigator.mediaSession.setActionHandler('play', play);
      navigator.mediaSession.setActionHandler('pause', pause);
      navigator.mediaSession.setActionHandler('previoustrack', prev);
      navigator.mediaSession.setActionHandler('nexttrack', next);
    } catch (e) { /* not supported */ }
  }

  /* ------------------------------------------------------------ search */
  const sInput = $('#search-input');
  const sList = $('#search-results');

  function runSearch() {
    const q = sInput.value.trim().toLowerCase();
    if (!q) { sList.hidden = true; sList.innerHTML = ''; return; }
    const hits = songs.filter((s) => [s.title, s.singer, s.author, s.movie, s.genre].join(' ').toLowerCase().includes(q)).slice(0, 8);
    sList.innerHTML = hits.length
      ? hits.map((s) => `<li><button type="button" class="result-btn" data-result="${s.id}">
          <img src="${s.image}" alt="" width="44" height="44">
          <span class="meta"><b>${esc(s.title)}</b><small>${esc(s.singer)} &middot; ${esc(s.movie)}</small></span></button></li>`).join('')
      : '<li class="no-result">No songs found</li>';
    sList.hidden = false;
  }
  function closeSearch(clear) { sList.hidden = true; if (clear) { sInput.value = ''; sList.innerHTML = ''; } }

  sInput.addEventListener('input', runSearch);
  sInput.addEventListener('focus', runSearch);
  sInput.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeSearch(false); sInput.blur(); }
    else if (e.key === 'Enter') { const first = $('.result-btn', sList); if (first) first.click(); }
    else if (e.key === 'ArrowDown') { const first = $('.result-btn', sList); if (first) { e.preventDefault(); first.focus(); } }
  });
  sList.addEventListener('keydown', (e) => {
    const btns = $$('.result-btn', sList), i = btns.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); (btns[i + 1] || btns[0]).focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); (i <= 0 ? sInput : btns[i - 1]).focus(); }
    if (e.key === 'Escape') { closeSearch(false); sInput.focus(); }
  });
  sList.addEventListener('click', (e) => {
    const b = e.target.closest('[data-result]');
    if (!b) return;
    playSongById(b.dataset.result);
    closeSearch(true);
    sInput.blur();
  });
  document.addEventListener('click', (e) => { if (!e.target.closest('#search-box')) closeSearch(false); });

  /* --------------------------------------------------------- nav links */
  const menuBtn = $('#menu-toggle'), links = $('#nav-links');
  function setMenu(open) {
    links.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuBtn.addEventListener('click', () => setMenu(!links.classList.contains('open')));
  document.addEventListener('click', (e) => { if (!e.target.closest('#navbar')) setMenu(false); });
  window.addEventListener('resize', () => { if (window.innerWidth > 860) setMenu(false); });
  $$('[data-nav]').forEach((a) => a.addEventListener('click', (e) => {
    setMenu(false);
    if (a.dataset.nav === 'home') { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }
  }));

  /* ------------------------------------------------------------- login */
  const modal = $('#login-modal'), form = $('#login-form'), loginBtn = $('#login-btn'), err = $('#login-error');
  function renderLogin() { loginBtn.textContent = state.user ? 'Logout (' + state.user + ')' : 'Login'; }
  function openLogin() { err.hidden = true; form.reset(); modal.hidden = false; $('#login-user').focus(); }
  function closeLogin() { modal.hidden = true; loginBtn.focus(); }
  loginBtn.addEventListener('click', () => {
    if (state.user) { state.user = null; store.set('mh_user', null); renderLogin(); toast('Logged out'); }
    else openLogin();
  });
  $$('[data-close]', modal).forEach((el) => el.addEventListener('click', closeLogin));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !modal.hidden) closeLogin(); });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const user = $('#login-user').value.trim(), pass = $('#login-pass').value;
    if (user.length < 2 || !pass) { err.textContent = 'Please enter a username (2+ characters) and a password.'; err.hidden = false; return; }
    state.user = user;
    store.set('mh_user', user);
    renderLogin();
    modal.hidden = true;
    toast('Welcome, ' + user + '!');
  });

  /* ----------------------------------------------- keep layout in sync */
  function measure() {
    const root = document.documentElement.style;
    root.setProperty('--footer-h', $('#footer').offsetHeight + 'px');
    root.setProperty('--nav-h', $('#navbar').offsetHeight + 'px');
  }
  if ('ResizeObserver' in window) {
    const ro = new ResizeObserver(measure);
    ro.observe($('#footer')); ro.observe($('#navbar'));
  }
  window.addEventListener('resize', measure);

  /* -------------------------------------------------------------- init */
  const savedVol = store.get('mh_vol', 0.8);
  audio.volume = typeof savedVol === 'number' ? savedVol : 0.8;
  updateVolumeUI();
  renderLogin();
  const lastIdx = songs.findIndex((s) => s.id === store.get('mh_last', songs[0].id));
  setSong(lastIdx >= 0 ? lastIdx : 0);        // loads first song but does not autoplay (browsers block it)
  measure();
  window.addEventListener('load', measure);

  // tiny hook used by automated tests
  window.__melody = { state, setSong, songs };
})();
