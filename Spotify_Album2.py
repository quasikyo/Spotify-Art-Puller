import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from PIL import Image
import io
import os
import json
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

# Start of package check
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ['spotipy', 'requests', 'PIL', 'tkinter']

for package in required_packages:
    try:
        # Try to import the package
        __import__(package)
    except ImportError:
        # If the import fails, ask the user if they want to install the package
        print(f"The {package} package is not installed.")
        install_prompt = input(f"Do you want to install {package}? (yes/no): ")
        if install_prompt.lower() in ['yes', 'y']:
            install(package)
        else:
            print(f"Error: The {package} package is required to run this script.")
            sys.exit(1)
#End of package check

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

    # Search for the album on Spotify
    results = sp.search(q='artist:' + artist_name + ' album:' + album_name, type='album')

    # Get the URL of the album art
    albums = results['albums']['items']
    if albums:
        album_art_url = albums[0]['images'][0]['url']
    else:
        print("Album not found.")
        exit()

    return album_art_url

def resize_image(album_art_url, width, height):
    # Fetch the album art image
    response = requests.get(album_art_url)
    img = Image.open(io.BytesIO(response.content))

    # Resize the image
    img.thumbnail((width, height), Image.LANCZOS)

    return img

def save_and_open_image(img, artist_name, album_name):
    filename = "{} - {}.jpg".format(artist_name, album_name)
    
    try:
        # Save the image
        img.save(filename)

        # Open the image in default photo viewer and wait for it to close
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
    
# Ask user for artist and album name and desired resolution
artist_name = input("Enter the name of the artist: ").replace('/', '_')
album_name = input("Enter the name of the album: ").replace('/', '_')

try:
    resolution = input("Enter the desired resolution (format - widthxheight): ")
    width, height = map(int, resolution.split('x'))
except ValueError:
    print("Invalid resolution format.")
else:
    credentials = get_credentials()
    
    try:
      album_art_url = fetch_album_art(artist_name, album_name)
      
      if album_art_url is not None:
          img = resize_image(album_art_url, width, height)
          
          if img is not None:
              save_and_open_image(img, artist_name, album_name)
              
      filename = "{} - {}.jpg".format(artist_name.replace('/', '_'), album_name.replace('/', '_'))
      os.remove(filename)
      
    except OSError as e:
      print(f"Error: {e.strerror}")
