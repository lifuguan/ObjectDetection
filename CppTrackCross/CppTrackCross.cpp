/*

@All right reserved.
@summary: used to track the black line to correct the diretion of the car
@author: LiHao
@date: 2018.7.29
@refer: https://docs.opencv.org/master/
@location: DJI
*/





#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <opencv2/opencv.hpp>
using namespace std;
using namespace cv;

Mat frame;
VideoCapture capture;

//要发送的数据集合
struct CV_Data
{
	int distance[2];
	float slope[2];
};

//实例化集合
CV_Data CD;

string IntToStr(int data)
{
	char ch_str[10] = { 0 };
	sprintf(ch_str, "%d", data);
	string  str_data(ch_str);
	return str_data;
}
/*@brief: 求点到直线距离
*         点斜式大法好
*/
int dst_calc(int x1, int y1, int x2, int y2, int tar_x = 144, int tar_y = 144)
{
	line(frame, Point(x1, y1), Point(x2, y2), Scalar(0, 155, 155), 3);
	double A, B, C, dst;
	A = y2 - y1;
	B = x1 - x2;
	C = x2 * y1 - x1 * y2;
	dst = abs(A*tar_x + B * tar_y + C) / sqrt(A*A + B * B);
	return int(dst);
}




//初始化图形并圈出
string detect(vector<Point> cnts_single, vector<Point> & approx)
{
	string shape = "undentified";
	double peri = arcLength(cnts_single, true);
	approxPolyDP(cnts_single, approx, 0.015 * peri, true);
	cout << "approx.size(): " << approx.size() << endl;
	if (approx.size() == 3)
	{
		shape = "triangle";
	}
	else if (approx.size() == 4)
	{
		shape = "rectangle";
		/*待完成*/
	}
	else if (approx.size() == 5)
	{
		shape = "pentagon";
	}
	else if (approx.size() > 10)
	{
		shape = "SHizi";
	}

	return shape;
}





bool CV_Close = false; //用于关闭摄像头CV
float slope_up;
int height;
int width;

int main()
{
	/*"C:\\Users\\10027\\Pictures\\Camera Roll\\final2.mp4"*/
	//frame = imread("C:\\Users\\10027\\Pictures\\Camera Roll\\final3_Moment.jpg");
	capture.open("C:\\Users\\10027\\Pictures\\Camera Roll\\final2.mp4");
	capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);//宽度 
	capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);//高度
											   //检测1
	if (!capture.isOpened())
	{
		printf("--(!)Error opening video capture\n"); return -1;
	}
	//计时5次， 取平均值
	int num = 0;
	while (capture.read(frame))		 //五次检测， 取平均值
	{
		num++;
		//Sobel算子

		Rect rect(200, 100, 320, 320);
		frame = frame(rect);
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

		//二值化大法好
		dst.convertTo(dst, -1, 2.5, 50);
		cvtColor(dst, dst, COLOR_BGR2GRAY);
		imshow("Gray Frame", dst);
		threshold(dst, dst, 100, 255, CV_THRESH_BINARY);
		imshow("thres Frame", dst);

		Mat erode_element = getStructuringElement(MORPH_RECT, Size(1, 1));
		//腐蚀后的图像
		erode(dst, dst, erode_element, Point(-1, -1), 1);
		//膨胀
		Mat dilate_element = getStructuringElement(MORPH_RECT, Size(5, 5));
		Mat dilate_out;     //膨胀后的图像
		dilate(dst, dilate_out, dilate_element, Point(-1, -1), 6);

		//截取白色干扰边框
		erode_element = getStructuringElement(MORPH_RECT, Size(4, 4));
		//再次腐蚀
		erode(dilate_out, dilate_out, erode_element, Point(-1, -1), 3);
		Rect rect_after(9, 9, 288, 288);
		dilate_out = dilate_out(rect_after);
		imshow("Dilate Frame", dilate_out);

		vector<vector<Point>>cnts;//获取了一堆又一堆点
		findContours(dilate_out, cnts, RETR_EXTERNAL, CHAIN_APPROX_NONE);





		for (int i = 0; i < cnts.size(); i++)
		{
			vector<Point> cnts_single = cnts[i];//获取了上面一堆点中的一个点
			if (cnts_single.size() > 300)
			{
				vector<Point> approx;
				string shape = detect(cnts_single, approx);
				Moments M = moments(cnts_single);
				int cX, cY;
				if (M.m10 != 0)
				{
					//表示图像重心
					cX = int((M.m10 / M.m00));
					cY = int((M.m01 / M.m00));
				}
				else
				{
					cX = cY = 0;
				}
				line(frame, Point(320, 0), Point(320, 480), (255, 255, 255), 4);//画中位线

				cout << shape << endl;


				line(frame, Point(cX, cY), Point(0, cY), Scalar(255, 255, 255), 1);//画质心线
				line(frame, Point(cX, cY), Point(cX, 0), Scalar(255, 255, 255), 1);

				putText(frame, "shape: " + shape, Point(cX, cY), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 2);
				line(frame, Point(cX, cY), Point(cX, cY), (255, 255, 255), 5);
				putText(frame, "position " + IntToStr(cX) + " , " + IntToStr(cY), Point(cX, cY + 20), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 0, 255), 2);  //质心位置

				float dst = 0;

				//避免出现三角形时pos_calc()报错
				if (shape == "rectangle" || shape == "square")
				{
				}
				else if (shape == "SHizi")
				{
					line(frame, approx[0], approx[0], Scalar(0, 0, 255), 15);   putText(frame, "1", approx[0], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[1], approx[1], Scalar(0, 0, 255), 15);   putText(frame, "2", approx[1], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[2], approx[2], Scalar(0, 0, 255), 15);   putText(frame, "3", approx[2], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[3], approx[3], Scalar(0, 0, 255), 15);   putText(frame, "4", approx[3], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[4], approx[4], Scalar(0, 0, 255), 15);   putText(frame, "5", approx[4], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[5], approx[5], Scalar(0, 0, 255), 15);   putText(frame, "6", approx[5], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[6], approx[6], Scalar(0, 0, 255), 15);   putText(frame, "7", approx[6], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[7], approx[7], Scalar(0, 0, 255), 15);   putText(frame, "8", approx[7], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[8], approx[8], Scalar(0, 0, 255), 15);   putText(frame, "9", approx[8], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
					line(frame, approx[9], approx[9], Scalar(0, 0, 255), 15);   putText(frame, "10", approx[9], FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);


					//垂直距离
					int dst = dst_calc(approx[1].x, approx[1].y, approx[2].x, approx[2].y);
					CD.distance[1] += int(dst);
					putText(frame, "distance_x: " + IntToStr(dst), Point(cX, cY + 40), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 0, 255), 2);  //质心位置
					dst = dst_calc(approx[4].x, approx[4].y, approx[5].x, approx[5].y);
					CD.distance[1] += int(dst);
					putText(frame, "distance_y: " + IntToStr(dst), Point(cX, cY + 60), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 0, 255), 2);  //质心位置


																																			//斜率

					height = float(approx[2].y - approx[1].y);
					width = float(-approx[2].x + approx[1].x);
					if (height != 0 && width != 0)
						slope_up = atan2(height, width) / (3.1415926 * 2) * 360 + 180;
					putText(frame, "slope_up: " + IntToStr(slope_up), Point(cX, cY + 80), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 0, 255), 2);  //质心位置

				}
			}
			else
			{
				//printf("too fucking small %d\n", cnts_single.size());
			}
		}
		imshow("Result Frame", frame);
		//waitKey(50);
		if (waitKey(50) == 'q' || CV_Close == true)
		{
			capture.release();
			break;
		} // escape
	}
	CD.distance[1] = CD.distance[1] / 5;
	CD.slope[1] = CD.slope[1] / 5;
	cout << CD.distance[1] << "      " << CD.slope[1] << endl;
	system("pause");
	return 0;
}


