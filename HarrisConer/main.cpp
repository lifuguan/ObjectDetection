#include "stdafx.h"
#include "opencv2/objdetect.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include <stdio.h>

using namespace std;
using namespace cv;
/** Function Headers */
void detectAndDisplay(Mat frame);


/** @function main */
int main(int argc, const char** argv)
{
	Mat frame;
	VideoCapture capture;

	capture.open(0);

	capture.set(CV_CAP_PROP_FRAME_WIDTH, 1280);//宽度 
	capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);//高度
											   //谜之设置帧数
											   //capture.set(CV_CAP_PROP_FPS, 0);//帧数

	printf_s("width = %.2f\n", capture.get(CV_CAP_PROP_FRAME_WIDTH));
	printf_s("height = %.2f\n", capture.get(CV_CAP_PROP_FRAME_HEIGHT));
	printf_s("fps = %.2f\n", capture.get(CV_CAP_PROP_FPS));

	int c = 0;
	//打开双目

	if (!capture.isOpened())
	{
		printf("--(!)Error opening video capture\n"); return -1;
	}

	while (capture.read(frame))
	{
		if (frame.empty())
		{
			printf(" --(!) No captured frame -- Break!");
			break;
		}

		//-- 3. Apply the classifier to the frame
		detectAndDisplay(frame);

		if (waitKey(10) == 27) { break; } // escape
	}
	return 0;
}

/** @function detectAndDisplay */
void detectAndDisplay(Mat frame)
{
	//-- Show what you got
	imshow("frame", frame);
}