#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <stdio.h>
#include <lcm/lcm-cpp.hpp>
#include "head/info_head.hpp"
#include "normal/info_normal.hpp"
using namespace std;


int16_t start_area = 0;
int16_t run_times = 0;

struct Point_Data
{
	float x, y;//绝对坐标
	int dir;//底盘顺时针旋转的角度
	Point_Data()
	{
		x = 0.0;
		y = 0.0;
		dir = 0;
	}

}start_data;
struct Run_Data
{
	int16_t num;
	int16_t resource[20];
	int16_t place[20];
	Run_Data()
	{
		num = 0;
	}
}van[20];

struct Action_Data
{
	int dir;//平移或直走
	Point_Data target_point;
};
class Handler
{
public:
	~Handler() {}

	void handleMessage1(const lcm::ReceiveBuffer* rbuf,
		const std::string& chan,
		const head::info_head* msg)
	{
		start_area = msg->start;
		run_times = msg->times;
	}
	void handleMessage2(const lcm::ReceiveBuffer* rbuf,
		const std::string& chan,
		const normal::info_normal* msg,int i)
	{
		van[i].num = msg->num;
		for (int j = 0; j < msg->num; ++j)
		{
			van[i].resource[j] = msg->resource[j];
			van[i].place[j] = msg->place[j];
		}
	}
};


int main(int argc, char** argv)
{
	lcm::LCM lcm;

	if (!lcm.good())
		return 1;
	Point_Data this_pos;
	Action_Data this_action;
	Handler handlerObject;

	lcm.subscribe("SENDHEAD", &Handler::handleMessage1, &handlerObject);
	switch (start_area) 
	{
	case 1:
		start_data.x = -0.93 / 2.0;
		start_data.y = -0.93 / 2.0;
		break;
	case 2:
		start_data.x = -0.93 / 2.0;
		start_data.y = 0.93 * 8.0 + 0.93 / 2.0;
		break;
	case 3:
		start_data.x = 0.93 * 8.0 + 0.93 / 2.0;
		start_data.y = 0.93 * 8.0 + 0.93 / 2.0;
		break;
	case 4:
		start_data.x = 0.93 * 8.0 + 0.93 / 2.0;
		start_data.y = -0.93 / 2.0;
		break;
	default:
		lcm.subscribe("SENDHEAD", &Handler::handleMessage1, &handlerObject);
		break;
	}
	this_pos.x = 0;
	this_pos.y = 0;

	for (int i = 0; i < run_times; ++i)
	{
		lcm.subscribe("SENDNORMAL", &Handler::handleMessage1, &handlerObject, i);
		int flag = 0;
		Point_Data resource_point_data[van[i].num+10];
		for (int j = 0; j < van[i].num; ++j)
		{
			
			int id = van[i].resource[j];
			int temp1 = id / 100, temp2 = (id / 10) % 10, temp3 = id % 10;
			switch(temp1)
			{
			case 1:
				int py = 0;
				if (temp3 == 3)py = 1;
				if (temp3 == 4)py = 2;
				if (temp3 == 5)py = 3;
				resource_point_data[j].x = float(temp2)* 0.93+0.31*py;
				resource_point_data[j].y = 7.0*0.93;
				resource_point_data[j].dir = 0;
				break;		   
			case 2:		
				int py = 0;
				if (temp3 == 3)py = 1;
				if (temp3 == 4)py = 2;
				if (temp3 == 5)py = 3;
				resource_point_data[j].x = 7.0*0.93;
				resource_point_data[j].y = (7.0 - temp2)*0.93 + (4 - py)*0.31;
				resource_point_data[j].dir = 90;
				break;		   
			case 3:			
				int py = 0;
				if (temp3 == 3)py = 1;
				if (temp3 == 4)py = 2;
				if (temp3 == 5)py = 3;
				resource_point_data[j].x = (7.0 - temp2)*0.93+ (4 - py)*0.31;
				resource_point_data[j].y = 0.0;
				resource_point_data[j].dir = 180;
				break;		   
			case 4:			 
				int py = 0;
				if (temp3 == 3)py = 1;
				if (temp3 == 4)py = 2;
				if (temp3 == 5)py = 3;
				resource_point_data[j].x = 0.0;
				resource_point_data[j].y = float(temp2)*0.93 +(py)*0.31;
				resource_point_data[j].dir = 270;
				break;
			default:
				continue;
				break;
			}
		
			if (resource_point_data[j].y == this_pos.y)
			{
				this_action.dir = 1;
				this_action.target_point = resource_point_data[j];
				//moveit();
				//getit();//包括this_action.target_point.dir-----底盘旋转方向。
			}
			else
			{
				
				this_action.dir = 1;//dir==1表示平移，dir==0表示直行
				this_action.target_point.y = this_pos.y;
				this_action.target_point.x = this_pos.x / 930 * 930+930;
				
				//moveit();//X=this_action.target_point.x//这次移动的目标点的坐标
				this_action.dir = 0;
				this_action.target_point.y = resource_point_data[j].y;
				this_action.target_point.x = this_pos.x;
				//moveit();
				this_action.dir = 1;
				this_action.target_point.y = this_pos.y;
				this_action.target_point.x = resource_point_data[j].x;
				//moveit();
				this_action.target_point.dir = resource_point_data[j].dir;//底盘旋转方向
				//getit();//抓取时调用地盘旋转方向，并在抓取结束转回0；
			}
		
		}
		Point_Data work_point_data[van[i].num+10];
		for (int j = 0; j < van[i].num; ++j)
		{
			int id = van[i].place[j];


			int y = (id-1) / 8 ;
			int x = (id -1)% 8 ;
			work_point_data[j].x = 930*x+930/2;
			work_point_data[j].y = 930*y;

			this_action.dir = 1;
			this_action.target_point.y = this_pos.y;
			this_action.target_point.x = this_pos.x / 930 * 930 + 930;
			//moveit();
			this_action.dir = 0;
			this_action.target_point.y = work_point_data[j].y;
			this_action.target_point.x = this_pos.x;
			//moveit();
			this_action.dir = 1;
			this_action.target_point.y = this_pos.y;
			this_action.target_point.x = work_point_data[j].x;
			//moveit();
			//putit();//放下块

		}
	

	
	}


	while (0 == lcm.handle());

	return 0;
}