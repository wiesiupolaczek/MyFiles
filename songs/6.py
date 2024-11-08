import os
import threading
import logging
from yt_dlp import YoutubeDL
from pathlib import Path
import customtkinter as ctk
import tkinter as tk
import re

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
        ctk.set_appearance_mode("dark")
        # Create the main app window
        self.app = ctk.CTk()
        self.app.title("YouTube Audio Downloader")
        self.app.geometry("500x350")

        # Create a label to prompt the user to enter the title
        self.url_label = ctk.CTkLabel(self.app, text="Enter the title of the YouTube video:")
        self.url_label.pack(padx=10, pady=10)

        # Create an entry widget to get the title from the user
        self.title_entry = ctk.CTkEntry(self.app, width=400)
        self.title_entry.pack(padx=10, pady=10)

        # Create a button to start the download process
        self.download_button = ctk.CTkButton(
            self.app,
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Download",
            command=self.main
        )
        self.download_button.pack(padx=10, pady=10)

        # Create a reset button
        self.reset_button = ctk.CTkButton(
            self.app,
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Reset",
            command=self.reset_app
        )
        self.reset_button.pack(padx=10, pady=10)

        # Create a close button
        self.close_button = ctk.CTkButton(
            self.app,
            fg_color="purple",
            hover_color="#B19CD9",
            text_color="black",
            text="Close",
            command=self.app.quit
        )
        self.close_button.pack(padx=10, pady=10)

        # Create a label to display the status of the download
        self.status_label = ctk.CTkLabel(self.app, text="")
        self.status_label.pack(padx=10, pady=10)

        # Define the output directory
        self.output_directory = Path(r'C:\Users\wiesi\Desktop\Github\sings')

        # Ensure the output directory exists
        if not self.output_directory.exists():
            self.output_directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {self.output_directory}")

    def download_youtube_audio(self, title):
        try:
            # Use ytsearch to find the video by title
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.output_directory / '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': r'C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                # Search for the first video matching the title
                'default_search': 'ytsearch1',
                'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 may cause issues
            }
            search_term = f"\"{title}\""  # Exact match
            with YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(search_term, download=True)
                if 'entries' in result:
                    video = result['entries'][0]
                else:
                    video = result
                audio_title = sanitize_filename(video['title']) + '.mp3'
            logging.info(f"Downloaded and converted to MP3: {audio_title}")
            return audio_title
        except yt_dlp.utils.DownloadError as e:
            logging.error("Download failed. Possible reasons: Invalid title, video unavailable.", exc_info=True)
            raise Exception("Download failed. Please check the YouTube title and try again.")
        except Exception as e:
            logging.error("An unexpected error occurred during download.", exc_info=True)
            raise Exception("An unexpected error occurred. Please try again later.")

    def main_thread(self, video_title):
        try:
            # Download YouTube audio using the title
            self.status_label.configure(text="Searching and downloading audio...")
            self.app.update()
            audio_filename = self.download_youtube_audio(video_title)

            self.status_label.configure(text=f"File saved as: {audio_filename}")
            self.app.update()
            logging.info(f"Download and save completed: {audio_filename}")

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            logging.error("An error occurred in main_thread.", exc_info=True)
            self.app.update()

    def main(self):
        self.center_window()
        video_title = self.title_entry.get()

        if not video_title:
            self.status_label.configure(text="Please enter a YouTube video title.")
            return

        # Start the download process in a separate thread
        download_thread = threading.Thread(target=self.main_thread, args=(video_title,), daemon=True)
        download_thread.start()
        logging.info(f"Started download thread for title: {video_title}")

    def reset_app(self):
        # Clear the entry widget and reset the status label
        self.title_entry.delete(0, tk.END)
        self.status_label.configure(text="")
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

    def run(self):
        self.center_window()
        self.app.mainloop()

if __name__ == "__main__":
    youtube_app = YouTubeDownloaderApp()
    youtube_app.run()
