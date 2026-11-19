#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *av[])
{

   if (getenv("LD_PRELOAD"))
	printf("%s\n", getenv("LD_PRELOAD"));
   else
	printf("no LD_PRELOAD found\n");

}

