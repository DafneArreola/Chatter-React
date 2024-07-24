# Chatter

Welcome to Chatter, a dynamic website that combines movie, music, and TV show APIs to create an engaging social platform for media enthusiasts. Here, you can explore a vast range of media content, search for your favorite songs, movies, and TV shows, and participate in a community-driven review and comment system.

## Features

- **Homepage Integration**: Our homepage showcases the latest movies, TV shows, and music tracks through integrations with various APIs.
- **Search Functionality**: Use the search bar to find specific songs, movies, or TV shows.
- **User Accounts**: Create an account to log in and out, manage your profile, and keep track of your activities.
- **Review System**: Leave reviews on movies, TV shows, and music, and view reviews left by other users.
- **Timestamped Comments**: Add comments on specific timestamps within media content, allowing you to engage in discussions or share insights as you watch or listen.

## Tech Stack

- **Flask**: Python framework to handle routing, account creation, etc.
- **SQL**: Database handling of users, ratings, comments, etc. 
- **HTML/CSS**: Front-End implementation.
- **TMDB API**: Retrieve movie and show information.
- **SPOTIFY API**: Retrieve music information.


## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/DafneArreola/Media-Live-Reactions.git

2. **Install Dependencies**:
- Navigate to the project directory and install the required Python packages:

   ```bash
   pip install -r requirements.txt

3. **Set Up the Database**:
- Ensure your database configuration is set up correctly in config.py and initialize it:

   ```bash
   pip install flash -sqlite

4. **Run the Application**:
- Start the Flask application:

   ```bash
   python3 app.py

5. **Visit the Site**:
- Open your web browser and go to http://localhost:5000 to start exploring.

## Assistance
If you’d like to contribute to Media Hub, please fork the repository and submit a pull request with your changes. We welcome contributions that improve the functionality and user experience of the website.

## Contact
For any questions or support, please contact our director at darreola@vassar.edu.