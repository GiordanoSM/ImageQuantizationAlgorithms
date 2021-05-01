import dit_encoder as ce
import dit_openner as co
from PIL import Image, UnidentifiedImageError, ImageOps
import numpy as np
import os
import matplotlib.pyplot as plt

filename_enc = "../ImageDatabase/lena.bmp"
filename_enc_colour = "../ImageDatabase/lena_colour.bmp"
filename_dec = "results/lena.dit"
filename_dec_colour = "results/lena_colour.dit"
directory_enc = "results"
results = []
total_pixels = 512*512
mse=[]
psnr=[]
bpp=[]
sizes=[]
bd = 8

M_l = [2, 8, 16]

results_colour = []
mse_colour=[]
psnr_colour=[]
bpp_colour=[]
sizes_colour=[]

#Escala de cinza
for b in [False, True]:
  for m in M_l:
    ce.encoder(filename_enc, m, directory_enc, b)
    results.append(co.openner(filename_dec, show_image=False))
    bpp.append(os.stat(filename_dec).st_size*8/total_pixels)
    sizes.append(os.stat(filename_dec).st_size)
    ce.encoder(filename_enc_colour, m, directory_enc, b)
    results_colour.append(co.openner(filename_dec_colour, show_image=False))
    bpp_colour.append(os.stat(filename_dec_colour).st_size*8/total_pixels)
    sizes_colour.append(os.stat(filename_dec_colour).st_size)

with Image.open(filename_enc) as im:
  data = np.asarray(im).astype(np.int16)
  mse = [np.sum((data - r.astype(np.int16))**2)/data.size for r in results]
  for i in range(len(results)):
    psnr.append(10 * np.log10((2**bd-1)**2/mse[i]))

with Image.open(filename_enc_colour) as im:
  data = np.asarray(im).astype(np.int16)
  mse_colour = [np.sum((data - r.astype(np.int16))**2)/data.size for r in results_colour]
  for i in range(len(results)):
    psnr_colour.append(10 * np.log10((2**bd-1)**2/mse[i]))

colors1 = ['blue', 'purple']
colors2 = ['red', 'orange']

fig, ax = plt.subplots()
for i in range(2):
  ax.scatter(bpp[i*len(M_l):i*len(M_l)+len(M_l)], mse[i*len(M_l):i*len(M_l)+len(M_l)],c=colors1[i] ,label= "GrayScale {} Dithering".format('with' if i else 'without'))
  ax.scatter(bpp_colour[i*len(M_l):i*len(M_l)+len(M_l)], mse_colour[i*len(M_l):i*len(M_l)+len(M_l)],c=colors2[i] ,label= "Colour {} Dithering".format('with' if i else 'without'))
ax.set_xlabel('bpp')
ax.set_ylabel('MSE')
ax.set_title('MSE x BPP')
ax.grid(True)
ax.legend()

fig, ax = plt.subplots()
ax.plot(bpp[:len(M_l)], psnr[:len(M_l)],label="GrayScale without Dithering")
ax.plot(bpp[len(M_l):], psnr[len(M_l):],label="GrayScale with Dithering")
ax.plot(bpp_colour[:len(M_l)], psnr_colour[:len(M_l)],label="Colour with Dithering")
ax.plot(bpp_colour[len(M_l):], psnr_colour[len(M_l):],label="Colour without Dithering")
ax.set_xlabel('bpp')
ax.set_ylabel('PSNR')
ax.set_title('PSNR x BPP')
ax.grid(True)
ax.legend()

plt.show()

for i in range(len(results)//2):
  im = Image.fromarray(results[i])
  im.save("../Plots/Parte4/lena_{}.png".format(M_l[i]))
  im = Image.fromarray(results_colour[i])
  im.save("../Plots/Parte4/lena_colour_{}.png".format(M_l[i]))
  im = Image.fromarray(results[i+len(M_l)])
  im.save("../Plots/Parte4/lena_{}_dit.png".format(M_l[i]))
  im = Image.fromarray(results_colour[i+len(M_l)])
  im.save("../Plots/Parte4/lena_colour_{}_dit.png".format(M_l[i]))