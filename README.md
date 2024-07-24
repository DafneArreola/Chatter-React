# Chatter 
## Description 
Chatter is a web application that leverages Spotify and The Movie Database API to facilitate a centralized hub for lovers of multiple forms of media and entertainment, specifically movies, shows, and music.
Chatter allows people to share their thoughts on media with their friends without having to find a sliver of time in each others busy schedules to coordinate a watch party, or a listen party. Instead they can do it on their own time but react to their friends opinions as if they were texting each other at the exact same time without spoiling any of the fun


This project was built with Python(Flask), and SQLite, utilizing the aforementioned API's to provide media-specific information.
Users can rate and indulge in commentary at any point in time through live commenting, allowing our users to react and interact with others opinions in real time for media new and old

## Requirements 
Ensure you have the following dependcies installed:

```
Flask~=3.0.3
Flask-SQLAlchemy
python-dotenv
requests
wtforms
flask_wtf
Flask-Migrate
SearchForm
flask_wtf 
flask-socketio
flask-login
```

## Setting Up
Follow these steps to install Chatter locally

### Environment Variables
  1. To obtain access to The Movie Database API, register for an API ket at [TMDB API Basics](https://developer.themoviedb.org/docs/getting-started/).
  2. To obtain access to Spotify API, register for an API ket at [Spotify Developer Portal](https://developer.spotify.com/documentation/web-api/tutorials/getting-started/).
  3. Now export your acquired API Key and Access Token as enviornment variables:

 ```bash
  export MOVIE_API_KEY=your-api-key
  export MOVIE_ACCESS_TOKEN=your-access-toke
  export TV_API_KEY=your-api-key
  export TV_ACCESS_TOKEN=your-acess-token
  export MUSIC_CLIENT_ID=your-client-id
  export MUSIC_CLIENT_SECRET=your-client-secret-key
   ```

### Install Dependencies
1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/Media-Live-Reactions.git
   ```
2. Navigate to the project directory:

   ```bash
   cd Media-Live Reactions
   ```

3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```
## How to Run

1. Run the application using Flask's development server:

   

   ```bash
   flask run
   ```

3. Access the application in your web browser at `http://localhost:5000`.
