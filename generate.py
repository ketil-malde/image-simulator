import sys

# check if python3 is used
if sys.version_info < (3, 0):
    print("This programs need python3x to run. Aborting.")
    sys.exit(1)

import os
import glob
import random
from PIL import Image
from math import floor

# Config
resolution      = (416,416)
backgrounds_dir = "backgrounds"
classes_dir     = "crops"
output          = "images_out"
maxobjs         = 6

# Loading data
backgrounds = os.listdir(backgrounds_dir)
class_names = os.listdir(classes_dir)
class_objects = [os.listdir(os.path.join(classes_dir,c)) for c in class_names]

# ignore scaling for now: .resize(resolution, Image.BICUBIC)
bgs = [Image.open(os.path.join(backgrounds_dir,b)) for b in backgrounds]

objs = []
for i,c in enumerate(class_objects):
    print('loading '+class_names[i]+' as '+str(i))
    objs = objs + [[Image.open(os.path.join(classes_dir,class_names[i],o)) for o in c]]

# Simulate an image
def mkimage(filename, objs=objs, bgs=bgs):
    log = []
    im = bgs[random.randint(0,len(backgrounds)-1)].copy()
    print('bg size='+str(im.size))
    for c in range(0,random.randint(1,maxobjs)):
        cls = random.randint(0,len(objs)-1)
        obj = random.choice(objs[cls])
        sizex,sizey = obj.size
        imx,imy = im.size
        posx = random.randint(-floor(sizex/2),imx-floor(sizex/2))
        posy = random.randint(-floor(sizey/2),imy-floor(sizey/2))
        im.paste(obj,(posx,posy),obj)
        log = log + ['{}\t{}\t{}\t{}\t{}\n'.format(cls,posy,posx,posy+sizey,posx+sizex)]
    im.save(os.path.join(output,filename+'.png'))
    with open(os.path.join(output,filename+'.txt'),'w') as f:
        for l in log: f.write(l)

mkimage('test')
