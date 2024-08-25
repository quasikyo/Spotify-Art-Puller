from fuzzywuzzy import fuzz
import json
import os
import spotipy
from typing import Optional

CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'


class SpotifyCredentialsLoadError(Exception):
	pass


def get_album_art_url(credentials: dict[str, str], artist_search: str, album_search: str) -> Optional[str]:
	spotify_credentials = spotipy.SpotifyClientCredentials(**credentials)
	spotify_client = spotipy.Spotify(client_credentials_manager=spotify_credentials)

	artists = spotify_client.search(q=f'artist:{artist_search}', type='artist')
	artist_match = _get_best_match(artists['artists']['items'], 'name', artist_search)
	if not artist_match:
		return None

	albums = spotify_client.artist_albums(artist_match['id'], include_groups='album,single')
	album_match = _get_best_match(albums['items'], 'name', album_search)
	if not album_match:
		return None

	return album_match['images'][0]['url']


def _get_best_match(results, result_field: str, search: str) -> Optional[dict]:
	best_match = None
	highest_score = 0
	for result in results:
		score = fuzz.ratio(result[result_field].lower(), search.lower())
		if score > highest_score:
			highest_score = score
			best_match = result

	return best_match


def save_credentials(file_path: str, client_id: str, client_secret: str) -> dict[str, str]:
	'''
	Attempts to save client_id and client_secrent to file_path.

	Parameters:
	- file_path: file to save the credentials to
	- client_id: the Spotify Client ID
	- client_secret: the Spotify Client secret
	- create_dirs: if this function should create parent directories if they do not exist

	Returns:
	- credentials dictionary

	Throws:
	- ValueError: if file_path is not .json
	'''
	credentials = {
		CLIENT_ID: client_id,
		CLIENT_SECRET: client_secret
	}

	parent_path = os.path.dirname(file_path)
	if not os.path.exists(parent_path):
		os.makedirs(parent_path)

	_, extension = os.path.split(file_path)
	if extension != '.json':
		raise ValueError(f'{file_path} is not a JSON file.')
	with open(file_path, 'w') as file:
		json.dump(credentials, file)

	return credentials


def load_credentials(file_path: str) -> dict[str, str]:
	'''
	Attempts to load Spotify credentials from given file path.

	Parameters:
	- file_path: file path to load credentials from

	Returns:
	- credentials dictionary

	Throws:
	- FileNotFoundError: file does not exist
	- JSONDecodeError: file contents are not proper JSON
	- SpotifyCredentialsLoadError: file contents do not contain the proper data
	'''
	credentials = None
	with open(file_path, 'r') as file:
		credentials = json.load(file)

	if CLIENT_ID not in credentials:
		raise SpotifyCredentialsLoadError(f'{CLIENT_ID} not found.')
	if CLIENT_SECRET not in credentials:
		raise SpotifyCredentialsLoadError(f'{CLIENT_SECRET} not found.')

	return credentials
