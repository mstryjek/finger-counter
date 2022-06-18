"""
Visualizer class for visualizing intermediate steps of image processing.

MS
"""

from typing import Any
import cv2
import numpy as np

from config import Config


class ProcessingVisualizer():
    """
    Class for visualizing images given to it.
    """
    def __init__(self, cfg: Config) -> None:
        self.CFG = cfg
        self.reset()
        self.inspect_mode = False
        ## TODO Precalculate textbox w,h and vertical margins for indicators

    def __enter__(self):
        """Enter context and create widnow."""
        cv2.namedWindow(self.CFG.VIS.WINNAME)
        return self


    def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
        """Safely exit."""
        cv2.destroyAllWindows()


    def draw_mask(self, img: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Draw a color mask on the image.
        """
        masked = img.copy()
        masked[mask != 0] = self.CFG.VIS.COLOR
        cv2.addWeighted(masked, self.CFG.VIS.ALPHA, img, 1.-self.CFG.VIS.ALPHA, 0, masked)
        return masked


    def draw_textbox(self, img: np.ndarray, num_fingers: int) -> np.ndarray:
        """
        Draw textbox info on an image.
        """
        



    def draw(self, img: np.ndarray, mask: np.ndarray, num_fingers: int) -> np.ndarray:
        """
        Draw detection results on an image.
        """
        drawn = self.draw_mask(img, mask)
        drawn = self.draw_textbox(img, mask)
        return drawn


    def reset(self) -> None:
        """Reset image list."""
        self.images = []


    def store(self, img: np.ndarray) -> None:
        """Store an image to be shown later."""
        self.images.append(img)
    

    def show(self) -> bool:
        """
        Show images and return whether program should exit.
        Shows first image given if in stream mode or iterates through processing steps with keyboard
        interaction if in inspect mode.
        Returns whether program should exit.
        """
        ## Safeguard against uninitialized visualizer
        if not self.images:
            return False

        ## Iterate through images via keyboard in inspect mode
        if self.inspect_mode:
            i = 0
            while i < len(self.images):
                cv2.imshow(self.CFG.VIS.WINNAME, self.images[i])
                key = cv2.waitKey(0)
                if key == ord(self.CFG.VIS.CONTINUE_KEY):
                    i += 1
                elif key == ord(self.CFG.VIS.BACK_KEY):
                    i = max(i-1, 0)
                elif key == ord(self.CFG.VIS.INSPECT_KEY):
                    self.inspect_mode = False
                    break
        ## Show raw stream
        else:
            cv2.imshow(self.CFG.VIS.WINNAME, self.images[-1])

            ## Check for change to inspect mode
            key = cv2.waitKey(1)
            if key == ord(self.CFG.VIS.INSPECT_KEY):
                self.inspect_mode = True

        if key == ord(self.CFG.VIS.BREAK_KEY):
            return True
        return False