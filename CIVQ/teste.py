import civq_encoder as ce
import civq_openner as co
import civq_codebook as cc
from PIL import Image, UnidentifiedImageError, ImageOps
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#Path(filename_enc).stat().st_size
filename_enc = "../ImageDatabase/lena.bmp"
filename_dec = "results/lena.cvq"
filename_cod = "codebooks/lena.cdb"
directory_code = "codebooks"
directory_enc = "results"
results = []
total_pixels = 512*512
original_bpp = os.stat(filename_enc).st_size*8/total_pixels
mse=[]
psnr=[]
bpp=[]
sizes=[]
bd = 8

L_l = [4, 16, 64]
M_l = [32, 64, 128, 256]

for l in L_l:
  for m in M_l:
    cc.codebookGen(filename_enc, m, l, directory_code)
    ce.encoder(filename_enc, filename_cod, directory_enc)
    results.append(co.openner(filename_dec, show_image=False))
    bpp.append(os.stat(filename_dec).st_size*8/total_pixels)
    sizes.append(os.stat(filename_dec).st_size)



with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse = [np.sum((data - r.astype(np.int16))**2)/total_pixels for r in results]
  for i in range(len(results)):
    psnr.append(10 * np.log10((2**bd-1)**2/mse[i]))

colors = ['red','green','blue']

fig, ax = plt.subplots()
for i in range(3):
  ax.scatter(bpp[i*4:i*4+4], mse[i*4:i*4+4], c=colors[i], label= "L={}".format(4**(i+1)))
ax.set_xlabel('bpp')
ax.set_ylabel('MSE')
ax.set_title('MSE x BPP')
ax.grid(True)
ax.legend()

lch_bpp = [bpp[8], bpp[9], bpp[4], bpp[5], bpp[6], bpp[7], bpp[1], bpp[2], bpp[3]]
lch_mse = [mse[8], mse[9], mse[4], mse[5], mse[6], mse[7], mse[1], mse[2], mse[3]]
lch_psnr = [psnr[8], psnr[9], psnr[4], psnr[5], psnr[6], psnr[7], psnr[1], psnr[2], psnr[3]]

fig, ax = plt.subplots()
ax.plot(lch_bpp, lch_mse)
ax.set_xlabel('bpp')
ax.set_ylabel('MSE')
ax.set_title('Lower Convex Hull')
ax.grid(True)
ax.legend()

jpg_names = ["test/lena4_8_9_10.jpg","test/lena5.jpg","test/lena6.jpg",
              "test/lena7_11.jpg","test/lena1.jpg","test/lena2.jpg",
              "test/lena3.jpg"]

bpp_jpg= [os.stat(f).st_size*8/total_pixels for f in jpg_names]

results_jpg = []
psnr_jpg = []

for filename in jpg_names:
  with Image.open(filename) as im:
    im = ImageOps.grayscale(im)
    data = np.asarray(im).astype(np.int16)
    results_jpg.append(data)


with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse_jpg = [np.sum((data - r.astype(np.int16))**2)/total_pixels for r in results_jpg]
  for i in range(len(results_jpg)):
    psnr_jpg.append(10 * np.log10((2**bd-1)**2/mse_jpg[i]))

fig, ax = plt.subplots()
ax.plot(lch_bpp, lch_psnr,label="CIQA")
ax.plot(bpp_jpg, psnr_jpg,label="JPEG")
ax.set_xlabel('bpp')
ax.set_ylabel('PSNR')
ax.set_title('PSNR x BPP')
ax.grid(True)
ax.legend()


plt.show()

#print(sizes)
