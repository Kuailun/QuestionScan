import cv2
import numpy as np

def pre_process_img(src):
    """Process the image and get the box information"""

    '''Check whether need to rotate'''
    src = return_rotate(src)
    img_copy=src

    '''Get checkbox informations'''
    checkbox_info=return_checkbox(src)

    '''Get input informations'''
    input_info=return_input(src)

    #for i in range(len(checkbox_info)):
    #    print(detect_box(src,checkbox_info[0][0],checkbox_info[0][1],checkbox_info[0][2],checkbox_info[0][3]))
    return checkbox_info,input_info,np.array(src)
def return_rotate(src):
    """Check and return rotated image"""
    img_copy=src
    '''Get the image in black and white'''
    src = rgb2binary(src,220)
    #display_img(src)

    '''Remove the check part in checkboxes(Kernel size is 10)'''
    src=remove_check(src, 10)
    #display_img(src)

    '''Remove the noise in image(Kernel size is 3)'''
    src = remove_noise(src, 3)
    #display_img(src)

    '''Get all available checkbox information'''
    check_stat,check_center=get_checkbox(src)


    """
    for i in range(len(check_stat)):
        cv2.rectangle(img_copy, (check_stat[i][0], check_stat[i][1]), (check_stat[i][0] + check_stat[i][2], check_stat[i][1] + check_stat[i][3]), (255, 0, 0), 2, 2, 0)
        cv2.putText(img_copy,str(check_stat[i][4]),(int(check_center[i][0]),int(check_center[i][1])),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,0),2)
    display_img(img_copy)
    """

    '''Check whether need to rotate'''
    ret=check_rotate(check_center,img_copy.shape[1])
    if(ret):
        img_copy = np.rot90(img_copy, 2)

    '''
    for i in range(len(check_stat)):
        cv2.rectangle(img_copy, (check_stat[i][0], check_stat[i][1]),
                      (check_stat[i][0] + check_stat[i][2], check_stat[i][1] + check_stat[i][3]), (255, 0, 0), 2, 2, 0)
        cv2.putText(img_copy, str(check_stat[i][4]), (int(check_center[i][0]), int(check_center[i][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
    display_img(img_copy)
    '''

    return img_copy
def return_checkbox(src):
    """Check and return rotated image"""
    img_copy = src
    '''Get the image in black and white'''
    src = rgb2binary(src, 220)
    #display_img(src)

    '''Remove the check part in checkboxes(Kernel size is 10)'''
    src = remove_check(src, 10)
    #display_img(src)

    '''Remove the noise in image(Kernel size is 3)'''
    src = remove_noise(src, 3)
    #display_img(src)

    '''Get all available checkbox information'''
    check_stat, check_center = get_checkbox(src)
    #print(check_stat)

    img_copy=cv2.merge([img_copy])
    #displayWithBlocks(img_copy,check_stat)

    '''Combine center into status'''
    for i in range(len(check_center)):
        check_stat[i].append(check_center[i][0])
        check_stat[i].append(check_center[i][1])
    #print(check_stat)
    return check_stat
def return_input(src):
    """Check and return rotated image"""
    img_copy = src
    '''Get the image in black and white'''
    src = rgb2binary(src, 220)
    #display_img(src)

    '''Use rectangle to be the kernel will have a smooth edge'''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))
    src = cv2.morphologyEx(src, cv2.MORPH_CLOSE, kernel)
    #src = remove_check(src, 3)
    #display_img(src)

    '''Remove the noise in image(Kernel size is 3)'''
    src = remove_noise(src, 5)
    #display_img(src)

    '''Get all available checkbox information'''
    input_stat, input_center = get_input(src,282,45)
    input_stat2, input_center2 = get_input(src, 468, 44)
    input_stat3, input_center3 = get_input(src, 216, 44)

    #print(len(input_stat2))

    if(len(input_stat2)!=0):
        for i in range(len(input_stat2)):
            input_stat.append(input_stat2[i])
    if (len(input_stat3) != 0):
        for i in range(len(input_stat3)):
            input_stat.append(input_stat3[i])

    img_copy=cv2.merge([img_copy])
    for i in range(len(input_stat)):
        cv2.rectangle(img_copy, (input_stat[i][0], input_stat[i][1]), (input_stat[i][0] + input_stat[i][2], input_stat[i][1] + input_stat[i][3]), (255, 0, 0), 2, 2, 0)
        #cv2.putText(img_copy,str(input_stat[i][4]),(int(input_center[i][0]),int(input_center[i][1])),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,0),2)
    #display_img(img_copy)

    '''Combine center into status'''
    for i in range(len(input_center)):
        input_stat[i].append(input_center[i][0])
        input_stat[i].append(input_center[i][1])

    return input_stat,input_center
def display_img(src):
    """Display the image and wait for key to quit"""

    win=cv2.namedWindow("window",flags=0)
    cv2.imshow('window',src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def rgb2binary(src,threshold):
    """Convert rgb to binary"""
    gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    #display_img(gray)
    ret, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    #display_img(binary)
    return binary
def rgb2gray(src):
    """Convert rgb to gray"""
    gray=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    return gray
def remove_noise(src,size):
    """Remove the noise in the image"""

    '''Use ellipse to be the kernel'''
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(size,size))
    opening=cv2.morphologyEx(src,cv2.MORPH_OPEN,kernel)
    #display_img(opening)
    return opening
def remove_check(src,size):
    """Remove the check in checkbox"""

    '''Use rectangle to be the kernel will have a smooth edge'''
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    closing=cv2.morphologyEx(src,cv2.MORPH_CLOSE,kernel)
    #display_img(closing)
    return closing
def get_checkbox(src):
    """Get the information of checkbox"""
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(src)
    ret_state=[]
    ret_center=[]
    for i in range(len(stats)):
        x = stats[i][0]
        y = stats[i][1]
        width = stats[i][2]
        height = stats[i][3]
        area = stats[i][4]
        if (area > 800 and area < 2400 and width > 33 and width < 47 and height > 33 and height < 47):
            ret_state.append([x,y,width,height,area])
            ret_center.append(centroids[i])
    return ret_state,ret_center
def get_input(src,p_length,p_height):
    """Get the information of inputbox"""
    _, labels, stats, centroids = cv2.connectedComponentsWithStats(src)
    ret_state=[]
    ret_center=[]
    #print(stats)
    #print("")
    for i in range(len(stats)):
        x = stats[i][0]
        y = stats[i][1]
        width = stats[i][2]
        height = stats[i][3]
        area = stats[i][4]
        if (area > p_length*p_height*0.7 and area < p_length*p_height*1.3 and width > p_length*0.9 and width < p_length*1.1 and height > p_height*0.8 and height < p_height*1.2):
            ret_state.append([x,y,width,height,area])
            ret_center.append(centroids[i])
    return ret_state,ret_center
def check_rotate(center,width):
    """Return whether need to return"""

    '''In case no squares'''
    if (len(center) == 0):
        return False
    sum=0
    for i in range(len(center)):
        sum+=center[i][0]
    if(sum/len(center)>width/2):
        return True
    return False
def detect_box(src,p_x,p_y,p_width,p_height):
    """Check whether this is a box basing the fill rate"""
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    crop=gray[int(p_y):int(p_y+p_height),int(p_x):int(p_x+p_width)]
    #display_img(crop)
    mean=cv2.mean(crop)
    #print(mean)
    crop=gray[int(p_y-25):int(p_y+p_height+25),int(p_x-p_width*0.05):int(p_x+p_width*1.05)]
    #display_img(crop)
    meann=cv2.mean(crop)
    #print(meann)
    if(mean[0]*0.92>meann[0]):
        return True
    print(meann[0]/mean[0])
    return False
def displayWithBlocks(src,stat):
    """Display image with boxes"""
    #print(stat)
    for i in range(len(stat)):
        cv2.rectangle(src, (int(stat[i][0]), int(stat[i][1])), (int(stat[i][0] + stat[i][2]), int(stat[i][1] + stat[i][3])), (255, 0, 0), 2, 2)
        cv2.putText(src,str(stat[i][4]),(int(stat[i][0]),int(stat[i][1])),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,0),2)
        #cv2.putText(src, str(stat[i][7]), (int(stat[i][0])+20, int(stat[i][1])+20), cv2.FONT_HERSHEY_SIMPLEX, 1.2,(0, 0, 255), 2)
    display_img(src)
def colorDetection(src, check_info, possibleList, point):
    """Calculate the colors"""
    #roi_r=src[int(point[0]+100):int(point[0]+200),int(point[1]-50):int(point[1]+50)]
    roi_r = src[int(point[1]-50):int(point[1]+50),int(point[0]+100):int(point[0]+200)]

    #cv2.rectangle(src, (0, 0), (200,200),(255, 0, 0), 2, 2)
    #cv2.rectangle(src, (int(point[0]+100), int(point[1]-50)), (int(point[0]+200), int(point[1]+50)),(255, 0, 0), 2, 2)

    temp=[]    #BGR
    temp.append(cv2.mean(src[:, :, 0]))
    temp.append(cv2.mean(src[:, :, 1]))
    temp.append(cv2.mean(src[:, :, 2]))

    meanm=[]
    meann=[temp[0][0],temp[1][0],temp[2][0]]

    #print(meann)
    #display_img(src)
    #display_img(src[:, :, 0])
    #display_img(src[:, :, 1])
    #display_img(src[:, :, 2])
    return meann
def getChecked(src,templateID,check_info):
    """Return the state of checkbox"""
    x=check_info[0]
    y=check_info[1]
    width=check_info[2]
    height=check_info[3]
    #print(check_info)
    if(x<0):
        width = width + x
        x=0
    if(y<0):
        height=height+y
        y=0
    '''crop the image'''
    cropImg=src[int(y):int(y+height),int(x):int(x+width)]
    cropGray=cv2.cvtColor(cropImg,cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(cropGray)
    #print(mean)

    ret, cropBinary_H = cv2.threshold(cropGray, 220, 255, cv2.THRESH_BINARY)
    ret, cropBinary_L = cv2.threshold(cropGray, 80, 255, cv2.THRESH_BINARY)

    cropDifference=cropBinary_L-cropBinary_H
    cropDD=remove_check(cropDifference,20)
    #display_img(cropGray)
    #display_img(cropDifference)
    #display_img(cropDD)

    mean1=cv2.mean(cropDifference)
    mean1=mean1[0]
    mean2 = cv2.mean(cropDD)
    mean2 = mean2[0]
    if(mean2==0):
        mean2=1
    rate=mean1/mean2

    checked=0
    if(mean2>60 and (rate<0.8 or mean2-mean1>20)):
        checked=1
    print(str(checked)+"   "+str(mean1)+"  "+str(mean2)+"  "+str(rate))
    if(mean2>60 and (rate<0.8 or mean2-mean1>20)):
        return 1
    return 0