import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Create a Spotify client instance with proper authentication using OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",  # Replace with your actual Spotify App client ID
    client_secret="YOUR_CLIENT_SECRET",  # Replace with your actual Spotify App client secret
    redirect_uri="http://localhost:8888/callback",  # Redirect URI set in your Spotify developer app
    scope="user-modify-playback-state,user-read-playback-state,user-read-currently-playing"  # Permissions required
))

# Define a function to search for and play a song by name
def play_song(song_name):
    try:
        # Search for the song on Spotify using the given song name
        results = sp.search(q=song_name, type='track', limit=1)
        
        # Extract the list of tracks from the search results
        tracks = results['tracks']['items']
        
        # Check if any track was found
        if tracks:
            # Get the URI of the first matching track
            track_uri = tracks[0]['uri']
            
            # Start playback of the track using its URI
            sp.start_playback(uris=[track_uri])
        else:
            # If no track was found, inform the user
            print("Song not found on Spotify.")
    except Exception as e:
        # Handle any exceptions (e.g., network errors, API errors)
        print(f"Error playing song on Spotify: {e}")


        # For YouTube links (if you want both YouTube and Spotify support):
music = {
    "Faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
    "Shape of You": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    # Add more songs as needed
}
