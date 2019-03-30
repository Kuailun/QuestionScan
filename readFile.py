import os
import cv2
import xlsxwriter
import imageData
import uuid
import json
import datetime

def get_file_list(p_dir):
    """Get the file names in a folder"""
    file_list=os.listdir(p_dir)
    return file_list

def get_img(p_path):
    """Get image data from a path"""
    src=cv2.imread(p_path)
    return src

def write_img(p_path,name,src):
    """Write image to path"""
    cv2.imwrite(p_path+"/"+name,src)

def checkCreate(p_path):
    """Create the directory if not existed"""
    folder=os.path.exists(p_path)

    if not folder:
        os.makedirs(p_path)

    mFile=open(p_path+"/read.json","w")

    return mFile

def WriteData(name,index,statusCode,result,info,worksheet):
    """Write data to the xlsx"""
    worksheet.write(index+1,0,index+1)
    worksheet.write(index + 1, 1, name)
    worksheet.write(index + 1, 2, statusCode)
    if(statusCode==-2):
        return
    if(statusCode==-1):
        return
    if(imageData.image_ChoiceLimit[statusCode]==-1):
        worksheet.write(index + 1, 3, 1)
    elif(imageData.image_ChoiceLimit[statusCode]==sum(result)):
        worksheet.write(index + 1, 3, 1)
    else:
        worksheet.write(index + 1, 3, 0)

    for i in range(len(result)):
        worksheet.write(index + 1, 6+i, result[i])
    worksheet.write(index + 1, 4, imageData.image_TargeTitle[statusCode])
    return

StoreBlank=[]
StoreUnsettled=[]
def WriteJson(name,index,statusCode,result,info,mFile,dir):
    if(statusCode<0):
        if(statusCode==-2):
            StoreBlank.append(name)
        if(statusCode==-1):
            StoreUnsettled.append(name)
        return
    choiceLimit=imageData.image_ChoiceLimit[statusCode]
    choiceNum=sum(result)
    # No checkbox checked
    if(choiceNum==0):
        return
    if(choiceLimit>0):
        if (choiceNum!=choiceLimit):
            return

    a_id=[];
    for i in range(len(result)):
        if(result[i]==1):
            a_id.append(imageData.answerIDforJson[statusCode][i])

    ret=False
    backName=""
    if(name.find("-a.png")>=0):
        backName=name.replace("-a.png","-b.png")
        ret=os.path.exists(dir+backName)
    elif(name.find("-b.png")>=0):
        backName = name.replace("-b.png", "-a.png")
        ret = os.path.exists(dir + backName)

    if not ret:
        backName=""

    mData=json.dumps({
        "id":str(uuid.uuid4()),#
        "q_id":imageData.templateIDforJson[statusCode],
        "a_id":a_id,
        "gender":"",#
        "age":"",#
        "zip_code":"",#
        "home":"",#
        "free_q_id":2,#
        "free_resp":"",#
        "survey_id":6,#
        "front":name,
        "back":backName,
        "timestamp":str(datetime.datetime.now())
    })
    mFile.write(mData)


