import os
from urllib import urlopen

'''
Download file at given url and save at path
'''
def wget(url, path):
	file_name = url.split('/')[-1]
	u = urlopen(url)
	target = file_name
	if path:
		target = path+'/'+target
	f = open(target+".temp", 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print("Downloading: %s Bytes: %s" % (file_name, file_size))
	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break
	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    sys.stdout.write(status)
	    if not '100.00' in status:
			sys.stdout.write('\r')
	f.close()
	os.rename(target+".temp", target)
	return target
