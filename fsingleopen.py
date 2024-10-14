from XRootD import client
from XRootD.client.flags import OpenFlags

import os, signal
import sys
import time
import random

#--------------------------------------------------------------`-----------------

port = 7779 # int( sys.argv[1] );

g_srv = "root://localhost:%d/" % port
g_com = "/xrdpfc_command/create_file/"
g_dir = "/test/"

#-------------------------------------------------------------------------------

def xxsend(args, file) :

  url = g_srv + g_com + args + g_dir + file
  print("Opening ", url)
  # return
  with client.File() as f:
    status, response = f.open(url, OpenFlags.READ)

    print('%r' % status)
    print('%r' % response)

#-------------------------------------------------------------------------------

# def sendrec(base, level) :

#   level += 1
#   adirs = [ "xxxxx"]

#   # for a0 in adirs:
#   for f in range(1, 3):
#     dirfile = "%s/file_%d.root" % (base,f)
#     print(dirfile)
#     actime = random.randint(0, 1000)
#     actimestr = " -t " + str(actime)
#     fsize = 4; # random.randint(1, 4)
#     fsizestr = "-s " + str(fsize) + "G"
#     xxsend(fsizestr + actimestr, dirfile)

#   if level < 4:
#     adirs = [ "a", "b", "c","d" ]
#     for a in adirs:
#       dirp = "%s/%s_LEVEL_%d" % (base, a, level)
#       sendrec(dirp, level)

#-------------------------------------------------------------------------------

print("Pid", os.getpid())

# Read and die, it seems

# f = client.File()
# f.open(g_srv + g_dir + "xrdmon-xxx/xmxxx-2016-09.root", OpenFlags.READ)

# # time.sleep(60)

# print("Open presumably finshed .. now reading first 4096 bytes, 30 sec timeout")
# status, data = f.read(0, 4096, 30)
# print('%r' % status)

url = 'root://localhost:7779//xrdpfc_command/create_file/-s 10G -t 918/test//d_LEVEL_1/BigFileXXXXX.root'
f = client.File()

status, response = f.open(url, OpenFlags.READ)

print('%r' % status)
print('%r' % response)




print("Killing myself horribly")
os.kill(os.getpid(), signal.SIGTERM)

print("Undt closing the foole")
f.close()
