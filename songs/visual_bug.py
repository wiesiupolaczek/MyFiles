import os
import threading
import logging
from yt_dlp import YoutubeDL
from pathlib import Path
import customtkinter as ctk
import tkinter as tk
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import queue
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()  # Load the .env file

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Set to DEBUG for detailed logs
)

# Configure Spotipy logging
logger = logging.getLogger('spotipy')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)


def sanitize_filename(filename):
    """
    Remove or replace characters that are invalid in filenames.
    """
    # Replace invalid characters with an underscore
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


class YouTubeDownloaderApp:
    def __init__(self):
        # Spotify Credentials - loaded from environment variables
        self.spotify_client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.spotify_client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.spotify_redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        self.spotify_scope = "playlist-read-private"

        # Validate that all Spotify credentials are provided
        if not all([self.spotify_client_id, self.spotify_client_secret, self.spotify_redirect_uri]):
            raise EnvironmentError("Spotify credentials are not fully set in environment variables.")

        # Initialize Spotify Client
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret,
            redirect_uri=self.spotify_redirect_uri,
            scope=self.spotify_scope,
            cache_path=".cache-youtube_downloader"
        ))

        # Output directory and FFmpeg path
        self.output_directory = Path(os.getenv('OUTPUT_DIR', 'downloads'))
        self.ffmpeg_path = os.getenv('FFMPEG_PATH', 'ffmpeg')  # Default to 'ffmpeg' if not set

        # Validate FFmpeg path
        if not Path(self.ffmpeg_path).exists():
            raise FileNotFoundError(f"FFmpeg not found at {self.ffmpeg_path}")

        # Initialize the Tkinter window
        self.app = ctk.CTk()
        self.app.title("YouTube and Spotify Downloader")
        self.app.attributes("-fullscreen", True)
        self.app.bind("<Escape>", self.exit_fullscreen)

        # Configure grid layout for the main window
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)

        # Ensure the output directory exists
        if not self.output_directory.exists():
            self.output_directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {self.output_directory}")

        self.queue = queue.Queue()
        self.app.after(100, self.process_queue)

        # Create Sidebar and Frames
        self.create_sidebar()
        self.create_frames()

    def exit_fullscreen(self, event=None):
        """
        Exit fullscreen mode.
        """
        self.app.attributes("-fullscreen", False)
        logging.info("Exited fullscreen mode.")

    def create_sidebar(self):
        """
        Create the sidebar with navigation buttons.
        """
        sidebar = ctk.CTkFrame(self.app, width=200)
        sidebar.grid(row=0, column=0, sticky="nswe")

        # Prevent the sidebar from expanding
        self.app.grid_columnconfigure(0, weight=0)

        # Add buttons to navigate between frames
        spotify_button = ctk.CTkButton(
            sidebar,
            text="Spotify",
            command=lambda: self.show_frame("Spotify"),
            fg_color="blue",
            hover_color="#749dd9"
        )
        spotify_button.pack(padx=10, pady=10, fill="x")

        youtube_button = ctk.CTkButton(
            sidebar,
            text="YouTube",
            command=lambda: self.show_frame("YouTube"),
            fg_color="blue",
            hover_color="#749dd9"
        )
        youtube_button.pack(padx=10, pady=10, fill="x")

        # Add a Reset Button
        reset_button = ctk.CTkButton(
            sidebar,
            text="Reset",
            command=self.reset_app,
            fg_color="red",
            hover_color="#e74c3c"
        )
        reset_button.pack(padx=10, pady=10, fill="x")

    def create_frames(self):
        """
        Create different frames for each feature.
        """
        container = ctk.CTkFrame(self.app)
        container.grid(row=0, column=1, sticky="nswe")

        # Configure grid weights to allow resizing
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Spotify Downloader Frame
        spotify_frame = ctk.CTkFrame(container)
        spotify_frame.grid(row=0, column=0, sticky="nswe")
        self.frames = {}
        self.frames["Spotify"] = spotify_frame

        # YouTube Downloader Frame
        youtube_frame = ctk.CTkFrame(container)
        youtube_frame.grid(row=0, column=0, sticky="nswe")
        self.frames["YouTube"] = youtube_frame

        # Create Spotify and YouTube interfaces
        self.create_spotify_frame(spotify_frame)
        self.create_youtube_frame(youtube_frame)

        # Show Spotify frame by default
        self.show_frame("Spotify")

    def show_frame(self, frame_name):
        """
        Bring the selected frame to the front.
        """
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            logging.info(f"Switched to {frame_name} Downloader.")
        else:
            logging.error(f"Frame '{frame_name}' does not exist.")

    def create_spotify_frame(self, frame):
        """
        Create the Spotify Downloader interface.
        """
        # Label for Spotify
        spotify_label = ctk.CTkLabel(frame, text="Spotify Downloader", font=ctk.CTkFont(size=20, weight="bold"))
        spotify_label.pack(padx=10, pady=10, anchor="w")

        # Authenticate Button
        authenticate_button = ctk.CTkButton(
            frame,
            text="Authenticate Spotify",
            command=self.authenticate_spotify,
            fg_color="green",
            hover_color="#2ecc71"
        )
        authenticate_button.pack(padx=10, pady=10, fill="x")

        # Playlist Dropdown
        self.playlist_var = tk.StringVar()
        playlist_dropdown = ctk.CTkOptionMenu(
            frame,
            dynamic_resizing=False,
            variable=self.playlist_var,
            values=[],  # To be populated after authentication
            command=self.on_select_playlist,
            state="disabled"
        )
        playlist_dropdown.pack(padx=10, pady=10, fill="x")
        self.playlist_dropdown = playlist_dropdown

        # Download Button
        self.spotify_download_button = ctk.CTkButton(
            frame,
            text="Download Playlist",
            command=self.download_playlist,
            state="disabled"
        )
        self.spotify_download_button.pack(padx=10, pady=10, fill="x")

        # Status Label
        self.spotify_status_label = ctk.CTkLabel(frame, text="")
        self.spotify_status_label.pack(padx=10, pady=10, anchor="w")

    def authenticate_spotify(self):
        """
        Authenticate with Spotify and load playlists.
        """
        logging.info("Initiating Spotify authentication.")
        self.spotify_status_label.configure(text="Authenticating with Spotify...")
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri=self.spotify_redirect_uri,
                scope=self.spotify_scope,
                cache_path=".cache-youtube_downloader"
            ))
            # Attempt to fetch playlists
            self.load_spotify_playlists()
        except spotipy.exceptions.SpotifyException as se:
            self.spotify_status_label.configure(text="Spotify authentication failed: Spotify Exception.")
            logging.error("Spotify authentication failed due to SpotifyException.", exc_info=True)
        except Exception as e:
            self.spotify_status_label.configure(text="Spotify authentication failed: Unknown error.")
            logging.error("Spotify authentication failed due to an unexpected error.", exc_info=True)

    def load_spotify_playlists(self):
        """
        Load Spotify playlists after authentication.
        """
        try:
            playlists = []
            results = self.sp.current_user_playlists()
            playlists.extend(results['items'])
            while results['next']:
                results = self.sp.next(results)
                playlists.extend(results['items'])

            playlist_names = [playlist['name'] for playlist in playlists]
            self.playlist_dropdown.configure(values=playlist_names, state="normal")
            self.spotify_status_label.configure(text="Successfully authenticated with Spotify.")
            self.spotify_download_button.configure(state="normal")
            logging.info("Spotify authentication successful.")
        except spotipy.exceptions.SpotifyException as se:
            self.spotify_status_label.configure(text="Spotify authentication failed: Spotify Exception.")
            logging.error("Spotify authentication failed due to SpotifyException.", exc_info=True)
        except Exception as e:
            self.spotify_status_label.configure(text="Spotify authentication failed: Unknown error.")
            logging.error("Spotify authentication failed due to an unexpected error.", exc_info=True)

    def on_select_playlist(self, selected_playlist):
        """
        Handle playlist selection.
        """
        self.spotify_status_label.configure(text=f"Selected Playlist: {selected_playlist}")
        logging.info(f"Selected Playlist: {selected_playlist}")

    def download_playlist(self):
        """
        Download all songs from the selected Spotify playlist.
        """
        selected_playlist = self.playlist_var.get()
        if not selected_playlist:
            self.spotify_status_label.configure(text="Please select a playlist.")
            return

        # Fetch the playlist ID
        try:
            playlists = self.sp.current_user_playlists()
            playlist_id = None
            for playlist in playlists['items']:
                if playlist['name'] == selected_playlist:
                    playlist_id = playlist['id']
                    break

            if not playlist_id:
                self.spotify_status_label.configure(text="Failed to retrieve playlist ID.")
                logging.error("Failed to retrieve playlist ID.")
                return

            # Fetch all tracks from the playlist
            tracks = []
            results = self.sp.playlist_tracks(playlist_id)
            tracks.extend(results['items'])
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])

            self.spotify_status_label.configure(text=f"Found {len(tracks)} tracks. Starting download...")
            logging.info(f"Found {len(tracks)} tracks in playlist '{selected_playlist}'.")

            # Start download in a separate thread
            download_thread = threading.Thread(target=self.download_tracks, args=(tracks,), daemon=True)
            download_thread.start()

        except Exception as e:
            self.spotify_status_label.configure(text="Error fetching playlist tracks.")
            logging.error("Error fetching playlist tracks.", exc_info=True)

    def download_tracks(self, tracks):
        """
        Iterate through tracks and download each song.
        """
        for idx, item in enumerate(tracks):
            track = item['track']
            if not track:
                continue  # Skip if track is None
            song = track['name']
            artist = ", ".join([artist['name'] for artist in track['artists']])
            search_query = f"{song} by {artist}"
            self.queue.put((self.spotify_status_label.configure,
                            ({"text": f"Downloading {idx + 1}/{len(tracks)}: {song} by {artist}"})))
            logging.info(f"Downloading {idx + 1}/{len(tracks)}: {song} by {artist}")

            try:
                audio_filename = self.download_youtube_audio(search_query)
                logging.info(f"Downloaded: {audio_filename}")
            except Exception as e:
                logging.error(f"Failed to download: {search_query}", exc_info=True)
                self.queue.put(
                    (self.spotify_status_label.configure, ({"text": f"Error downloading: {song} by {artist}"})))

        self.queue.put((self.spotify_status_label.configure, ({"text": "Download completed for all tracks."})))
        logging.info("Completed downloading all tracks.")

    def create_youtube_frame(self, frame):
        """
        Create the YouTube Downloader interface.
        """
        # Label for YouTube
        youtube_label = ctk.CTkLabel(frame, text="YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold"))
        youtube_label.pack(padx=10, pady=10, anchor="w")

        # Create a tab view
        tab_view = ctk.CTkTabview(frame, width=700, height=600)
        tab_view.pack(padx=20, pady=20, fill="both", expand=True)

        # Add two tabs: URL and Title
        tab_view.add("Download via URL")
        tab_view.add("Download via Title")

        # --- Download via URL Tab ---
        url_tab = tab_view.tab("Download via URL")

        # URL Entry Label
        url_label = ctk.CTkLabel(url_tab, text="Enter the YouTube video or playlist URL:")
        url_label.pack(padx=10, pady=(20, 5), anchor="w")

        # URL Entry
        url_entry = ctk.CTkEntry(url_tab, width=500)
        url_entry.pack(padx=10, pady=5, fill="x")

        # Download Button
        url_download_button = ctk.CTkButton(
            url_tab,
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Download from URL",
            command=lambda: self.download_youtube_from_url(url_entry.get()),
            state="normal"  # Initially enabled
        )
        url_download_button.pack(padx=10, pady=10, fill="x")

        # Status Label
        url_status_label = ctk.CTkLabel(url_tab, text="")
        url_status_label.pack(padx=10, pady=10, anchor="w")
        self.youtube_url_status_label = url_status_label

        # --- Download via Title Tab ---
        title_tab = tab_view.tab("Download via Title")

        # Title Entry Label
        title_label = ctk.CTkLabel(title_tab, text="Enter the YouTube video title:")
        title_label.pack(padx=10, pady=(20, 5), anchor="w")

        # Title Entry
        title_entry = ctk.CTkEntry(title_tab, width=500)
        title_entry.pack(padx=10, pady=5, fill="x")

        # Download Button
        title_download_button = ctk.CTkButton(
            title_tab,
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Download by Title",
            command=lambda: self.download_youtube_by_title(title_entry.get()),
            state="normal"  # Initially enabled
        )
        title_download_button.pack(padx=10, pady=10, fill="x")

        # Status Label
        title_status_label = ctk.CTkLabel(title_tab, text="")
        title_status_label.pack(padx=10, pady=10, anchor="w")
        self.youtube_title_status_label = title_status_label

    def download_youtube_from_url(self, url):
        """
        Download YouTube audio or playlist based on the provided URL.
        """
        if not url.strip():
            self.youtube_url_status_label.configure(text="Please enter a YouTube URL.")
            return

        if not self.is_valid_youtube_url(url):
            self.youtube_url_status_label.configure(text="Invalid YouTube URL.")
            return

        self.youtube_url_status_label.configure(text=f"Starting download: {url}")
        logging.info(f"Starting download for YouTube URL: {url}")

        # Start download in a separate thread
        download_thread = threading.Thread(target=self.handle_youtube_download_url, args=(url,), daemon=True)
        download_thread.start()

    def handle_youtube_download_url(self, url):
        """
        Handle the YouTube download process for a given URL.
        """
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.output_directory / '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': self.ffmpeg_path,
                'quiet': True,
                'no_warnings': True,
                # Handle both single video and playlists
                'playliststart': 1,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                if 'entries' in info_dict:
                    # It's a playlist
                    for entry in info_dict['entries']:
                        if entry:  # Some entries might be None
                            audio_title = sanitize_filename(entry['title']) + '.mp3'
                            self.queue.put(
                                (self.youtube_url_status_label.configure, ({"text": f"Downloaded: {audio_title}"})))
                            logging.info(f"Downloaded and converted to MP3: {audio_title}")
                else:
                    # It's a single video
                    audio_title = sanitize_filename(info_dict['title']) + '.mp3'
                    self.queue.put((self.youtube_url_status_label.configure, ({"text": f"Downloaded: {audio_title}"})))
                    logging.info(f"Downloaded and converted to MP3: {audio_title}")

        except Exception as e:
            self.queue.put((self.youtube_url_status_label.configure, ({"text": f"Error downloading: {url}"})))
            logging.error(f"Error downloading YouTube URL: {url}", exc_info=True)

    def download_youtube_by_title(self, title):
        """
        Download YouTube audio based on the provided title.
        """
        if not title.strip():
            self.youtube_title_status_label.configure(text="Please enter a YouTube video title.")
            return

        self.youtube_title_status_label.configure(text=f"Starting download: {title}")
        logging.info(f"Starting download for YouTube title: {title}")

        # Start download in a separate thread
        download_thread = threading.Thread(target=self.handle_youtube_download_title, args=(title,), daemon=True)
        download_thread.start()

    def handle_youtube_download_title(self, title):
        """
        Handle the YouTube download process based on a song title.
        """
        try:
            audio_filename = self.download_youtube_audio(title)
            self.queue.put((self.youtube_title_status_label.configure, ({"text": f"Downloaded: {audio_filename}"})))
            logging.info(f"Successfully downloaded: {audio_filename}")
        except Exception as e:
            self.queue.put((self.youtube_title_status_label.configure, ({"text": f"Error downloading: {title}"})))
            logging.error(f"Error downloading YouTube title: {title}", exc_info=True)

    def download_youtube_audio(self, query):
        """
        Download YouTube audio based on the search query.
        """
        try:
            # Use ytsearch to find the video by song title and artist
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.output_directory / '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': self.ffmpeg_path,
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                # Search for the first video matching the query
                'default_search': 'ytsearch1',
                'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 may cause issues
            }
            search_term = f"\"{query}\""  # Exact match
            with YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(search_term, download=True)
                if 'entries' in result:
                    video = result['entries'][0]
                else:
                    video = result
                audio_title = sanitize_filename(video['title']) + '.mp3'
            logging.info(f"Downloaded and converted to MP3: {audio_title}")
            return audio_title
        except Exception as e:
            logging.error(f"Failed to download audio for query: {query}", exc_info=True)
            raise Exception(f"Failed to download: {query}")

    def is_valid_youtube_url(self, url):
        """
        Validate if the provided URL is a valid YouTube link.
        """
        youtube_regex = re.compile(
            r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
        )
        return youtube_regex.match(url) is not None

    def reset_app(self):
        """
        Reset the application to its initial state.
        """
        # Reset Spotify
        self.playlist_dropdown.configure(values=[], state="disabled")
        self.playlist_var.set('')
        self.spotify_status_label.configure(text="")
        self.spotify_download_button.configure(state="disabled")

        # Reset YouTube via URL
        self.youtube_url_entry.delete(0, tk.END)
        self.youtube_url_status_label.configure(text="")

        # Reset YouTube via Title
        self.youtube_title_entry.delete(0, tk.END)
        self.youtube_title_status_label.configure(text="")

        self.app.update()
        logging.info("Reset the application.")

    def center_window(self, fullscreen=True):
        self.app.update_idletasks()
        if not fullscreen:
            width = 800
            height = 600
            x = (self.app.winfo_screenwidth() // 2) - (width // 2)
            y = (self.app.winfo_screenheight() // 2) - (height // 2)
            self.app.geometry(f"{width}x{height}+{x}+{y}")
            logging.debug(f"Window centered at ({x}, {y}) with size {width}x{height}.")
        else:
            # Fullscreen mode is already set via attributes
            logging.debug("Fullscreen mode is enabled.")

    def process_queue(self):
        try:
            while True:
                func, args = self.queue.get_nowait()
                func(*args)
        except queue.Empty:
            pass
        self.app.after(100, self.process_queue)

    def run(self):
        self.center_window()
        self.app.mainloop()


if __name__ == "__main__":
    try:
        youtube_app = YouTubeDownloaderApp()
        youtube_app.run()
    except Exception as e:
        logging.critical("Application crashed due to an unexpected error.", exc_info=True)
        print("Application crashed. Check the log file for details.")