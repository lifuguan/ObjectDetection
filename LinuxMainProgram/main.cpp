#include <iostream>
#include "SerialPort.h"
#include "data_processing.h"
#include <lcm/lcm-cpp.hpp>
#include "head/info_head.hpp"
#include "normal/info_normal.hpp"


using namespace std;
#define SIZE 10
char x[SIZE], y[SIZE], angle[SIZE];

/*@brief: 转换函数
*
*/
string FloatToStr(float data)
{
	char x[10];
	sprintf(x, "%.2f", data);
	string str_data(x);
	return str_data;
}

int main()
{
	/*******     初始化UART1,UART4           *******/

	int fd_uart1, fd_uart4;
	char *UART1 = "/dev/ttyTHS0"; //Uart1
	char *UART2 = "/dev/ttyS0"; //UART4
	sleep(1);
	fd_uart1 = OpenDev(UART1); //open uart1
	fd_uart4 = OpenDev(UART2); //open uart2
	if (fd_uart1>0)
	{
		set_speed(fd_uart1, 19200); //set speed
	}
	else
	{
		printf("Can't Open Serial Port UART1!\n");
		exit(0);
	}

	if (fd_uart4 > 0)
	{
		set_speed(fd_uart4, 19200); //set speed
	}
	else
	{
		printf("Can't Open Serial Port UART4!\n");
		exit(0);
	}


	if (set_Parity(fd_uart1, 8, 1, 'N') == FALSE) //set parity
	{
		printf("Set Parity 1  Error\n");
		exit(1);
	}
	if (set_Parity(fd_uart4, 8, 1, 'N') == FALSE) //set parity
	{
		printf("Set Parity 4  Error\n");
		exit(1);
	}

	/***********  初始化LCM    ***********/

	lcm::LCM lcm;
	if (!lcm.good())
		return 1;
	Point_Data this_pos;
	Action_Data this_action;
	Handler handlerObject;
	lcm.subscribe("SENDHEAD", &Handler::handleMessage1, &handlerObject);

	/*******    无限循环      *********/
	while (1)
	{

		
		switch (start_area)
		{
		case 1:
			start_data.x = -930 / 2;
			start_data.y = -930 / 2;
			break;
		case 2:
			start_data.x = -930 / 2;
			start_data.y = 930 * 8+ 930 / 2;
			break;
		case 3:
			start_data.x = 930 * 8+ 930 / 2;
			start_data.y = 930 * 8+ 930 / 2;
			break;
		case 4:
			start_data.x = 930 * 8+ 930 / 2;
			start_data.y = -930 / 2;
			break;
		default:
			break;
		}
		this_pos.x = 0;
		this_pos.y = 0;

		for (int i = 0; i < run_times; ++i)
		{
			lcm.subscribe("SENDNORMAL", &Handler::handleMessage1, &handlerObject, i);
			int flag = 0;
			Point_Data resource_point_data[van[i].num + 10];
			for (int j = 0; j < van[i].num; ++j)
			{

				int id = van[i].resource[j];
				int temp1 = id / 100, temp2 = (id / 10) % 10, temp3 = id % 10;
				switch (temp1)
				{
				case 1:
					int py = 0;
					if (temp3 == 3)py = 1;
					if (temp3 == 4)py = 2;
					if (temp3 == 5)py = 3;
					resource_point_data[j].x = float(temp2) * 930 + 310 * py;
					resource_point_data[j].y = 7 * 930;
					resource_point_data[j].dir = 0;
					break;
				case 2:
					int py = 0;
					if (temp3 == 3)py = 1;
					if (temp3 == 4)py = 2;
					if (temp3 == 5)py = 3;
					resource_point_data[j].x = 7 * 930;
					resource_point_data[j].y = (7 - temp2) * 930 + (4 - py) * 310;
					resource_point_data[j].dir = 90;
					break;
				case 3:
					int py = 0;
					if (temp3 == 3)py = 1;
					if (temp3 == 4)py = 2;
					if (temp3 == 5)py = 3;
					resource_point_data[j].x = (7 - temp2) * 930 + (4 - py) * 310;
					resource_point_data[j].y = 0.0;
					resource_point_data[j].dir = 180;
					break;
				case 4:
					int py = 0;
					if (temp3 == 3)py = 1;
					if (temp3 == 4)py = 2;
					if (temp3 == 5)py = 3;
					resource_point_data[j].x = 0;
					resource_point_data[j].y = float(temp2) * 930 + (py) * 310;
					resource_point_data[j].dir = 270;
					break;
				default:
					continue;
					break;
				}

				if (resource_point_data[j].y == this_pos.y)
				{
					//平移
					this_action.dir = 1;
					this_action.target_point = resource_point_data[j];
					string pos_string = "G1 X" + FloatToStr(this_action.target_point.x / 930 * 930) + " Y" + FloatToStr(this_action.target_point.y) + " A0" + ";";
					Trans_Port(fd_uart1, pos_string);
					Calibrate_Port(fd_uart1);
					//moveit();
					string pos_string = "G1 X0 Y0 A" + FloatToStr(this_action.target_point.dir) + ";";
					Trans_Port(fd_uart1, pos_string);
					/*****    此处启动抓机   *******/

					//getit();//包括this_action.target_point.dir-----底盘旋转方向。
				}
				else
				{
					this_action.dir = 1;//dir==1表示平移，dir==0表示直行
					this_action.target_point.y = this_pos.y;
					this_action.target_point.x = resource_point_data[j].x / 930 * 930;
					string pos_string = "G1 X" + FloatToStr(resource_point_data[j].x / 930 * 930) + " Y" + FloatToStr(this_pos.y) + " A0" + ";";
					Trans_Port(fd_uart1, pos_string);
					Calibrate_Port(fd_uart1);
					//moveit();//X=this_action.target_point.x//这次移动的目标点的坐标
					this_action.dir = 0;
					this_action.target_point.y = resource_point_data[j].y;
					this_action.target_point.x = this_pos.x;
					string pos_string = "G1 X" + FloatToStr(this_pos.x) + " Y" + FloatToStr(resource_point_data[j].y) + " A0" + ";";
					Trans_Port(fd_uart1, pos_string);
					Calibrate_Port(fd_uart1);
					//moveit();
					this_action.dir = 1;
					this_action.target_point.y = this_pos.y;
					this_action.target_point.x = resource_point_data[j].x;
					string pos_string = "G1 X" + FloatToStr(resource_point_data[j].x) + " Y" + FloatToStr(this_pos.y) + " A0" + ";";
					Trans_Port(fd_uart1, pos_string);
					Calibrate_Port(fd_uart1);
					//moveit();
					this_action.target_point.dir = resource_point_data[j].dir;//底盘旋转方向
					string pos_string = "G1 X" + FloatToStr(0) + " Y" + FloatToStr(0) + " A" + FloatToStr(resource_point_data[j].dir) + ";";
					Trans_Port(fd_uart1, pos_string);
					Calibrate_Port(fd_uart1);
					/*****    此处启动抓机   *******/

					//getit();//抓取时调用地盘旋转方向，并在抓取结束转回0；
				}

			}
			Point_Data work_point_data[van[i].num + 10];
			for (int j = 0; j < van[i].num; ++j)
			{
				int id = van[i].place[j];


				int y = (id - 1) / 8;
				int x = (id - 1) % 8;
				work_point_data[j].x = 930 * x + 930 / 2;
				work_point_data[j].y = 930 * y;

				this_action.dir = 1;
				this_action.target_point.y = this_pos.y;
				this_action.target_point.x = this_pos.x / 930 * 930 + 930;
				string pos_string = "G1 X" + FloatToStr(this_pos.x / 930 * 930 + 930) + " Y" + FloatToStr(this_pos.y) + " A0" + ";";
				Trans_Port(fd_uart1, pos_string);
				Calibrate_Port(fd_uart1);
				//moveit();

				this_action.dir = 0;
				this_action.target_point.y = work_point_data[j].y;
				this_action.target_point.x = this_pos.x;
				string pos_string = "G1 X" + FloatToStr(this_pos.x) + " Y" + FloatToStr(work_point_data[j].y) + " A0" + ";";
				Trans_Port(fd_uart1, pos_string);
				Calibrate_Port(fd_uart1);
				//moveit();

				this_action.dir = 1;
				this_action.target_point.y = this_pos.y;
				this_action.target_point.x = work_point_data[j].x;
				string pos_string = "G1 X" + FloatToStr(this_pos.x / 930 * 930 + 930) + " Y" + FloatToStr(this_pos.y) + " A0" + ";";
				Trans_Port(fd_uart1, pos_string);
				Calibrate_Port(fd_uart1);
				//moveit();
				string pos_string = "G1 X0 Y0 A" + FloatToStr(this_action.target_point.dir) + ";";
				Trans_Port(fd_uart1, pos_string);
				//putit();//放下块
				/*******    此处启动抓机   *******/


			}

		}
		while (0 == lcm.handle());

	}	   
	close(fd_uart1);
	exit(0);
	return 0;
}
