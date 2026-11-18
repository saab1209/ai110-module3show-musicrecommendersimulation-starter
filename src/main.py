"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_profile_results(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print("=" * 60)
    print(f"PROFILE: {label}")
    print(f"Preferences: {user_prefs}")
    print("-" * 60)
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']} ({song['genre']}, {song['mood']}) - Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    profiles = {
        "1. High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "2. Chill Lofi Study": {"genre": "lofi", "mood": "chill", "energy": 0.38},
        "3. Intense Rock Workout": {"genre": "rock", "mood": "intense", "energy": 0.92},
        "4. Adversarial Edge Case (High-Energy Sad Metal)": {"genre": "metal", "mood": "sad", "energy": 0.90},
        "5. Weight Shift Experiment (Energy x2.0, Genre x0.5)": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "genre_weight": 0.5,
            "energy_weight": 2.0,
        },
    }

    for label, prefs in profiles.items():
        print_profile_results(label, prefs, songs, k=5)


if __name__ == "__main__":
    main()
