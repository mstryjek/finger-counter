"""
TODO Desc

KF
"""
import numpy as np
import cv2

from config import Config

from typing import List, Tuple, Any


class ImageProcessor():
	"""
	Comprehensive image processing class, containing all logic & vision algorithms.
	"""
	def __init__(self, cfg: Config) -> None:
		self.CFG = cfg

		## Lower HSV threshold for skin area detection
		self.skin_bounds_low = np.array([
			self.CFG.PROCESSING.COLOR_BOUNDS.LOW.H,
			self.CFG.PROCESSING.COLOR_BOUNDS.LOW.S,
			self.CFG.PROCESSING.COLOR_BOUNDS.LOW.V
		], dtype=np.uint8)

		## Upper HSV threshold for skin area detection
		self.skin_bounds_high = np.array([
			self.CFG.PROCESSING.COLOR_BOUNDS.HIGH.H,
			self.CFG.PROCESSING.COLOR_BOUNDS.HIGH.S,
			self.CFG.PROCESSING.COLOR_BOUNDS.HIGH.V
		], dtype=np.uint8)



	def __enter__(self):
		"""
		Enter context.
		"""
		return self
	

	def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
		pass


	def equalize(self, img: np.ndarray) -> np.ndarray:
		"""
		Equalize a BGR image along the value channel.
		"""
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
		return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


	def smooth(self, img: np.ndarray) -> np.ndarray:
		"""
		Blur an image to reduce noise.		
		"""
		return cv2.GaussianBlur(img, (self.CFG.PROCESSING.BLUR_SIZE,)*2, 0)



	def extract_color_mask(self, img: np.ndarray) -> np.ndarray:
		"""
		Extract a denoised, filtered version of the skin color mask.
		"""
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange(hsv, self.skin_bounds_low, self.skin_bounds_high)

		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.CFG.PROCESSING.CLOSE_SIZE,)*2)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=self.CFG.PROCESSING.CLOSE_ITERS)

		return mask


	def extract_largest_contour(self, mask: np.ndarray) -> np.ndarray:
		"""
		Extract the contour with the largest area.
		"""
		contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
		areas = [cv2.contourArea(cnt) for cnt in contours]
		
		cnt_max_area = contours[np.argmax(areas)]
		
		filtered_mask = np.zeros(mask.shape, dtype=np.uint8)
		return cv2.drawContours(filtered_mask, [cnt_max_area], -1, (255, 255, 255), -1)

