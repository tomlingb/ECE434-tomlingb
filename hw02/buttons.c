
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <signal.h>	// Defines signal-handling functions (i.e. trap Ctrl-C)
#include "gpio-utils.h"

 /****************************************************************
 * Constants
 ****************************************************************/
 
#define POLL_TIMEOUT (3 * 10000) /* 30 seconds */
#define MAX_BUF 64

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;	// Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "Ctrl-C pressed, cleaning up and exiting..\n" );
	keepgoing = 0;
}

/****************************************************************
 * Main
 ****************************************************************/
int main(int argc, char **argv, char **envp)
{
	struct pollfd fdset[8];
	int nfds = 8;
	int gpioin_fd1, gpioin_fd2, gpioin_fd3, gpioin_fd4, gpioout_fd1, gpioout_fd2, gpioout_fd3, gpioout_fd4, timeout, rc;
	char buf[MAX_BUF];
	unsigned int gpioin1, gpioin2, gpioin3, gpioin4, gpioout1, gpioout2, gpioout3, gpioout4;
	int len;

// 	if (argc < 2) {
// 		printf("Usage: gpio-int <gpio-pin>\n\n");
// 		printf("Waits for a change in the GPIO pin voltage level or input on stdin\n");
// 		exit(-1);
// 	}

	// Set the signal callback for Ctrl-C
	signal(SIGINT, signal_handler);

	gpioin1 = 117;
	gpioin2 = 115;
	gpioin3 = 113;
	gpioin4 = 111;
	
	gpioout1 = 60;
	gpioout2 = 31;
	gpioout3 = 50;
	gpioout4 = 48;

	gpio_export(gpioin1);
	gpio_set_dir(gpioin1, "in");
	gpio_set_edge(gpioin1, "both");  // Can be rising, falling or both
	gpioin_fd1 = gpio_fd_open(gpioin1, O_RDONLY);
	
	gpio_export(gpioin2);
	gpio_set_dir(gpioin2, "in");
	gpio_set_edge(gpioin2, "both");  // Can be rising, falling or both
	gpioin_fd2 = gpio_fd_open(gpioin2, O_RDONLY);
	
	gpio_export(gpioin3);
	gpio_set_dir(gpioin3, "in");
	gpio_set_edge(gpioin3, "both");  // Can be rising, falling or both
	gpioin_fd3 = gpio_fd_open(gpioin3, O_RDONLY);
	
	gpio_export(gpioin4);
	gpio_set_dir(gpioin4, "in");
	gpio_set_edge(gpioin4, "both");  // Can be rising, falling or both
	gpioin_fd4 = gpio_fd_open(gpioin4, O_RDONLY);

	gpio_export(gpioout1);
	gpio_set_dir(gpioout1, "out");
	gpioout_fd1 = gpio_fd_open(gpioout1, O_WRONLY);
	
	gpio_export(gpioout2);
	gpio_set_dir(gpioout2, "out");
	gpioout_fd2 = gpio_fd_open(gpioout2, O_WRONLY);
	
	gpio_export(gpioout3);
	gpio_set_dir(gpioout3, "out");
	gpioout_fd3 = gpio_fd_open(gpioout3, O_WRONLY);
	
	gpio_export(gpioout4);
	gpio_set_dir(gpioout4, "out");
	gpioout_fd4 = gpio_fd_open(gpioout4, O_WRONLY);

	timeout = POLL_TIMEOUT;
 
	while (keepgoing) {
		memset((void*)fdset, 0, sizeof(fdset));

		fdset[0].fd = STDIN_FILENO;
		fdset[0].events = POLLIN;
      
		fdset[1].fd = gpioin_fd1;
		fdset[1].events = POLLPRI;
		
		fdset[2].fd = gpioin_fd2;
		fdset[2].events = POLLPRI;
		
		fdset[3].fd = gpioin_fd3;
		fdset[3].events = POLLPRI;
		
		fdset[4].fd = gpioin_fd4;
		fdset[4].events = POLLPRI;

		rc = poll(fdset, nfds, timeout);      

		if (rc < 0) {
			printf("\npoll() failed!\n");
			return -1;
		}
      
		if (rc == 0) {
// 			printf(".");
		}
            
		if (fdset[1].revents & POLLPRI) {
			lseek(fdset[1].fd, 0, SEEK_SET);  // Read from the start of the file
			len = read(fdset[1].fd, buf, MAX_BUF);
// 			printf("\npoll() GPIO %d interrupt occurred, value=%c, len=%d\n",
				//  gpioin1, buf[0], len);
			if (buf[0] == 49) { 
				write(gpioout_fd1, "1", 2);
			}
			if (buf[0] == 48) {
				write(gpioout_fd1, "0", 2);
			}
		}
		
		if (fdset[2].revents & POLLPRI) {
			lseek(fdset[2].fd, 0, SEEK_SET);  // Read from the start of the file
			len = read(fdset[2].fd, buf, MAX_BUF);
// 			printf("\npoll() GPIO %d interrupt occurred, value=%c, len=%d\n",
				//  gpioin2, buf[0], len);
			if (buf[0] == 49) { 
				write(gpioout_fd2, "1", 2);
			}
			if (buf[0] == 48) {
				write(gpioout_fd2, "0", 2);
			}
		}
		
		if (fdset[3].revents & POLLPRI) {
			lseek(fdset[3].fd, 0, SEEK_SET);  // Read from the start of the file
			len = read(fdset[3].fd, buf, MAX_BUF);
// 			printf("\npoll() GPIO %d interrupt occurred, value=%c, len=%d\n",
				//  gpioin3, buf[0], len);
			if (buf[0] == 49) { 
				write(gpioout_fd3, "1", 2);
			}
			if (buf[0] == 48) {
				write(gpioout_fd3, "0", 2);
			}
		}
		
		if (fdset[4].revents & POLLPRI) {
			lseek(fdset[4].fd, 0, SEEK_SET);  // Read from the start of the file
			len = read(fdset[4].fd, buf, MAX_BUF);
// 			printf("\npoll() GPIO %d interrupt occurred, value=%c, len=%d\n",
				//  gpioin4, buf[0], len);
			if (buf[0] == 49) { 
				write(gpioout_fd4, "1", 2);
			}
			if (buf[0] == 48) {
				write(gpioout_fd4, "0", 2);
			}
		}

		if (fdset[0].revents & POLLIN) {
			(void)read(fdset[0].fd, buf, 1);
			printf("\npoll() stdin read 0x%2.2X\n", (unsigned int) buf[0]);
		}

		fflush(stdout);
	}

	gpio_fd_close(gpioin_fd1);
	gpio_fd_close(gpioout_fd1);
	gpio_fd_close(gpioin_fd2);
	gpio_fd_close(gpioout_fd2);
	gpio_fd_close(gpioin_fd3);
	gpio_fd_close(gpioout_fd3);
	gpio_fd_close(gpioin_fd4);
	gpio_fd_close(gpioout_fd4);
	return 0;
}

