#!/bin/python3
import mavros
import mavros_msgs
import rospy
import tf2_ros
import std_msgs

from mavros_msgs.msg import Mavlink
from geometry_msgs.msg import PoseStamped

if __name__ == "__main__":
    rospy.init_node('position_publisher', anonymous=True)
    pub = rospy.Publisher('/mavros/vision_pose/pose', PoseStamped, queue_size=10)
    rate = rospy.Rate(10)
    tfBuffer = tf2_ros.Buffer()
    tfListener = tf2_ros.TransformListener(tfBuffer)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('map', 'camera', rospy.Time())
            init_pos = PoseStamped()
            print(trans)
            header = std_msgs.msg.Header()
            header.stamp = rospy.Time.now()
            header.frame_id = 'base_link'
            init_pos.header = header
            init_pos.pose.position.x = -trans.transform.translation.x
            init_pos.pose.position.y = -trans.transform.translation.y
            init_pos.pose.position.z = trans.transform.translation.z
            init_pos.pose.orientation.x = trans.transform.rotation.x
            init_pos.pose.orientation.y = trans.transform.rotation.y
            init_pos.pose.orientation.z = trans.transform.rotation.z
            init_pos.pose.orientation.w = trans.transform.rotation.w
            pub.publish(init_pos)
        except Exception as e:
            print(e)

        rate.sleep()
