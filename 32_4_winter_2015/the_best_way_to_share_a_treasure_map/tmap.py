#!/usr/bin/python

import zfec
from Crypto.Cipher import AES
from Crypto import Random
import sys

def tmapzfecsplit(data, m, k):
    splitter = zfec.easyfec.Encoder(k, m)
    splitdata = splitter.encode(data)
    # calc pad
    padlen = len(splitdata[0])*k - len(data)
    # prepend k,m sharenum, and padlen to each block - can't recreate without it
    splitdata = [str(k)+","+str(m)+","+str(snum)+","+str(padlen)+":"+sdata for snum, sdata in enumerate(splitdata)]
    return splitdata

def tmaprecreate(datablocks):
    sharenums = []
    cleanblocks = []
    k = 0
    m = 0
    padlen = 0
    for block in datablocks:
        splitdata = block.split(":", 1)
        cleanblocks.append(splitdata[1])
        metadata = splitdata[0].split(",")
        k = int(metadata[0])
        m = int(metadata[1])
        sharenums.append(int(metadata[2]))
        padlen = int(metadata[3])

    if len(cleanblocks) < k:
        # not enough blocks provided
        raise Exception("Can't recreate file. Need {} parts, only have {}.".format(k, len(cleanblocks)))

    decoder = zfec.easyfec.Decoder(k,m)
    origdata = decoder.decode(cleanblocks, sharenums, padlen)
    return origdata

def tmap_encryptdata(data):
    # AES-256 encrypts the data, pre-pending the IV and appending the key
    # the IV is the stringified padding value to get to 16 byte blocksize
    # 32 byte key is random
    padlen = 16 - (len(data) % 16)
    iv = "0" * (16- len(str(padlen))) + str(padlen)
    data = data + "0" * padlen
    key = Random.new().read(32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptedData = iv + cipher.encrypt(data) + key
    return encryptedData

def tmap_decryptdata(encryptedData):
    # AES-256 decrypts data
    # expects first 16 bytes is IV (and padlen)
    # and last 32 is the key
    iv = encryptedData[:16]
    key = encryptedData[-32:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = encryptedData[16:-32]
    data = cipher.decrypt(msg)
    padlen = int(iv)
    data = data[:-padlen]
    return data

def tmap_split(filename, m, k):
    # encrypts data in filename
    # splits the data into m parts, k of which can recreate the file
    # prepends the filename to each file
    # saves as filename-X.tmap
    f = open(filename)
    data = f.read()
    f.close()
    enc_data = tmap_encryptdata(data)
    datablocks = tmapzfecsplit(enc_data, m, k)

    for filenum, data in enumerate(datablocks):
        f = open("{}-{}.tmap".format(filename, filenum+1), "wb")
        data = filename+":"+data
        f.write(data)
        f.close()

    return

def tmap_rebuild(filenames):
    # rebuilds a tmap file from the parts in filenames
    savefilename = ""
    datablocks = []
    for name in filenames:
        fr = open(name, "rb")
        data_raw = fr.read()
        fr.close()
        data_split = data_raw.split(":", 1)
        if savefilename == "":
            savefilename = data_split[0]
        elif not savefilename == data_split[0]:
            raise Exception("Not all data is from the same file. Cannot recreate")
        datablocks.append(data_split[1])

    enc_data = tmaprecreate(datablocks)
    data = tmap_decryptdata(enc_data)
    f = open(savefilename, "wb")
    f.write(data)

def tmap_cmdline(args):
    # not using getopt to save code space, but harder to detect errors
    help_text = 'Usage:\ntmap --make m k filename\n\tSplit filename into m parts, k of which are needed to recover\n'
    help_text = help_text + 'tmap --recover file1 file2 file3 ... filen\n\tAttempt to recover the file from the listed parts.'
    help_text = help_text + '\nArguments must be in order!!'

    if len(args) < 3:
        print help_text
        sys.exit(2)

    try:
        if args[1] == "--make":
            m = int(args[2])
            k = int(args[3])
            tmap_split(args[4], m, k)
            print "{} split into {} parts, {} needed to recover.".format(args[4], m, k)
        elif args[1] == "--recover":
            tmap_rebuild(args[2:])
            print "File recovered!"
        else:
            print help_text
    except Exception as e:
        print "Failed to work:"
        print e.args[0]
        sys.exit(2)

tmap_cmdline(sys.argv)


