import maya.cmds as cmds
import pxr.Usd as Usd

def new_empty_uds(path):
    # USDステージを作成
    stage = Usd.Stage.CreateNew(path)
    
    # ルートレイヤーを取得
    root_layer = stage.GetRootLayer()
    
    # ノードを作成
    #cube = cmds.polyCube()[0]
    
    # Xformを作成し、ノードをアタッチ
    #cube_xform = UsdGeom.Xform.Define(stage, "/cube")
    #UsdMaya.WriteTransformAttrs(cube, cube_xform)
    
    # USDファイルに書き込む
    stage.Save()

new_usd_file_path="D:/MOSADesign/WorkTools/Maya/MOSATool/python/USD_Temp/empty6_Payload.usd"



from pxr import Usd, UsdGeom

def USD_02_PayloadMaker(new_usd_file_path,CheckBox_Absolute_Path_Bool):
    print(">>USD_02_PayloadMaker")
    import os
    # ディレクトリ取得
    usd_dir = os.path.dirname(new_usd_file_path)
    # カレントディレクトリを変更
    os.chdir(usd_dir)
    # 現在のカレントディレクトリ取得
    #nowDir=os.getcwd()
    nowDir=cmds.workspace( q=True, rootDirectory=True )
    print("nowDir="+nowDir)
    # カレントディレクトリまでの絶対パス取得
    #nowdir_abspath=os.path.abspath('.')
    nowdir_abspath=os.path.abspath(nowDir)
    print("nowdir_abspath="+nowdir_abspath)
    #========================================================
    # 指定したディレクトリからの相対パス取得
    new_usd_file_rel_path=os.path.relpath(new_usd_file_path,nowdir_abspath)
    new_usd_file_rel_path=new_usd_file_rel_path.replace('\\', '/')
    print("new_usd_file_rel_path=" +new_usd_file_rel_path)
    #=======================================================
    # 絶対パスをスラッシュパスに
    new_usd_file_abs_path=new_usd_file_path.replace('\\', '/')
    #=======================================================
    
    filename = os.path.basename(new_usd_file_path)
    filename_no_extension = os.path.splitext(filename)[0]
    print("filename_no_extension="+filename_no_extension)
    #new_payload_usd_file_path=new_usd_file_path.replace('.usd', '_Payload.usd')
    new_payload_usd_file_path=new_usd_file_path.replace('_Geom.usda', '_Payload.usda')
    print("new_payload_usd_file_path="+new_payload_usd_file_path)
    new_empty_uds(new_payload_usd_file_path)
    # Open
    #
    stage = Usd.Stage.Open(new_payload_usd_file_path)
    
    # Xformを作成し、ノードをアタッチ
    #xform = UsdGeom.Xform.Define(stage, "/"+filename_no_extension)  #OK
    #maya_node = "maya_node"  #OK
    #usd_node = stage.DefinePrim("/myXform/" + maya_node)  #OK
    #UsdMaya.WriteTransformAttrs(maya_node, usd_node, time=1.0) #NG
    
    # Reference
    payload_path = '/'+filename_no_extension
    #payload_prim = stage.DefinePrim(payload_path, 'Xform')
    # Local(そのレイヤーに定義を作る)
    prim = stage.DefinePrim(payload_path)
    stage.SetDefaultPrim(prim)
    #payload_prim.GetReferences().AddReference(new_usd_file_path)
    if(CheckBox_Absolute_Path_Bool==True):
        prim.GetReferences().AddReference(new_usd_file_abs_path)
    else:
        prim.GetReferences().AddReference(new_usd_file_rel_path)
    stage.Save()
    """
    # Payload
    #cube_path = "/myXform/"
    cube_path = "/"+filename_no_extension
    cube_prim = stage.DefinePrim(cube_path, 'Xform')
    cube_prim.GetPayloads().AddPayload(new_usd_file_path)
    stage.Save()
    print("new_usd_file_path="+new_usd_file_path)
    """

    
    USD_03_PayloadMaker(new_usd_file_path,CheckBox_Absolute_Path_Bool)
    
def USD_03_PayloadMaker(new_usd_file_path,CheckBox_Absolute_Path_Bool):
    print(">>USD_03_PayloadMaker")
    import os
    # ディレクトリ取得
    usd_dir = os.path.dirname(new_usd_file_path)
    # カレントディレクトリを変更
    os.chdir(usd_dir)
    # 現在のカレントディレクトリ取得
    #nowDir=os.getcwd()
    nowDir=cmds.workspace( q=True, rootDirectory=True )
    print("nowDir="+nowDir)
    # カレントディレクトリまでの絶対パス取得
    #nowdir_abspath=os.path.abspath('.')
    nowdir_abspath=os.path.abspath(nowDir)
    print("nowdir_abspath="+nowdir_abspath)
    #========================================================
    # 指定したディレクトリからの相対パス取得
    new_usd_file_rel_path=os.path.relpath(new_usd_file_path,nowdir_abspath)
    new_usd_file_rel_path=new_usd_file_rel_path.replace('\\', '/')
    print("new_usd_file_rel_path=" +new_usd_file_rel_path)
    #=======================================================
    # 絶対パスをスラッシュパスに
    new_usd_file_abs_path=new_usd_file_path.replace('\\', '/')
    #=======================================================
    filename = os.path.basename(new_usd_file_path)
    filename_no_extension = os.path.splitext(filename)[0]
    print("filename_no_extension="+filename_no_extension)
    #new_payload_usd_file_path=new_usd_file_path.replace('.usd', '_Payload.usd')
    new_payload_usd_file_path=new_usd_file_path.replace('_Geom.usda', '.usda')
    print("new_payload_usd_file_path="+new_payload_usd_file_path)
    new_empty_uds(new_payload_usd_file_path)
    # Open
    #
    stage = Usd.Stage.Open(new_payload_usd_file_path)
    
    # Xformを作成し、ノードをアタッチ
    #xform = UsdGeom.Xform.Define(stage, "/"+filename_no_extension)  #OK
    #maya_node = "maya_node"  #OK
    #usd_node = stage.DefinePrim("/myXform/" + maya_node)  #OK
    #UsdMaya.WriteTransformAttrs(maya_node, usd_node, time=1.0) #NG
    
    # Reference
    #payload_path = '/'+filename_no_extension
    #payload_prim = stage.DefinePrim(payload_path, 'Xform')
    #payload_prim.GetReferences().AddReference(new_usd_file_path)
    
    # Payload
    #cube_path = "/myXform/"
    cube_path = "/"+filename_no_extension
    #cube_prim = stage.DefinePrim(cube_path, 'Xform')
    # Local(そのレイヤーに定義を作る)
    prim = stage.DefinePrim(cube_path)
    stage.SetDefaultPrim(prim)
    #cube_prim.GetPayloads().AddPayload(new_usd_file_path)
    if(CheckBox_Absolute_Path_Bool==True):
        new_payload_file_abs_path=new_usd_file_abs_path.replace('_Geom.usda', '_Payload.usda')
        prim.GetPayloads().AddPayload(new_payload_file_abs_path)
        print("!!!!new_payload_file_abs_path= "+new_payload_file_abs_path)
        #prim.GetPayloads().AddPayload(new_usd_file_abs_path)
    else:
        new_payload_file_rel_path=new_usd_file_rel_path.replace('_Geom.usda', '_Payload.usda')
        prim.GetPayloads().AddPayload(new_payload_file_rel_path)
        print("!!!!new_payload_file_rel_path= "+new_payload_file_rel_path)
        #prim.GetPayloads().AddPayload(new_usd_file_rel_path)
    stage.Save()
    print("new_usd_file_path="+new_usd_file_path)
    
    # このUSDをMayaで開いても再現されないので使わない。
    #USD_04_LayoutMaker(new_usd_file_path)
    
def USD_04_LayoutMaker(new_usd_file_path):
    print(">>USD_04_Layout")
    import os
    from pxr import Usd, UsdGeom, Sdf
    # ディレクトリ取得
    usd_dir = os.path.dirname(new_usd_file_path)
    # カレントディレクトリを変更
    os.chdir(usd_dir)
    # 現在のカレントディレクトリ取得
    nowDir=os.getcwd()
    print("nowDir="+nowDir)
    # カレントディレクトリまでの絶対パス取得
    nowdir_abspath=os.path.abspath('.')
    print("nowdir_abspath="+nowdir_abspath)
    #========================================================
    # 指定したディレクトリからの相対パス取得
    new_usd_file_rel_path=os.path.relpath(new_usd_file_path,nowdir_abspath)
    
    new_usd_file_rel_path=new_usd_file_rel_path.replace('_Geom.usda', '.usda')
    print("new_usd_file_rel_path=" +new_usd_file_rel_path)
    #=======================================================
    # 絶対パスをスラッシュパスに
    new_usd_file_abs_path=new_usd_file_path.replace('\\', '/')
    #=======================================================
    filename = os.path.basename(new_usd_file_path)
    filename_no_extension = os.path.splitext(filename)[0]
    print("filename_no_extension="+filename_no_extension)
    #new_payload_usd_file_path=new_usd_file_path.replace('.usd', '_Payload.usd')
    new_layout_usd_file_path=new_usd_file_path.replace('_Geom.usda', '_Layout.usda')
    print("new_layout_usd_file_path="+new_layout_usd_file_path)
    new_empty_uds(new_layout_usd_file_path)
    # Open
    #
    
    stage = Usd.Stage.Open(new_layout_usd_file_path)
    
    # Xformを作成し、ノードをアタッチ
    #xform = UsdGeom.Xform.Define(stage, "/"+filename_no_extension)  #OK
    #maya_node = "maya_node"  #OK
    #usd_node = stage.DefinePrim("/myXform/" + maya_node)  #OK
    #UsdMaya.WriteTransformAttrs(maya_node, usd_node, time=1.0) #NG
    
    # Reference
    payload_path = '/'+filename_no_extension
    #payload_prim = stage.DefinePrim(payload_path, 'Xform')
    # Local(そのレイヤーに定義を作る)
    prim = stage.DefinePrim(payload_path)
    stage.SetDefaultPrim(prim)
    
    prim.GetReferences().AddReference(new_usd_file_path)
    
    
    
    # Payload
    #cube_path = "/myXform/"
    """
    cube_path = "/"+filename_no_extension
    cube_prim = stage.DefinePrim(cube_path, 'Xform')
    #cube_prim.GetPayloads().AddPayload(new_usd_file_path)
    cube_prim.GetPayloads().AddPayload(new_usd_file_rel_path)
    """
    #-----------------------------------------------------------
    
    #stage = Usd.Stage.Open('S_Stg_Cys_Gate_Com.usda')
    #parent_prim = stage.DefinePrim('/Parent')
    #default_prim = UsdGeom.Xform.Define('/Parent/Child', 'Xform')
    #stage.SetDefaultPrim(default_prim)
    #===========================================================
    #stage = Usd.Stage.Open('example.usda')
    #xform_prim = UsdGeom.Xform.Define(stage, '/MyXform')
    #xform_prim = UsdGeom.Xform.Define('/MyXform')
    #xform_path = Sdf.Path('/MyXform')
    #xform_prim = UsdGeom.Xform.Define(stage, xform_path)
    #stage.SetDefaultPrim(xform_prim)
    
    #===========================================================
    
    stage.Save()
    print("new_usd_file_path="+new_usd_file_path)