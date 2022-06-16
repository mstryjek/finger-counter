import cv2
from cv2 import sqrt
from cv2 import threshold
from cv2 import mean
import numpy as np
from copy import copy
'''import sys
np.set_printoptions(threshold=sys.maxsize)'''


class ImgAq:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)

    def reader(self) -> np.ndarray:
        success, img = self.cap.read()
        return img

class Skin_Detector():
    def __init__(self):
        '''
        Setting skin color bounderies for skin detection. HSV
        '''
        self.skin_boundary_low = np.array([0,30,15], dtype=np.uint8)
        self.skin_boundary_high = np.array([20,255,160], dtype=np.uint8)

        #main source frames
        self.frame: np.ndarray = [[[]]]
        self.frame_skin: np.ndarray = [[[]]]

        #list of boundaries of objects that went through the first thresholding
        self.object_arrays: list = []

        #list of valid objects with their respective ndarrays (after the second thresholding)
        self.valid_object_frames: list = []

    def get_frame(self, frame: np.ndarray) -> None:
        self.frame = frame

    def equalise_frame(self) -> None:
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.frame[:, :, 2] = cv2.equalizeHist(self.frame[:, :, 2])

    def get_frame_shape(self) -> None:
        self.frame_height = self.frame.shape[0]
        self.frame_width = self.frame.shape[1]
    
    def detect_white(self) -> np.hstack:
        '''
        Parsing passed frame for skin presence
        '''
        skinMask = cv2.inRange(self.frame, self.skin_boundary_low, self.skin_boundary_high)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        skinMask = cv2.erode(skinMask, kernel, iterations=2)
        skinMask = cv2.dilate(skinMask, kernel, iterations=2)
        
        skinMask = cv2.GaussianBlur(skinMask, (3,3), 0)
        self.frame_skin = cv2.bitwise_and(self.frame, self.frame, mask=skinMask)
        return np.hstack([self.frame, self.frame_skin])
    
    def differentiate_objects(self) -> list:
        '''
        Method used for object differentiation - false positives of skin, different body parts etc.
        '''
        self.object_arrays: list = []

        #variable threshold
        avg_per_pixel_vertical_threshold: float = 7.0
    
        copied_frame = cv2.transpose(self.frame_skin)
        for vertical_f in enumerate(copied_frame):
            if np.sum(vertical_f[1])>avg_per_pixel_vertical_threshold*self.frame_width:
                #copied_frame = cv2.line(copied_frame, (0, vertical_f[0]), (self.frame_height, vertical_f[0]), color=(0,0,255), thickness=1)
                self.object_arrays.append(vertical_f[0])               
        else:
            #copied_frame = cv2.transpose(copied_frame)
            #cv2.imshow('Framed', copied_frame)
            return
    
    def clear_boundaries(self):
        '''
        Setting limits for boundaries established in differentiate_objects method
        '''
        
        limit: int = int(self.frame_width*0.05)
        false_limits: list = []

        for boundary in enumerate(self.object_arrays):
            if boundary[0] == len(self.object_arrays)-1 or boundary[0] == 0:
                continue
            if abs(boundary[1]-self.object_arrays[boundary[0]-1])<limit and abs(boundary[1]-self.object_arrays[boundary[0]+1])<limit:
                false_limits.append(boundary[0])
        
        false_limits.reverse()
        for fal_lim in false_limits:
            self.object_arrays.pop(fal_lim)
    
    def draw_lines(self, lines) -> None:
        '''
        Helper method: used purely for the visualisation of boundaries of objects
        '''
        copied_frame = cv2.transpose(self.frame_skin)
        for line in lines:
            copied_frame = cv2.line(copied_frame, (0, line), (self.frame_height, line), color=(0,0,255), thickness=1)
        else:
            copied_frame = cv2.transpose(copied_frame)
            cv2.imshow('Cleared boundaries',copied_frame)
    
    def create_object_frames(self):
        '''
        Creation of separate ndarrays of objects after the first thresholding.

        IMPORTANT: NOT for continuous use if imshow method is in use. Used for visualisation purposes 
        only in single frame per script execution.
        '''
        self.valid_object_frames: list = []

        for i in range(0, len(self.object_arrays)-1, 2):
            temp: np.ndarray = np.zeros((self.frame_width, self.frame_height), dtype=np.uint8)
            temp = cv2.transpose(self.frame_skin[:,self.object_arrays[i]:self.object_arrays[i+1]])
            temp = cv2.transpose(temp)
            self.valid_object_frames.append(temp)
            #cv2.imshow(str(i), temp) #DO NOT use in continuous frame capture

    def valid_object_detection(self):
        '''
        The second thresholding of objects. If minimal object width and pixels mean requirements are met
        then objects are further analysed.
        '''
        
        width_threshold: int = int(self.frame_width*0.15)
        avg_per_pixel_threshold: int = 50
        for frame in enumerate(self.valid_object_frames):
            #print('Area:{}, mean: {}'.format(frame[0],str(np.mean(frame[1]))))
            if frame[1].shape[1]<width_threshold and np.sum(frame[1])>avg_per_pixel_threshold*self.frame_width:
                self.valid_object_frames.pop(frame[0])
        '''else:
            [cv2.imshow(str(fr[0]),fr[1]) for fr in enumerate(self.valid_object_frames)]'''
    
    def hand_detection(self):
        for frame in self.valid_object_frames:
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                epsilon = 0.01*cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                frame = cv2.drawContours(frame, [approx], 0, (0), 3)
            else:
                cv2.imshow(str(epsilon), frame)
    

def main():
    '''
    continuous use
    '''
    acquisitor = ImgAq()
    detector = Skin_Detector()
    while True:
        sing_frame=acquisitor.reader()
        detector.get_frame(sing_frame)
        cv2.imshow("Original",sing_frame)
        detector.get_frame_shape()
        detector.equalise_frame()
        detector.detect_white()
        detector.differentiate_objects()
        detector.clear_boundaries()
        detector.draw_lines(detector.object_arrays)
        #print(len(detector.object_arrays))
        detector.create_object_frames()
        detector.valid_object_detection()
        #print(len(detector.valid_object_frames))
        #detector.hand_detection()
        cv2.imshow("Tester",detector.frame_skin)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            return
            
if __name__=='__main__':
    main()
    
