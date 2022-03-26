#!/bin/python3
import mavros
import mavros_msgs
import std_msgs
import rospy

from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from mavros_msgs.msg import HilGPS
from mavros_msgs.msg import Mavlink
from geometry_msgs.msg import PoseStamped

if __name__ == "__main__":
#    rospy.init_node('position_faker', anonymous=True)
#    #pub = rospy.Publisher('/mavros/global_position/global', NavSatFix, queue_size=10)
#    pub = rospy.Publisher('/mavlink/to', Mavlink, queue_size=10)
#    rate = rospy.Rate(10)
#    while not rospy.is_shutdown():
#        init_pos = NavSatFix()
#        header = std_msgs.msg.Header()
#        header.stamp = rospy.Time.now()
#        header.frame_id = 'base_link'
#        init_pos.header = header
#        init_pos.status.status = 0
#        init_pos.status.service = 1
#        init_pos.latitude = 0.0
#        init_pos.longitude = 0.0
#        init_pos.altitude = 0.0
#        pub.publish(init_pos)
#        rate.sleep()
    rospy.init_node('position_faker', anonymous=True)
    pub = rospy.Publisher('/mavros/vision_pose/pose', PoseStamped, queue_size=10)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        init_pos = PoseStamped()
        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'base_link'
        init_pos.header = header
        init_pos.pose.position.x = 0
        init_pos.pose.position.y = 0
        init_pos.pose.position.z = 0
        init_pos.pose.orientation.x = 0
        init_pos.pose.orientation.y = 0
        init_pos.pose.orientation.z = 0
        init_pos.pose.orientation.w = 0
        pub.publish(init_pos)
        rate.sleep()
