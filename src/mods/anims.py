import bpy

def alert(msg):
    bpy.ops.piana.message('INVOKE_DEFAULT', message = msg)

def selectchilds_recv(tree_dict,bone):

    list = tree_dict[bone.name]
    for x in list:
        x.select = True
        selectchilds_recv(tree_dict,x)
    return

def selectallchilds(arm, abone):
    bones = arm.data.bones

    #map bone to tree
    tree_dict ={ x.name : [] for x in bones}
    for x in bones:
        p = x.parent
        if p != None:
            tree_dict[p.name].append(x)
    # active_bone
    # abone = bpy.context.active_bone
    
    #call def
    selectchilds_recv(tree_dict, abone)   

def refresh_screen():
    bpy.context.view_layer.update()
    # bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1) # Blender画面更新

def reset_childs(amt, bone):
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    # amt.data.bones[bone].select = True
    selectallchilds(amt, amt.data.bones[bone])
    bpy.ops.anim.keyframe_clear_v3d()
    bpy.ops.pose.transforms_clear()
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()
    
def reset_twst(amt):
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    for bone in amt.data.bones:
        if 'Twst' in bone.name:
            bone.select = True
    bpy.ops.anim.keyframe_clear_v3d()
    bpy.ops.pose.transforms_clear()
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()