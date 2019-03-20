import readFile
import processImage
import analyzeInformation


PROJ_DATA_DIR = 'E:/Workspace/Project/Question/'
SCAN_DIR = PROJ_DATA_DIR + 'raw/'
'''check the directory'''
mFile=readFile.checkCreate(PROJ_DATA_DIR+"database")

#   Get the file list in a directory
fileList=readFile.get_file_list(SCAN_DIR)

for i in range(len(fileList)):
    print("index:"+str(i))
    src=readFile.get_img(SCAN_DIR+fileList[i])

    '''return the checkbox information, inputbox information and rotated image'''
    check_info,input_info,srcc=processImage.pre_process_img(src)

    '''statusCode   =   -2   blank page'''
    '''             =   -1   Not settled image'''
    '''             =   0-9  Settled image template id'''
    '''result               bool of image checked when statusCode is 2'''
    '''info                 checkbox information'''
    '''structure            question structure'''
    statusCode,result,info=analyzeInformation.analyze(check_info,input_info,srcc)

    '''Save to file'''
    readFile.WriteJson(fileList[i],i,statusCode,result,info,mFile)
mFile.close()

