#!/bin/python3
import mavros
import mavros_msgs
import std_msgs
import rospy

from geometry_msgs.msg import PoseStamped

if __name__ == "__main__":
    rospy.init_node('vison_pose_publisher', anonymous=True)
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
