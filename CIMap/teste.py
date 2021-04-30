import cimap_encoder as ce
import cimap_openner as co
from PIL import Image, UnidentifiedImageError, ImageOps
import numpy as np
import os
import matplotlib.pyplot as plt

filename_enc = "../ImageDatabase/kodim05.png"
filename_dec = "results/kodim05.cmp"
directory_enc = "results"
results = []
total_pixels = 512*768
mse=[]
psnr=[]
bpp=[]
sizes=[]
bd = 8

M_l = [16, 32, 64, 128, 256]

for m in M_l:
  ce.encoder(filename_enc, m, directory_enc)
  results.append(co.openner(filename_dec, show_image=False))
  bpp.append(os.stat(filename_dec).st_size*8/total_pixels)
  sizes.append(os.stat(filename_dec).st_size)

#print(sizes)

with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse = [np.sum((data - r.astype(np.int16))**2)/data.size for r in results]
  for i in range(len(results)):
    psnr.append(10 * np.log10((2**bd-1)**2/mse[i]))

colors = ['red','green','blue', 'orange', 'purple']

fig, ax = plt.subplots()
for i in range(5):
  ax.scatter(bpp[i], mse[i], label= "M={}".format(16*2**i))
ax.set_xlabel('bpp')
ax.set_ylabel('MSE')
ax.set_title('MSE x BPP')
ax.grid(True)
ax.legend()

jpg_names = ["test/kodim05_0.jpg","test/kodim05_1.jpg","test/kodim05_2.jpg",
              "test/kodim05_3.jpg","test/kodim05_4.jpg"]

bpp_jpg= [os.stat(f).st_size*8/total_pixels for f in jpg_names]

results_jpg = []
psnr_jpg = []

for filename in jpg_names:
  with Image.open(filename) as im:
    data = np.asarray(im).astype(np.int16)
    results_jpg.append(data)


with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse_jpg = [np.sum((data - r.astype(np.int16))**2)/data.size for r in results_jpg]
  for i in range(len(results_jpg)):
    psnr_jpg.append(10 * np.log10((2**bd-1)**2/mse_jpg[i]))

fig, ax = plt.subplots()
ax.plot(bpp, psnr,label="CIMap")
ax.plot(bpp_jpg, psnr_jpg,label="JPEG")
ax.set_xlabel('bpp')
ax.set_ylabel('PSNR')
ax.set_title('PSNR x BPP')
ax.grid(True)
ax.legend()

for i in range(len(results)):
  im = Image.fromarray(results[i])
  im.save("../Plots/Parte3/kodim05_{}.png".format(int(16*2**i)))

plt.show()