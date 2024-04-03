#     Blender addon for managing Northstar settings
#     Copyright (C) 2023 EM4Volts
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import bpy, time, bmesh, mathutils
from bpy.props import StringProperty, CollectionProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences, UIList, Menu
from .qcparse import *
from .mdl_structs import *

#        _      _____  _____ _______ _____       __  __  __ _____  _____  _____
#       | |    |_   _|/ ____|__   __/ ____|     / / |  \/  |_   _|/ ____|/ ____|
#       | |      | | | (___    | | | (___      / /  | \  / | | | | (___ | |
#       | |      | |  \___ \   | |  \___ \    / /   | |\/| | | |  \___ \| |
#       | |____ _| |_ ____) |  | |  ____) |  / /    | |  | |_| |_ ____) | |____
#       |______|_____|_____/   |_| |_____/  /_/     |_|  |_|_____|_____/ \_____|





#MAIN COLLECTION FOR MATERIAL MANAGEMENT
class PerimeterQCMainCollection( bpy.types.PropertyGroup ):

    name: bpy.props.StringProperty() #not used right now, keeping beccause, well idk wy
    model_name: bpy.props.StringProperty(default="")
    surfaceprop: bpy.props.StringProperty(default="")
    test: bpy.props.PointerProperty( type=bpy.types.Material )

    #contents        : bpy.props.StringProperty(default="")
    #cdmaterials     : bpy.props.StringProperty(default="")
    #bonemerge       : bpy.props.StringProperty(default="")
    #includemodel    : bpy.props.StringProperty(default="")





#MAIN OPERATOR FOR MATERIAL MANAGEMENT LIST
class PERIMETER_UL_QCManagementTexturegroupList( UIList ):
    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        split = layout.split(  )
        split.prop( item.test, "name", text="", emboss=False, translate=False, icon="MATERIAL")


# Define a custom property group to store the strings
class PerimeterTexturegroupItem( bpy.types.PropertyGroup ):
    Materials: bpy.props.StringProperty()



class PerimeterBodygroupMeshFile( bpy.types.PropertyGroup ):
    mesh_file: bpy.props.StringProperty( default="unnamed_mesh_file" )

class PerimeterBodygroupItem( bpy.types.PropertyGroup ):
    bodygroup_name: bpy.props.StringProperty( default="blank" )
    bodygroup_meshes: CollectionProperty(type = PerimeterBodygroupMeshFile)
    bodygroup_meshes_index: bpy.props.IntProperty()

class PERIMETER_UL_BodygroupList( UIList ):
    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        split = layout.split(  )
        split.prop( item, "bodygroup_name", text="", emboss=False, translate=False, icon="GROUP")\
        

class PERIMETER_UL_BodygroupMeshList( UIList ):
    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        split = layout.split(  )
        split.prop( item, "mesh_file", text="", emboss=False, translate=False, icon="MESH_CUBE")


#       ______ _    _ _   _  _____ _______ _____ ____  _   _  _____
#      |  ____| |  | | \ | |/ ____|__   __|_   _/ __ \| \ | |/ ____|
#      | |__  | |  | |  \| | |       | |    | || |  | |  \| | (___
#      |  __| | |  | | . ` | |       | |    | || |  | | . ` |\___ \
#      | |    | |__| | |\  | |____   | |   _| || |__| | |\  |____) |
#      |_|     \____/|_| \_|\_____|  |_|  |_____\____/|_| \_|_____/













#        _____        _   _ ______ _            __  __  __ ______ _   _ _    _  _____
#       |  __ \ /\   | \ | |  ____| |          / / |  \/  |  ____| \ | | |  | |/ ____|
#       | |__) /  \  |  \| | |__  | |         / /  | \  / | |__  |  \| | |  | | (___
#       |  ___/ /\ \ | . ` |  __| | |        / /   | |\/| |  __| | . ` | |  | |\___ \
#       | |  / ____ \| |\  | |____| |____   / /    | |  | | |____| |\  | |__| |____) |
#       |_| /_/    \_\_| \_|______|______| /_/     |_|  |_|______|_| \_|\____/|_____/



class PerimeterQCBodygroupManager( bpy.types.Panel ):
    bl_idname = "qcfile_bodygroup_manager"
    bl_label = "QC Bodygroup Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Northstar"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        
        col1 = row.column()

        if context.scene.qc_bodygroups_found:
            selected_index = bpy.context.scene.perimeter_bodygroup_collection_index
            try:
                selected_item = bpy.context.scene.perimeter_bodygroup_collection[selected_index]
            except:
                selected_item = None

            col1.label( text="BODYGROUP", icon="SEQ_STRIP_DUPLICATE" )

            col1.template_list( "PERIMETER_UL_BodygroupList", "", context.scene, "perimeter_bodygroup_collection", context.scene, "perimeter_bodygroup_collection_index" )
            row1 = col1.row()
            row1.operator( "northstar.add_bodygroup_item", text=f"Add", icon="ADD")
            removerow = row1.row()
            if not selected_item == None:
                removerow.enabled = True
            else:
                removerow.enabled = False
            removerow.operator( "northstar.remove_bodygroup_item", text=f"Remove", icon="REMOVE")



   
            if not selected_item == None:
                col2 = row.column()
                col2.label( text="MESH FILE", icon="FILE_VOLUME" )
                col2.template_list("PERIMETER_UL_BodygroupMeshList", "", selected_item, "bodygroup_meshes", selected_item, "bodygroup_meshes_index", rows=5)
                row2 = col2.row()
                row2.operator("northstar.add_bodygroup_mesh_item", text=f"Add", icon="ADD")
                removerow1 = row2.row()
                if selected_item.bodygroup_meshes:
                    removerow1.enabled = True
                else:
                    removerow1.enabled = False
                removerow1.operator("northstar.remove_bodygroup_mesh_item", text=f"Remove", icon="REMOVE")
                row = layout.row()
                row.operator( "northstar.write_bodygroups", text=f"Write Bodygroups", icon="DISK_DRIVE")
                row.scale_y = 2.0
        else: 
            col1.label( text="BODYGROUPS NOT INITIALIZED", icon="ERROR")
            col1.label( text="SELECT QC FILE IN QC File Management", icon="ERROR")

class PerimeterQCManagementPanel( bpy.types.Panel ):
    bl_idname = "qcfile_management_panel"
    bl_label = "QC File Management"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Northstar"



    def draw(self, context):
        layout = self.layout
        scene = context.scene

        selected_index = 0
        try:
            selected_item = bpy.context.scene.perimeter_qc_main_collection[selected_index]

        except:
            selected_item = None

        col = layout.column()
        col.operator( "perimeter.qc_parser", text="Select QC File", icon="FILE_FOLDER" )
        #col.operator( "northstar.rui_mesh_import", text="import rui (d_s no)") disabled for now til finished.
        subcol = col.column()
        if not context.scene.qc_file_selected:
            subcol.enabled = False
        subcol.prop( context.scene, "qc_file_path", text="QC FILE", icon="MEMORY")
        #col.operator( "northstar.write_qc_file", text="Save to selected QC File", icon="SEQ_CHROMA_SCOPE")
        #col.template_list( "PERIMETER_UL_QCManagementTexturegroupList", "", context.scene, "perimeter_qc_main_collection", context.scene, "perimeter_qc_main_collection_index" )
        #col.label( text="MODELNAME", icon="OUTLINER_DATA_MESH")
        #col.prop( context.scene, "qc_model_name", text="")
        #col.label( text="MAXVERTS", icon="GROUP_VERTEX" )
        #col.prop( context.scene, "qc_maxverts", text="")
        #col.label( text="SURFACEPROP", icon="OUTLINER_OB_SURFACE" )
        #col.prop( context.scene, "surfaceprops", text="")

        strings = context.scene.texturegroup_materials

        col = col.column()
        col.operator( "northstar.qc_skeleton_parser", text="EXPERIMENTAL Import Attachements to Skeleton", icon="STICKY_UVS_DISABLE" )
        Texturegroups_box = layout.box()
        col2 = Texturegroups_box.column()
        col2.label( text="TEXTUREGROUPS", icon="IMAGE_PLANE")
        col2.label( text="TEXTUREGROUP NAME", icon="FILE_FONT" )
        col2.prop( context.scene, "qc_texturegroup_name", text="" )
        row2 = col2.row()

        s_string = ""
        if len(strings) > 1:
            s_string = "s"

        if context.scene.qc_expand_texturegroups:


            row2.prop( context.scene, "qc_expand_texturegroups", text=f"Expand {len(strings)} Line{s_string}", icon="TRIA_DOWN")
        else:
            row2.prop( context.scene, "qc_expand_texturegroups", text=f"Collapse Line{s_string}", icon="TRIA_UP")

            col2.operator("perimeter.add_texturegroup_item", text="Add Material(s)", icon='ADD')

            for i, string_item in enumerate(strings):
                row = Texturegroups_box.row()
                row.prop(string_item, "Materials", text=f"")
                row.operator("perimeter.remove_texturegroup_item", text="", icon='TRASH').index = i
            col2.operator("perimeter.qcpanel_write_texgroups", text="Write Groups", icon="DISK_DRIVE")




#         ____  _____  ______ _____         _______ ____  _____   _____
#        / __ \|  __ \|  ____|  __ \     /\|__   __/ __ \|  __ \ / ____|
#       | |  | | |__) | |__  | |__) |   /  \  | | | |  | | |__) | (___
#       | |  | |  ___/|  __| |  _  /   / /\ \ | | | |  | |  _  / \___ \
#       | |__| | |    | |____| | \ \  / ____ \| | | |__| | | \ \ ____) |
#        \____/|_|    |______|_|  \_\/_/    \_\_|  \____/|_|  \_\_____/






class PerimeterWriteBodygroups(bpy.types.Operator):
    bl_idname = "northstar.write_bodygroups"
    bl_label = "Remove Material from Texturegroup"
  
    def execute(self, context):

        #initialize an empty dict "bodygroup_dict"
        bodygroup_dict = {}
        for bodygroup in context.scene.perimeter_bodygroup_collection:
            bodygroup_name = bodygroup.bodygroup_name
            bodygroup_meshes = []
            for mesh in bodygroup.bodygroup_meshes:
                if not mesh.mesh_file == "unnamed_mesh_file":
                    bodygroup_meshes.append(mesh.mesh_file)
            bodygroup_dict[bodygroup_name] = bodygroup_meshes
        write_bodygroups_to_file(context.scene.qc_file_path, bodygroup_dict)

        return {'FINISHED'}


class PerimeterWriteQCArguments(bpy.types.Operator):
    bl_idname = "northstar.write_qc_file"
    bl_label = "Remove Material from Texturegroup"
  
    def execute(self, context):

        #initialize an empty dict "bodygroup_dict"
        bodygroup_dict = {}
        for bodygroup in context.scene.perimeter_bodygroup_collection:
            bodygroup_name = bodygroup.bodygroup_name
            bodygroup_meshes = []
            for mesh in bodygroup.bodygroup_meshes:
                if not mesh.mesh_file == "unnamed_mesh_file":
                    bodygroup_meshes.append(mesh.mesh_file)
            bodygroup_dict[bodygroup_name] = bodygroup_meshes
        write_bodygroups_to_file(context.scene.qc_file_path, bodygroup_dict)

        return {'FINISHED'}



class PerimeterAddTextureGroupItem(bpy.types.Operator):
    bl_idname = "perimeter.add_texturegroup_item"
    bl_label = "Add Material to Texturegroup"

    def execute(self, context):
        strings = context.scene.texturegroup_materials
        strings.add()
        return {'FINISHED'}


class PerimeterRemoveTextureGroupItem(bpy.types.Operator):
    bl_idname = "perimeter.remove_texturegroup_item"
    bl_label = "Remove Material from Texturegroup"

    index: bpy.props.IntProperty()

    def execute(self, context):
        strings = context.scene.texturegroup_materials
        strings.remove(self.index)
        return {'FINISHED'}

class PerimeterAddBodyGroupItem(bpy.types.Operator):
    bl_idname = "northstar.add_bodygroup_item"
    bl_label = "Add Material to Texturegroup"

    def execute(self, context):
        items = context.scene.perimeter_bodygroup_collection
        items.add()

        return {'FINISHED'}




class PerimeterRemoveBodyGroupItem(bpy.types.Operator):
    bl_idname = "northstar.remove_bodygroup_item"
    bl_label = "Remove Material from Texturegroup"

    index: bpy.props.IntProperty()

    def execute(self, context):
        selected_index = bpy.context.scene.perimeter_bodygroup_collection_index
        selected_item = bpy.context.scene.perimeter_bodygroup_collection[selected_index]
        bpy.context.scene.perimeter_bodygroup_collection.remove( selected_index )

        return {'FINISHED'}

class PerimeterAddBodyGroupMeshItem(bpy.types.Operator):
    bl_idname = "northstar.add_bodygroup_mesh_item"
    bl_label = "Add Material to Texturegroup"

    @classmethod
    def poll(cls, context):
        return context.scene.perimeter_bodygroup_collection and context.scene.perimeter_bodygroup_collection_index >= 0
    
    def execute(self, context):
        selected_index = context.scene.perimeter_bodygroup_collection_index
        selected_item = context.scene.perimeter_bodygroup_collection[selected_index]
        
        # Add a new PerimeterBodygroupMeshFile to the bodygroup_meshes list
        new_mesh = selected_item.bodygroup_meshes.add()
        # Optionally, you can set properties of the newly added mesh here
        # new_mesh.mesh_file = "new_mesh_file_name"
        
        return {'FINISHED'}


class PerimeterRemoveBodyGroupMeshItem(bpy.types.Operator):
    bl_idname = "northstar.remove_bodygroup_mesh_item"
    bl_label = "Remove Material from Texturegroup"
  
    @classmethod
    def poll(cls, context):
        return context.scene.perimeter_bodygroup_collection and context.scene.perimeter_bodygroup_collection_index >= 0
    
    def execute(self, context):
        selected_index = context.scene.perimeter_bodygroup_collection_index
        selected_item = context.scene.perimeter_bodygroup_collection[selected_index]
        
        if selected_item.bodygroup_meshes_index >= 0 and selected_item.bodygroup_meshes_index < len(selected_item.bodygroup_meshes):
            selected_item.bodygroup_meshes.remove(selected_item.bodygroup_meshes_index)
            selected_item.bodygroup_meshes_index -= 1  # Move index to the previous item
            return {'FINISHED'}
        else:
            self.report({'INFO'}, "No mesh selected")
            return {'CANCELLED'}

class PerimeterQCParserOperator( bpy.types.Operator ):   #PARSE THE SELECTED QC FILE, POPULATE PANEL WITH THE VALUES 
    bl_idname = "perimeter.qc_parser"
    bl_label = ""
    bl_description = "Parse QC File"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty( subtype="FILE_PATH" )


    def execute( self, context ):
        qc_file_path = bpy.path.abspath( self.filepath )
        #save the qc file path to the scene prefs
        context.scene.qc_file_path = qc_file_path
        context.scene.qc_bodygroups_found = False
        #initialize QC class
        QuakeC_file = QC(qc_file_path)
        texturegroup_mats = context.scene.texturegroup_materials
        bodygroup_name_list = context.scene.perimeter_bodygroup_collection

        context.scene.qc_model_name = QuakeC_file.model_name
        context.scene.qc_surfaceprop = QuakeC_file.surfaceprop

        texturegroup_mats.clear()
        bodygroup_name_list.clear()
        context.scene.qc_texturegroup_name = QuakeC_file.texturegroups[0]

        for material_line in QuakeC_file.texturegroups[1]:
            cur_mat = texturegroup_mats.add()
            cur_mat.Materials = material_line    


        bodygroup_names = bodygroup_name_list
        
        for bodygroup_name, mesh_file in QuakeC_file.bodygroups.items():
            context.scene.qc_bodygroups_found = True
            cur_bodygroup = bodygroup_names.add()
            cur_bodygroup.bodygroup_name = bodygroup_name
            for i in range(len(mesh_file)):
                newmesh = cur_bodygroup.bodygroup_meshes.add( )
                newmesh.mesh_file = mesh_file[i]     
                newindex = cur_bodygroup.bodygroup_meshes_index
                newindex = i
                    

        if type(QuakeC_file.maxverts) == list:
            context.scene.qc_maxverts = ""
        else:
            context.scene.qc_maxverts = QuakeC_file.maxverts

        context.scene.qc_file_selected = True
        return {'FINISHED'}
        
    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}





class PerimeterQCManagementPanelWriteTexGroups( Operator ):
    bl_idname = "perimeter.qcpanel_write_texgroups"
    bl_label = "Export RPAK"
    bl_description = "Exports the currently selected material to an RPAK"

    def execute( self, context ):

        lines = []
        for material in context.scene.texturegroup_materials:
            lines.append(material.Materials)

        write_texturegroup_materials(lines, "Skinfamilies", context.scene.qc_file_path)
        

        return {'FINISHED'}


class PerimeterQCManagementPanelUpdateQCFile( Operator ):
    bl_idname = "perimeter.qcpanel_test"
    bl_label = "Export RPAK"
    bl_description = "Exports the currently selected material to an RPAK"

    def execute( self, context ):
        selected_index = bpy.context.scene.perimeter_qc_main_collection_index
        selected_item = bpy.context.scene.perimeter_qc_main_collection[selected_index]
        addon_prefs = context.preferences.addons[__package__].preferences


        if selected_item.rpak_shader_is_set:
            if selected_item.export_rpak:
                if addon_prefs.repak_path == "":
                    self.report( {'ERROR'}, "RPAK Export Path not set, set in Preferences" )
                    return {'CANCELLED'}

        return {'FINISHED'}

""" currently commented. not finished."""
def create_mesh_from_lists(name, verts, faces, offset):

    print(verts)

    print(faces)
    mesh = bpy.data.meshes.new(name)

    obj = bpy.data.objects.new(name, mesh)

    collection = bpy.context.scene.collection
    collection.objects.link(obj)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bm = bmesh.new()   
    bm.from_mesh(mesh)  

    verticies_list = []
    for newvert in verts:
        new = bm.verts.new(newvert)
        verticies_list.append(new)
    bm.to_mesh(mesh)
    bm.free()  
    #nl = tuple(faces)
    #for subface in nl:
    #    print(subface)
    #    subface = tuple(subface)
    #    bmface_conv = (verticies_list[subface[0]], verticies_list[subface[1]], verticies_list[subface[2]])
        #bm.faces.new(bmface_conv)
        #bm.faces


    

def create_text_at_verts(vertex_list):
    scene = bpy.context.scene
    
    for i, vertex in enumerate(vertex_list):
        # Create a new text object
        text_data = bpy.data.curves.new(type="FONT", name=f"Text_{i}")
        text_object = bpy.data.objects.new(name=f"Text_{i}", object_data=text_data)
        scene.collection.objects.link(text_object)
        text_object.location = vertex  # Set text object location to the vertex
        text_object.rotation_euler = (0, 0, 0)  # Reset rotation
        
        # Set text content
        text_object.data.body = f"{i}"
        text_object.data.extrude = 0.001  # Set extrude to make the text visible
        text_object.data.size = 0.1  # Set text size

def get_bone_transform_location(armature_obj, bone_name):
    if armature_obj and armature_obj.type == 'ARMATURE':
        armature = armature_obj.data
        bone = armature.bones.get(bone_name)
        if bone:
            bone_matrix_world = armature_obj.matrix_world @ mathutils.Matrix(bone.matrix_local)
            return bone_matrix_world.translation

    return None

# Example usage:


class PerimeterRUIMeshMaker(bpy.types.Operator):
    bl_idname = "northstar.rui_mesh_import"
    bl_label = "Add Material to Texturegroup"

    filepath: bpy.props.StringProperty( subtype="FILE_PATH" )


    def execute(self, context):
        mdl_file_path = bpy.path.abspath( self.filepath )
        
        rui_meshes = get_mdl_rui_meshes(mdl_file_path)
        armature_obj = bpy.context.active_object
        for rui_mesh in rui_meshes:
            #facedata, vert_list, vertmaps

            
            face_data_list = rui_mesh[0]
            vertex_list = rui_mesh[1]
            vertexmap_list = rui_mesh[2]
            name = rui_mesh[3]
            parent = rui_mesh[4][0]
            print(parent)
            
            
            #bone_name = "YourBoneName"
            print(get_bone_transform_location(armature_obj, "def_c_bolt"))
            create_mesh_from_lists(name, vertex_list, vertexmap_list, "def_c_bolt")
            create_text_at_verts(vertex_list)
        return {'FINISHED'}
    
    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}
    