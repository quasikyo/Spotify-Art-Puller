import PIL
import PIL.Image
import cv2
import numpy as np


def resize_image_cv2(imageBytes: bytes, widthPx: int, heightPx: int) -> PIL.Image:
	image = PIL.Image.open(imageBytes)
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
	image = cv2.resize(image, (widthPx, heightPx), interpolation = cv2.INTER_LINEAR)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	return PIL.Image.fromarray(image)


def resize_image_pil(imageBytes: bytes, widthPx: int, heightPx: int) -> PIL.Image :
	image = PIL.Image.open(imageBytes)
	return image.resize((widthPx, heightPx), PIL.Image.LANCZOS)
