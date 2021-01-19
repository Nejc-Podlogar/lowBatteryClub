/*
 * printf.h
 */

#ifndef PRINTF_H_
#define PRINTF_H_
#include <stdio.h>
#include <stdint.h>

int _write(int file, char *ptr, int len)
{
	/* Implement your write code here, this is used by puts and printf for example */
	int i = 0;
	for( i = 0 ; i < len ; i++)
		ITM_SendChar((*ptr++));
	return len;
}

#endif /* PRINTF_H_ */
