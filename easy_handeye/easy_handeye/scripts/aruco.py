#!/home/bepgroup/Desktop/peract_env/bin/python3

import rospy
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Pose

def get_end_effector_position():
    
    pose_publisher =rospy.Publisher('/target_pose', Pose, queue_size=10)


    rospy.init_node('get_end_effector_position', anonymous=True)
    tf_buffer = Buffer()
    listener = TransformListener(tf_buffer)

    rate = rospy.Rate(10.0)  # 10 Hz

    while not rospy.is_shutdown():
        try:
            # Change 'base_link' and 'end_effector_link' to your specific robot's frame names
            trans = tf_buffer.lookup_transform('panda_link0', 'aruco_marker_frame', rospy.Time(0)).transform.translation
            rot = tf_buffer.lookup_transform('panda_link0', 'aruco_marker_frame', rospy.Time(0)).transform.rotation

            # Create a Pose message
            pose_msg = Pose()
            pose_msg.position.x = trans.x
            pose_msg.position.y = trans.y
            pose_msg.position.z = trans.z
            pose_msg.orientation.w = rot.w
            pose_msg.orientation.x = rot.x
            pose_msg.orientation.y = rot.y
            pose_msg.orientation.z = rot.z

            # Publish the Pose message
            pose_publisher.publish(pose_msg)

            # Log the position
            rospy.loginfo("Marker Position: x=%f, y=%f, z=%f", trans.x, trans.y, trans.z)
            rate.sleep()
        except Exception as e:
            rospy.logwarn_throttle(10.0, "Failed to get end effector position: %s", str(e))

if __name__ == '__main__':
    try:
        get_end_effector_position()
    except rospy.ROSInterruptException:
        pass

