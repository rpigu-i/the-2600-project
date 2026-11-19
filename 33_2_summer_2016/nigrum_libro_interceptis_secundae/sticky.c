#define _GNU_SOURCE

#include <stdio.h>
#include <unistd.h>
#include <dlfcn.h>
#include <string.h>
#include <sys/types.h>

typedef char *(*getenv_t)(const char *name);
typedef int (*setenv_t)(const char *name, const char *value, int overwrite);
typedef int (*unsetenv_t)(const char *name);

char *getenv(const char *name)
{
   static getenv_t real_getenv = NULL;
   real_getenv = dlsym(RTLD_NEXT, "getenv");

   fprintf(stderr,"hooked getenv\n");
   if (!strcmp("LD_PRELOAD",name))
   {
	fprintf(stderr,"getenv subvert\n");
	return NULL;
   }
   else
   {
	return real_getenv(name);
   }
}
int setenv(const char *name, const char *value, int overwrite)
{
   static setenv_t real_setenv = NULL;
   real_setenv = dlsym(RTLD_NEXT, "setenv");

   fprintf(stderr,"hooked setenv\n");
   if (!strcmp("LD_PRELOAD",name))
   {
	fprintf(stderr,"setenv subvert\n");
	return NULL;
   }
   else
   {
	return real_setenv(name,value,overwrite);
   
}

int unsetenv(const char *name)
{
   static unsetenv_t real_unsetenv = NULL;
   real_unsetenv = dlsym(RTLD_NEXT, "unsetenv");

   fprintf(stderr,"hooked unsetenv\n");
   if (!strcmp("LD_PRELOAD",name))
   {
	fprintf(stderr,"unsetenv subvert\n");
	return NULL;
   }
   else
   {
	return real_unsetenv(name);
   }
}
