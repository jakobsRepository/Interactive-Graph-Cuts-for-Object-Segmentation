import numpy as np
import matplotlib.pyplot as plt

'''
This method opens the image and lets the user enter the seeds for the segmentation. Every click selects the
surrounding square of the pixel (21*21) as seed. (seeds = pre defined pixels belonging to foreground
or background) 
'''
def Chose_initial_values_image_segmantation(image):
    changed_pixels = []
    pixels_indexes = []
    pixels = image.load()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image, cmap = 'gray')

    coords = []

    def onclick(event):
        ix, iy = event.xdata, event.ydata
        print('x = %d, y = %d' % (ix, iy))

        coords.append((iy, ix))

        pixelLeft = max(0,int(ix)-10)
        pixelRight = min(int(ix)+10,image.width-1)
        pixelTop = max(0,int(iy)-10)
        pixelDown = min(int(iy)+10,image.height-1)
        for x in range(pixelLeft,pixelRight+1):
            for y in range(pixelTop,pixelDown+1):
                changed_pixels.append(pixels[x, y])
                pixels_indexes.append((y, x))
        return coords

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    return image,np.array(changed_pixels),np.array(pixels_indexes)