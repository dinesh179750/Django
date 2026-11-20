"""
Song catalogue (single source of truth).

To add your own song:
  1. Put   <slug>.mp3  in  static/audio/
           <slug>.mp4  in  static/video/   (a silent or normal video - audio comes from the mp3)
           <slug>.jpg  in  static/images/songs/
  2. Add one dictionary to the SONGS list below using the same slug.

All titles / names below are fictional. The music is original synthesized
audio created for this demo, so there are no copyright problems.
"""

SONGS = [
    {"id": 1, "slug": "neon-skyline", "title": "Neon Skyline", "singer": "Aria Vale",
     "author": "Rohan Kestrel", "movie": "Midnight Drive", "genre": "Synthwave", "year": 2024,
     "colors": ["#1b0b3a", "#ff2e93", "#ff4fd8"]},
    {"id": 2, "slug": "monsoon-lofi", "title": "Monsoon Lofi", "singer": "Mira Solenne",
     "author": "Dev Harlow", "movie": "Rainy Window", "genre": "Lofi", "year": 2023,
     "colors": ["#0f2a3d", "#3b6e8f", "#7fd6ff"]},
    {"id": 3, "slug": "golden-hour", "title": "Golden Hour", "singer": "Tara Winslow",
     "author": "Neel Aurelio", "movie": "Golden Hour", "genre": "Pop", "year": 2022,
     "colors": ["#ff7a2f", "#ffd36e", "#ffe29a"]},
    {"id": 4, "slug": "desert-caravan", "title": "Desert Caravan", "singer": "Zayan Oryx",
     "author": "Samira Dune", "movie": "Caravan of Sand", "genre": "World", "year": 2021,
     "colors": ["#7a2e12", "#e8a15a", "#ffb870"]},
    {"id": 5, "slug": "cosmic-drift", "title": "Cosmic Drift", "singer": "Lyra Nova",
     "author": "Orion Blake", "movie": "Stardust Odyssey", "genre": "Ambient", "year": 2025,
     "colors": ["#0a0a2e", "#4b2e83", "#9ea7ff"]},
    {"id": 6, "slug": "rooftop-groove", "title": "Rooftop Groove", "singer": "Jax Monroe",
     "author": "Nia Castell", "movie": "Rooftop Nights", "genre": "Funk", "year": 2024,
     "colors": ["#12372a", "#1fbf75", "#5dffb0"]},
    {"id": 7, "slug": "temple-bells", "title": "Temple Bells", "singer": "Meera Kaveri",
     "author": "Pranav Idris", "movie": "Temple Dawn", "genre": "World", "year": 2020,
     "colors": ["#5a1030", "#d9822b", "#ffd166"]},
    {"id": 8, "slug": "sunrise-waltz", "title": "Sunrise Waltz", "singer": "Elise Moreau",
     "author": "Luca Bellini", "movie": "Waltz of Dawn", "genre": "Pop", "year": 2019,
     "colors": ["#3a1c71", "#ffaf7b", "#ffd1a6"]},
    {"id": 9, "slug": "thunder-run", "title": "Thunder Run", "singer": "Kade Ironwood",
     "author": "Blaze Hartman", "movie": "Thunder Run", "genre": "Synthwave", "year": 2023,
     "colors": ["#101010", "#c1121f", "#ff5964"]},
    {"id": 10, "slug": "ocean-breeze", "title": "Ocean Breeze", "singer": "Isla Marlow",
     "author": "Theo Briar", "movie": "Ocean Breeze Summer", "genre": "Lofi", "year": 2022,
     "colors": ["#023e58", "#19c3b1", "#6df2e0"]},
]

# Songs shown in the "Favourite songs" section the first time the site is opened
DEFAULT_FAVOURITES = [1, 3, 6, 7, 10]
