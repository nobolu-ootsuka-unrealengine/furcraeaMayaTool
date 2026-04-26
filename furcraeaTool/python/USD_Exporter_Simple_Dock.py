
# -*- coding: utf-8 -*-
import os
from functools import partial
import time
import imp
import random

#--------------------USD pipline Tool-----------------------------
import maya.cmds as cmds
from mayaUsd.lib import proxyAccessor as pa
import mayaUsd.lib as mayaUsdLib

from pxr import Usd, Sdf, UsdGeom
from mayaUsd import schemas as mayaUsdSchemas


import mayaUsd.ufe
import mayaUsd.lib
import ufe
import os,subprocess

class USD:
    mayaPath = []

#-----------------------------------------------------------------
"""
PySide2モジュールを探し、ある場合はそちらをインポートします。
"""
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *

except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *


LOGO_IMAGE = r"D:\furcraeaTokyo\furcraeaTool\python\image\furcraeaToolUSDexporter.png"


def get_maya_pointer():
    """
    Mayaのメインウィンドウを取得する関数
    """
    try:
        import maya.cmds as cmds
        from maya import OpenMayaUI

    except ImportError:
        return None

    """
    実は2017ではshibokenも2になっているので、あればshiboken2をインポートします。
    """
    try:
        imp.find_module("shiboken2")
        import shiboken2
        return shiboken2.wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QWidget)

    except ImportError:
        import shiboken
        return shiboken.wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QWidget)

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

#class Example_connectAttr(MayaQWidgetDockableMixin, QScrollArea):
class Example_connectAttr(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, node=None, *args, **kwargs):
        super(Example_connectAttr, self).__init__(*args, **kwargs)
        # Member Variables
        self.nodeName = node               # Node name for the UI
        self.attrUI = None                 # Container widget for the attr UI widgets
        self.attrWidgets = {}              # Dict key=attrName, value=widget
        
        randomInt=random.randint(0,9999)
        self.setObjectName("MyDock_Window"+str(randomInt))
        self.setWindowTitle("MyDock Window")
        self._initUI()
        
        
    def _initUI(self):
        wrapper = QWidget()
        self.setCentralWidget(wrapper)

        mainLayout = QVBoxLayout()
        wrapper.setLayout(mainLayout)
        #-----------------------------------------------------------------------
        # First row
        #-----------------------------------------------------------------------
        firstHolizontalArea = QVBoxLayout()
        firstHolizontalArea.setSpacing(2)
        mainLayout.addLayout(firstHolizontalArea)

        labelArea = QVBoxLayout()
        labelArea.setSpacing(2)
        #labelArea = QHBoxLayout()
        firstHolizontalArea.addLayout(labelArea)

        
        #-------------------LOGO---------------------
        imageWidget = QLabel()
        imageWidget.setPixmap(QPixmap(LOGO_IMAGE))
        labelArea.addWidget(imageWidget)
        labelArea.addStretch()
        #---------------------------------------
        
        labelWidget = QLabel("出力したいメッシュのトップノードで[_Geom]のついたノードを選択して、")
        labelArea.addWidget(labelWidget)
        
        labelWidget2 = QLabel("[USD Export Selected]を押してください。")
        labelArea.addWidget(labelWidget2)
        
        labelArea.addWidget(self._makeHorizontalLine())
        
        labelWidget3 = QLabel("ExportPath:")
        labelArea.addWidget(labelWidget3)
        
        self.lineEdit_ExportPath = QLineEdit()
        #self.lineEdit_ExportPath.setMaximumWidth(350)
        self.lineEdit_ExportPath.setText(F_get_lastExportDirPath())
        firstHolizontalArea.addWidget(self.lineEdit_ExportPath)
        
        #-----------------------------------------------------------------------
        # sixth row
        #-----------------------------------------------------------------------
        sixthHorizontalArea = QHBoxLayout()
        sixthHorizontalArea.setSpacing(2)
        mainLayout.addLayout(sixthHorizontalArea)
        
        msgBoxBtn = QPushButton("Browse")
        sixthHorizontalArea.addWidget(msgBoxBtn)
        msgBoxBtn.clicked.connect(F_select_exportDir)
        
        colorDialogBtn = QPushButton("Scene")
        sixthHorizontalArea.addWidget(colorDialogBtn)
        colorDialogBtn.clicked.connect(F_btn_scene)

        progressDialogBtn = QPushButton("Open")
        sixthHorizontalArea.addWidget(progressDialogBtn)
        progressDialogBtn.clicked.connect(F_folderOpen)
        
        mainLayout.addWidget(self._makeHorizontalLine())
        
        #-----------------------------------------------------------------------
        # Third row
        #-----------------------------------------------------------------------
        thirdHorizontalArea = QVBoxLayout()
        thirdHorizontalArea.setSpacing(2)
        mainLayout.addLayout(thirdHorizontalArea)

        self.checkBox1_kind = QCheckBox("Kind設定をして/エンジンでメッシュを分離する。")
        thirdHorizontalArea.addWidget(self.checkBox1_kind)
        self.checkBox1_kind.setChecked(True)
        
        self.checkBox2_moveZero = QCheckBox("原点に移動する")
        thirdHorizontalArea.addWidget(self.checkBox2_moveZero)
        self.checkBox2_moveZero.setChecked(False)
        
        self.checkBox3_absolutePath = QCheckBox("絶対パスでusdaをリンクする")
        thirdHorizontalArea.addWidget(self.checkBox3_absolutePath)
        self.checkBox3_absolutePath.setChecked(False)
        
        self.checkBox4_onlyGeom = QCheckBox("Geomのみ書き出す")
        thirdHorizontalArea.addWidget(self.checkBox4_onlyGeom)
        self.checkBox4_onlyGeom.setChecked(False)
        
        #-----------------------------------------------------------------------
        # sixth row
        #-----------------------------------------------------------------------
        sevenHorizontalArea = QHBoxLayout()
        sevenHorizontalArea.setSpacing(2)
        mainLayout.addLayout(sevenHorizontalArea)
        
        msgBoxBtn = QPushButton("USD Export Selected")
        sevenHorizontalArea.addWidget(msgBoxBtn)
        msgBoxBtn.clicked.connect(F_USD_Export_All3)
        
    def _makeHorizontalLine(self):
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        return hline
        
        


#------------------------------------------------------------------------------------------------------------
#----------------------------------------USD pipline Tool---------------------------------------------------- 



def F_USD_Export_All3():
    print(USD.mayaPath)
    scenefilePath = cmds.file(q=1, sceneName=1)
    USD.mayaPath,mayaFile = os.path.split(scenefilePath)
    meshList = cmds.ls( sl = True)
    meshNum = len(meshList)
    #exPath = USD.mayaPath + '/Usd'
    exPath = USD.mayaPath 
    if not os.path.exists(exPath):
        print("フォルダがない場合は作成します。 exPath= "+exPath)
        os.makedirs(exPath)
    if meshNum > 0 and not meshList == [] :
        F_changeTextFld

            
        #  Kind設定あり
        #CheckBox_Kind_Bool = cmds.checkBox('CheckBox_Kind', q=True, value=True)
        CheckBox_Kind_Bool = ui.checkBox1_kind.isChecked()
        if CheckBox_Kind_Bool:
            #  チェックされている場合に実行したい
            F_USD_00_Kind_Func(meshList)
        
        
        
        F_USD_01_mayaUSDExport_Func(meshList)
        F_USD_02_Payload_Func(meshList)
    else:
        cmds.confirmDialog(title='Warning',message='メッシュが選択されていないか、\nシーンのパスが取得できません')
    return None

def F_getTransform_MayaObj():
    selectTed=cmds.ls(sl=True)
    # コピー元のオブジェクト名
    source_obj = selectTed[0]
    
    # オブジェクトの座標を取得
    pos = cmds.xform(source_obj, q=True, ws=True, t=True)
    
    # オブジェクトの回転を取得
    rot = cmds.xform(source_obj, q=True, ws=True, ro=True)
    
    # オブジェクトのスケールを取得
    scl = cmds.xform(source_obj, q=True, ws=True, s=True)
    
    return pos,rot,scl
    
def F_setTransform_MayaObj(pos,rot,scl):
    selectTed=cmds.ls(sl=True)
    # コピー元のオブジェクト名
    source_obj = selectTed[0]

    # オブジェクトの座標を取得
    cmds.xform(source_obj, ws=True, t=pos)
    
    # オブジェクトの回転を取得
    cmds.xform(source_obj, ws=True, ro=rot)
    
    # オブジェクトのスケールを取得
    cmds.xform(source_obj, ws=True, s=scl)
    
    #return pos,rot,scl




def F_USD_00_Kind_Func(meshList):
    print("USD_00_Kind_Func")
    # 単体のアセットとして出力する際には、トップノードを"compornent"にしてまるっと集約するケースもあるので、デフォルトはオフに
    print("--------------------USD_SetAttribute.set_USD_Kind_Auto()--------------------------------START")
    import USD_SetAttribute
    USD_SetAttribute.set_USD_Kind_Auto_Selected()
    print("--------------------USD_SetAttribute.set_USD_Kind_Auto()----------------------------------END")
    
    
    F_USD_01_mayaUSDExport_Func(meshList)
    
def F_USD_01_mayaUSDExport_Func(meshList):
    print(">>USD_01_mayaUSDExport_Func　Geomの出力")
    
    for i in meshList:
        # select
        cmds.select(i)
        #  原点に移動あり
        #CheckBox_MoveToOrigin_Bool = cmds.checkBox('CheckBox_Move_to_Origin', q=True, value=True)
        CheckBox_MoveToOrigin_Bool = ui.checkBox2_moveZero.isChecked()
        pos=(0,0,0) 
        rot=(0,0,0) 
        scl=(0,0,0) 
        #pos,rot,scl = getPrimXForm()
        pos,rot,scl = F_getTransform_MayaObj()
        if CheckBox_MoveToOrigin_Bool:
            #  チェックされている場合に実行したい
            # 原点に移動
            #setPrimXForm([0,0,0],rot,scl)
            Origin_pos=(0,0,0)
            F_setTransform_MayaObj(Origin_pos,rot,scl)

            #cmds.file(save=True, force=True)
        
        basePath = F_get_lastExportDirPath()
        F_set_lastExportDirPath(basePath)
        #exportPath = USD.mayaPath +'/Usd/' + i + '.usda'
        exportPath = basePath + i + '.usda'
        
        cmds.select(i)
        cmds.mayaUSDExport(
            file=exportPath,
            selection=True,
            defaultUSDFormat="usda",
            defaultMeshScheme="none",
            materialsScopeName="mtl",
            exportDisplayColor=True,
            renderLayerMode="modelingVariant"
            #geomSidedness="single",       無効なフラグ 'geomSidedness' # 
            #exportComponentTags=False     無効なフラグ 'exportComponentTags' # 
            )
            #materialsScopeName="mat",
            #kind="group",

        if CheckBox_MoveToOrigin_Bool:
            #  チェックされている場合に実行したい
            #元に戻す
            cmds.select(i)
            #setPrimXForm(pos,rot,scl)
            F_setTransform_MayaObj(pos,rot,scl)
            #cmds.file(save=True, force=True)
    
def F_USD_02_Payload_Func(meshList):
    print(">>USD_02_Payload_Func   meshList= "+str(meshList))
    
    #CheckBox_Absolute_Path_Bool = cmds.checkBox('CheckBox_Absolute_Path', q=True, value=True)
    CheckBox_Absolute_Path_Bool =  ui.checkBox3_absolutePath.isChecked()
    #CheckBox_Only_Geom_Output_Bool = cmds.checkBox('CheckBox_Only_Geom_Output', q=True, value=True)
    CheckBox_Only_Geom_Output_Bool =  ui.checkBox4_onlyGeom.isChecked()
    #if CheckBox_Absolute_Path_Bool:
    
    if(CheckBox_Only_Geom_Output_Bool==False):
        #Geom以外も出力する
        
        for i in meshList:
    
            # エクスポート
            basePath = F_get_lastExportDirPath()
            exportPath = basePath + i + '.usda'
            cmds.select(i)
            
            
            
            
            import USD_02_PayloadMaker
            USD_02_PayloadMaker.USD_02_PayloadMaker(exportPath,CheckBox_Absolute_Path_Bool)


def F_select_exportDir(self):
    
    filePath = cmds.fileDialog2( cap = '書き出しディレクトリの選択', okc = '書き出しディレクトリを設定',ds = 2, fm = 3,startingDirectory=F_get_lastExportDirPath())
    if filePath == None:
        return False
    else:
        F_set_lastExportDirPath(filePath[0]+"/")
        
        
def F_exportFile():
    filePath = cmds.fileDialog2(fileFilter = '*.json', cap = '書き出し', okc = '書き出し',ds = 2, fm = 0)
    if filePath == None:
        return False
               
def F_importFile():
    filePath = cmds.fileDialog2(fileFilter = '*.json', cap = '読み込み', okc = '読み込み',ds = 2, fm = 1)
    if filePath == None:
        return False

def F_get_lastExportDirPath_ExistBool():
    lastExportDirPath_ExistBool=False
    Attlist=cmds.listAttr( r=True )
    print("Attlist= "+str(Attlist))
    for AttName in Attlist:
        #print("AttName= "+AttName)
        if(AttName=="lastExportDirPath"):
            lastExportDirPath_ExistBool=True
            print("HIT!!!!!!!lastExportDirPath")
    return lastExportDirPath_ExistBool

def F_addAttr_lastExportDirPath():
    lastExportDirPath_ExistBool= F_get_lastExportDirPath_ExistBool()
    if(lastExportDirPath_ExistBool==False):
        cmds.addAttr(longName='lastExportDirPath',dataType='string')
        

def F_set_lastExportDirPath(lastExportDirPath):
    
    selectList=cmds.ls(sl=True)
    if(str(selectList)== "[]"):
        print("なにも選択されていません。0 set_lastExportDirPath")
    else:

        for i in selectList:
            cmds.select(i)
            #---------------------------
            F_addAttr_lastExportDirPath()
            #---------------------------
            print("i= "+str(i))
            attName=i+"."+'lastExportDirPath'
            print("attName= "+attName)
            cmds.setAttr( attName, lastExportDirPath,type="string")
            
    #text_Field_id="USD_Export_window|USD_layout|pathTxtFld"
    #cmds.textField(text_Field_id, edit=True, text=lastExportDirPath)
    ui.lineEdit_ExportPath.setText(lastExportDirPath)
    cmds.select(selectList)



def F_get_lastExportDirPath():

    selectList=cmds.ls(sl=True)
    
    lastExportDirPath=""
    if(str(selectList)== "[]"):
        print("なにも選択されていません。3 get_lastExportDirPath")
        lastExportDirPath = F_get_scenePath()
    else:
        for i in selectList:
            cmds.select(i)
            #---------------------------
            F_addAttr_lastExportDirPath()
            #---------------------------
            print("i= "+str(i))
            attName=i+"."+'lastExportDirPath'
            print("attName= "+attName)
            lastExportDirPath = cmds.getAttr(attName)
            print("lastExportDirPath="+str(lastExportDirPath))
            if(str(lastExportDirPath)=="None"):
                lastExportDirPath = F_get_scenePath()
        cmds.select(selectList)
    return lastExportDirPath
text_Field_id=""    


def F_folderOpen(self):
    Exportpath = F_get_lastExportDirPath()
    Exportpath = Exportpath.replace('/', '\\')
    #Exportpath = "r"+Exportpath
    #subprocess.Popen(["explorer", Exportpath], shell=True)
    #subprocess.Popen(["explorer", "/root,", Exportpath], shell=True)
    Exportpath = os.path.realpath(Exportpath)
    # subprocessでコマンドシェルを実行
    subprocess.Popen(f'explorer.exe /select, {Exportpath}')
    print(Exportpath)

def F_get_scenePath():
    scenefilePath = cmds.file(q=1, sceneName=1)
    mayaPath,mayaFile = os.path.split(scenefilePath)
    #mayaPath = mayaPath + "/Usd/"
    #mayaPath = mayaPath + "/"
    mayaPath=os.path.abspath(mayaPath)
    mayaPath=mayaPath.replace('\\', '/')
    print("mayaPath= "+mayaPath)
    mayaPath_len=len(mayaPath)
    last_str=mayaPath[mayaPath_len-1:]
    print("mayaPath= "+mayaPath+ " last_str= "+last_str)
    if(last_str=="/"):
        pass
    else:
        mayaPath=mayaPath+"/"
    
    return mayaPath
    
def F_btn_scene(self):
    scenePath = F_get_scenePath()
    
    
    
    F_set_lastExportDirPath(scenePath)
    
def F_changeTextFld(*arg):
    #mayaPath = get_scenePath()
    #cmds.textField("pathTxtFld", edit=True, text=get_lastExportDirPath())
    #pathTxtFld_value=cmds.textField("pathTxtFld", r=True, v=True)
    #pathTxtFld_value = cmds.textField("pathTxtFld", q=True, text=True)
    text_Field_id="USD_Export_window|USD_layout|pathTxtFld"
    print("text_Field_id= "+text_Field_id)
    pathTxtFld_value = cmds.textField(text_Field_id, q=True, text=True)
    #pathTxtFld_value = pathTxtFld
    print("pathTxtFld_value= "+pathTxtFld_value)
    F_set_lastExportDirPath(pathTxtFld_value)
    
    

    
#----------------------------------------USD pipline Tool----------------------------------------------------
#------------------------------------------------------------------------------------------------------------



ui= 0
def start():
    maya_win = get_maya_pointer()
    ui = Example_connectAttr(node = maya_win)
    ui.show(dockable=True, floating=True)
    return ui

def starter():
    global ui
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    ui = start()
    app.exec_()
print("__name__ = "+__name__)
if __name__ == '__main__' or __name__ == "NppMaya" or __name__ == "main":
    starter()