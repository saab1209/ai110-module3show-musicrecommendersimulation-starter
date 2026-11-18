# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch Weighted Recommender 1.0**

---

## 2. Intended Use  

**VibeMatch 1.0** is an educational content-based music recommendation simulator designed for classroom exploration and algorithmic transparency testing rather than commercial deployment. It generates ranked top-$K$ song playlists alongside plain-English explanations showing why each track was selected. The system assumes a listener can explicitly state their preferred genre, mood, and target energy level, and that musical similarity can be approximated from structured metadata alone without live listening history.

---

## 3. How the Model Works  

Imagine rating every song in a small library on a checklist before picking the top five tracks for a friend. First, the model checks if a song matches the listener's favorite genre and gives it **2.0 points** if it does. Next, it checks if the song matches their preferred mood and adds **1.0 point**. Then, it measures how close the song's energy level is to the listener's target energy—songs right on target earn up to **1.0 extra point**, while songs that are way too loud or too quiet earn closer to **0 points**. Finally, it sorts all songs from highest score to lowest and displays the top picks along with a short note explaining which features earned those points. Compared to the empty starter template, I implemented both a functional CLI pipeline (`load_songs`, `score_song`, `recommend_songs`) and an object-oriented `Recommender` class with configurable feature weights and tie-safe sorting.

---

## 4. Data  

The catalog (`data/songs.csv`) contains **20 songs** with 10 attributes per track (`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`). I expanded the original 10-song starter dataset by adding **10 diverse tracks** covering `r&b`, `afrobeats`, `metal`, `classical`, `latin`, `folk`, `hip-hop`, and `electronic`, alongside `sad` moods not present in the original file. Even after expansion, the catalog remains very small and lacks subgenres, lyrics, release year, cultural context, and user behavioral signals like skips or repeat plays.

---

## 5. Strengths  

* **Clear Vibe Alignment for Cohesive Profiles:** When a listener's preferences naturally align—such as `pop` + `happy` + `0.80 energy` (*Sunrise City*) or `lofi` + `chill` + `0.38 energy` (*Midnight Coding* and *Library Rain*)—the top recommendations match human musical intuition immediately.
* **Transparent Explanations:** Every recommendation includes an itemized breakdown (e.g., `genre match (+2.0), mood match (+1.0), energy closeness (+0.98)`), making it easy to verify why a track ranked first.
* **Tunable Weights:** Separating `genre_weight`, `mood_weight`, and `energy_weight` allows rapid experimentation without rewriting the core scoring loop.

---

## 6. Limitations and Bias  

Because `genre` carries the highest fixed weight (`+2.0`), the system suffers from a **genre filter bubble** that over-prioritizes exact genre labels even when the emotional mood clashes. For example, for a listener wanting upbeat `happy` pop (`energy: 0.80`), *Gym Hero* (`pop`, `intense`, `energy: 0.93`) ranked #2 (`2.87`) ahead of *Havana Breeze* (`latin`, `happy`, `energy: 0.81`) (`1.99`) simply because *Gym Hero* shared the `pop` label. In addition, the model ignores lyrics, vocal language, artist diversity, and listening history, and small catalogs with multiple tracks in one genre (`lofi` has 3 tracks while `jazz` has 2 and `metal` has 1) unintentionally favor overrepresented genres.

---

## 7. Evaluation  

I evaluated the system across four distinct listener profiles plus an adversarial edge case and a weight-sensitivity experiment:

* **High-Energy Pop vs. Chill Lofi Study:** High-Energy Pop surfaced upbeat, high-tempo tracks (*Sunrise City*, *Gym Hero*, *Havana Breeze*), whereas Chill Lofi shifted cleanly to low-energy acoustic tracks (*Midnight Coding*, *Library Rain*, *Spacewalk Thoughts*), confirming that energy distance and categorical rules separate opposite vibes effectively.
* **Intense Rock Workout vs. Adversarial High-Energy Sad Metal:** Intense Rock ranked *Storm Runner* (`rock`, `intense`, `0.91 energy`) first as expected. On the adversarial `High-Energy Sad Metal` profile (`genre: metal`, `mood: sad`, `energy: 0.90`), *Iron Collapse* (`metal`, `intense`, `0.96 energy`) still ranked #1 (`2.94`) over *Autumn Nocturne* (`classical`, `sad`, `0.22 energy`, score `1.32`) because `genre` + `energy` outweighed `mood`, showing how high genre weights can override emotional tone.
* **Weight Shift Experiment (`genre_weight=0.5`, `energy_weight=2.0`):** Reducing the genre bonus and doubling energy closeness allowed cross-genre `happy` tracks (*Havana Breeze*, *Lagos Sun*, *Rooftop Lights*) to rise above *Gym Hero*, producing a noticeably better playlist for the user's mood.

---

## 8. Future Work  

* **Multi-Feature & Normalized Scoring:** Incorporate `valence`, `tempo_bpm`, `danceability`, and `acousticness` by default alongside user-adjustable sliders so listeners can prioritize mood or tempo over genre.
* **Diversity Reranking (MMR):** Add a post-ranking diversity penalty so the top 5 recommendations do not repeat the same artist or genre back-to-back.
* **Implicit Feedback Loop:** Track simulated "likes" and "skips" to dynamically update a user's target energy and feature weights over time.

---

## 9. Personal Reflection  

Building this recommender showed me that recommendation algorithms are not magic—they are concrete mathematical trade-offs chosen by engineers. The most surprising discovery was how a simple `+2.0` genre weight immediately created a filter bubble that pushed an `intense` workout song ahead of `happy` cross-genre matches for a user who wanted happy music. It changed how I view apps like Spotify and TikTok by making me realize that every "For You" feed reflects specific weighting choices that can either broaden discovery or trap users inside narrow genre loops.
