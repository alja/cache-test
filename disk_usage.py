import os
import shutil
cache_path = "/data2/alja/xrootd/cached-data"

gb = 1024*1024*1024

# giga bytes from config
f0 = 200 * gb
f1 =1000 * gb
f2 =1100 * gb

w1 = 3000 * gb
w2 = 5000 * gb

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            # print(f)
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                #print("accumulate size ", total_size)

    return total_size

# utility func
def clamp(x, bytes_to_remove, lowval, highval):
    print("clam val ", x, "bytest to remove ", bytes_to_remove)
   # print("clam val Gb", bytes_to_remove >> 30)
    print ("clamp bytest to remove ", bytes_to_remove/(1024*1024*1024) )
    val = x
    newval = val - bytes_to_remove

    if (newval < lowval):
        return lowval - val

    if (newval > highval):
        return highval - val

    return bytes_to_remove

#########################################################
## MAIN
#######################################################

stat = shutil.disk_usage(cache_path) 

cache_size = get_size(cache_path)
print("total size ",stat.total >> 30)
print("used size ",stat.used >> 30 )
print("cache size ", cache_size >> 30)


print("percentage used ", float(stat.used)/stat.total)
print("used ", stat.used >> 30,  "percantage w2 ", float(w2)/stat.total)

print("------- are there bytes to remove ? ")

if (cache_size < f0):
   print("x less f0")
   quit()


if (stat.used > w2):
    print("u > w2")
    bytes_to_remove = 0
    frac_x = float(cache_size -f0)/(f1-f0)
    # W2 == T ??????
    frac_u = float(stat.used -w2)/(stat.total - w2)
    print ("frac_u ", frac_u, " frac_x ", frac_x)
    if (frac_x > frac_u):
        bytes_to_remove = (frac_x - frac_u) * (f1- f0);

    bytes_to_remove = clamp(cache_size, bytes_to_remove, f0, f2);
    print("bytes to remove ", bytes_to_remove)
    quit()

if ( stat.used> w1 and cache_size > f1):
    print("u > w1")
    bytes_to_remove = 0
    frac_u = float ( stat.used - w1 ) / (w2 - w1)
    frac_x = float ( cache_size - f1 ) / (f2 - f1)
    print("frac_u ", frac_u, " frac_x ", frac_x)
    if (frac_x > frac_u):
        bytes_to_remove = (frac_x - frac_u) * (f2 - f1);
      
    bytes_to_remove = clamp(cache_size, bytes_to_remove, f0, f2);
    print("bytes to remove ", bytes_to_remove)
    quit()

print("no bytes to remove")