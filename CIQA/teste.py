import ciqa_encoder as ce
import ciqa_openner as co
from PIL import Image, UnidentifiedImageError, ImageOps
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#Path(filename_enc).stat().st_size
filename_enc = "../ImageDatabase/peppers.bmp"
filename_dec = "results/peppers.cqa"
directory = "results"
results = []
total_pixels = 512*512
original_bpp = os.stat(filename_enc).st_size*8/total_pixels
mse=[]
psnr=[]
bpp=[]
sizes=[]
bd = 8

N_l = [4, 8, 16, 32]
M_l = [2, 4, 8, 16]

for n in N_l:
  for m in M_l:
    ce.encoder(n, m, filename_enc, directory)
    results.append(co.openner(filename_dec, show_image=False))
    bpp.append(os.stat(filename_dec).st_size*8/total_pixels)
    sizes.append(os.stat(filename_dec).st_size)



with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse = [np.sum((data - r.astype(np.int16))**2)/total_pixels for r in results]
  for i in range(len(results)):
    psnr.append(10 * np.log10((2**bd-1)**2/mse[i]))

colors = ['red','orange','green','blue']

fig, ax = plt.subplots()
for i in range(4):
  ax.scatter(bpp[i*4:i*4+4], mse[i*4:i*4+4], c=colors[i], label= "N={}".format(4*2**i))
ax.set_xlabel('bpp')
ax.set_ylabel('MSE')
ax.set_title('MSE x BPP')
ax.grid(True)
ax.legend()

lch_bpp = [bpp[12], bpp[8], bpp[4], bpp[0], bpp[5], bpp[1], bpp[6], bpp[2], bpp[3]]
lch_mse = [mse[12], mse[8], mse[4], mse[0], mse[5], mse[1], mse[6], mse[2], mse[3]]
lch_psnr = [psnr[12], psnr[8], psnr[4], psnr[0], psnr[5], psnr[1], psnr[6], psnr[2], psnr[3]]

fig, ax = plt.subplots()
ax.plot(lch_bpp, lch_mse)
ax.set_xlabel('bpp')
ax.set_ylabel('MSE')
ax.set_title('Lower Convex Hull')
ax.grid(True)
ax.legend()

jpg_names = ["test/peppers8_12.jpg","test/peppers4.jpg","test/peppers0.jpg",
              "test/peppers5.jpg","test/peppers1.jpg","test/peppers6.jpg",
              "test/peppers2.jpg", "test/peppers3.jpg"]

bpp_jpg= [os.stat(f).st_size*8/total_pixels for f in jpg_names]

results_jpg = []

for filename in jpg_names:
  with Image.open(filename) as im:
    im = ImageOps.grayscale(im)
    data = np.asarray(im).astype(np.int16)
    results_jpg.append(data)


with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse_jpg = [np.sum((data - r.astype(np.int16))**2)/total_pixels for r in results_jpg]
  for i in range(len(results_jpg)):
    psnr.append(10 * np.log10((2**bd-1)**2/mse_jpg[i]))

fig, ax = plt.subplots()
ax.plot(lch_bpp, lch_psnr,label="CIQA")
ax.plot(bpp_jpg, mse_jpg,label="JPEG")
ax.set_xlabel('bpp')
ax.set_ylabel('PSNR')
ax.set_title('PSNR x BPP')
ax.grid(True)
ax.legend()

#0 1 2 3 4 5 6 8 12


plt.show()

#print(sizes)
