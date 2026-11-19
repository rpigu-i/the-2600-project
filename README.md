```
 _____ _            _____   ____ _____  _____  ______          _           _    
|_   _| |          / __  \ / ___|  _  ||  _  | | ___ \        (_)         | |   
  | | | |__   ___  `' / /'/ /___| |/' || |/' | | |_/ / __ ___  _  ___  ___| |_  
  | | | '_ \ / _ \   / /  | ___ \  /| ||  /| | |  __/ '__/ _ \| |/ _ \/ __| __| 
  | | | | | |  __/ ./ /___| \_/ \ |_/ /\ |_/ / | |  | | | (_) | |  __/ (__| |_  
  \_/ |_| |_|\___| \_____/\_____/\___/  \___/  \_|  |_|  \___/| |\___|\___|\__| 
                                                             _/ |               
                                                            |__/                
 _____           _         ___           _     _                                
/  __ \         | |       / _ \         | |   (_)                               
| /  \/ ___   __| | ___  / /_\ \_ __ ___| |__  ___   _____                      
| |    / _ \ / _` |/ _ \ |  _  | '__/ __| '_ \| \ \ / / _ \                     
| \__/\ (_) | (_| |  __/ | | | | | | (__| | | | |\ V /  __/                     
 \____/\___/ \__,_|\___| \_| |_/_|  \___|_| |_|_| \_/ \___|        

```


A project to containerize/virtualize all the code from every 2600 magazine and serve from VMS, K8s or other container serving environment. This project is not linked to #2600 Magazine (https://www.2600.com/) in any official capacity. 


## Background

The purpose of this project is to collect all the old source code published in 2600, and create a set of containers so these can be run.
Not only does this preserve the code for future research, container based environments will allow you to run legacy operating systems and packages.

Threfore what we are creating is an archive of legacy code that will be available to anyone interested in running it, researching it or experimenting with it.


## Contributing

Check if the code has been ported to this repository. If not follow these steps:


1. Grab this repository by forking it.

2. Create a folder/use the folder for the magazine edition e.g. `23-4: Winter 2006-2007` would be: `23_4_winter_2006`

3. Clone and add a Dockerfile for the project, or other environment file required to run the code. 

4. Add in the code from 2600 Magazine

5. Get it running and update the README, including the magazine edition, a quick synopsis and the original author who created it. Any instructions to run the code should be included.

6. Create a PR from your Fork to this repository


Note: Some code may be copied over without a Dockerfile initially. If you would like to help get it running, follow the steps above, but add the Dockerfile to the folder with the code, and work to get it running.


## Disclaimer

The code in this repository is for educational and research purposes only. As many of the files contain work arounds, hacks and examples of bypassing security tooling, use at your own risk and use responsibly. 


## Magazine Editions Ported

* Spring 2004 - Autumn 2026 (All editions from Volume 21 through Volume 43, Issue 3)

### Complete List by Year:

**2004 (Volume 21):** Spring, Summer, Autumn, Winter

**2005 (Volume 22):** Spring, Summer, Autumn, Winter

**2006 (Volume 23):** Spring, Summer, Autumn, Winter

**2007 (Volume 24):** Spring, Summer, Autumn, Winter

**2008 (Volume 25):** Spring, Summer, Autumn, Winter

**2009 (Volume 26):** Spring, Summer, Autumn, Winter

**2010 (Volume 27):** Spring, Summer, Autumn, Winter

**2011 (Volume 28):** Spring, Summer, Autumn, Winter

**2012 (Volume 29):** Spring, Summer, Autumn, Winter

**2013 (Volume 30):** Spring, Summer, Autumn, Winter

**2014 (Volume 31):** Spring, Summer, Autumn, Winter

**2015 (Volume 32):** Spring, Summer, Autumn, Winter

**2016 (Volume 33):** Spring, Summer, Autumn, Winter

**2017 (Volume 34):** Spring, Summer, Autumn, Winter

**2018 (Volume 35):** Spring, Summer, Autumn, Winter

**2019 (Volume 36):** Spring, Summer, Autumn, Winter

**2020 (Volume 37):** Spring, Summer, Autumn, Winter

**2021 (Volume 38):** Spring, Summer, Autumn, Winter

**2022 (Volume 39):** Spring, Summer, Autumn, Winter

**2023 (Volume 40):** Spring, Summer, Autumn, Winter

**2024 (Volume 41):** Spring, Summer, Autumn, Winter

**2025 (Volume 42):** Spring, Summer, Autumn, Winter

**2026 (Volume 43):** Spring, Summer, Autumn

## Thanks and ShoutOuts


Thanks to Nightride FM for providing an awesome soundtrack while porting the code over.

Check out their live feed on YouTube at: https://www.youtube.com/watch?v=cZRj9Sk0IPc

For more details:

* Join their community at: https://discord.gg/synthwave
* Visit their main website for higher quality audio at:  https://nightride.fm
* Support them on Patreon at: https://patreon.com/nightridefm


Shoutout to DefCon Group 561. 
