#include<iostream>
#include<opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main(void)
{

	Mat image=imread("pic.jpeg");
	namedWindow("demo", 0);
	resizeWindow("demo", 500, 500);
	imshow("demo", image);
	waitKey(1000);
	destroyAllWindows();
	return 0;

}

