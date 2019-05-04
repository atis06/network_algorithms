import imageio
import os
import time
import sys

real_path = os.path.dirname(os.path.realpath(__file__))

img_dict = dict()

images_raw = os.listdir(os.path.join(real_path, 'graphs'))
for png in images_raw:
    if png.endswith('.png'):
        # print(png)
        img_dict[int(png.split('.')[0])] = png
        pass
    pass

images = list()
x = list(img_dict.keys())
x.sort()
for k in x:
    print(img_dict[k])
    images.append(imageio.imread(os.path.join('graphs', img_dict[k])))
    pass

imageio.mimsave('implicit_election_{}.gif'.format(str(int(time.time()))), images, loop=1)

sys.exit(0)
