#include <iostream>
#include <string>
#include <stdlib.h>
#include <unistd.h>     /*Unix标准函数定义*/
#include <sys/types.h>  /**/
#include <sys/stat.h>   /**/
#include <fcntl.h>      /*文件控制定义*/
#include <termios.h>    /*PPSIX终端控制定义*/
#include <errno.h>      /*错误号定义*/
#include <string.h>
#include <string>

#include "info_head.hpp"
#include "info_inter.hpp"

#define max 100
#define FALSE 1
#define TRUE 0

using namespace std;
int fd_uart1, fd_uart4;
char *UART1 = "/dev/ttyTHS0"; //Uart1
char *UART2 = "/dev/ttyS0"; //UART4
bool needMove = false;


char *recchr = "We received:\"";

int speed_arr[] = { B921600, B460800, B230400, B115200, B57600, B38400, B19200, B9600, B4800, B2400, B1200, B300, B38400, B19200, B9600, B4800, B2400, B1200, B300, };
int name_arr[] = { 921600, 460800, 230400, 115200, 57600, 38400,  19200,  9600,  4800,  2400,  1200,  300, 38400,  19200,  9600, 4800, 2400, 1200,  300, };

void Trans_Port(int fd, string trans_str);
int OpenDev(char *Dev);
string pos_string;

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
				perror("tcseuart1tattr fd1");
			return;
		}
		tcflush(fd, TCIOFLUSH);
	}
}
void Trans_Port(int fd, string trans_str)
{
	char buff[512];
	bool checkStauts = false;
	int nread;

	write(fd, trans_str.c_str(), trans_str.length());
	cout << trans_str << endl;

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

int main()
{
	/*******     初始化UART1,UART4           *******/

	cout << "Powered by Team12" << endl;

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
	if (set_Parity(fd_uart1, 8, 1, 'N') == FALSE) //set parity
	{
		printf("Set Parity 1  Error\n");
		exit(1);
	}
	cout << "Second!!!!!!!!!!!!!!!!!!!!!11" << endl;

	lcm::LCM lcm;

	if (!lcm.good())
		return 1;
	Handler handlerObject;
	lcm.subscribe("SENDINTER", &Handler::handleMessage, &handlerObject);
	while (0 == lcm.handle())
	{
		if (needMove)
		{
			Trans_Port(fd_uart1, pos_string);
			close(fd_uart1);
			sleep(1);
			system("./TrackTour");
			fd_uart1 = OpenDev(UART1); //open uart1
			cout << "End" << endl;
			needMove = false;

		}

	}
	return 0;
}


