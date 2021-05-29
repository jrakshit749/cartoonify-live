import numpy as np
import cv2

filename= input('Enter filename with extension:')

#resize the image
def resizeImg(image):
    scale_ratio=0.3
    width=int(image.shape[1]*scale_ratio)
    height=int(image.shape[0]*scale_ratio)
    new_dims=(width,height)
    resized=cv2.resize(image,new_dims,interpolation=cv2.INTER_AREA)
    return resized

#finding edges using canny edge detection
def findContours(image):
    contoured_image=image
    gray=cv2.cvtColor(contoured_image, cv2.COLOR_BGR2GRAY)
    edged=cv2.Canny(gray, 10, 100) #the parameter entered are (image,threshold1,threshold2) --threshold values are intensity gradients //lower the thresholds more the gradients detected
    contours, hierarchy=cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #RETR_EXTERNAL-it return only the extreme outer contours..all child contours are ignored #CHAIN_APPROX_NONE-it returns absolutely all points of the image where contours are present
    cv2.drawContours(contoured_image,contours, contourIdx=-1, color=1, thickness=1)
    cv2.imshow("Image after contouring ", contoured_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return contoured_image

#quantizing the colors
def colorQuantization(image, K=4):
    Z=image.reshape((-1,3))
    Z=np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)
    compactness, label, center = cv2.kmeans(Z, K, None, criteria, 1, cv2.KMEANS_RANDOM_CENTERS)
    center=np.uint8(center)
    res=center[label.flatten()]
    res2=res.reshape((image.shape))
    return res2

if __name__ == "__main__":

    image=cv2.imread(filename)
    resized_image=resizeImg(image)
    colored=colorQuantization(resized_image)
    contoured=findContours(colored)
    final_img=contoured
    #save_q=input('Save the image? [y]/[n]')
    # if save_q=='y' or save_q=='Y':
    #     cv2.imwrite("toonized_"+filename, final_img)
    #     print("Image Saved...")
