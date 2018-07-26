/*
@All right reserved.
@summary: used to Serial communicate between STM32 MCU and Ubuntu14.04
@author: LiHao
@date: 2018.7.25
@refer: https://www.csdn.com
@location: DJI
*/

#include <stdio.h>      /*标准输入输出定义*/
#include <stdlib.h>     /*标准函数库定义*/
#include <unistd.h>     /*Unix标准函数定义*/
#include <sys/types.h>  /**/
#include <sys/stat.h>   /**/
#include <fcntl.h>      /*文件控制定义*/
#include <termios.h>    /*PPSIX终端控制定义*/
#include <errno.h>      /*错误号定义*/
#include <string.h>
#include <string>

#include "TrackTour.h"


/*@brief  设置串口通信速率
*@param  fd     类型 int  打开串口的文件句柄
*@param  speed  类型 int  串口速度
*@return  void
*/
#define FALSE 1
#define TRUE 0

char *recchr = "We received:\"";

int speed_arr[] = { B921600, B460800, B230400, B115200, B57600, B38400, B19200, B9600, B4800, B2400, B1200, B300, B38400, B19200, B9600, B4800, B2400, B1200, B300, };
int name_arr[] = { 921600, 460800, 230400, 115200, 57600, 38400,  19200,  9600,  4800,  2400,  1200,  300, 38400,  19200,  9600, 4800, 2400, 1200,  300, };
void set_speed(int fd, int speed)
{
	int   i;
	int   status;
	struct termios   Opt;
	tcgetattr(fd, &Opt);
	for (i = 0; i < sizeof(speed_arr) / sizeof(int); i++)
	{
		if (speed == name_arr[i])
		{
			tcflush(fd, TCIOFLUSH);
			cfsetispeed(&Opt, speed_arr[i]);
			cfsetospeed(&Opt, speed_arr[i]);
			status = tcsetattr(fd, TCSANOW, &Opt);
			if (status != 0)
				perror("tcsetattr fd1");
			return;
		}
		tcflush(fd, TCIOFLUSH);
	}
}
/*
*@brief  设置串口数据位，停止位和效验位
*@param  fd       类型  int  打开的串口文件句柄*
*@param  databits 类型  int  数据位   取值 为 7 或者8*
*@param  stopbits 类型  int  停止位   取值为 1 或者2*
*@param  parity   类型  int  效验类型 取值为N,E,O,,S
*/
int set_Parity(int fd, int databits, int stopbits, int parity)
{
	struct termios options;
	if (tcgetattr(fd, &options) != 0)
	{
		perror("SetupSerial 1");
		return(FALSE);
	}
	options.c_cflag &= ~CSIZE;
	switch (databits) /*设置数据位数*/
	{
	case 7:
		options.c_cflag |= CS7;
		break;
	case 8:
		options.c_cflag |= CS8;
		break;
	default:
		fprintf(stderr, "Unsupported data size\n");
		return (FALSE);
	}
	switch (parity)
	{
	case 'n':
	case 'N':
		options.c_cflag &= ~PARENB;   /* Clear parity enable */
		options.c_iflag &= ~INPCK;     /* Enable parity checking */
		break;
	case 'o':
	case 'O':
		options.c_cflag |= (PARODD | PARENB);  /* 设置为奇效验*/
		options.c_iflag |= INPCK;             /* Disnable parity checking */
		break;
	case 'e':
	case 'E':
		options.c_cflag |= PARENB;     /* Enable parity */
		options.c_cflag &= ~PARODD;   /* 转换为偶效验*/
		options.c_iflag |= INPCK;       /* Disnable parity checking */
		break;
	case 'S':
	case 's':  /*as no parity*/
		options.c_cflag &= ~PARENB;
		options.c_cflag &= ~CSTOPB;
		break;
	default:
		fprintf(stderr, "Unsupported parity\n");
		return (FALSE);
	}
	/* 设置停止位*/
	switch (stopbits)
	{
	case 1:
		options.c_cflag &= ~CSTOPB;
		break;
	case 2:
		options.c_cflag |= CSTOPB;
		break;
	default:
		fprintf(stderr, "Unsupported stop bits\n");
		return (FALSE);
	}
	/* Set input parity option */
	if (parity != 'n')
		options.c_iflag |= INPCK;
	options.c_cc[VTIME] = 150; // 15 seconds
	options.c_cc[VMIN] = 0;

	tcflush(fd, TCIFLUSH); /* Update the options and do it NOW */
	if (tcsetattr(fd, TCSANOW, &options) != 0)
	{
		perror("SetupSerial 3");
		return (FALSE);
	}
	return (TRUE);
}
/*
*@breif 打开串口
*/
int OpenDev(char *Dev)
{
	int fd = open(Dev, O_RDWR | O_NONBLOCK);         //| O_NOCTTY | O_NDELAY
	if (-1 == fd)
	{ /*设置数据位数*/
		perror("Can't Open Serial Port");
		return -1;
	}
	else
		return fd;

}

/*
*@breif:  传输运动数据
*@usage:  发送数据然后等待回传
*/
void Trans_Port(int fd, string trans_str)
{
	char buff[512];
	bool checkStauts = false;
	int nread;

	write(fd, trans_str.c_str(), trans_str.length());
	//读取返回信息
	while (true)
	{

		if (nread = read(fd, buff, 512) > 0)
		{
			buff[nread] = '\0';
			//读取到OK则执行操作
			if (buff == "OK")
			{
				checkStauts = true;
			}
		}
		if (checkStauts == true)   // 如果接收到OK， 立即退出循环
		{
			break;
		}
	}
}


/*
*@brief: 传输摄像头校准数据
*@usage：在到达目的地后调用该函数进行校准数据传输
*/
void Calibrate_Port(int fd)
{
	int distance_x, distance_y, slope;
	if (OpenCV_Main(0) == 0)
	{
		distance_x = CD.distance[0];
	}
	if (OpenCV_Main(1) == 0)
	{
		distance_y = CD.distance[1];
		slope = CD.slope[1];
	}
	string pos_string = "G1 X" + FloatToStr(distance_x) + " Y" + FloatToStr(distance_y) + " Z" + FloatToStr(slope) + ";";
	Trans_Port(fd, pos_string);

	char buff[512];
	bool checkStauts = false;
	int nread;

	//读取返回确认信息
	while (true)
	{
		if (nread = read(fd, buff, 512) > 0)
		{
			buff[nread] = '\0';
			//读取到OK则执行操作
			if (buff == "OK")
			{
				checkStauts = true;
			}
		}
		if (checkStauts == true)   // 如果接收到OK， 立即退出循环
		{
			break;
		}
	}
}