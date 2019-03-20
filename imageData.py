
image_Matrix=[
# 0: My preferred transport mode(s) in 2020 will be...
    [[1,1,1,1,1],[0,0,0,0,0],[1,1,1,1,1]],
# 1: In 2040, the average person will...
    [[1,1,1,0,0],[1,1,0,0,0],[0,0,0,0,0]],
# 2:Responsibility for autonomous vehicle accidents belongs to...
    [[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]],
# 3:In 2040, commuting will take...
    [[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]],
# 4:In 2040, everyone will have access to...
    [[1,1,1,1,1],[0,0,0,0,0],[1,1,1,1,1]],
# 5:The future of mobility will make the world
    [[1,1,1,0,0],[0,0,0,0,0],[0,0,0,0,0]],
# 6:In the future, my transportation costs will...
    [[1,1,1,0,0],[0,0,0,0,0],[0,0,0,0,0]],
# 7:Future mobility options will have the greatest imapact on...
    [[1,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0]],
# 8:In 2040...
    [[1,1,1,1,0],[0,0,0,0,0],[0,0,0,0,0]],
# 9:Travel in the future will be more dangerous for...
    [[1,1,0,0,0],[1,0,0,0,0],[1,0,0,0,0]]
]
image_TargetNum=[10,5,5,5,10,3,3,4,4,4]
image_TargetColor=[
# 0: My preferred transport mode(s) in 2020 will be...
    [85,89,189],
# 1: In 2040, the average person will...
    [60,54,96],
# 2:Responsibility for autonomous vehicle accidents belongs to...
    [129,207,229],
# 3:In 2040, commuting will take...
    [129,181,127],
# 4:In 2040, everyone will have access to...
    [88,77,62],
# 5:The future of mobility will make the world
    [117,89,112],
# 6:In the future, my transportation costs will...
    [93,120,71],
# 7:Future mobility options will have the greatest imapact on...
    [137,114,202],
# 8:In 2040...
    [138,90,49],
# 9:Travel in the future will be more dangerous for...
    [92,124,239]
]
image_TargeTitle=[
    "0: My preferred transport mode(s) in 2020 will be...",
    "1: In 2040, the average person will...",
    "2:Responsibility for autonomous vehicle accidents belongs to...",
    "3:In 2040, commuting will take...",
    "4:In 2040, everyone will have access to...",
    "5:The future of mobility will make the world",
    "6:In the future, my transportation costs will...",
    "7:Future mobility options will have the greatest imapact on...",
    "8:In 2040...",
    "9:Travel in the future will be more dangerous for..."
]

"""Convert id from [image_TargetTitle] to survey_question.xlsx"""
templateIDforJson=[
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    12,
    13,
    14
]
answerIDforJson=[
    [15,21,48,18,16,20,47,19,49,17,23],
    [10,12,11,46,14],
    [24,25,27,28,58],
    [30,31,32,33,34],
    [15,21,48,18,16,20,47,19,49,17,23],
    [60,61,62],
    [38,39,40],
    [41,42,63,43],
    [50,51,52,53,23],
    [54,55,56,57,23]
]
image_ChoiceLimit=[3,-1,1,-1,1,1,1,1,1,1]