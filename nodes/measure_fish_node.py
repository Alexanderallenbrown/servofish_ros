#!/usr/bin/env python

#Alex Brown
#2013

#currently, this node is in the process of being updated. Its purpose is to "measure" the lanes in a preview-sense. Currently, it does not use any map information, but eventually it will subscribe to the current "best" pose estimate, and use the map geometry to help estimate depth, etc. Right now the flat road assumption is key. There are a lot of commented debugging tools embedded here, that can be used if needed, but the idea now is to publish the lane marker feature (right lane at this writing) as a marker message, probably a line_strip or a points_list type. This way, you can see the relationship between the original image, the local locations of points perceived, and their global locations easily in RVIZ without messing around with costly CVwindows, etc. 

#remember, for this to work, the ROS TFs representing the relationship between car and world (/world frame to /car frame) and car to camera have to be set up and published properly. When this is achieved, ROS does all of the coordinate transformations for us in RVIZ.


import roslib
roslib.load_manifest('servofish_ros')
import sys
import rospy
#from cv2 import cv
from std_msgs.msg import *
from geometry_msgs.msg import *
#from preview_filter.msg import * #this is very important! we have custom message types defined in this package!!
from sensor_msgs.msg import Image
from visualization_msgs.msg import Marker #we will use this message for the perceived fish. then pop it into Rviz
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from numpy import pi
import math
import cv2
import tf

class measure_fish:

  def __init__(self):
    #dictionary of aruco markers
    self.dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    self.D = np.array([-0.40541413163196455, 0.09621547958919903, 0.029070017586547533, 0.005280797822816339, 0.0])
    self.K = np.array([[529.8714858851022, 0.0, 836.4563887311622], [0.0, 1547.2605077363528, 83.19276259345895], [0.0, 0.0, 1.0]])

    #this is how we get our image in to use openCV
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/image_raw",Image,self.callback,queue_size=1)#change this to proper name!
    self.fishmarkerpub = rospy.Publisher('/measured_fishmarker',Marker,queue_size=1)
    self.timenow = rospy.Time.now()

    self.cam_pos = (0,0,18*.0254)
    self.cam_quat = tf.transformations.quaternion_from_euler(pi,0,0)

  #this function fires whenever a new image_raw is available. it is our "main loop"
  def callback(self,data):
    try:
      frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
      print e
    self.timenow = rospy.Time.now()
    rows,cols,depth = frame.shape
    if rows>0:
        corns,ids,rejected = cv2.aruco.detectMarkers(frame,self.dict)
        if ids is not None:
            rvecs,tvecs = cv2.aruco.estimatePoseSingleMarkers(corns,.025,self.K,self.D)
            #print rvecs
            fishquat = tf.transformations.quaternion_from_euler(rvecs[0][0][0],rvecs[0][0][1],rvecs[0][0][2])
            br = tf.TransformBroadcaster()
            br.sendTransform((tvecs[0][0][0],tvecs[0][0][1],tvecs[0][0][2]),fishquat,self.timenow,'/fish_measured','/camera1')
            br.sendTransform(self.cam_pos,self.cam_quat,self.timenow,'/camera1','world')
            #publish a marker representing the fish body position
            fishmarker = Marker()
            fishmarker.header.frame_id='/fish_measured'
            fishmarker.header.stamp = self.timenow
            fishmarker.type = fishmarker.MESH_RESOURCE
            fishmarker.mesh_resource = 'package://servofish_ros/meshes/fishbody.dae'
            fishmarker.mesh_use_embedded_materials = True
            fishmarker.action = fishmarker.MODIFY
            fishmarker.scale.x = 1
            fishmarker.scale.y = 1
            fishmarker.scale.z = 1
            tempquat = tf.transformations.quaternion_from_euler(0,0,0)#this is RELATIVE TO FISH ORIENTATION IN TF (does the mesh have a rotation?)
            fishmarker.pose.orientation.w = tempquat[3]
            fishmarker.pose.orientation.x = tempquat[0]
            fishmarker.pose.orientation.y = tempquat[1]
            fishmarker.pose.orientation.z = tempquat[2]
            fishmarker.pose.position.x = 0
            fishmarker.pose.position.y = 0
            fishmarker.pose.position.z = 0
            fishmarker.color.r = .8
            fishmarker.color.g = .5
            fishmarker.color.b = .5
            fishmarker.color.a = 1.0#transparency

            self.fishmarkerpub.publish(fishmarker)

def main(args):
  
  rospy.init_node('measure_fish', anonymous=True)
  ic = measure_fish()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv2.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
