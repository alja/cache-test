from XRootD import client
from XRootD.client.flags import OpenFlags

import os, signal
import sys
import time
import random
import time
import argparse

# Define the parser
parser = argparse.ArgumentParser(description='Short sample app')
#--------------------------------------------------------------`-----------------

port = 7777 # int( sys.argv[1] );

g_srv = "root://localhost:%d/" % port
g_com = "/xrdpfc_command/create_file/"
g_dir = "/fake-samples/" + str(random.getrandbits(128)) # + "/"

parser.add_argument('--dir', action="store", dest='dir', default=g_dir)
#-------------------------------------------------------------------------------

def xxsend(args, file) :

  url = g_srv + g_com + args + g_dir + file
  print("Opening ", url)
  # return
  with client.File() as f:
    status, response = f.open(url, OpenFlags.READ)
    time.sleep(0.0001)

    print('%r' % status)
    print('%r' % response)
    f.close()

#-------------------------------------------------------------------------------

def sendrec(base, level) :

  #maximum depth
  max_level = 1

  for f in range(0, 2):
    dirfile = "%s/Bfile_%d.root" % (base,f)
    print(dirfile)
    epoch_time = int(time.time())
    actime = epoch_time - random.randint(0, 1000)
    actimestr = " -t " + str(actime) + " "
    # fsize =  random.randint(1, 9)
    fsize = 512
    fsizestr = "-s " + str(fsize) + "M"
    xxsend(fsizestr + actimestr, dirfile)

  if level < max_level:
    level += 1
    adirs = [ "a", "b", "c", "d",  "e", "f", "g"]
    # adirs = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" ]
    for a in adirs:
      dirp = "%s/%s_LEVEL_%d" % (base, a, level)
      sendrec(dirp, level)
      time.sleep(1.5)

#-------------------------------------------------------------------------------

print("Pid", os.getpid())
sc_args = parser.parse_args()
g_dir=sc_args.dir


sendrec("", 0)

sys.exit(0)

# Read and die, it seems

f = client.File()
f.open(g_srv + g_dir + "xrdmon-xxx/xmxxx-2016-09.root", OpenFlags.READ)

# time.sleep(60)

print("Open presumably finshed .. now reading first 4096 bytes, 30 sec timeout")
status, data = f.read(0, 4096, 30)
print('%r' % status)

print("Killing myself horribly")
os.kill(os.getpid(), signal.SIGTERM)

print("Undt closing the foole")
f.close()
