#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float64.h"
#include <sstream>

int main(int argc, char **argv) {
    ros::init(argc, argv, "publisher_node");
    ros::NodeHandle n;

    ros::Publisher float_pub = n.advertise<std_msgs::Float64>("float_topic", 1000);
    ros::Publisher string_pub = n.advertise<std_msgs::String>("string_topic", 1000);

    ros::Rate loop_rate(10);

    int count = 0;
    while (ros::ok()) {
        std_msgs::Float64 float_msg;
        std_msgs::String string_msg;

        float_msg.data = 1.23; // 浮点数
        string_msg.data = "Hello, ROS!"; // 字符串

        // 发布消息
        float_pub.publish(float_msg);
        string_pub.publish(string_msg);

        // 输出发布的消息
        ROS_INFO("Published Float: %.2f, String: %s", float_msg.data, string_msg.data.c_str());

        ros::spinOnce();

        loop_rate.sleep();
        ++count;
    }

    return 0;
}
