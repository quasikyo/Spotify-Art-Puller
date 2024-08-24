# Spotify Art Puller
This script fetches album art from Spotify using the Spotipy library and resizes the image using the Python Imaging Library (PIL) or OpenCV (cv2).


## Setup
```
git clone https://github.com/quasikyo/Spotify-Art-Puller
cd Spotify-Art-Puller
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
Creating a virtual environment isn't necessary, but it is strongly recommended.

## Running
```
python main.py
```

1. Run the script in your Python environment.
2. When prompted, enter your Spotify client ID and client secret.
3. Enter the name of the artist and album/single you want to fetch the art for.
4. Enter the desired resolution for the image.
5. The script will fetch the album art, resize it, and display it in a new window.
6. Right-click on the image and select "Save as" to save the image.

Please note that you need to have a Spotify developer account to use these scripts as they require a client ID and client secret from Spotify.

Remember to replace any '/' in artist or album names with '_' to prevent issues with file paths.
