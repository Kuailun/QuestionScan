import processImage
import imageData
def analyze(check_info,input_info,src):
    """analyze the structure of boxes and get question number"""
    #print(check_info)

    '''extract the center and round their location'''
    center=[]
    for i in range(len(check_info)):
        x=round(check_info[i][5])
        y=round(check_info[i][6])
        center.append([x,y,i])
    '''if location difference is smaller than +-5, they are in same row/ column'''
    x_min=10000
    y_min=10000
    for i in range(len(center)):
        for j in range(i,len(center)):
            if(center[j][0]+5>center[i][0] and center[j][0]-5<center[i][0]):
                center[j][0]=center[i][0]
            if (center[j][1] + 5 > center[i][1] and center[j][1] - 5 < center[i][1]):
                center[j][1] = center[i][1]
            if(center[i][0]<x_min):
                x_min=center[i][0]
            if (center[i][1] < y_min):
                y_min = center[i][1]

    '''get the minmum interval between boxes vertically'''
    center_sort_y=center
    center_sort_y.sort(key=lambda x:x[1])
    #print(center_sort_y)

    '''form a matrix to represent the boxes'''
    '''[0][0] [1][0] [2][0]...'''
    '''[0][1] [1][1] [2][1]...'''
    '''[0][2] [1][2] [2][2]...'''
    matrix=[[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    for i in range(len(center)):
        m=round(int((center[i][0]-x_min)/195))
        n=round(int((center[i][1]-y_min)/57))
        if(n>=5):
            n=4
        #print(str(m)+" "+str(n))
        matrix[m][n]=center[i][2]


    '''This is a blank page'''
    if(sum(map(sum,matrix))==-15):
        print("Blank page")
        return -2,0,0

    '''Get x,y intervals'''
    interval_x = 240
    interval_y = 69
    index_xx = -1
    index_xy = -1
    index_yx = -1
    index_yy = -1
    pos_x = 0;
    pos_y = 0;
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] != -1 and index_xx == -1):
                pos_x = matrix[i][j]
                index_xx = i
                index_xy = j
            if (matrix[i][j] != -1 and index_yy == -1):
                pos_y = matrix[i][j]
                index_yx = i
                index_yy = j
            if (index_xx != -1 and matrix[i][j] != pos_x and matrix[i][j] != -1 and index_xx != i):
                #print("x1:" + str(check_info[matrix[i][j]][5]) + "x2:" + str(check_info[matrix[index_xx][index_xy]][5]) + "   " + str(i) + "  " + str(index_xx))
                interval_x = round(
                    abs((check_info[matrix[i][j]][5] - check_info[matrix[index_xx][index_xy]][5]) / (i - index_xx)))
            if (index_yy != -1 and matrix[i][j] != pos_y and matrix[i][j] != -1 and index_yy != j):
                interval_y = round(abs(
                    (check_info[matrix[i][j]][6] - check_info[matrix[index_yx][index_yy]][6]) / (j - index_yy)))

    '''Correct the matrix'''
    matrix_binary,matrix,check_info=correctMatrix(matrix,check_info,x_min,y_min,interval_x,interval_y+2)

    #print(matrix_binary)

    possibleList=getPossible(matrix_binary)

    #printMatrix(matrix)
    #print(possibleList)
    #print("box numbers:"+str(len(check_info)))

    #processImage.display_img(src)
    '''Going into guess and match process'''
    #if(len(possibleList)==0):
    #    print(possibleList)
    #    guess_and_match(matrix,matrix_binary,check_info,src)
    #    processImage.display_img(src)

    colors=processImage.colorDetection(src,check_info,possibleList,[x_min,y_min])
    templateID=settleTemplate(colors,possibleList)

    if(templateID==-1):
        '''template is not settled'''
        print("Template is not settled")
        return -1,0,0

    print("PossibleListe:" + str(possibleList))
    #print(imageData.image_TargeTitle[templateID])
    '''Final Detect'''
    #printMatrix(matrix)
    result,structure,check_info=finalDetect(src,matrix,templateID,check_info)
    #processImage.display_img(src)
    #processImage.displayWithBlocks(src, check_info)
    return templateID,result,check_info
def printMatrix(matrix):
    '''Print my matrix'''
    for i in range(len(matrix[0])):
        m_string=""
        for j in range(len(matrix)):
            m_string=m_string+str(matrix[j][i])+"  "
        print(m_string)
def getPossible(matrix):
     """Get possible template"""
     possibleList=[]
     for i in range(len(imageData.image_Matrix)):
         if(convolute(matrix,imageData.image_Matrix[i])==0):
             possibleList.append(i)
     return possibleList
def convolute(p_matrix,t_matrix):
     """Convolute 2 matrix and return sum"""
     ret = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
     for i in range(len(p_matrix)):
         for j in range(len(p_matrix[0])):
             ret[i][j]=p_matrix[i][j]-t_matrix[i][j]
             if(ret[i][j]!=0):
                 return -1
     #print(ret)
     #print(sum(map(sum,ret)))
     return sum(map(sum,ret))
def binaryMatrix(matrix):
    """Convert the matrix to a binary one"""
    matrix_binary = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] != -1):
                matrix_binary[i][j] = 1
    return matrix_binary
def correctMatrix(matrix,check_info,x_min,y_min,interval_x,interval_y):
    """As their are some scenario that we can be sure it lost some thing,
       we can add it manually"""

    matrix_binary=binaryMatrix(matrix)

    s=sum(map(sum,matrix_binary))
    '''If matrix[0][0] is not detected'''

    if (matrix[0][0] == -1):
        matrix[0][0] = s
        check_info.append([x_min - 20, y_min - 20, 40, 40, 1600, x_min, y_min])
        s = s + 1
        matrix_binary = binaryMatrix(matrix)
    '''If upper one and lower one is detected, then there should be a middle one'''
    for i in range(len(matrix)):
        for j in range(1,len(matrix[0])-1):
            if(matrix_binary[i][j-1]==1 and matrix_binary[i][j+1]==1 and matrix_binary[i][j]==0):
                matrix[i][j]=s
                s=s+1
                check_info.append(
                    [x_min - 20 + interval_x * i, y_min - 20 + interval_y * j, 40, 40, 1600, x_min + interval_x * i,
                     y_min + interval_y * j])
                matrix_binary = binaryMatrix(matrix)
    '''If the lower one is detected, then this one must be a checkbox'''
    for i in range(len(matrix)):
        if (matrix_binary[i][1] == 1 and matrix_binary[i][0] == 0):
            matrix[i][0] = s
            s = s + 1
            check_info.append(
                [x_min - 20 + interval_x * i, y_min - 20 + interval_y * 0, 40, 40, 1600, x_min + interval_x * i,
                 y_min + interval_y * 0])
            matrix_binary = binaryMatrix(matrix)
    '''If box is more than 6, then there should be 10'''
    if(s>=6):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if(((matrix_binary[0][j]==1)or(matrix_binary[2][j]==1)) and matrix[i][j]==-1and i!=1):
                    matrix[i][j] = s
                    s = s + 1
                    check_info.append([x_min - 20+interval_x*i, y_min - 20+interval_y*j, 40, 40, 1600, x_min+interval_x*i, y_min+interval_y*j])
                    matrix_binary=binaryMatrix(matrix)

    return binaryMatrix(matrix),matrix,check_info
def guess_and_match(matrix,matrix_binary,information,src):
    '''guess and match the matrix with template'''
    #printMatrix(matrix)



    gray=processImage.rgb2gray(src)
    matrix_bool=[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix_bool[i][j]=1-matrix[i][j]
def finalDetect(src,matrix,templateID,check_info):
    """Final detect of the boxes and return result"""

    '''Sort the questions'''
    matrix_binary = binaryMatrix(matrix)
    num=sum(map(sum,matrix_binary))
    matrix,check_info=matrixSort(matrix,check_info,num)
    #printMatrix(matrix_binary)

    '''Check the state of checkbox'''
    answerChecked=[0 for i in range(num)]

    for i in range(num):
        answerChecked[i]=processImage.getChecked(src,templateID,check_info[i])
    print(answerChecked)

    return answerChecked,matrix,check_info

    #processImage.display_img(src)
def matrixSort(matrix,check_info,num):
    """Sort the matrix:
    0   1   2
    3   4   5
    6   7   8
    9   10  11
    12  13  14"""
    ret_matrix=[[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    ret_check_info=[]
    index=0
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            if(index==num):
                break
            if(matrix[i][j]!=-1):
                ret_matrix[i][j]=index
                index=index+1
                check_info[matrix[i][j]].append(ret_matrix[i][j])
                ret_check_info.append(check_info[matrix[i][j]])
    #printMatrix(ret_matrix)
    return ret_matrix,ret_check_info
def getPossibleFromColor(color):
    """Return possible template list from color"""
def settleTemplate(color,possibleList):
    """Return one specific id for template basing color and possibleList"""
    if(len(possibleList)>2 or len(possibleList)==0):
        '''Template is not settled'''
        return -1
    if(len(possibleList)==1):
        return possibleList[0]
    if keyinList(possibleList,0) or keyinList(possibleList,4):
        if(color[2]>120):
            return 0
        else:
            return 4
    if keyinList(possibleList,2) or keyinList(possibleList,3):
        if(color[2]>170):
            return 2
        else:
            return 3
    if keyinList(possibleList,5) or keyinList(possibleList,6):
        if(color[0]>color[1] and color[2]>color[1]):
            return 5
        else:
            return 6
    if keyinList(possibleList,7) or keyinList(possibleList,8):
        if(color[2]>125):
            return 7
        else:
            return 8
def keyinList(p_list,p_key):
    for i in range(len(p_list)):
        if(p_key==p_list[i]):
            return True
    return False