#include<ros/ros.h>
#include<iostream>
#include<string>
#include<cv_bridge/cv_bridge.h>
#include<sensor_msgs/image_encodings.h>
#include<image_transport/image_transport.h>
#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/opencv.hpp>
#include <opencv2/core/types.hpp>

using namespace std;
using namespace cv;

    

int main(int argc,char** argv)
{	ros::init(argc, argv, "arrow_test");
	ros::NodeHandle nh;
	image_transport::ImageTransport it(nh);
	image_transport::Publisher pub = it.advertise("camera/image", 1);
	//ros::Publisher arrow_test = nh.advertise<test::detector>("arrowdata",1000);
	//sensor_msgs::ImagePtr msg;

	CascadeClassifier cascader2Straight;
	CascadeClassifier cascader2Right;
	CascadeClassifier cascader2Left;
	String straightfile = "/home/bosonlee/arrow_test/src/test/Parameter/cascade2Straight.xml";
	String rightfile = "/home/bosonlee/arrow_test/src/test/Parameter/cascade2Right.xml";
	String leftfile = "/home/bosonlee/arrow_test/src/test/Parameter/cascade2Left.xml";
    Mat buffer;//buffer = src
    Mat buffer_crop;
	Mat croppedImage;
    VideoCapture capture = VideoCapture(2);
	int counter_s, counter_r, counter_l;
	size_t s_t, r_t, l_t;
	s_t = 0;
	r_t = 0;
	l_t = 0;
	counter_s = 0;
	counter_r = 0;
	counter_l = 0;
	ros::Rate loop_rate(30);
	//test::detector msg;
	
	if(!cascader2Straight.load(straightfile)){
		ROS_INFO("Could not load Straight...\n\n");
	}
	if(!cascader2Right.load(rightfile)){
		ROS_INFO("Could not load Right...\n\n");
	}
	if(!cascader2Left.load(leftfile)){
		ROS_INFO("Could not load Left...\n\n");
	}
    //Imagesource_subscriber = nh.subscribe("/usb_cam/image_raw", 10, GetImagesourceFunction);																											//for	pc
    //namedWindow("output", CV_WINDOW_AUTOSIZE);
    while (nh.ok())
    {
			capture >> buffer_crop;
			resize(buffer_crop,buffer,Size(320,240));
        	if (buffer.empty())
			{
				ROS_INFO("could not load images \n\n");
			}
        	else
        	{
        		ros::spinOnce();
				Mat gray;
				vector<Rect> Straight;
				vector<Rect> Right;
				vector<Rect> Left;
				cvtColor(buffer, gray, COLOR_BGR2GRAY);
				equalizeHist(gray, gray);

				cascader2Straight.detectMultiScale(gray, Straight, 1.1, 2, 0, Size(10, 10));
				cascader2Right.detectMultiScale(gray, Right, 1.1, 2, 0, Size(10, 10));
				cascader2Left.detectMultiScale(gray, Left, 1.1, 2, 0, Size(10, 10));

    	        if(Straight.size())
				{
					rectangle(buffer, Straight[s_t], Scalar(255, 0, 0), 2, 8, 0);
					ROS_INFO(" straight \n\n");
					waitKey(10);
					cv::Rect ROI(Straight[s_t].x , Straight[s_t].y , Straight[s_t].width ,Straight[s_t].height);
					croppedImage = buffer(ROI);
					String filename = format("/home/bosonlee/Desktop/Straight arrow/%d.jpg", s_t);
	    			imwrite(filename,croppedImage);
				    waitKey(10);
					s_t++;
					counter_s += 1;
				}
				else
				{
					counter_s = 0;
    	            ROS_INFO("could not straight \n\n");
				}	

				if(Right.size())
				{
					rectangle(buffer, Right[r_t], Scalar(255, 0, 0), 2, 8, 0);
					//waitKey(30);
					cv::Rect ROI(Right[r_t].x , Right[r_t].y , Right[r_t].width ,Right[r_t].height);
					croppedImage = buffer(ROI);
					//waitKey(10);
					String filename = format("/home/bosonlee/Desktop/Right arrow/%d.jpg", r_t);
	    			imwrite(filename,croppedImage);
					waitKey(10);
                	r_t++;
					counter_r += 1;
				}
				else
				{
					counter_r = 0;
    	            ROS_INFO("could not right \n\n");
	            }

				if(Left.size())
				{	
					ROS_INFO("left \n\n");
					rectangle(buffer, Left[l_t], Scalar(255, 0, 0), 2, 8, 0);
					waitKey(10);
					//ROS_INFO(" %d \n\n",Left[l_t].x);
					//ROS_INFO(" %d \n\n",Left[l_t].y);
					cv::Rect ROI(Left[l_t].x , Left[l_t].y , Left[l_t].width , Left[l_t].height);
					croppedImage = buffer(ROI);
					String filename = format("/home/bosonlee/Desktop/Left arrow/%d.jpg", l_t);
    				imwrite(filename,croppedImage); 
					waitKey(10);
                	l_t++;
					counter_l += 1;
				}
				else
				{
					counter_l = 0;
            	    ROS_INFO("could not left \n\n");
				}
				sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", croppedImage).toImageMsg();
        		pub.publish(msg);
        		cv::waitKey(30);
        	}
			//msg.croppedImage = croppedImage;
			//arrow_test.publish(msg);
			//imshow("output",buffer);
        	//waitKey(10);
    }
    waitKey(0);
	loop_rate.sleep();
	capture.release();
	
    return 0;
}
