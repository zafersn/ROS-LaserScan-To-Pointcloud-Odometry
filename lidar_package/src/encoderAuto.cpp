#include "ros/ros.h"
#include <sensor_msgs/JointState.h>
#include <std_msgs/Header.h>
#include "serial/serial.h"
#include <string>
#include <iostream>
#include <cstdio>

using std::string;

int pozisyon = 0;
int ang=0;
double encoder_resolution=4200;


char a[] = {"base_tilt_joint"}; // F: Front - B: Back - R: Right - L: Left

double pos[]={0.0}; /// stores arduino time
double vel[]={0.0};
double eff[]={0.0};
serial::Serial my_serial("/dev/lidar_motor", 57600, serial::Timeout::simpleTimeout(10));
sensor_msgs::JointState robot_state;

double degreTOrad(double degre);
//string trim(const string& str);

int main(int argc, char **argv)
{

  ros::init(argc, argv, "joint_state_publisher");

  ros::NodeHandle n;
  
  std_msgs::Header header;


  ros::Publisher chatter_pub = n.advertise<sensor_msgs::JointState>("joint_states", 10);

  ros::Rate loop_rate(100);



  robot_state.header;
  robot_state.header.stamp=ros::Time::now();
  robot_state.name.resize(1);
  robot_state.velocity.resize(1);
  robot_state.position.resize(1); /// here used for arduino time
  robot_state.effort.resize(1); /// here used for arduino time

    robot_state.name[0]=(a);
    pos[0]=degreTOrad(pozisyon);
	


    robot_state.position[0] = pos[0];
    robot_state.velocity[0] = vel[0];
    robot_state.effort[0] = eff[0];
    if(my_serial.isOpen())
      std::cout << " Yes." <<std:: endl;
    else
      std::cout << " No." <<std:: endl;
  while (ros::ok())
  {

    string s= my_serial.read(32);
   // ROS_INFO("I heard1: [%u]",buf[0]);
   /* ROS_INFO("I heard2: [%u]",buf[1]);
    ROS_INFO("I heard3: [%u]",buf[2]);
    ROS_INFO("I heard4: [%u]",buf[3]);*/
    //ROS_INFO("Buf: [%lu]",sizeof(buf));
    // ROS_INFO("pozisyon: [%d]",pozisyon);
 //ROS_INFO("ss: %s",s.c_str());
 //ROS_INFO("ssss2: %c",s[0]);
 if(s[0]=='!'&&s.find("#")!=-1){
  string sss=s.substr(s.find("!")+1,s.find("#")-1);
 // ROS_INFO("ss: %s",sss.c_str());
  int a= std::stoi((sss.c_str()));
  pozisyon=a;
   // ROS_INFO("iiii: %d",a);
}
   // my_serial.flush();
/*if(!s.empty()){
    int a= std::stoi(trim(s.c_str()));
    ROS_INFO("ss: %d",a);
    }*/
   ang=((pozisyon/encoder_resolution)*360.0);  // calculate angel according to pulse count
   ang=int(ang)%360;
   ROS_INFO("anglee: %d",(ang));
   
   
    pos[0]=degreTOrad(ang);
    robot_state.header.stamp=ros::Time::now();
    robot_state.position[0] = pos[0];
    robot_state.velocity[0] = 0;
    robot_state.effort[0] = 0;
  /* pozisyon++;
   if(pozisyon==8400){pozisyon=0;}*/
    //uint8_t buf[1];

   
    chatter_pub.publish(robot_state);

    ros::spinOnce();

    loop_rate.sleep();

  }


  return 0;
}

double degreTOrad(double degre){
  
  
  return (degre/57.2958);
  
  }

