# load the model
from keras.models import load_model
import numpy as np
import cv2
testmodel = load_model("eyeModel2.h5")

def preProcess(img):
    # use matplotlib to plot the first image from cnv_images
    from PIL import Image
    import matplotlib.pyplot as plt
    # plt.imshow(img)
    # plt.show()


    # applymedian filter to the image
    import numpy as np
    median = cv2.medianBlur(img, 5)
    # plt.imshow(median)
    # plt.show()


    # ehnance the image using another library
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(Image.fromarray(median))
    enhanced_im = enhancer.enhance(2.0)
    # plt.imshow(enhanced_im)
    # plt.show()

    # apply thresholding to the enhanced image
    
    ret,thresh1 = cv2.threshold(np.array(enhanced_im), 50, 255, cv2.THRESH_BINARY)
    # plt.imshow(thresh1)
    # plt.show()

    # set the pixels of cnv_images[0] to 0 where thresh1 is 0
    img[thresh1==0] = 0
    # plt.imshow(img)
    # plt.show()

    # crop img 100 from top
    img = img[50:,:]
    # plt.imshow(img)
    # plt.show()
    # crop img 100 from bottom
    img = img[:-50,:]
    # plt.imshow(img)
    # plt.show()

    # resize the image to 256x256
    img = cv2.resize(img, (256,256))
    # plt.imshow(img)
    # plt.show()

    # apply cannny edge detection
    edges = cv2.Canny(img, 100, 200)
    # plt.imshow(edges)
    # plt.show()
    # color the edges red in the img
    img[edges>0] = (255,0,0)
    # plt.imshow(img)
    # plt.show()

    return img

def predictImage(img):
    
    labelsMap = {"CNV":0, "DME":1, "DRUSEN":2, "NORMAL":3}
    # preprocess the image
    img = preProcess(img)

    # convert the image into numpy array
    img = np.array(img.tolist())

    # reshape the image
    img = img.reshape(1, 256, 256, 3)

    # predict the image
    prediction = testmodel.predict(img)
    prediction = np.argmax(prediction, axis=1)
    # return prediction from labelsMap
    return list(labelsMap.keys())[list(labelsMap.values()).index(prediction[0])]
