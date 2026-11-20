"""
Song catalogue (single source of truth).

To add your own song:
  1. Put   <slug>.mp3  in  static/audio/
           <slug>.mp4  in  static/video/   (a silent or normal video - audio comes from the mp3)
           <slug>.jpg  in  static/images/songs/
  2. Add one dictionary to the SONGS list below using the same slug.

The 10 demo songs below have fictional Telugu-style titles and names. The music is original synthesized
audio created for this demo, so there are no copyright problems.
"""

# --- The Paradise (Telugu, 2026) - music by Anirudh Ravichander ---------------
# Add your own legally obtained mp3 as static/audio/<slug>.mp3 and the song appears.
# (cover: static/images/songs/<slug>.jpg and clip: static/video/<slug>.mp4 are optional)
PARADISE = [
    {"id": 101, "slug": "aaya-sher", "title": "Aaya Sher", "singer": "—",
     "author": "—", "movie": "The Paradise", "genre": "Telugu", "year": 2026,
     "colors": ["#1a0a05", "#e8590c", "#fcc419"]},
    {"id": 102, "slug": "yeshanagula", "title": "Yeshanagula", "singer": "—",
     "author": "—", "movie": "The Paradise", "genre": "Telugu", "year": 2026,
     "colors": ["#1a0a05", "#c92a2a", "#fcc419"]},
]

SONGS = PARADISE + [
    {"id": 1, "slug": "neon-skyline", "title": "Raathri Rangulu", "singer": "Anvika Rao",
     "author": "Sai Kiran", "movie": "Nallani Vennela", "genre": "Telugu", "year": 2024,
     "colors": ["#1b0b3a", "#ff2e93", "#ff4fd8"]},
    {"id": 2, "slug": "monsoon-lofi", "title": "Vaana Jallu", "singer": "Harini Devi",
     "author": "Charan Teja", "movie": "Vaana Kaalam", "genre": "Telugu", "year": 2023,
     "colors": ["#0f2a3d", "#3b6e8f", "#7fd6ff"]},
    {"id": 3, "slug": "golden-hour", "title": "Bangaru Sandhya", "singer": "Sahithi Varma",
     "author": "Vamsi Krishna", "movie": "Sandhya Ragam", "genre": "Telugu", "year": 2022,
     "colors": ["#ff7a2f", "#ffd36e", "#ffe29a"]},
    {"id": 4, "slug": "desert-caravan", "title": "Edari Payanam", "singer": "Karthik Raju",
     "author": "Sameera Reddy", "movie": "Edari Gaadhalu", "genre": "Telugu", "year": 2021,
     "colors": ["#7a2e12", "#e8a15a", "#ffb870"]},
    {"id": 5, "slug": "cosmic-drift", "title": "Tara Teeram", "singer": "Vennela Rao",
     "author": "Aditya Varma", "movie": "Chukkala Loka", "genre": "Telugu", "year": 2025,
     "colors": ["#0a0a2e", "#4b2e83", "#9ea7ff"]},
    {"id": 6, "slug": "rooftop-groove", "title": "Meda Mida Masti", "singer": "Rakesh Chandra",
     "author": "Sneha Naidu", "movie": "Meda Rojulu", "genre": "Telugu", "year": 2024,
     "colors": ["#12372a", "#1fbf75", "#5dffb0"]},
    {"id": 7, "slug": "temple-bells", "title": "Gudi Gantalu", "singer": "Lakshmi Prasanna",
     "author": "Pavan Sharma", "movie": "Aalaya Prabhatam", "genre": "Telugu", "year": 2020,
     "colors": ["#5a1030", "#d9822b", "#ffd166"]},
    {"id": 8, "slug": "sunrise-waltz", "title": "Arunodaya Raagam", "singer": "Divya Sree",
     "author": "Mohan Kumar", "movie": "Ushodayam", "genre": "Telugu", "year": 2019,
     "colors": ["#3a1c71", "#ffaf7b", "#ffd1a6"]},
    {"id": 9, "slug": "thunder-run", "title": "Merupu Veta", "singer": "Rudra Tej",
     "author": "Bhanu Prakash", "movie": "Merupu Veta", "genre": "Telugu", "year": 2023,
     "colors": ["#101010", "#c1121f", "#ff5964"]},
    {"id": 10, "slug": "ocean-breeze", "title": "Sagara Teeram", "singer": "Keerthana Rao",
     "author": "Naveen Babu", "movie": "Samudra Geetham", "genre": "Telugu", "year": 2022,
     "colors": ["#023e58", "#19c3b1", "#6df2e0"]},
]

# Songs shown in the "Favourite songs" section the first time the site is opened
DEFAULT_FAVOURITES = [101, 102, 3, 6, 7]
