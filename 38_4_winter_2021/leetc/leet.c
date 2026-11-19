/*
 * Dictionary Augmentation               (2021)
 *
 *    - Justin Parrott
 *
 * Augment your dictionary attack by altering the case and
 * substituting numbers for letters and letters for numbers.
 * Also by shuffling each word.  We're going to iterate
 * through all of our possibilities for each word in our
 * dictionary.
 *
 * I.E.:
 *  o In l33tsp3ak, "elite" becomes "e1i73" et al.
 *  o When shuffling, "elite" becomes "tleie" et al.
 *
 * DICTINARIES:
 *  A dictionary for password cracking is just a list of words. Each
 *  word is on its own line and no whitespace follows the word.
 *
 * UNIX USE:
 *  step 0) source code in 'leet.c', wordlist in 'words'
 *  step 1) cc -o leet -std=c99 leet.c      # compile it
 *  step 2) ln leet shuffle                 # link shuffle
 *  step 3) echo test | ./leet              # test 1337sp34k
 *  step 4) echo test | ./shuffle           # test shuffling
 *  step 5) echo test | ./leet | ./shuffle  # test both together
 *  step 6) ./leet < words                  # augment your dictionary
 *      or) ./shuffle < words
 *  step 7) pipe step 7 to stdin on your password cracker
 *
 * WINDOWS NOTES:
 *  on step 1) I use clang to compile on Windows 10 (add the -w option)
 *             i.e. clang -o leet.exe -std=c99 -w leet.c
 *  on step 2) Use: mklink shuffle.exe leet.exe
 *  on steps 3,4,5,6) you don't need the "./"
 *  on step 6) Use: type words | leet
 *              or: type words | shuffle
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINELEN 64

#ifdef _WIN32
#define DIR_CHAR '\\'
#else
#define DIR_CHAR '/'
#endif

#ifndef min
#define min(a,b) ((a) < (b) ? (a) : (b))
#endif

/* If we find one character in the string, iterate the whole group.
 * i.e. we find '7' in the string "tT7", so we iterate tT7.  This
 * is how we group our characters.
 */
char *groups[] = {
	"aA4@", "bB86&", "cC", "dD", "eE3",
	"fF", "gG", "hH#", "iI1lL!", "jJ",
	"kK", "mM", "nN", "oO0", "pP", "qQ",
	"rR9", "sSzZ52$", "tT7", "uUvV",
	"wW", "xX", "yY", NULL
};

/* lookup a character group for 133tsp34k translation */
char *
lookupg(char c)
{
	char *s, **g = groups;

	while (*g) {
		for (s = *g; *s; s++)
			if (*s == c)
				return *g;
		g++;
	}
	return NULL;
}

/* translate a word to 1337sp3ak */
void
leet(char *s, const char *word)
{
	char *grp, tbuf[LINELEN];

	if (*s) {
		if (grp = lookupg(*s)) {
			while (*grp) {
				sprintf(tbuf, "%s%c", word, *grp++);
				leet(s + 1, tbuf);
			}
		} else {
			sprintf(tbuf, "%s%c", word, *s);
			leet(s + 1, tbuf);
		}
	} else
		puts(word);
}

/* shuffle characters of a word */
void
shuffle(char *s, size_t slen, const char *word)
{
	char c, cpy[LINELEN], tbuf[LINELEN];
	bool mod = false;

	memcpy(cpy, s, slen + 1);

	for (size_t i = 0; i < slen; i++) {
		if (c = cpy[i]) {
			cpy[i] = '\0';
			sprintf(tbuf, "%s%c", word, c);
			shuffle(cpy, slen, tbuf);
			cpy[i] = c;
			mod = true;
		}
	}
	if (!mod)
		puts(word);
}

int
main(int argc, char *argv[])
{
	bool shfl = false;
	char line[LINELEN], *p = strchr(argv[0], DIR_CHAR);

	/* the program name tells us what to do */
	if (p) p++;
	else p = argv[0];
	/* compare against "shuffle", excluding ".exe", for Windows */
	if (!strncmp(p, "shuffle", min(strlen(p), 7)))
		shfl = true;

	while (fgets(line, sizeof line, stdin)) {
		line[strcspn(line, "\n")] = '\0';
		if (shfl)
			shuffle(line, strlen(line), "");
		else
			leet(line, "");
	}

	return 0;
}


