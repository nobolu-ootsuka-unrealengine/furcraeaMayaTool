import maya.cmds as cmds

class attrType:
    typeA = "group"
    typeB = "compornent"
    typeC = "assemble"
    typeD = "render"
    typeE = "proxy"
    typeF = "guide"
    
def set_USD_Kind(kindType): 
    objList = cmds.ls( sl = True)
    for obj in  objList:
        print(obj)
        if cmds.attributeQuery('USD_kind', node=obj, exists=1) != True :
            cmds.addAttr( longName= "USD_kind" ,dataType="string")
            cmds.setAttr(obj + ".USD_kind", kindType,type = "string" )
        else:
            print("カスタムアトリビュートは存在します")
            cmds.setAttr(obj + ".USD_kind", kindType,type = "string" )
    return None

    
    
def set_USD_Purpose(purposeType): 
    objList = cmds.ls( sl = True)
    for obj in  objList:
        print(obj)
        if cmds.attributeQuery('USD_ATTR_purpose', node=obj, exists=1) != True :
            cmds.addAttr( longName= "USD_ATTR_purpose" ,dataType="string")
            cmds.setAttr(obj + ".USD_ATTR_purpose", purposeType,type = "string" )
        else:
            print("カスタムアトリビュートは存在します")
            cmds.setAttr(obj + ".USD_ATTR_purpose", purposeType,type = "string" )
    return None    

def createAttrWindow():
    Attr_window = cmds.window("Add_CustomAttr_window")
    Attr_layout = cmds.columnLayout(adjustableColumn=True, parent=Attr_window)
    cmds.text (label="カスタムアトリビュートを付与したいノードを選択してください", align='left', parent=Attr_layout)
    cmds.separator(parent=Attr_layout)
    cmds.separator(parent=Attr_layout)
    cmds.text (label="kind設定", align='left', parent=Attr_layout)
    row1 = cmds.rowLayout(numberOfColumns=3, parent=Attr_window)
    cmds.button(label="kindの自動設定 Selected", command=callCmd_set_USD_Kind_Auto_Selected, parent=Attr_layout)
    cmds.button(label="kindの自動設定 ALL", command=callCmd_set_USD_Kind_Auto_All, parent=Attr_layout)
    cmds.button(label="group", command=callCmdA, parent=row1)
    cmds.button(label="compornent", command=callCmdB, parent=row1)
    cmds.button(label="assemble", command=callCmdC, parent=row1)
    cmds.separator(parent=Attr_layout)
    cmds.text (label="purpose設定", align='left', parent=Attr_layout)
    row2 = cmds.rowLayout(numberOfColumns=3, parent=Attr_window)
    cmds.button(label="render", command=callCmdD, parent=row2)
    cmds.button(label="proxy", command=callCmdE, parent=row2)
    cmds.button(label="guide", command=callCmdF, parent=row2)
    
    
    #cmds.button(label="Set Attr『USD_kind:compornent』", command=set_USD_Attr(A), parent=Attr_layout)
    cmds.showWindow(Attr_window)
    return None
    
def callCmdA(self):
    set_USD_Kind(attrType.typeA)
def callCmdB(self):
    set_USD_Kind(attrType.typeB)
def callCmdC(self):
    set_USD_Kind(attrType.typeC)
def callCmdD(self):
    set_USD_Purpose(attrType.typeD)
def callCmdE(self):
    set_USD_Purpose(attrType.typeE)
def callCmdF(self):
    set_USD_Purpose(attrType.typeF)   

def callCmd_set_USD_Kind_Auto_Selected(self):
    set_USD_Kind_Auto_Selected()
def callCmd_set_USD_Kind_Auto_All(self):
    set_USD_Kind_Auto_All() 

    
def USD_SetAttribute():
    if cmds.window("Add_CustomAttr_window",exists=True):
        cmds.deleteUI("Add_CustomAttr_window")
    createAttrWindow()
    
def set_USD_Kind_Auto_Selected():
    TopList = cmds.ls(sl=True, assemblies = True)
    set_USD_Kind_Auto_Main(TopList)

def set_USD_Kind_Auto_All():
    TopList = cmds.ls( assemblies = True)
    set_USD_Kind_Auto_Main(TopList)

def set_USD_Kind_Auto_Main(TopList):
    print("TopList="+str(TopList))
    RejectList=['persp', 'top', 'front', 'side']
    TopSet=set(TopList)
    RejectSet=set(RejectList)
    GoodTopSet=TopSet-RejectSet
    print("GoodTopSet="+str(GoodTopSet))
    GoodTopList=list(GoodTopSet)
    print("GoodTopList="+str(GoodTopList))
    for myObj in GoodTopList:
        # Top Node List Loop
        # Get mashGroup List
        mashGroupList=[]
        myObjList = cmds.ls(myObj, dagObjects = True,type='mesh',long=True)
        print("myObjList="+str(myObjList))
        for obj in myObjList:
            nodeTypeStr=cmds.nodeType(obj)
            print("nodeTypeStr="+str(nodeTypeStr))
            if cmds.nodeType(obj) == 'mesh':
                print("Shape="+str(obj))
                parentNode = cmds.listRelatives(obj,parent=True,fullPath=True)
                mashGroupList.append(parentNode[0])   
        print("mashGroupList="+str(mashGroupList))
        
        # Get transformList
        transformList2 = cmds.ls(myObj, dagObjects = True,type='transform',long=True)
        #print("transformList2="+str(transformList2))
        
        # Set transformList - mashGroupList
        transformSet=set(transformList2)
        mashGroupSet=set(mashGroupList)
        GoodtransformSet=transformSet-mashGroupSet
        
        print("GoodtransformSet="+str(GoodtransformSet))
        cmds.select(GoodtransformSet)
        set_USD_Kind(attrType.typeA)
        cmds.select(cl=True)
        cmds.select(mashGroupList)
        set_USD_Kind(attrType.typeB)
        cmds.select(cl=True)
    
#set_USD_Kind_Auto()