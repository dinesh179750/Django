import mimetypes
import re

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse

from .songs import DEFAULT_FAVOURITES, SONGS

MEDIA_KINDS = {"audio": ".mp3", "video": ".mp4"}


def index(request):
    """Single page (index.html) that includes navbar, favourites, container, video and footer."""
    songs = []
    for s in SONGS:
        # Songs are listed only once their mp3 exists in static/audio/
        if not (settings.BASE_DIR / "static" / "audio" / f"{s['slug']}.mp3").is_file():
            continue
        item = dict(s)
        # cover / video fall back to a default if you haven't added your own
        cover = s["slug"] if (settings.BASE_DIR / "static" / "images" / "songs" / f"{s['slug']}.jpg").is_file() else "golden-hour"
        clip = s["slug"] if (settings.BASE_DIR / "static" / "video" / f"{s['slug']}.mp4").is_file() else "golden-hour"
        item["image"] = static(f"images/songs/{cover}.jpg")
        item["audio"] = reverse("player:stream", args=["audio", f"{s['slug']}.mp3"])
        item["video"] = reverse("player:stream", args=["video", f"{clip}.mp4"])
        songs.append(item)
    context = {
        "songs": songs,                       # rendered into the page with |json_script
        "default_favourites": DEFAULT_FAVOURITES,
    }
    return render(request, "player/index.html", context)


def stream(request, kind, filename):
    """
    Serve files from static/audio or static/video with Range support.

    Django's development server ignores the HTTP "Range" header, which stops browsers
    from seeking (clicking on the progress bar) in audio/video. This tiny view fixes that.
    The files still live in the static folder.
    """
    if kind not in MEDIA_KINDS or not filename.endswith(MEDIA_KINDS[kind]):
        raise Http404
    base = (settings.BASE_DIR / "static" / kind).resolve()
    path = (base / filename).resolve()
    if base not in path.parents or not path.is_file():      # blocks ../ tricks
        raise Http404

    size = path.stat().st_size
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    start, end, status = 0, size - 1, 200

    header = request.headers.get("Range", "")
    if header:
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", header.strip())
        if not m or (not m.group(1) and not m.group(2)):
            return HttpResponseBadRequest("Bad Range header")
        if m.group(1):
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else size - 1
        else:                                                # suffix range: last N bytes
            start = max(0, size - int(m.group(2)))
        end = min(end, size - 1)
        if start > end or start >= size:
            resp = HttpResponse(status=416)
            resp["Content-Range"] = f"bytes */{size}"
            return resp
        status = 206

    with open(path, "rb") as fh:
        fh.seek(start)
        data = fh.read(end - start + 1)

    resp = HttpResponse(data if request.method != "HEAD" else b"", status=status, content_type=ctype)
    resp["Accept-Ranges"] = "bytes"
    resp["Content-Length"] = str(len(data))
    if status == 206:
        resp["Content-Range"] = f"bytes {start}-{end}/{size}"
    resp["Cache-Control"] = "public, max-age=3600"
    return resp
