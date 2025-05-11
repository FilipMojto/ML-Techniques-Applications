import requests
import random

BASE_URL = "http://localhost:5000"

def test_recommendation(username: str, n_likes: int, k_recommendations: int, method: str = "tfidf"):
    # 1. Create user (if not already exists)
    user_payload = {"username": username}
    res = requests.post(f"{BASE_URL}/user/", json=user_payload)
    if res.status_code == 409:
        print(f"User '{username}' already exists.")
    else:
        res.raise_for_status()
        print(f"User '{username}' created.")

    # 2. Fetch all available movies
    movies = requests.get(f"{BASE_URL}/movies/")
    movies.raise_for_status()
    movie_ids = [movie['movie_id'] for movie in movies.json()]
    
    if not movie_ids:
        raise ValueError("No movies found in the database.")

    # 3. Randomly like n movies
    liked_ids = random.sample(movie_ids, min(n_likes, len(movie_ids)))
    for movie_id in liked_ids:
        like_payload = {"username": username, "movie_id": movie_id}
        res = requests.post(f"{BASE_URL}/movies/like", json=like_payload)
        if res.status_code not in (200, 400):  # 400 = already liked
            print(f"Error liking movie ID {movie_id}: {res.text}")

    print(f"User '{username}' liked {len(liked_ids)} movies.")

    # 4. Get recommendations
    recommend_payload = {
        "username": username,
        "method": method,
        "no_of_recommendations": k_recommendations
    }

    response = requests.post(f"{BASE_URL}/recommend", json=recommend_payload)
    response.raise_for_status()
    recommendations = response.json()

    print(f"\nPrecision: {recommendations['precision']}")
    print(f"Recall: {recommendations['recall']}")
    print(f"F1 Score: {recommendations['f1_score']}")
    print("Recommendations:")
    for r in recommendations["recommendations"]:
        print("-", r["title"])

# Example usage:
test_recommendation("testuser_dynamic", n_likes=10, k_recommendations=100)