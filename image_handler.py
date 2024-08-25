from enum import Enum
import cv2
import numpy as np
import os
import PIL.Image
from tkinter import filedialog
from typing import Callable

DEFAULT_IMAGE_SIZE = 640
DEFAULT_IMAGE_EXTENSION = '.jpg'


class ResizeOption(Enum):
	OPEN_CV = 'open_cv'
	PILLOW = 'pillow'


def save_image(image: PIL.Image.Image, file_name: str) -> None:
	name_to_save = filedialog.asksaveasfilename(
		initialdir=os.getcwd(),
		initialfile=file_name,
		defaultextension=DEFAULT_IMAGE_EXTENSION,
		filetypes=[
			('JPG Image', '.jpg'),
			('JPEG Image', '.jpeg'),
			('PNG Image', '.png')
		]
	)

	if name_to_save is None or name_to_save == '':
		print('Filename not provided. Exiting...')
		return
	image.save(name_to_save)


def get_resize_function(flag: ResizeOption) -> Callable[[bytes, int, int], PIL.Image.Image]:
	match flag:
		case ResizeOption.OPEN_CV:
			return resize_image_cv2
		case ResizeOption.PILLOW:
			return resize_image_pil
		case _:
			raise ValueError(f'Option of {flag} is not supported.')


def resize_image_cv2(imageBytes: bytes, widthPx: int, heightPx: int) -> PIL.Image.Image:
	image = PIL.Image.open(imageBytes)
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
	image = cv2.resize(image, (widthPx, heightPx), interpolation = cv2.INTER_LINEAR)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return PIL.Image.fromarray(image)


def resize_image_pil(imageBytes: bytes, widthPx: int, heightPx: int) -> PIL.Image.Image:
	image = PIL.Image.open(imageBytes)
	return image.resize((widthPx, heightPx), PIL.Image.Resampling.LANCZOS)
