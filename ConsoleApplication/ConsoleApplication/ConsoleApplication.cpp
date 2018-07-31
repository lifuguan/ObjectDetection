
#define _CRT_SECURE_NO_WARNINGS
#include "stdafx.h"


#include <opencv2/opencv.hpp>
#include <string>
#include <iostream>
using namespace std;

using namespace cv;


VideoCapture capture;
Mat frame;

//初始化图形并圈出
string detect(vector<Point> cnts_single, vector<Point> & approx)
{
	string shape = "undentified";
	double peri = arcLength(cnts_single, true);
	approxPolyDP(cnts_single, approx, 0.1 * peri, true);
	cout << "approx.size(): " << approx.size() << endl;
	if (approx.size() == 3)
	{
		//shape = "triangle";
	}
	else if (approx.size() == 4)
	{
		//shape = "rectangle";
		/*待完成*/
	}
	else if (approx.size() == 5)
	{
		//shape = "pentagon";
	}
	else if (approx.size() == 12)
	{
		shape = "shi zi";
	}

	return shape;
}

int main()
{
	//Mat frame = imread("C:\\Users\\10027\\source\\repos\\ObjectDetection\\PythonApplication\\RoboSample\\mix\\black1.jpg");



	capture.open("C:\\Users\\10027\\Pictures\\Camera Roll\\final2.mp4");
	capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);//宽度 
	capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);//高度
	while (capture.read(frame))
	{

		Mat kernel = (Mat_<float>(3, 3) << 0, -1, 0, 0, 5, 0, 0, -1, 0);
		filter2D(frame, frame, CV_8UC3, kernel);

		Mat grad_x, grad_y;
		Mat abs_grad_x, abs_grad_y, dst;

		//求x方向梯度
		Sobel(frame, grad_x, CV_16S, 1, 0, 3, 1, 1, BORDER_DEFAULT);
		convertScaleAbs(grad_x, abs_grad_x);
		//求y方向梯度
		Sobel(frame, grad_y, CV_16S, 0, 1, 3, 1, 1, BORDER_DEFAULT);
		convertScaleAbs(grad_y, abs_grad_y);
		//合并梯度
		addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0, dst);

		dst.convertTo(dst, -1, 2.9, 99);
		cvtColor(dst, dst, COLOR_BGR2GRAY);
		imshow("Gray Frame", dst);
		threshold(dst, dst, 95, 255, CV_THRESH_BINARY);
		imshow("thres Frame", dst);

		//膨胀
		Mat dilate_element = getStructuringElement(MORPH_RECT, Size(3, 3));
		//膨胀后的图像
		dilate(dst, dst, dilate_element, Point(-1, -1), 4);


		vector<vector<Point> > contours;

		findContours(dilate_element, contours, CV_RETR_EXTERNAL, CHAIN_APPROX_NONE);

		for (int i = 0; i < contours.size(); i++)
		{
			vector<Point> cnts_single = contours[i];//获取了上面一堆点中的一堆点
			vector<Point> approx;
			string shape = detect(cnts_single, approx);
			for (int i = 0; i < approx.size(); i++)
			{
				line(dst, approx[i], approx[i], Scalar(0, 255, 0), 8);
			}
			cout << "shape: " << shape <<endl;
			
		}

		imshow("Dilate Frame", dst);
		if (waitKey(30) == 'q')
		{
			break;
		}
	}


	return 0;
}
