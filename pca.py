import cv2
import matplotlib.pyplot as plt
from skimage.io import imshow, imread
from skimage.color import rgb2hsv, hsv2rgb
from skimage.color import rgb2gray
from skimage import util 


img = imread('lines_images/image0.jpg')

red_filtered = (img[:,:,0] > 180) & (img[:,:,1] < 60) & (img[:,:,2] < 80)
plt.figure(num=None, figsize=(8, 6), dpi=80)
img_new = img.copy()
img_new[:, :, 0] = img_new[:, :, 0] * red_filtered
img_new[:, :, 1] = img_new[:, :, 1] * red_filtered
img_new[:, :, 2] = img_new[:, :, 2] * red_filtered

inverted_img = util.invert(img_new)
gray = rgb2gray(inverted_img)
#imshow(gray)
plt.imsave('images_test/test.jpg', gray, cmap = plt.cm.gray)
#plt.show()


img = cv2.imread("images_test/test.jpg", 0)
threshold = 200
ret,thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)
height, width = thresh.shape[:2]
mass = 0
Xcm  = 0.0
Ycm  = 0.0

for i in range(width) :
    for j in range(height) :
        if not thresh[j][i] :
            mass += 1
            Xcm  += i
            Ycm  += j

Xcm = Xcm/mass
Ycm = Ycm/mass

'''fig = plt.figure()
fig.clear()
plot = fig.add_subplot(111)
plot.imshow(thresh, 'gray')
plot.scatter([Xcm], [Ycm], s=30, c='yellow', edgecolors='red')
plt.show()
'''

print(round(Xcm), round(Ycm))

