#!/usr/bin/env python3

import sys, select, tty, termios
import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    # Publish a ‘keys’ message, the message type is String, and the buffer is 1
    key_pub = rospy.Publisher('keys', String, queue_size=1)
    # Node Initialization
    rospy.init_node("keyboard_driver")
    # Set frequency
    rate = rospy.Rate(100)
    # Get keyboard strokes, modify terminal properties
    old_attr = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    print("Publishing keystrokes. Press Ctrl-C to exit...")

    while not rospy.is_shutdown():
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
            # release the news
            key_pub.publish(sys.stdin.read(1))
        try:
            rate.sleep()
        except:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
    # Restore the terminal to standard mode
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
