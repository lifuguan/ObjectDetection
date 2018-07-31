#include <iostream>
#include "SerialPort.h"
#include "data_processing.h"


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
	fd_uart4 = OpenDev(UART2); //open uart4
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


	if (set_Parity(fd_uart1, 8, 1, 'N') == FALSE) //set parity	 1
	{
		printf("Set Parity 1  Error\n");
		exit(1);
	}
	if (set_Parity(fd_uart4, 8, 1, 'N') == FALSE) //set parity	 4
	{
		printf("Set Parity 4  Error\n");
		exit(1);
	}
	write(fd_uart1, "G0 X0.93 Y0 W0", 20);
	
	//exit(0);
	return 0;
}

