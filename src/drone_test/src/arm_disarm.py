#!/bin/python3
import rospy
import mavros

from mavros_msgs.srv import CommandBool

if __name__ == "__main__":
    rospy.init_node('drone_launcher')
    rospy.wait_for_service("/mavros/cmd/arming")
    try:
        arm_proxy = rospy.ServiceProxy(
                '/mavros/cmd/arming', CommandBool)
        arm_flag = True
        rospy.loginfo("Arming Drone")
        arm_proxy(arm_flag)

        rospy.sleep(5)

        arm_flag = False
        rospy.loginfo("Disarming Drone")
        arm_proxy(arm_flag)
    except:
        rospy.loginfo("Encountered Exception")
	

