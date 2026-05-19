# Movie App v2

A full stack ML-powered movie discovery and recommendation web app. It features semantic search and personalized recommendations using sentence transformers.

**[Live Demo](https://movie-app-production-d6e9.up.railway.app/base)** | **[GitHub](https://github.com/manrajstudios-spec/Movie-APP-v2)**

---

## Screenshots
Home Page
<img width="1920" height="1080" alt="Screenshot From 2026-05-19 16-01-25" src="https://github.com/user-attachments/assets/548cd1dd-76c0-4887-9366-f6f0ee072683" />

Sign In
<img width="1920" height="1080" alt="Screenshot From 2026-05-19 16-01-36" src="https://github.com/user-attachments/assets/26757ae3-9c75-4eca-990d-de546b8bbafe" />

Menu
<img width="1920" height="1080" alt="Screenshot From 2026-05-19 16-01-44" src="https://github.com/user-attachments/assets/1d914bd1-4844-4a4d-8200-51d852345986" />

List movies
<img width="1920" height="1080" alt="Screenshot From 2026-05-19 16-02-17" src="https://github.com/user-attachments/assets/46da291f-07be-4043-a984-2c45bbb955d1" />

watch movie
<img width="1920" height="1080" alt="Screenshot From 2026-05-19 16-02-21" src="https://github.com/user-attachments/assets/33f901fb-79cf-4b27-9b76-775fd84fa6cb" />

rating page 
<img width="1920" height="1080" alt="Screenshot From 2026-05-19 16-12-17" src="https://github.com/user-attachments/assets/565be95d-2236-4c72-9433-fd9abcd0a5ef" />

---

## Features

- **Semantic Search**: Search movies by description using sentence transformers instead of just keywords.
- **Personalized Recommendations**: Get recommendations based on your watch history using cosine similarity on semantic embeddings.
- **Similar Movies**: Find movies similar to any movie you select.
- **Filter Movies**: Filter by genre, rating, and votes with a weighted scoring system.
- **Random Movie**: Discover something new.
- **Surprise Me**: Picks a random watched movie and finds similar ones.
- **Watchlist**: Save movies to watch later.
- **Watch History**: Track everything you've watched with timestamps.
- **Ratings and Reviews**: Rate and review movies.
- **YouTube Trailer**: Open any movie's trailer directly.
- **User Authentication**: Register and login with bcrypt hashed passwords.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask |
| Database | MongoDB Atlas |
| ML / Search | Sentence Transformers (all-MiniLM-L6-v2) |
| Similarity | Scikit-learn Cosine Similarity |
| Fuzzy Search | RapidFuzz |
| Data | TMDB 5000 Movie Dataset |
| Posters | TMDB API |
| Auth | bcrypt |
| Deployment | Railway |

---

## How the Recommendation System Works

**Semantic Search:**
User enters keywords; sentence transformer encodes the query; cosine similarity is calculated against precomputed movie embeddings; results are ranked.

**Personalized Recommendations:**
Each watched movie is embedded using a mix of overview, genres, and keywords. Cosine similarity is computed between all watched movie embeddings and all unwatched movies. The mean similarity across watched movies is taken, naturally weighing the genres you watch most. Results are ranked by a weighted score that combines similarity, rating, and vote count.

**Why Sentence Transformers over TF-IDF:**
TF-IDF matches keywords. Sentence transformers match meaning. "A criminal who steals corporate secrets" and "a thief who takes company information" are the same in meaning. Sentence transformers find that link, while TF-IDF does not.

---

## Run Locally

```bash
git clone https://github.com/manrajstudios-spec/Movie-APP-v2
cd Movie-APP-v2
pip install -r requirements.txt
```

Set environment variables:
```
MONGODB_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
TMDB_API_KEY=your_tmdb_api_key
```

Run:
```bash
python Scripts/app.py
```

---

## Project Structure

```
Movie-APP-v2/
├── Scripts/
│   ├── app.py                        # Flask routes
│   ├── Movie_Manager.py              # Core movie logic
│   ├── Movie_Recommendation_Manager.py  # ML recommendation engine
│   ├── Data_Loader.py                # Dataset loading and cleaning
│   ├── User_Saving.py                # User auth and storage
│   └── db.py                         # MongoDB connection
├── templates/                        # Jinja2 HTML templates
├── static/                           # CSS and assets
├── Data/                             # Dataset and precomputed embeddings
├── requirements.txt
└── Procfile
```

---

## What I Learned

- Building a semantic recommendation system using sentence transformer embeddings.
- Precomputing and storing embeddings for efficient runtime inference.
- Designing a weighted scoring system that combines similarity, rating, and popularity.
- Flask application structure with clear separation of concerns.
- Integrating MongoDB Atlas with proper indexing.
- Deploying ML applications to production using Railway.
- Managing environment variables and production configuration.

---

Built by [Manraj](https://github.com/manrajstudios-spec)
