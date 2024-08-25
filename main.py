import argparse
import image_handler
import io
from json import JSONDecodeError
import package_handler
import requests
import spotify_handler
from spotify_handler import CLIENT_ID, CLIENT_SECRET, SpotifyCredentialsLoadError
import sys
from typing import Union

REQUIRMENTS_FILE = 'requirements.txt'
DEFAULT_CREDENTIALS_FILE = 'credentials.json'


def parse_args() -> dict[str, Union[str | image_handler.ResizeOption]]:
	parser = argparse.ArgumentParser(
		prog='Spotify Art Puller',
		description='Downloads album art from Spotify by artist and album.'
	)
	parser.add_argument(
		'-c', '--credentials',
		help=f'JSON file that contains {CLIENT_ID} and {CLIENT_SECRET} for Spotify.',
		type=str,
		required=False,
		default=DEFAULT_CREDENTIALS_FILE
	)
	parser.add_argument(
		'--artist',
		help='Spotify artist to search under.',
		type=str,
		required=True
	)
	parser.add_argument(
		'--album',
		help='Spotify album/etc. to search for.',
		type=str,
		required=True
	)
	parser.add_argument(
		'-s', '--size',
		help='Pixel size of saved image (SIZExSIZE).',
		type=int,
		required=False,
		default=image_handler.DEFAULT_IMAGE_SIZE
	)
	parser.add_argument(
		'--resize',
		help='Resize the image using Python Imaging Library (pillow) or OpenCV (open_cv).',
		choices=[option.value for option in image_handler.ResizeOption],
		type=str,
		required=False,
		default=image_handler.ResizeOption.PILLOW.value
	)

	parsed_args = vars(parser.parse_args())
	parsed_args['resize'] = image_handler.ResizeOption(parsed_args['resize'])
	return parsed_args


if __name__ == '__main__':
	# Check package dependencies
	print('Checking packages...')
	packages = package_handler.get_missing_packages(REQUIRMENTS_FILE)
	if len(packages) > 0:
		package_handler.prompt_package_install(packages)

	args = parse_args()

	# Credential checking
	credentials = None
	try:
		print('Loading credentials...')
		credentials = spotify_handler.load_credentials(args['credentials'])
	except FileNotFoundError:
		print(f'{args["credentials"]} was not found.')
	except JSONDecodeError:
		print(f'{args["credentials"]} was not valid JSON.')
	except SpotifyCredentialsLoadError as e:
		print(e)

	if credentials is None:
		# TODO: implement input for this
		print('Credentials not found. Exiting...')
		sys.exit(0)

	# Spotify query
	art_url = spotify_handler.get_album_art_url(
		credentials=credentials,
		artist_search=args['artist'],
		album_search=args['album']
	)
	if art_url is None or art_url == '':
		print(f'Matching result for search of artist:{args["artist"]} album:{args["album"]} not found. Exiting...')
		sys.exit(0)
	print(f'Retrieved art URL of {art_url}')

	# Image management
	print('Fetching image...')
	imageBytes = io.BytesIO(requests.get(art_url).content)
	resizer = image_handler.get_resize_function(args['resize'])
	image = resizer(imageBytes, args['size'], args['size'])
	image_handler.save_image(image, f'{args["artist"]} - {args["album"]}')
