#!/bin/python3
from pymavlink import mavutil
import time
import os, pty, serial


if __name__ == "__main__":

    master, slave = pty.openpty()
    slave_name = os.ttyname(slave)
    master_name = os.ttyname(master)
    print("Launched {} master and {} slave".format(master_name,slave_name))
    # Start a connection listening to a UDP port
    the_connection = mavutil.mavlink_connection('udpout:localhost:14650', source_system=1,source_component=1)
    #the_connection = mavutil.mavlink_connection(master_name)

    # Wait for the first heartbeat 
    #   This sets the system and component ID of remote system for the link
    #the_connection.wait_heartbeat()
    #print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
    print("Sending VISION_POSITION_ESTIMATE")
    while True:
        #the_connection.mav.hil_gps_send(int(time.time()),3,0,0,1,2**16-1, 2**16-1, 2**16-1, 0,0,0, 2**16-1, 20)
        the_connection.mav.vision_position_estimate_send(int(time.time()),123,321,1,0,0,0)
        #the_connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID,0,0,0)
        time.sleep(0.5)
