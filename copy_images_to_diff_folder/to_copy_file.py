import glob
import shutil
import os

src_dir = "/home/sai/Aish/copytrial/"
dst_dir = "/home/sai/Aish/copytrial/gas_cylinder_img"
for i in range(1,32):
	for jpgfile in glob.iglob(os.path.join(src_dir+str(i), "*.jpg")):
		shutil.copy(jpgfile, dst_dir)