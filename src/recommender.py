import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Song:
    """Represents a song and its musical attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a listener's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Object-oriented recommendation engine for Song and UserProfile models."""

    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a catalog of Song objects."""
        self.songs = songs

    def _score_object(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Calculate compatibility score and human-readable reasons for a Song object."""
        score = 0.0
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append(f"genre match: {song.genre} (+2.00)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append(f"mood match: {song.mood} (+1.00)")

        energy_closeness = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        score += energy_closeness
        reasons.append(f"energy closeness ({energy_closeness:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.5:
            score += 0.5
            reasons.append("acoustic vibe (+0.50)")
        elif not user.likes_acoustic and song.acousticness < 0.5:
            score += 0.5
            reasons.append("non-acoustic vibe (+0.50)")

        return round(score, 4), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked from highest to lowest score."""
        scored = [
            (self._score_object(user, song)[0], song)
            for song in self.songs
        ]
        scored.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation string for why a song matches a user."""
        score, reasons = self._score_object(user, song)
        reason_text = ", ".join(reasons) if reasons else "general catalog fit"
        return f"Score {score:.2f} — {reason_text}"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields to int/float."""
    songs: List[Dict] = []
    with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"].strip(),
                "artist": row["artist"].strip(),
                "genre": row["genre"].strip(),
                "mood": row["mood"].strip(),
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a weighted compatibility score and explanation reasons for one song."""
    score = 0.0
    reasons: List[str] = []

    genre_weight = user_prefs.get("genre_weight", 2.0)
    mood_weight = user_prefs.get("mood_weight", 1.0)
    energy_weight = user_prefs.get("energy_weight", 1.0)

    pref_genre = str(user_prefs.get("genre", "")).strip().lower()
    if pref_genre and song.get("genre", "").strip().lower() == pref_genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    pref_mood = str(user_prefs.get("mood", "")).strip().lower()
    if pref_mood and song.get("mood", "").strip().lower() == pref_mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    if "energy" in user_prefs and "energy" in song:
        closeness = max(0.0, 1.0 - abs(float(song["energy"]) - float(user_prefs["energy"])))
        energy_pts = closeness * energy_weight
        score += energy_pts
        reasons.append(f"energy closeness (+{energy_pts:.2f})")

    if "valence" in user_prefs and "valence" in song:
        closeness = max(0.0, 1.0 - abs(float(song["valence"]) - float(user_prefs["valence"])))
        score += closeness
        reasons.append(f"valence closeness (+{closeness:.2f})")

    if "tempo_bpm" in user_prefs and "tempo_bpm" in song:
        closeness = max(0.0, 1.0 - abs(float(song["tempo_bpm"]) - float(user_prefs["tempo_bpm"])) / 140.0)
        score += closeness
        reasons.append(f"tempo closeness (+{closeness:.2f})")

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top k sorted highest to lowest."""
    scored_results: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "baseline match"
        scored_results.append((song, score, explanation))

    ranked = sorted(scored_results, key=lambda item: item[1], reverse=True)
    return ranked[:k]

