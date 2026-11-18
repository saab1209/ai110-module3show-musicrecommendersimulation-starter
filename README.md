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

PROFILE: 5. Weight Shift Experiment (Energy x2.0, Genre x0.5)
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'genre_weight': 0.5, 'energy_weight': 2.0}
------------------------------------------------------------
1. Sunrise City by Neon Echo (pop, happy) - Score: 3.46
   Because: genre match (+0.5), mood match (+1.0), energy closeness (+1.96)
2. Havana Breeze by Mateo Sol (latin, happy) - Score: 2.98
   Because: mood match (+1.0), energy closeness (+1.98)
3. Rooftop Lights by Indigo Parade (indie pop, happy) - Score: 2.92
   Because: mood match (+1.0), energy closeness (+1.92)
4. Lagos Sun by Kofi Blaze (afrobeats, happy) - Score: 2.90
   Because: mood match (+1.0), energy closeness (+1.90)
5. Gym Hero by Max Pulse (pop, intense) - Score: 2.24
   Because: genre match (+0.5), energy closeness (+1.74)
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

* **Diverse & Adversarial User Profiles:** Tested four distinct listener profiles (`High-Energy Pop`, `Chill Lofi Study`, `Intense Rock Workout`, and an adversarial `High-Energy Sad Metal` profile). When given conflicting traits (`metal` + `sad` + `0.90 energy`), *Iron Collapse* (`metal`, `intense`, `0.96 energy`) still ranked #1 because `genre` (`+2.0`) and `energy` (`+0.94`) outweighed the `mood` mismatch, whereas *Autumn Nocturne* (`classical`, `sad`, `0.22 energy`) only earned `+1.0` for mood.
* **Weight Shift Experiment (Genre `2.0 -> 0.5`, Energy `1.0 -> 2.0`):** Lowering the `genre` bonus and doubling `energy` closeness broke the pop filter bubble. Cross-genre tracks like *Havana Breeze* (`latin`, `happy`, `0.81 energy`) and *Lagos Sun* (`afrobeats`, `happy`, `0.85 energy`) jumped ahead of *Gym Hero* (`pop`, `intense`, `0.93 energy`), producing recommendations that matched the user's upbeat vibe far better than strict genre matching.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

* **Tiny Catalog Size:** The recommender only works on a small 20-song CSV catalog (`data/songs.csv`), which limits variety and forces the system to fill top-$K$ slots with partial matches when a listener requests a niche genre or mood.
* **No Understanding of Lyrics or Language:** Because the algorithm relies solely on numeric audio scores (`energy`, `tempo_bpm`, `valence`) and single-word tags, it cannot read lyrics, detect vocal language, or recognize sensitive themes and cultural context.
* **Over-Favoring One Genre or Mood (Filter Bubble):** Awarding `+2.0` points for an exact genre match causes the system to over-favor tracks from the same genre even when the mood clashes—such as ranking an `intense` pop song above a `happy` Latin or Afrobeats track for a listener seeking happy music.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building and stress-testing this simulation showed me how recommender systems turn raw song metadata into ranked predictions through explicit mathematical rules. By converting qualitative musical traits like `genre`, `mood`, and `energy` into numerical points and distance scores, the algorithm transforms subjective listening preferences into a repeatable ranking formula—showing that predictions are simply the direct result of the features and weights an engineer chooses to prioritize.

Testing diverse and adversarial listener profiles also revealed how easily bias and unfairness can emerge in systems like this. When `genre` carries a high weight (`+2.0`), the recommender creates a filter bubble that rewards exact label matches even when the mood clashes, while underrepresenting niche genres and ignoring lyrics or cultural context. Small design choices—such as feature weights or catalog representation—directly shape which artists get surfaced and which listeners get overlooked.

