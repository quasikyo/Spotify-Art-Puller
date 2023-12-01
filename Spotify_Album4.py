import os
import subprocess
import sys
import shutil

# Start of package check
def install(packages):
    try:
        # Create requirements.txt file
        with open('requirements.txt', 'w') as f:
            for package in packages:
                f.write(package + '\n')

        # Install packages using requirements.txt file
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", 'requirements.txt'])
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Delete requirements.txt file
        if os.path.exists('requirements.txt'):
            os.remove('requirements.txt')

required_packages = {'spotipy': 'spotipy', 'requests': 'requests', 'PIL': 'Pillow', 'tkinter': 'tkinter', 'fuzzywuzzy': 'fuzzywuzzy', 'Levenshtein': 'python-Levenshtein'}
missing_packages = []

for package in required_packages:
    try:
        # Try to import the package
        __import__(package)
    except ImportError:
        # If the import fails, add it to the list of missing packages
        missing_packages.append(required_packages[package])

# If there are any missing packages, ask the user if they want to install them
if missing_packages:
    print(f"The following packages are not installed: {', '.join(missing_packages)}")
    install_prompt = input(f"Do you want to install these packages? (yes/no): ")
    if install_prompt.lower() in ['yes', 'y']:
        install(missing_packages)
    else:
        print(f"Error: The following packages are required to run this script: {', '.join(missing_packages)}")
        sys.exit(1)
# End of package check

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import io
import os
import json
from tkinter import *
from tkinter import filedialog
from fuzzywuzzy import fuzz
from PIL import ImageTk, Image as PilImage

def get_credentials():
    # Check if credentials file exists
    if os.path.isfile('credentials.json'):
        # Load credentials from file
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
        reuse = input("Do you wish to reuse the last Spotify client ID and secret? (yes/no): ")
        if reuse.lower() not in ['yes', 'y']:
            # Ask user for new credentials
            credentials['client_id'] = input("Enter your Spotify client ID: ")
            credentials['client_secret'] = input("Enter your Spotify client secret: ")
            # Save new credentials to file
            with open('credentials.json', 'w') as f:
                json.dump(credentials, f)
    else:
        # Ask user for credentials
        credentials = {}
        credentials['client_id'] = input("Enter your Spotify client ID: ")
        credentials['client_secret'] = input("Enter your Spotify client secret: ")
        # Save credentials to file
        with open('credentials.json', 'w') as f:
            json.dump(credentials, f)
    return credentials

def fetch_album_art(artist_name, album_name):
    # Set up Spotify API credentials
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for the artist on Spotify
    results = sp.search(q='artist:' + artist_name, type='artist')

    # Find the artist that best matches the input artist name using fuzzy matching
    best_match = None
    highest_score = 0
    for artist in results['artists']['items']:
        score = fuzz.ratio(artist['name'].lower(), artist_name.lower())
        if score > highest_score:
            highest_score = score
            best_match = artist

    if best_match is not None:
        artist_id = best_match['id']
    else:
        print("Artist not found.")
        return None

    # Get the artist's albums and singles
    albums_and_singles = sp.artist_albums(artist_id, album_type='album,single')

    # Find the album/single that best matches the input album/single name using fuzzy matching
    best_match = None
    highest_score = 0
    for album in albums_and_singles['items']:
        score = fuzz.ratio(album['name'].lower(), album_name.lower())
        if score > highest_score:
            highest_score = score
            best_match = album

    if best_match is not None:
        album_art_url = best_match['images'][0]['url']
    else:
        print("Album or single not found.")
        return None

    return album_art_url

def resize_image(album_art_url, width, height):
    response = requests.get(album_art_url)
    img = PilImage.open(io.BytesIO(response.content))
    img = img.resize((width, height), PilImage.LANCZOS) # LANCZOS is a high-quality downsampling filter
    return img

def save_and_open_image(img, artist_name, album_name):
    filename = "{} - {}.jpg".format(artist_name, album_name)
    try:
        img.save(filename)
        root = Tk()
        canvas = Canvas(root, width=img.width, height=img.height)
        canvas.pack()
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=NW, image=photo)

        def save_image_as():
            save_filename = filedialog.asksaveasfilename(defaultextension='.jpg', initialfile=filename)
            if save_filename:
                img.save(save_filename)

        def popup(event):
            menu.post(event.x_root, event.y_root)

        menu = Menu(root, tearoff=0)
        menu.add_command(label="Save as", command=save_image_as)
        canvas.bind("<Button-3>", popup)
        root.mainloop()

    except IOError:
        print("Failed to save image.")

artist_name = input("Enter the name of the artist: ").replace('/', '_')
album_name = input("Enter the name of the album/single: ").replace('/', '_')

while True:
    try:
        resolution = input("Enter the desired resolution (format - widthxheight): ")
        width, height = map(int, resolution.split('x'))
    except ValueError:
        print("Invalid resolution format. Please enter in the format widthxheight.")
    else:
        break

credentials = get_credentials()

while True:
    album_art_url = fetch_album_art(artist_name, album_name)
    if album_art_url is not None:
        break
    else:
        artist_name = input("Enter the name of the artist: ").replace('/', '_')
        album_name = input("Enter the name of the album: ").replace('/', '_')

try:
    img = resize_image(album_art_url, width, height)
    if img is not None:
        save_and_open_image(img, artist_name, album_name)
    else:
        print("Failed to resize image.")
except OSError as e:
    print(f"Error: {e.strerror}")

filename = "{} - {}.jpg".format(artist_name.replace('/', '_'), album_name.replace('/', '_'))
os.remove(filename)