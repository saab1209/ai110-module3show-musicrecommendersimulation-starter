# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful. 

How System Works:
 Real-world platforms like Spotify and TikTok predict what listeners want by combining **collaborative filtering** (finding patterns across millions of users' likes, skips, and playlists) with **content-based filtering** (matching audio characteristics directly to a user's listening history). Because this simulation runs offline without live behavioral logs from millions of users, it uses a **content-based weighted scoring model**. My version prioritizes categorical vibe matches (`genre` and `mood`) first, then refines recommendations using numerical closeness on `energy`, `valence`, and `tempo_bpm`.

 ## Data Model & Features
* **`Song` Features:** `id`, `title`, `artist`, `genre`, `mood`, `energy` (0.0–1.0), `valence` (0.0–1.0), `tempo_bpm`, and `popularity`.
* **`UserProfile` Features:** `preferred_genres`, `preferred_moods`, `target_energy`, `target_valence`, `target_tempo`, and configurable feature weights (`genre_weight`, `mood_weight`, `energy_weight`, `valence_weight`, `tempo_weight`).

### Scoring & Ranking Logic
1. **Scoring Rule (Per Song):** Each song starts at `0.0` points. Matching a user's preferred `genre` adds `2.0` points, matching `mood` adds `1.5` points, and numerical features (`energy`, `valence`, `tempo_bpm`) add weighted points based on inverse distance (`1 - abs(song_val - target_val) / max_range`) so tracks closest to the user's target score highest.
2. **Ranking Rule (Full Catalog):** After every song is scored, the recommender sorts the entire catalog in descending order by score (breaking ties using `popularity` and `title`) and returns the top $N$ tracks.

### Finalized Algorithm Recipe & Expected Biases
* **Data Flow:** `UserProfile` + `data/songs.csv` $\rightarrow$ Loop through every track in the catalog and compute a weighted compatibility score $\rightarrow$ Sort tracks in descending order by score $\rightarrow$ Return the Top $K$ recommendations with score breakdowns.
* **Point-Weighting Recipe:**
  * **Genre Match:** `+2.0` points if `song.genre` matches the user's preferred genre (`0.0` otherwise).
  * **Mood Match:** `+1.0` point if `song.mood` matches the user's preferred mood (`0.0` otherwise).
  * **Numerical Closeness (`energy`, `valence`, `tempo_bpm`, `danceability`, `acousticness`):** Up to `+1.0` point each based on inverse normalized distance (`1 - abs(song_val - target_val) / max_range`), rewarding songs closest to the user's target vibe rather than simply the highest values.
* **Expected Algorithmic Biases:** Because `genre` carries the highest weight (`+2.0`), the system can create a **genre filter bubble**—over-favoring tracks in the user's preferred genre even when their mood or energy misses the mark, while burying strong cross-genre matches that fit the exact vibe.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



