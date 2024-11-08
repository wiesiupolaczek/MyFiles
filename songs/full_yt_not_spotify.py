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
            scope=self.spotify_scope
        ))

        ctk.set_appearance_mode("dark")
        # Create the main app window
        self.app = ctk.CTk()
        self.app.title("YouTube & Spotify Audio Downloader")
        self.app.geometry("900x700")  # Increased size to accommodate sidebar and tabs

        # Configure grid layout
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)

        # Initialize sidebar
        self.create_sidebar()

        # Initialize frames for different features
        self.frames = {}
        self.create_frames()

        # Define the output directory and ffmpeg path from environment variables
        self.ffmpeg_path = os.getenv('FFMPEG_PATH')
        self.output_directory = Path(os.getenv('OUTPUT_DIR'))

        # Validate that ffmpeg_path and output_directory are set
        if not self.ffmpeg_path:
            raise EnvironmentError("FFmpeg path is not set in environment variables.")
        if not self.output_directory:
            raise EnvironmentError("Output directory is not set in environment variables.")

        # Ensure the output directory exists
        if not self.output_directory.exists():
            self.output_directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {self.output_directory}")

        self.queue = queue.Queue()
        self.app.after(100, self.process_queue)

    def create_sidebar(self):
        """
        Create a sidebar with a burger menu containing different features.
        """
        self.sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        # Configure grid layout for sidebar
        self.sidebar.grid_rowconfigure(0, minsize=10)  # Spacer
        self.sidebar.grid_rowconfigure(5, weight=1)  # Push buttons to top

        # Title label in sidebar
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Button to navigate to Spotify Downloader
        self.spotify_button = ctk.CTkButton(
            self.sidebar,
            text="Spotify Downloader",
            command=lambda: self.show_frame("Spotify"),
            width=180
        )
        self.spotify_button.grid(row=1, column=0, padx=10, pady=10)

        # Button to navigate to YouTube Downloader
        self.youtube_button = ctk.CTkButton(
            self.sidebar,
            text="YouTube Downloader",
            command=lambda: self.show_frame("YouTube"),
            width=180
        )
        self.youtube_button.grid(row=2, column=0, padx=10, pady=10)

        # Button to reset the application
        self.reset_button = ctk.CTkButton(
            self.sidebar,
            text="Reset",
            command=self.reset_app,
            width=180
        )
        self.reset_button.grid(row=3, column=0, padx=10, pady=10)

    def create_frames(self):
        """
        Create different frames for each feature.
        """
        container = ctk.CTkFrame(self.app)
        container.grid(row=0, column=1, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Spotify Downloader Frame
        spotify_frame = ctk.CTkFrame(container)
        spotify_frame.grid(row=0, column=0, sticky="nswe")
        self.create_spotify_frame(spotify_frame)
        self.frames["Spotify"] = spotify_frame

        # YouTube Downloader Frame with Tabs
        youtube_frame = ctk.CTkFrame(container)
        youtube_frame.grid(row=0, column=0, sticky="nswe")
        self.create_youtube_frame(youtube_frame)
        self.frames["YouTube"] = youtube_frame

        # Show Spotify frame by default
        self.show_frame("Spotify")

    def show_frame(self, frame_name):
        """
        Bring the selected frame to the front.
        """
        frame = self.frames[frame_name]
        frame.tkraise()
        logging.info(f"Switched to {frame_name} Downloader.")

    def create_spotify_frame(self, frame):
        """
        Create the Spotify Downloader interface.
        """
        # Create a label to prompt the user to authenticate Spotify
        auth_label = ctk.CTkLabel(frame, text="Authenticate with Spotify to select a playlist:")
        auth_label.pack(padx=10, pady=10)

        # Create a button to authenticate Spotify
        auth_button = ctk.CTkButton(
            frame,
            fg_color="green",
            hover_color="#90EE90",
            text_color="black",
            text="Authenticate Spotify",
            command=self.authenticate_spotify
        )
        auth_button.pack(padx=10, pady=10)

        # Create a dropdown for playlists (initially disabled)
        self.playlist_var = tk.StringVar()
        playlist_dropdown = ctk.CTkOptionMenu(
            frame,
            dynamic_resizing=True,
            variable=self.playlist_var,
            values=[],
            state="disabled",
            command=self.on_select_playlist
        )
        playlist_dropdown.pack(padx=10, pady=10)

        # Create a button to start the download process
        download_button = ctk.CTkButton(
            frame,
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Download Selected Playlist",
            command=self.download_playlist,
            state="disabled"
        )
        download_button.pack(padx=10, pady=10)

        # Create a label to display the status of the download
        status_label = ctk.CTkLabel(frame, text="")
        status_label.pack(padx=10, pady=10)

        # Assign widgets to instance variables for later access
        self.spotify_auth_button = auth_button
        self.spotify_playlist_dropdown = playlist_dropdown
        self.spotify_download_button = download_button
        self.spotify_status_label = status_label

    def create_youtube_frame(self, frame):
        """
        Create the YouTube Downloader interface with tabs for URL and Title-based downloading.
        """
        # Create a tab view
        tab_view = ctk.CTkTabview(frame, width=700, height=600)
        tab_view.pack(padx=20, pady=20, fill="both", expand=True)

        # Add two tabs: URL and Title
        tab_view.add("Download via URL")
        tab_view.add("Download via Title")

        # Configure grid layout for tabs
        tab_view.tab("Download via URL").grid_columnconfigure(0, weight=1)
        tab_view.tab("Download via Title").grid_columnconfigure(0, weight=1)

        # ----------------- Download via URL -----------------
        # Create a label to prompt the user to enter the YouTube URL
        url_label = ctk.CTkLabel(tab_view.tab("Download via URL"), text="Enter the YouTube video or playlist URL:")
        url_label.pack(padx=10, pady=10)

        # Entry for YouTube URL
        url_entry = ctk.CTkEntry(tab_view.tab("Download via URL"), width=500)
        url_entry.pack(padx=10, pady=10)

        # Create a button to start the download process
        url_download_button = ctk.CTkButton(
            tab_view.tab("Download via URL"),
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Download from URL",
            command=lambda: self.download_youtube_from_url(url_entry.get()),
            state="normal"  # Initially enabled
        )
        url_download_button.pack(padx=10, pady=10)

        # Create a label to display the status of the download
        url_status_label = ctk.CTkLabel(tab_view.tab("Download via URL"), text="")
        url_status_label.pack(padx=10, pady=10)

        # ----------------- Download via Title -----------------
        # Create a label to prompt the user to enter the YouTube video title
        title_label = ctk.CTkLabel(tab_view.tab("Download via Title"), text="Enter the title of the YouTube video:")
        title_label.pack(padx=10, pady=10)

        # Entry for YouTube video title
        title_entry = ctk.CTkEntry(tab_view.tab("Download via Title"), width=500)
        title_entry.pack(padx=10, pady=10)

        # Create a button to start the download process
        title_download_button = ctk.CTkButton(
            tab_view.tab("Download via Title"),
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Download by Title",
            command=lambda: self.download_youtube_by_title(title_entry.get()),
            state="normal"  # Initially enabled
        )
        title_download_button.pack(padx=10, pady=10)

        # Create a label to display the status of the download
        title_status_label = ctk.CTkLabel(tab_view.tab("Download via Title"), text="")
        title_status_label.pack(padx=10, pady=10)

        # Assign widgets to instance variables for later access
        self.youtube_url_entry = url_entry
        self.youtube_url_download_button = url_download_button
        self.youtube_url_status_label = url_status_label

        self.youtube_title_entry = title_entry
        self.youtube_title_download_button = title_download_button
        self.youtube_title_status_label = title_status_label

    def authenticate_spotify(self):
        """
        Authenticate with Spotify and load playlists.
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
        except Exception as e:
            self.spotify_status_label.configure(text="Spotify authentication failed.")
            logging.error("Spotify authentication failed.", exc_info=True)

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

    def download_tracks(self, tracks):
        """
        Iterate through tracks and download each song.
        """
        for idx, item in enumerate(tracks):
            track = item['track']
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

    def download_youtube_from_url(self, url):
        """
        Download YouTube audio or playlist based on the provided URL.
        """
        if not url.strip():
            self.youtube_url_status_label.configure(text="Please enter a YouTube URL.")
            return

        self.youtube_url_status_label.configure(text=f"Starting download: {url}")
        logging.info(f"Starting download for YouTube URL: {url}")

        # Start download in a separate thread
        download_thread = threading.Thread(target=self.handle_youtube_download_url, args=(url,), daemon=True)
        download_thread.start()

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

    def reset_app(self):
        """
        Reset the application to its initial state.
        """
        # Reset Spotify
        self.spotify_playlist_dropdown.configure(values=[], state="disabled")
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

    def center_window(self):
        self.app.update_idletasks()
        width = self.app.winfo_width()
        height = self.app.winfo_height()
        x = (self.app.winfo_screenwidth() // 2) - (width // 2)
        y = (self.app.winfo_screenheight() // 2) - (height // 2)
        self.app.geometry(f"{width}x{height}+{x}+{y}")
        logging.debug(f"Window centered at ({x}, {y}).")

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
    youtube_app = YouTubeDownloaderApp()
    youtube_app.run()