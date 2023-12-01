# Spotify Art Puller (Final Version)

# Spotify_Album4: Album Art Fetcher with PIL for Image Resizing

This script fetches album art from Spotify using the Spotipy library and resizes the image using the Python Imaging Library (PIL). It checks for necessary packages and installs any missing ones. 
It then asks for your Spotify credentials and uses them to fetch album art for a specified artist and album. The image is resized using PIL's LANCZOS filter, which is a high-quality downsampling filter.

# Spotify_Album4CV: Album Art Fetcher with OpenCV for Image Resizing

This script is very similar to the first one but uses OpenCV (cv2) instead of PIL for image resizing. OpenCV provides more advanced image processing capabilities and might give better results when resizing images.

# How to Use

1. Run the script in your Python environment.
2. When prompted, enter your Spotify client ID and client secret.
3. Enter the name of the artist and album/single you want to fetch the art for.
4. Enter the desired resolution for the image.
5. The script will fetch the album art, resize it, and display it in a new window.
6. Right-click on the image and select "Save as" to save the image.

Please note that you need to have a Spotify developer account to use these scripts as they require a client ID and client secret from Spotify.

Remember to replace any '/' in artist or album names with '_' to prevent issues with file paths.
