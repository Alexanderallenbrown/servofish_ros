import cv2
import numpy as np
import sys

#make a dictionary based on one of the library's defaults
#4x4 binary with 50 markers inthe dict.
mydict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)


#A C++ example of marker detection from the documentation:
#  c++ cv::Mat inputImage;
#  vector< int > markerIds;
# vector< vector<Point2f> > markerCorners, rejectedCandidates;
# cv::aruco::DetectorParameters parameters;
# cv::aruco::Dictionary dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6X6_250); 
# cv::aruco::detectMarkers(inputImage, dictionary, markerCorners, markerIds, parameters, rejectedCandidates);
#  


#tutorial for estimating pose: https://longervision.github.io/2017/03/10/opencv-external-posture-estimation-ArUco-single-marker/

D = np.array([-0.40541413163196455, 0.09621547958919903, 0.029070017586547533, 0.005280797822816339, 0.0])
K = np.array([[529.8714858851022, 0.0, 836.4563887311622], [0.0, 1547.2605077363528, 83.19276259345895], [0.0, 0.0, 1.0]])

if __name__ == '__main__':

    # load video
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    if not ret:
        print("can't open video!")
        sys.exit(-1)

    while ret:
        corns,ids,rejected = cv2.aruco.detectMarkers(frame_gray,mydict)
    
        
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame,corns,ids)
            #cv::aruco::estimatePoseSingleMarkers(corners, 0.05, cameraMatrix, distCoeffs, rvecs, tvecs);
            rvecs,tvecs=cv2.aruco.estimatePoseSingleMarkers(corns,.05,K,D)
            print rvecs,tvecs
            #draw axes onto image
            try:
                imgWithAruco = cv2.aruco.drawAxis(frame, K, D, rvecs, tvecs, .05)    # axis length 100 can be changed according to your requirement
            except:
                pass

        cv2.imshow("frame", frame)
        cv2.waitKey(10)
        
        # read next frame
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)