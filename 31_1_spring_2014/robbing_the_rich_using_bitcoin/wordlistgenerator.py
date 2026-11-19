### wordlistgenerator.py by blerbl
import re, sys, os, urllib
#### custom useragent
class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0(compatable;MSIE 9.0; Windows NT 6.1; Trident/5.0)"

urllib._urlopener = AppURLopener()
uopen = urllib.urlopen
uencode = urllib.urlencode

###############################################################
###
### Helper Function
###

def ls(file):
    print(open(file,'rb').read())

def google(query,numget=10,verbose=0):
    numget = int(numget)
    start = 0
    results = []
    if verbose == 2:
        print "[+]Getting " + str(numget) + " results"
    while len(results) < numget:
        print "[+]"+str(len(results)) + " so far..."
        data =
uopen("https://www.google.com/search?q="+query+"&start="+str(start))
        if data.code != 200:
            print "Error " + str(data.code)
            break
        results.extend(re.findall("<a href=\"([^\"]*)\"
class=(?:l|s)",data.read()))
        start += 10
    if verbose == 2: print "[+] Got " + str(numget) + " results"
    return results[:numget]

def genWordlist(targetlist,word_reg,outfile,verbose=0,quotes=True):
    quote_reg = re.compile("\"([^\"]{2,35})\"")
    ###
    ### Initialize Engine
    ###
    words = []
    append = False
    total_wb = 0
    dircount = 0
    totalcount = 0
    ###
    ### Read the old list
    ###
    if outfile.startswith("+"):
        outfile = outfile[1:]
        words = open(outfile).readlines()
        append = True
        total_wb = len(words)
    ###
    ### Hit the sources
    ###

    for target in targetlist:

        data = None
        ###
        ### Get the data
        ###
        if os.path.isfile(target):
            data = open(target).read()
        elif os.path.isdir(target):
            dircount += 1 # for stats in end
            subtargets = os.listdir(target)
            for subtarget in subtargets:
                if os.path.isfile(subtarget):
                    data = "\n\n" + os.read(subtarget)
                else:
                    targetlist.append(subtarget)
                    #We will get it the next time around
        else:
            try:
                res = uopen(target)
                if res.code != 200:
                    print "[!]Error: " + str(res.code)
                else:
                    data = res.read()
            except Exception as e:
                print "[!]"+str(e)

        totalcount += 1
        if not data:
            if verbose: print "[-]No data from source: " + str(target)
            continue
        else:
            if verbose:
                sys.stdout.write(str(totalcount) + " of ~" +
str(len(targetlist)) + " sources complete\r")
                sys.stdout.flush()
            else:
                pass
        ###
        ### Format the data
        ###
        data = re.sub("(<!--|-->)"," ",data) # keep comments as normal text
        data = re.sub("</?[^>]+>"," ",data) # remove the html tags

        data = re.sub("\r|\n"," ",data) # make it a strait file

        ###
        ### Add the new words
        ###
        allwords = word_reg.findall(data)
        allquotes = quote_reg.findall(data)
        for quote in allquotes:
            allwords.append(quote)
            allwords.append(quote.replace(" ",""))
            #flw = ''
            #for each in quote.split(' '):
            # if len(each) > 0: flw += each[0]
            #if flw: allwords.append(flw)

        for word in allwords:
            ###
            ### Mangle
            ###

            if( word.endswith('.') or
                word.endswith(',') or
                word.endswith('!') or
                word.endswith('?') or
                word.endswith(';') or
                word.endswith('"') or
                word.endswith('\'')):
                allwords.append(word.strip('.,!?;"\''))
            if re.match("\A.*\.(jpg|png|txt|com|html)\Z",word):
                allwords.append(word.rsplit('.',1)[0])

            ###
            ### Add
            ###
            if not word in words:
                words.append(word)

    total_wa = len(words)
    total_s = len(targetlist)
    words.sort()
    of = open(outfile,'w')
    for word in words:
        of.write(word+"\n")
    of.close()
    if verbose:
        print "[+]Complete!"
        print "[+]"+ str(total_wa) + " words in the list."
        if append: print "[+]"+str(total_wa - total_wb)+" are new."
        print "[+]Collected from " + str(total_s - dircount) + " sources."

if __name__ == "__main__":
    ###
    ### User input
    ###

    verbose = 2
    minlen = 6
    maxlen = None
    find_quotes = True

    wordrules = ["A-z","A-z0-9","A-z0-9*-.!$#@%"]

    wordrule = None
    while not wordrule:
        print "Select a word rule:"
        for i,rule in enumerate(wordrules):
            print str(i + 1) + " -- " + wordrules[i]
        print str(i+2) + " Custom (WARNING: ADVANCED!! not validation)"
        que = raw_input("Rule[1-"+str(i+2)+"]:")
        try: que = int(que.strip())
        except: que = -1
        if que == i+2:
            wordrule = raw_input("Wordrule:").strip()
        elif que < 1 or que > i+2:
            print "Not a valid selection"
        else:
            wordrule = wordrules[i-1]

    if not minlen: minlen = 3
    outfile = raw_input("Filename:")
    if os.path.exists(outfile) and not outfile.startswith("+"):
        que = raw_input("[?]This file exists! Overwrite[y|N]:")
        if not 'y' in que.lower():
            exit(0)
    targetlist = raw_input("Input target list, separate by ';' no space or
quote\n"+
                            "Use %g<query>%<numresults> to use google query
sites\n"+
                            "Targets:")
    targetlist = targetlist.split(';')
    for target in targetlist:
        if re.match("%g[^%]+%[0-9]+",target):
            if verbose == 2: print "[+]Google sources: " +
target[2:].split('%')[0]
            new_targets =
google(target[2:].split("%")[0],target[2:].split("%")[1],verbose)
            targetlist.remove(target)
            targetlist.extend(new_targets)
    if verbose == 2:
        print "[+]Gathering data from the following targets:"
        for target in targetlist: print "[+]"+target
        print "============================================="
    ###
    ### Prepare and call
    ###
    word_reg =
re.compile("(["+wordrule+"]{"+str(minlen)+","+str(maxlen)+"})")
    genWordlist(targetlist,word_reg,outfile,verbose)

