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

bl_info = {
    "name": "Perimeter",
    "author": "EM4V",
    "version": ( 2, 21 ),
    "blender": ( 2, 80, 0),
    "location": "Sidebar > Perimeter",
    "description": "Addon for managing Northstar settings",
    "category": "Scene",
    "wiki_url": "https://github.com/EM4Volts/Perimeter",
    "tracker_url": "https://github.com/EM4Volts/Perimeter/issues"
}



import bpy
from . import addon_updater_ops
from bpy.props import StringProperty, CollectionProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences, UIList
import os, ast, json, subprocess, shutil, math, mathutils
from subprocess import Popen, CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS, run, call
from io_scene_valvesource.export_smd import SmdExporter
from io_scene_valvesource.GUI import SMD_MT_ExportChoice
from .shader import *
from .animationporting import *
from .lib_qc import *
from .rpak import *
from .material_management_panel import *
from .qcparse import *
from .qc_management_panel import *



bpy.types.WindowManager.map_file_location = bpy.props.StringProperty( name="Map File Location", subtype='FILE_PATH' )



def perimeterPrint( text ):
    print( "[Perimeter] " + str(text) )

class MODLIST:
    def __init__( self, tf2_path ):
        self.mods_path = tf2_path + "/r2northstar/mods"

        self.modlist_folders = []
        self.modlist_names = []

        # for each folder in mods_path add to modlist if there is a mod.json file in it
        for folder in os.listdir( self.mods_path ):
            if os.path.isfile( self.mods_path + "/" + folder + "/mod.json" ):
                # load mod.json file and append its name key to modlist_names
                try:
                    with open( self.mods_path + "/" + folder + "/mod.json" ) as json_file:
                        data = json.load( json_file )
                        if "Name" in data:
                            self.modlist_names.append( data["Name"] )
                        if "name" in data:
                            self.modlist_names.append( data["name"] )
                        self.modlist_folders.append( folder )
                except:
                    perimeterPrint( "Error loading mod.json in " + folder )
        #remove duplicates from modlist_names
        self.modlist_names = list( dict.fromkeys( self.modlist_names ) )
        self.modlist_folders = list( dict.fromkeys( self.modlist_folders ) )

        # sort modlist_names alphabetically
        self.modlist_names.sort()

# Operator to launch the specified .exe
class NSLauncherOperator( Operator ):
    bl_idname = "northstar.launch"
    bl_label = "Launch Northstar"
    bl_description = "Launch Northstar"

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        launch_exe = addon_prefs.ns_launch_exe + "/northstarlauncher.exe"

        perimeterPrint( "Launching Northstar..." )


        proc = Popen( [launch_exe, addon_prefs.launch_args], creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS )
        return {'FINISHED'}

# Operator to select a folder and set the ns_launch_exe variable
class NSFolderSelectorOperator( Operator ):
    bl_idname = "northstar.folder_selector"
    bl_label = "Select Titanfall 2 Folder"
    bl_description = "Select Titanfall 2 Folder"

    filepath: bpy.props.StringProperty( subtype="DIR_PATH" )

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        addon_prefs.ns_launch_exe = bpy.path.abspath( self.filepath )
        return {'FINISHED'}

    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}

# Operator to refresh the mod list
class NSRefreshModlistOperator( Operator ):
    bl_idname = "northstar.refresh_modlist"
    bl_label = "Refresh Modlist"
    bl_description = "Refresh Modlist"

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        modlist = MODLIST( addon_prefs.ns_launch_exe )

        # Clear the current mod items
        bpy.context.scene.northstar_items.clear()

        # Load enabled mods from enabledmods.json
        enabled_mods = {}
        try:
            enabled_mods_file = os.path.join( addon_prefs.ns_launch_exe, "r2northstar", "enabledmods.json" )
            with open( enabled_mods_file ) as json_file:
                enabled_mods = json.load( json_file )
        except:
            perimeterPrint( "Error loading enabledmods.json" )

        # Populate the mod items from the modlist
        for mod_name in modlist.modlist_names:
            item = bpy.context.scene.northstar_items.add()
            item.name = mod_name
            if mod_name in enabled_mods:
                item.enabled = enabled_mods.get( mod_name, False )

        return {'FINISHED'}

# Operator for "Export Model" button
class NSExportModelOperator( Operator ):
    bl_idname = "northstar.export_model"
    bl_label = "Export Model"
    bl_description = "Export Model"
    def execute( self, context ):
        # Code to export the model

        perimeterPrint( "Exporting model..." )

        return {'FINISHED'}

    def invoke( self, context, event ):
        context.scene.has_exported = True
        bpy.ops.wm.call_menu(name="SMD_MT_ExportChoice")
        return {'FINISHED'}


# Operator for "Disable Selected" button
class NSDisableSelectedOperator( Operator ):
    bl_idname = "northstar.disable_selected"
    bl_label = "Disable Selected"
    bl_description = "Disable Selected Mod"
    def execute( self, context ):
        selected_index = bpy.context.scene.northstar_items_index
        selected_item = bpy.context.scene.northstar_items[selected_index]
        perimeterPrint( "Disabling mod: " + selected_item.name )

        addon_prefs = context.preferences.addons[__name__].preferences
        enabled_mods_file = os.path.join( addon_prefs.ns_launch_exe, "r2northstar", "enabledmods.json" )

        # Read the enabled mods from the JSON file
        enabled_mods = {}
        if os.path.exists( enabled_mods_file ):
            with open( enabled_mods_file, "r" ) as f:
                enabled_mods = json.load( f )

        # Disable the selected mod by setting its value to False
        enabled_mods[selected_item.name] = False

        # Update the enabledmods.json file
        with open( enabled_mods_file, "w" ) as f:
            json.dump( enabled_mods, f, indent=4 )

        # Refresh the mod list to reflect the changes
        bpy.ops.northstar.refresh_modlist()

        return {'FINISHED'}

# Operator for "Enable Selected" button
class NSEnableSelectedOperator( Operator ):
    bl_idname = "northstar.enable_selected"
    bl_label = "Enable Selected"
    bl_description = "Enable Selected Mod"
    def execute( self, context ):
        selected_index = bpy.context.scene.northstar_items_index
        selected_item = bpy.context.scene.northstar_items[selected_index]
        perimeterPrint( "Enabling mod: " + selected_item.name )

        addon_prefs = context.preferences.addons[__name__].preferences
        enabled_mods_file = os.path.join( addon_prefs.ns_launch_exe, "r2northstar", "enabledmods.json" )

        # Read the enabled mods from the JSON file
        enabled_mods = {}
        if os.path.exists( enabled_mods_file ):
            with open( enabled_mods_file, "r" ) as f:
                enabled_mods = json.load( f )

        # Enable the selected mod by setting its value to True
        enabled_mods[selected_item.name] = True

        # Update the enabledmods.json file
        with open( enabled_mods_file, "w" ) as f:
            json.dump( enabled_mods, f, indent=4 )

        # Refresh the mod list to reflect the changes
        bpy.ops.northstar.refresh_modlist()

        return {'FINISHED'}

# Operator for refreshing the launch args
class NSRefreshLaunchArgsOperator( Operator ):
    bl_idname = "northstar.refresh_launch_args"
    bl_label = "Refresh Launch Args"
    bl_description = "Refresh Launch Args"
    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences

        # Load the contents of ns_startup_args.txt into launch_args
        ns_startup_args_file = os.path.join( addon_prefs.ns_launch_exe, "ns_startup_args.txt" )
        if os.path.exists( ns_startup_args_file ):
            with open( ns_startup_args_file, "r" ) as f:
                addon_prefs.launch_args = f.read().strip()

        return {'FINISHED'}

# Operator for updating the launch args
class NSUpdateLaunchArgsOperator( Operator ):
    bl_idname = "northstar.update_launch_args"
    bl_label = "Update Launch Args"
    bl_description = "Update Launch Args in ns_startup_args.txt"
    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences

        # Write the contents of launch_args into ns_startup_args.txt
        ns_startup_args_file = os.path.join( addon_prefs.ns_launch_exe, "ns_startup_args.txt" )
        with open( ns_startup_args_file, "w" ) as f:
            f.write( addon_prefs.launch_args )

        return {'FINISHED'}

# Operator for "Compare Animation Files" button
class NSCompareAnimationFilesOperator( Operator ):
    bl_idname = "northstar.compare_animation_files"
    bl_label = "Compare Animation Files"
    bl_description = "Compare Animation Files"
    def execute( self, context ):
        # Code to compare animation files
        perimeterPrint( "Comparing animation files..." )
        return {'FINISHED'}


class NSAnimationPortingStageOneOperator( bpy.types.Operator ):
    bl_idname = "northstar.animation_porting_stage_one"
    bl_label = "Animation Porting Stage One"
    bl_description = "Export animation lengths"

    filepath: bpy.props.StringProperty( subtype="DIR_PATH" )

    def execute( self, context ):
        folder_path = bpy.path.abspath( self.filepath )
        export_animation_lengths( folder_path )
        return {'FINISHED'}

    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}

# Operator for "Animation Porting Stage Two" button
class NSAnimationPortingStageTwoOperator( Operator ):
    bl_idname = "northstar.animation_porting_stage_two"
    bl_label = "Animation Porting Stage Two"

    filepath: bpy.props.StringProperty( subtype="DIR_PATH" )

    def execute( self, context ):
        # Code for animation porting stage two
        folder_path = bpy.path.abspath( self.filepath )
        import_animation_lengths( folder_path )
        perimeterPrint( "Performing animation porting stage two..." )
        return {'FINISHED'}

    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}

# Operator for "All in One > Test" button
class NSAppendShadersToMeshesOperator( Operator ):
    bl_idname = "northstar.append_shaders"
    bl_label = "Append Shader"
    bl_description = "Appends the TF2 Shader to each Material in the selected Mesh"

    def execute( self, context ):


        # Get the active object
        obj = bpy.context.active_object

        path = bpy.context.preferences.addons[__name__].preferences.texture_path

        #check if both paths are empty, if so do not proceed and print error
        if bpy.context.preferences.addons[__name__].preferences.texture_path == "":
            perimeterPrint( "No Texture Path Selected!" )
            return {'FINISHED'}
        else:
            #check if diffuse only is enabled, if so only use the diffuse texture
            if bpy.context.preferences.addons[__name__].preferences.diffuse_only == True:
                perimeterPrint( "Diffuse Only Enabled! Using only the diffuse texture." )
                setup_diffuse_shader( obj, path )
            else:
                perimeterPrint( "Diffuse Only Disabled! Using all textures." )
                setup_shader( obj, path , True, False)
        return {'FINISHED'}

# UIList item
class NSListItem( bpy.types.PropertyGroup ):
    name: bpy.props.StringProperty()
    enabled: bpy.props.BoolProperty( default=True )

# UIList
class NS_UL_List( UIList ):
    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        split = layout.split( factor=0.3 )
        split.label( text=item.name, icon="SEQUENCE_COLOR_05" if item.enabled else "SEQUENCE_COLOR_01" )

class QCFileSelectorOperator( bpy.types.Operator ):
    bl_idname = "object.qc_file_selector"
    bl_label = "Select QC File"

    filepath: bpy.props.StringProperty( subtype="FILE_PATH" )

    def execute( self, context ):
        addon_props = context.scene.my_addon_properties
        addon_props.qc_file_path = self.filepath
        return {'FINISHED'}

\
"""
# Panel for the Perimeter tab
class NSManagerPanel( Panel ):
    bl_idname = "SIDEBAR_PT_ns_manager"
    bl_label = "Perimeter"
    bl_category = "Northstar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    def draw( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences

        if addon_prefs.perimeter_panel_enabled:
            layout = self.layout

            # Launch button
            row = layout.row()
            row.operator( "northstar.launch", text="Launch Northstar", icon="PLAY" )
            row.scale_y = 2.0

            # Launch Args
            row = layout.row( align=True )
            row.prop( addon_prefs, "launch_args", text="Launch Args", icon="OPTIONS" )
            refresh_launch_args_operator = row.operator( "northstar.refresh_launch_args", text="", icon="FILE_REFRESH" )

            # Update Launch Args button
            row = layout.row()
            row.operator( "northstar.update_launch_args", text="Update Launch Args", icon="FILE_TICK" )

            # Folder selection
            row = layout.row()
            col = row.column( align=True )
            col.label( text="Titanfall 2 Folder:" )
            col.prop( addon_prefs, "ns_launch_exe", text="" )

            # Refresh modlist button
            row = layout.row( align=True )
            row.operator( "northstar.refresh_modlist", text="Refresh Modlist", icon="FILE_REFRESH" )
            row.scale_x = 0.3

            # UIList
            row = layout.row()
            row.template_list( "NS_UL_List", "", bpy.context.scene, "northstar_items", bpy.context.scene, "northstar_items_index" )

            # Disable Selected button
            row = layout.row()
            row.operator( "northstar.disable_selected", text="Disable Selected", icon="CANCEL" ),

            # Enable Selected button
            row.operator( "northstar.enable_selected", text="Enable Selected", icon="CHECKMARK" )

            # Isle for buttons and input field
            box = layout.box()

            # Compiled mod name input field


            # Version label
            version = str( bl_info["version"][0] ) + "." + str( bl_info["version"][1] )
            new_col = box.column( align=True )
            new_col.label( text="Perimeter v" + version, icon="INFO" )
        else:
            layout = self.layout
            row = layout.row()
            layout.label( text="Perimeter Panel Disabled, enable in settings!", icon="CANCEL" )

"""

def refresh_rpak_export_list( self, context):

    blacklisted_materials = ["Material", "Dots Stroke"]
    bpy.context.scene.northstar_rpak_materials.clear()
    rpak_materials_dict = return_mesh_maps( context )
    for material in bpy.data.materials:
        if not material.name in blacklisted_materials:
            if material.name in rpak_materials_dict:
                item = bpy.context.scene.northstar_rpak_materials.add()
                item.name = material.name
                item.original_material_name = material.name
                item.do_export = True
                context.scene.northstar_rpak_materials_enabled = True


# Panel for the MDLutils tab
class NSMDLUtilsPanel( Panel ):
    bl_idname = "SIDEBAR_PT_ns_mdl_utils"
    bl_label = "Load Game Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Northstar"



    def draw( self, context ):

        addon_prefs = context.preferences.addons[__name__].preferences

        layout = self.layout



        #ANIMATIONS TAB
        #ANIMATIONS TAB
        #ANIMATIONS TAB
        """
        box = layout.box()
        # Compare Animation Files button
        row = box.column()
        row.label( text="Animations", icon="ANIM_DATA" )


        # Animation Porting Stage One button
        row = box.row()
        row.operator( "northstar.animation_porting_stage_one", text="Animation Porting Stage One", icon="IPO_SINE" )

        # Animation Porting Stage Two button
        row.operator( "northstar.animation_porting_stage_two", text="Animation Porting Stage Two", icon="IPO_QUAD" )
        """
        #SHADERS TAB
        #SHADERS TAB
        #SHADERS TAB


        shader_box = layout.box()
        row = shader_box.column()
        row.label( text="Setup Shaders From Folder", icon="OUTLINER_OB_IMAGE" )
        row.separator( factor=3.5 )
        row.operator( "northstar.append_shaders", text="Setup Material Shader for Mesh", icon="SHADING_TEXTURE" )
        row.label( text="Materials Folder Path:" )
        row.prop( addon_prefs, "texture_path", text="" )
        row.prop( addon_prefs, "diffuse_only", text="Diffuse Only ( More Performant with less detail, speeds up viewport )" )









def create_attachment(attachment_list):
    # Get the active armature
    armature = bpy.context.active_object
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch to Object mode
    
    # Loop through the input list
    for attachment_data in attachment_list:
        attachment_name, parent_bone, offset_x, offset_y, offset_z, rot_x, rot_y, rot_z = attachment_data
        
        # Create cone mesh
        bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=3.1, radius2=0, depth=7.3, location=(0, 0, 0))
        attachment = bpy.context.object
        attachment.name = attachment_name.strip('"')  # Set attachment name
        
        # Get the parent bone
        bone = armature.data.bones.get(parent_bone.strip('"'))
        if bone:
            # Set attachment location based on the offset
            attachment.location = (float(offset_x), float(offset_y), float(offset_z))
            
            # Calculate cone direction based on Euler angles
            direction = math.sqrt(math.pow(math.cos(math.radians(float(rot_x))), 2) + math.pow(math.cos(math.radians(float(rot_y))), 2))
            
            # Set cone rotation based on Euler angles
            attachment.rotation_euler = (math.radians(float(rot_z)), 0, math.atan2(math.cos(math.radians(float(rot_x))), math.cos(math.radians(float(rot_y)))))
            
            # Parent the attachment to the bone
            attachment.parent = armature
            attachment.parent_type = 'BONE'
            attachment.parent_bone = parent_bone.strip('"')
            
            # Set the armature as the active object
            bpy.context.view_layer.objects.active = armature
            
            # Deselect all objects and select the attachment
            bpy.ops.object.select_all(action='DESELECT')
            attachment.select_set(True)
            bpy.context.view_layer.objects.active = attachment
            
            # Switch to Object mode and update the attachment
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)



class NSQCSkeletonOperator( Operator ):
    bl_idname = "northstar.qc_skeleton_parser"
    bl_label = "QC Skeleton Parser"
    bl_description = "Parse QC Skeleton"

    filepath: bpy.props.StringProperty( subtype="FILE_PATH" )


    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        qc_file_path = bpy.path.abspath( self.filepath )
        qc_file_name = get_model_name( qc_file_path )


        qc_file_init = QC( qc_file_path )
        input_list = []
        for attachement in qc_file_init.attachements:
            current_attachement = [ attachement.attachement_name, attachement.parent_bone, attachement.offset_x, attachement.offset_y, attachement.offset_z, attachement.rotate_x, attachement.rotate_y, attachement.rotate_z ]
            input_list.append(current_attachement)

        create_attachment(input_list)
        #save the qc file path to the addon prefs
        context.scene.qc_file_path = qc_file_path


        return {'FINISHED'}

    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}



# Sample dictionary

class NSQCBodygroupOperator( Operator ):
    bl_idname = "ns.qc_bodygroup"
    bl_label = "QC Bodygroup"

    item_name: bpy.props.StringProperty()
    dict_list_string: bpy.props.StringProperty()
    visible: bpy.props.BoolProperty()

    def execute( self, context ):
        entries = []
        dict_list_string = self.dict_list_string.replace( "'", '"' )
        current_dict_string = self.dict_list_string.strip( '][' ).split( ', ' )
        for i in current_dict_string:
            i = i.replace( "'", '' )
            i = i.replace( '"', '' )
            entries.append( i )

        if self.visible:
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH' and obj.name in entries:
                    obj.hide_set( True )

            self.visible = False
        else:
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH' and obj.name in entries:
                    obj.hide_set( False )
            self.visible = True

        return {'FINISHED'}


# UIList
class NSQC_UL_MaterialList( UIList ):

    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        row = layout.row()
        row.label( text=item.name, icon="MATSPHERE" )
        row.label( text=item.override_material_path, icon="SHADING_TEXTURE" )
        row = layout.row()

class NSQCMaterilListRefreshOperator( Operator ):
    bl_idname = "ns.qc_material_list_refresh"
    bl_label = "Refresh Material List"
    bl_description = "Refresh Material List"

    def execute( self, context ):

        blacklisted_materials = ["Material", "Dots Stroke"]
        bpy.context.scene.northstar_materials.clear()
        for material in bpy.data.materials:
            if not material.name in blacklisted_materials:
                item = bpy.context.scene.northstar_materials.add()
                item.name = material.name
                item.enabled = True
        return {'FINISHED'}

class NSMaterialNamePopup( Operator ):
    bl_idname = "ns.material_name_popup"
    bl_label = "Set Override"
    bl_description = "Refresh Material List"

    text_input: StringProperty( name="Material Path ( Full Path )" )

    def execute( self, context ):
        selected_index = bpy.context.scene.northstar_materials_index
        selected_item = bpy.context.scene.northstar_materials[selected_index]
        text = self.text_input
        selected_item.override = text
        return {'FINISHED'}

    def invoke( self, context, event ):
        return context.window_manager.invoke_props_dialog( self )

# Operator for "All in One > Test" button
class NSAllInOneTestOperator( Operator ):
    bl_idname = "northstar.all_in_one_test"
    bl_label = "All in One"
    bl_description = "Compiles the selected QC File with settings, then builds RPAKS if enabled"

    def execute( self, context ):
        perimeterPrint( "All in One Test..." )
        #export model
        #compile model
        #convert model
        #make testmod
        #launch testmod
        #return {'FINISHED'}
        addon_prefs = context.preferences.addons[__name__].preferences
        if not context.scene.qc_file_path.endswith( ".qc" ):
            self.report( {'ERROR'}, "No QC File Selected!" )
        else:
            #export model
            perimeterPrint( "Exporting model..." )

            qc_file_path = bpy.path.abspath( context.scene.qc_file_path )


            #save_material_override( qc_file_path, perimeter_return_materialoverrides( context ) )

            compile_model( context )
            convert_model( context )



 
            mod_path = make_testmod( self, context )

            if not context.scene.northstar_rpak_materials_enabled:
                perimeterPrint( "RPAK Materials Disabled, not exporting RPAKs!" )

            else:

                perimeterPrint( "Exporting RPAKs..." )
                #if paks folder does not exist, create it
                if not os.path.exists( os.path.join( mod_path, "paks" ) ):
                    os.mkdir( os.path.join( mod_path, "paks" ) )


                old_export_path = bpy.context.scene.perimeter_rpak_export_path

                bpy.context.scene.perimeter_rpak_export_path = os.path.join( mod_path, "paks" )

                perimeter_make_refactor_rpak( context, "all_mats" )


                bpy.context.scene.perimeter_rpak_export_path = old_export_path

                rpak_json_dict = {"Postload": {}}
                for file in os.listdir( os.path.join( mod_path, "paks" ) ):
                    if file.endswith( "pak" ):
                        if not file.endswith( "starpak" ):
                            rpak_json_dict["Postload"][file] = "common.rpak"
                with open( os.path.join( mod_path, "paks", "rpak.json" ), 'w' ) as f:
                    json.dump( rpak_json_dict, f, indent=4 )


            launch_exe = addon_prefs.ns_launch_exe + "/northstarlauncher.exe"

            perimeterPrint( "Launching Northstar..." )

            proc = Popen( [launch_exe, addon_prefs.launch_args], creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS )


        return {'FINISHED'}


def compile_model( context ):

    #exectue studiomdl.exe with subprocess
    addon_prefs = context.preferences.addons[__name__].preferences
    
    qc_file_path = bpy.path.abspath( context.scene.qc_file_path )
    qc_file_name = get_model_name( qc_file_path )
    perimeterPrint( qc_file_path )
    renamemateriallines = []
    write_material_override = False
    for material in context.scene.perimeter_material_main_collection:
        if material.material_override_enabled:
            renameline = '$renamematerial "' + material.blender_material.name + '" "' + material.material_override_path + '"' 
            renamemateriallines.append( renameline )
            write_material_override = True

    if write_material_override:
        save_material_override( qc_file_path, renamemateriallines)

    if context.scene.perimeter_empty_cdmaterials:
        print("pr_")
        remove_cdmaterials( qc_file_path )

    if context.scene.perimeter_overwrite_maxverts:
        change_maxverts( qc_file_path )


    stripped_gameinfo_path = os.path.dirname(addon_prefs.gameinfo_path)
    stuidmdlpath_complete = addon_prefs.mdlstudio_path
    gameinfopaath_complete = '"' + stripped_gameinfo_path + '\\"'
    qc_file_path = '"' + qc_file_path + '"'
    studiomdl_args = f"-game {gameinfopaath_complete} -nop4 -verbose"
    perimeterPrint( f" Compiling with command {stuidmdlpath_complete} {studiomdl_args} {qc_file_path}, please wait...")

    studiomdlcommand = f"{stuidmdlpath_complete} {studiomdl_args} {repr(qc_file_path)}"
    qc_path = os.path.dirname( qc_file_path )
    cmd = f'"{stuidmdlpath_complete}" {studiomdl_args} {qc_file_path}'.replace( "\\", "/")
    
    compiler = run( cmd, shell=True, capture_output=True)
    mdlshit_line = ""
    for line in compiler.stdout.decode( "utf-8" ).split( "\n" ):
        #strip line of whitespaces
        print(line)
        line = line.strip()
        if line.startswith( "writing" ):
            if line.endswith( ".mdl:" ):
                line= line.replace( "writing ", "" )[:-1]
                mdlshit_line = line.replace( "\\" , "/" )
    if mdlshit_line != "":
        context.scene.mdlshit_mdl = mdlshit_line
        return mdlshit_line
    
    context.scene.has_exported = False


# Operator for "Compile Model" button
class NSCompileModelOperator( Operator ):
    bl_idname = "northstar.compile_model"
    bl_label = "Compile Model"
    bl_description = "Compile Model"
    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        if not context.scene.qc_file_path.endswith( ".qc" ):
            print(context.scene.qc_file_path)
            self.report( {'ERROR'}, "No QC File Selected!" )
        else:

            compiled = compile_model( context )
            if compiled.endswith( ".mdl" ):
                self.report( {'INFO'}, "Compiled Model: " + compiled )
        return {'FINISHED'}


def convert_model( context ):

    mdl_extensions = [".mdl", ".phy", ".vvd", ".vtx"]
    addon_prefs = context.preferences.addons[__name__].preferences
    if context.scene.mdlshit_mdl == "":
        perimeterPrint( "Converting Model failed, no precompiled model in scene!" )
    else:

        mdl_name = os.path.basename( context.scene.mdlshit_mdl )


        mdlshit_mdl_path = os.path.dirname( context.scene.mdlshit_mdl )

        for file in os.listdir( mdlshit_mdl_path ):
            for ext in mdl_extensions:
                if file.endswith( ext ):
                    #see if filename matches mdl_name without extension
                    if os.path.splitext( file )[0] == os.path.splitext( mdl_name )[0]:
                        perimeterPrint( "Found matching file: " + file )
                        #copy matching file to export path
                    else:
                        if not file.endswith( ".mdl" ):
                            #rename file to match mdl_name without extension
                            os.replace( os.path.join( mdlshit_mdl_path, file ), os.path.join( mdlshit_mdl_path, os.path.splitext( mdl_name )[0] + ext ) )
                    mdl_extensions.remove( ext )
            #check for missing extensions
        for ext in mdl_extensions:
            #make empty file with extension
            open( os.path.join( mdlshit_mdl_path, os.path.splitext( mdl_name )[0] + ext ), 'a' ).close()


        mdlshit_path = addon_prefs.mdlshit_path
        perimeterPrint( f"Converting Model with command {mdlshit_path} --noui {context.scene.mdlshit_mdl}, please wait...")
        cmd = f'"{mdlshit_path}" --noui "{context.scene.mdlshit_mdl}"'.replace( "\\", "/")
        compiler = run( cmd, shell=True)

        conv_mdl_path = os.path.join( mdlshit_mdl_path, os.path.splitext( mdl_name )[0] + "_conv.mdl" )
        perimeterPrint( "Converted Model: " + conv_mdl_path)

        return conv_mdl_path



def make_testmod( self, context ):

    #makes a testmod, formated as a basic n* mod for testing purposes, not intended for redist
    #steps:
    #check if valid Titanfall 2 folder is selected and exists
    #make a mod folder in titanfall2 folder /r2northstar/mods/ called "perimeter.<compiled mod name>"
    #make a json file in the mod folder called "mod.json"

    addon_prefs = context.preferences.addons[__name__].preferences
    if not os.path.exists( addon_prefs.ns_launch_exe ):
        perimeterPrint( addon_prefs.ns_launch_exe)
        self.report( {'ERROR'}, "No Titanfall 2 Folder Selected!" )
    else:
        #make mod folder
        #check if mod folder exists, if so delete it
        if os.path.exists( os.path.join( addon_prefs.ns_launch_exe, "r2northstar", "mods", "perimeter." + context.scene.compiled_mod_name ) ):
            shutil.rmtree( os.path.join( addon_prefs.ns_launch_exe, "r2northstar", "mods", "perimeter." + context.scene.compiled_mod_name ) )
        mod_folder = os.path.join( addon_prefs.ns_launch_exe, "r2northstar", "mods", "perimeter." + context.scene.compiled_mod_name )
        os.makedirs( mod_folder )
        #make mod.json
        mod_json = os.path.join( mod_folder, "mod.json" )
        mod_json_dict = {"Name": context.scene.compiled_mod_name, "description": context.scene.compiled_mod_description, "Version": context.scene.compiled_mod_version, "LoadPriority": context.scene.compiled_mod_priority}
        with open( mod_json, 'w' ) as f:
            json.dump( mod_json_dict, f, indent=4 )
        #make models folder in mod folder
        os.makedirs( os.path.join( mod_folder, "mod", "models" ) )
        #copy compiled model to mod folder

        #strip context.scene.mdlshit_mdl from the model_name scene property
        model_name = os.path.dirname( context.scene.mdlshit_mdl )
        gameinfo_path = len(os.path.dirname(addon_prefs.gameinfo_path))
        #remove the gameinfo path from the model_name
        model_folder = model_name[gameinfo_path:].replace( "\\", "/" )

        #make the model folder in the mod folder
        os.makedirs( os.path.join( mod_folder + "/mod/" + model_folder ), exist_ok=True )
        perimeterPrint( model_name )

        

        #copy the model to the mod folder and then remove the _conv
        folder_from = os.path.dirname( context.scene.mdlshit_mdl ) + "/" + os.path.basename( context.scene.mdlshit_mdl[:-4] + "_conv.mdl" )
        folder_to = os.path.join( mod_folder + "/mod/" + model_folder )
        perimeterPrint( folder_from )
        perimeterPrint( folder_to )

        shutil.copy( folder_from, folder_to )
        #rename the model to remove the _conv
        os.replace( os.path.join( folder_to, os.path.basename( context.scene.mdlshit_mdl[:-4] + "_conv.mdl" ) ), os.path.join( folder_to, os.path.basename( context.scene.mdlshit_mdl[:-4] + ".mdl" ) ) )

        return mod_folder

# Operator for "Convert Model" button
class NSConvertModelOperator( Operator ):
    bl_idname = "northstar.convert_model"
    bl_label = "Convert Model"
    bl_description = "Convert Model"
    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        if not context.scene.mdlshit_mdl.endswith( ".mdl" ):
            self.report( {'ERROR'}, "No precompiled model in scene!" )
        else:

            conv_mdl = convert_model( context )

            if os.path.isfile( conv_mdl ):
                self.report( {'INFO'}, "Converted Model: " + conv_mdl )


        return {'FINISHED'}




class NSQCFilePanel( bpy.types.Panel ):
    bl_idname = "SIDEBAR_PT_ns_qc_file"
    bl_label = "Mod Compiler"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Northstar"

    def draw( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        row = self.layout.column()
        #row.label( text="QC File Info", icon="FILE" )
        layout = self.layout
        row = layout.column()
        row.label( text="PRE-Compilation steps", icon="PRESET" )


        row = layout.row()
        compile_box = layout.box()
        row = compile_box.row()



        row.operator( "perimeter.qc_parser", text="Select QC File", icon="FILE_FOLDER" )
        row = compile_box.row()


        row.label( text="Mod Packer", icon="PLUGIN" )
        row = compile_box.column()
        row.prop( context.scene, "compiled_mod_name", text="Mod Name" )
        row.prop( context.scene, "compiled_mod_description", text="Description")
        row.prop( context.scene, "compiled_mod_version", text="Version")
        row.prop( context.scene, "compiled_mod_priority", text="Priority")



        # All in One Test button
        row.label( text="PRE-Compilation steps", icon="PRESET" )

        row = compile_box.row()
        
        row.prop( context.scene, "perimeter_empty_cdmaterials", text="Overwriting CDMATERIALS" if context.scene.perimeter_empty_cdmaterials else "Not Overwriting CDMATERIALS", icon="CHECKMARK" if context.scene.perimeter_empty_cdmaterials else "CANCEL", expand = True)

        row.prop( context.scene, "northstar_rpak_materials_enabled", text="Include RPAKs in Mod" if context.scene.northstar_rpak_materials_enabled else "RPAKs not Exporting into Mod", icon="CHECKMARK" if context.scene.northstar_rpak_materials_enabled else "CANCEL", expand = True)
        
        row.prop( context.scene, "perimeter_overwrite_maxverts", text="Overwrite MAXVERTS" if context.scene.perimeter_overwrite_maxverts else "Not Overwriting MAXVERTS", icon="CHECKMARK" if context.scene.perimeter_overwrite_maxverts else "CANCEL", expand = True)

        row = compile_box.column()
        if context.scene.qc_file_selected:
            row.enabled = True
            row.label( text="The big Button", icon="SNAP_FACE_CENTER")

        else:
            row.label( text="NO QC FILE SELECTED!", icon="ERROR")
            row.enabled = False
            

        row.operator( "northstar.all_in_one_test", text="Compile Mod", icon="PLAY" )
        row.scale_y = 2.0
        row = compile_box.column()
        version = str( bl_info["version"][0] ) + "." + str( bl_info["version"][1] )
        row.label( text="Perimeter v" + version, icon="INFO" )




class NSGameFolderOperator( Operator ):
    bl_idname = "northstar.game_folder"
    bl_label = "Select Studiomdl Game Folder"
    bl_description = "Select Studiomdl Game"

    filepath: bpy.props.StringProperty( subtype="DIR_PATH" )

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        addon_prefs.game_path = bpy.path.abspath( self.filepath )
        #check for which game is selected, then set the game path
        #for each game make sum path shit, use later on as pref vars

        if addon_prefs.game_path.endswith("Portal 2\\"):
            addon_prefs.gameinfo_path = addon_prefs.game_path +  "portal2/gameinfo.txt"
            addon_prefs.mdlstudio_path = addon_prefs.game_path +  "portal2/bin/studiomdl.exe"
        elif addon_prefs.game_path.endswith("SourceFilmmaker\\"):
            addon_prefs.gameinfo_path = addon_prefs.game_path +  "game\\usermod\\gameinfo.txt"
            addon_prefs.mdlstudio_path = addon_prefs.game_path +  "game\\bin\\studiomdl.exe"
        elif addon_prefs.game_path.endswith("Alien Swarm\\"):
            addon_prefs.gameinfo_path = addon_prefs.game_path + "/swarm/gameinfo.txt"
            addon_prefs.mdlstudio_path = addon_prefs.game_path +  "bin/studiomdl.exe"

        perimeterPrint(f"studiomdl set to {addon_prefs.mdlstudio_path} | gameinfo set to {addon_prefs.gameinfo_path}")
        return {"INTERFACE"}
    def invoke( self, context, event ):
        context.window_manager.fileselect_add( self )
        return {'RUNNING_MODAL'}


class NSPreferencesStudiomdlSetup( Operator ):
    bl_idname = "ns.studiomdlsetup"
    bl_label = "Setup Compiler"
    bl_description = "Setup Compiler"


    selected_game: bpy.props.EnumProperty(
    name="Game for Studiomdl",
        items=[
            ('portal2', 'Portal 2', '', 'SELECT_SUBTRACT', 0),
            ('sfm', 'Source Film Maker', '', 'RENDER_ANIMATION', 1),
            ('alienswarm', 'Alien Swarm', '', 'GHOST_DISABLED', 2),
        ],
    default='portal2',
    )

    game_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Game Path"
    )

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        addon_prefs.selected_game = self.selected_game
        return {'FINISHED'}

    def invoke( self, context, event ):

        return context.window_manager.invoke_props_dialog( self )

    def draw( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        row = self.layout.column()
        row.label( text="Select Studiomdl Game Folder")
        row.label( text="Either: ")
        #Portal 2, Alien Swarm or Source Film Maker
        row.label( text="Portal 2")
        row.label( text="Alien Swarm")
        row.label( text="Source Film Maker")
        row.operator("northstar.game_folder", icon="FILE_FOLDER")



# Addon Preferenc
class NSAddonPreferences( AddonPreferences ):
    bl_idname = __name__

    auto_check_update : bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

    updater_interval_months : bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

    updater_interval_days : bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

    updater_interval_hours :bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

    updater_interval_minutes : bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)
    
    ns_launch_exe: StringProperty(
        name="Titanfall 2 Folder",
        default="No Folder Selected!",
        subtype='DIR_PATH'
     )

    launch_args: StringProperty(
        name="Launch Args",
        default="",
        description="Arguments to pass when launching Northstar"
     )

    texture_path: StringProperty(
        name="Texture Path",
        subtype='DIR_PATH'
     )

    diffuse_only: bpy.props.BoolProperty(
        name="Only use diffuse textures for shaders",
        description="Only uses a basic diffuse texture for shaders, instead of the full set of textures",
        default=False
     )
    perimeter_panel_enabled: bpy.props.BoolProperty(
        name="Perimeter Panel",
        description="Enable the Perimeter panel",
        default=True
    )
    selected_game: bpy.props.EnumProperty(
    name="Game for Studiomdl",
        items=[
            ('portal2', 'Portal 2', '', '', 0),
            ('sfm', 'Source Film Maker', '', '', 1),
            ('alienswarm', 'Alien Swarm', '', '', 2),
        ],
    default='sfm',
    )
    game_path: bpy.props.StringProperty(
        name="Game Path (Automatically set if SETUP used)",
        description="Path to the game folder",
        default="",
        subtype='DIR_PATH'
    )
    gameinfo_path: StringProperty(
        name="Gameinfo.txt Path (Automatically set if SETUP used)",
        description=f"Path to gameinfo.txt, see {bl_info['wiki_url']} for more info",
        default="",
        subtype='FILE_PATH'
    )
    mdlstudio_path: StringProperty(
        name="MDLStudio Path (Automatically set if SETUP used)",
        description=f"Path to MDLStudio, see {bl_info['wiki_url']} for more info",
        default="",
        subtype='FILE_PATH'
    )
    mdlshit_path: StringProperty(
        name="MDLSHIT Path",
        description=f"Path to MDLShit, see {bl_info['wiki_url']} for more info",
        default="",
        subtype='FILE_PATH'
    )
    repak_path: StringProperty(
        name="Repak Path",
        description=f"Path to Repak, see {bl_info['wiki_url']} for more info",
        default="",
        subtype='FILE_PATH'
    )
    texconv_path: StringProperty(
        name="Texconv Path",
        description=f"Path to Texconv, see {bl_info['wiki_url']} for more info",
        default="",
        subtype='FILE_PATH'
    )
    testmod_make_rpak: bpy.props.BoolProperty(
        name="Make RPak",
        description="Make RPak when making testmod",
        default=True
    )



    selected_materials: bpy.props.CollectionProperty( type=bpy.types.PropertyGroup )
    def draw( self, context ):
        addon_updater_ops.check_for_update_background()
        layout = self.layout
        layout.label( text="Perimeter Settings")
        layout.prop( self, "ns_launch_exe" )
        layout.prop( self, "texture_path" )

        #make box
        row = layout.box()
        row.operator( "ns.studiomdlsetup", text="Setup Studiomdl", icon="FILE_REFRESH", depress=True)
        row.prop( self, "game_path" )
        row.prop( self, "gameinfo_path" )
        row.prop( self, "mdlstudio_path" )
        row.label( text="")
        row.prop( self, "mdlshit_path" )
        row.prop( self, "repak_path" )
        row.prop( self, "texconv_path" )
        row.label( text="" )
        #check if io_scene_valvesource is installed, if not, display error
        if "io_scene_valvesource" in bpy.context.preferences.addons:
            row.label( text="Blender Source Tools is installed!", icon="CHECKMARK" )
        else:
            row.label( text="Blender Source Tools is not installed!", icon="CANCEL" )
        row = layout.row()
        row.label( text="For help see the wiki", icon="URL" )
        row.operator( "wm.url_open", text="Github/Wiki", icon="URL" ).url = bl_info["wiki_url"]
        addon_updater_ops.update_settings_ui(self,context)
        addon_updater_ops.update_notice_box_ui(self, context)



classes = ( # classes for the register and unregister functions

    NSAddonPreferences, # Addon Preferences
    NSPreferencesStudiomdlSetup, # preferences setup for studiomdl

    #NSManagerPanel, # Perimeter tab
    PerimeterMaterialManagementPanel, # Material Management tab
    NSMDLUtilsPanel, # MDLutils tab
    PerimeterQCManagementPanel,
    PerimeterQCBodygroupManager,
    NSQCFilePanel, # QC File tab

    NSGameFolderOperator,  # Game Folder Selector for Studiomdl
    NSLauncherOperator, # Launch button bl_idname: northstar.launcher
    NSFolderSelectorOperator, # Titanfall 2 Folder selection bl_idname: northstar.folder_selector
    NSRefreshModlistOperator, # Refresh modlist button bl_idname: northstar.refresh_modlist
    NSExportModelOperator, # Export Model button bl_idname: northstar.export_model
    NSCompileModelOperator, # Compile Model button bl_idname: northstar.compile_model
    NSConvertModelOperator, # Convert Model button bl_idname: northstar.convert_model
    NSAllInOneTestOperator, # All in One Test button bl_idname: northstar.all_in_one_test
    NSDisableSelectedOperator, # Disable Selected button bl_idname: northstar.disable_selected
    NSEnableSelectedOperator, # Enable Selected button bl_idname: northstar.enable_selected
    NSRefreshLaunchArgsOperator, # Refresh Launch Args button bl_idname: northstar.refresh_launch_args
    NSUpdateLaunchArgsOperator, # Update Launch Args button bl_idname: northstar.update_launch_args
    NSCompareAnimationFilesOperator, # Compare Animation Files button, currently disabled bl_idname: northstar.compare_animation_files
    NSAnimationPortingStageOneOperator, # Animation Porting Stage One button bl_idname: northstar.animation_porting_stage_one
    NSAnimationPortingStageTwoOperator, # Animation Porting Stage Two button bl_idname: northstar.animation_porting_stage_two
    NSAppendShadersToMeshesOperator, # Append Shaders to Meshes button bl_idname: northstar.append_shaders_to_meshes
    NSListItem, # UIList item for modlist bl_idname: northstar.list_item
    NS_UL_List, # UIList for modlist bl_idname: northstar.ul_list
    QCFileSelectorOperator, # QC File Selector button bl_idname: northstar.qc_file_selector
    PerimeterQCParserOperator, # QC Parser button bl_idname: northstar.qc_parser
    NSQCBodygroupOperator, # QC Bodygroup visiblity switcher button bl_idname: ns.qc_bodygroup
    NSQC_UL_MaterialList, # UIList for QC Material Overrides bl_idname: ns.qc_material_list
    NSQCMaterilListRefreshOperator, # Refresh QC Material Overrides  bl_idname: ns.qc_material_list_refresh
    NSMaterialNamePopup, # Set Override popup bl_idname: ns.material_name_popup
    PerimeterMaterialMainCollection,
    PERIMETER_UL_MaterialManagementList,
    PerimeterMaterialManagementAddMaterialOperator,
    PerimeterMaterialManagementRemoveMaterialOperator,
    PeriimeterMaterialManagementAddEmptyShader,
    PerimeterRefreshShader,
    PerimeterMaterialManagementPanelExportRPAK,
    NSQCSkeletonOperator,
    PerimeterQCMainCollection,
    PERIMETER_UL_QCManagementTexturegroupList,
    PerimeterQCManagementPanelUpdateQCFile,
    PerimeterTexturegroupItem,
    PerimeterAddTextureGroupItem,
    PerimeterRemoveTextureGroupItem,
    PERIMETER_UL_BodygroupList,
    PERIMETER_UL_BodygroupMeshList,
    PerimeterAddBodyGroupItem,
    PerimeterRemoveBodyGroupItem,
    PerimeterBodygroupMeshFile,
    PerimeterBodygroupItem,
    PerimeterAddBodyGroupMeshItem,
    PerimeterRemoveBodyGroupMeshItem,   
    PerimeterWriteBodygroups,
    PerimeterWriteQCArguments,
    PerimeterQCManagementPanelWriteTexGroups,
    PerimeterRUIMeshMaker,
    PerimeterMaterialManagementImportPerimeterMaterial,
    PerimeterMaterialManagementExportPerimeterMaterial,


  

 )

preview_collections = {}

surface_prop_list = ['alienflesh', 'arc_grenade', 'boulder', 'cardboard', 'carpet', 'cloth', 'concrete', 'concrete_block', 'default', 'dirt', 'flesh', 'flyerflesh', 'foliage', 'glass', 'glass_breakable', 'glassbottle', 'grass', 'gravel', 'grenade', 'grenade_triple_threat', 'ice', 'metal', 'metal_barrel', 'metal_bouncy', 'metal_box', 'metal_spectre', 'metal_titan', 'metalgrate', 'metalpanel', 'metalvehicle', 'metalvent', 'paper', 'papercup', 'plaster', 'plastic', 'plastic_barrel', 'plastic_barrel_buoyant', 'plastic_box', 'pottery', 'rock', 'rubber', 'rubbertire', 'sand', 'shellcasing_large', 'shellcasing_small', 'solidmetal', 'stone', 'tile', 'upholstery', 'water', 'weapon', 'wood', 'wood_box', 'wood_furniture', 'wood_plank', 'wood_solid', 'xo_shield']


def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class( cls )


    bpy.types.Scene.northstar_items = CollectionProperty( type=NSListItem )
    bpy.types.Scene.northstar_items_index = bpy.props.IntProperty()


    bpy.types.Scene.compiled_mod_name = bpy.props.StringProperty(default="Perimeter Mod")
    bpy.types.Scene.compiled_mod_description = bpy.props.StringProperty(default="Mod made using Perimeter")
    bpy.types.Scene.compiled_mod_version = bpy.props.StringProperty(default="1.0.0")
    bpy.types.Scene.compiled_mod_priority = bpy.props.IntProperty(min=-5, max=40, default=3)


    bpy.types.Scene.material_path = bpy.props.StringProperty()
    bpy.types.Scene.ns_qc_selected = bpy.props.BoolProperty()
    bpy.types.Scene.mdlshit_mdl = bpy.props.StringProperty()
    bpy.types.Scene.qc_file_path = bpy.props.StringProperty(subtype='FILE_PATH')
    bpy.types.Scene.has_exported = bpy.props.BoolProperty()
    bpy.types.Scene.northstar_rpak_materials_enabled = bpy.props.BoolProperty()
    bpy.types.Scene.perimeter_material_main_collection = CollectionProperty( type=PerimeterMaterialMainCollection )
    bpy.types.Scene.perimeter_material_main_collection_index = bpy.props.IntProperty()

    #QC SHIT
    bpy.types.Scene.perimeter_qc_main_collection = CollectionProperty( type=PerimeterQCMainCollection )
    bpy.types.Scene.perimeter_qc_main_collection_index = bpy.props.IntProperty()
    bpy.types.Scene.qc_model_name = bpy.props.StringProperty()
    bpy.types.Scene.qc_surfaceprop = bpy.props.StringProperty()
    bpy.types.Scene.qc_maxverts = bpy.props.StringProperty()
    bpy.types.Scene.texturegroup_materials = bpy.props.CollectionProperty(type=PerimeterTexturegroupItem)
    bpy.types.Scene.qc_texturegroup_name = bpy.props.StringProperty()
    bpy.types.Scene.qc_expand_texturegroups = bpy.props.BoolProperty( default=True)

    bpy.types.Scene.perimeter_bodygroup_collection = CollectionProperty( type=PerimeterBodygroupItem )
    bpy.types.Scene.perimeter_bodygroup_collection_index = bpy.props.IntProperty()
    bpy.types.Scene.perimeter_mesh_file_collection = CollectionProperty( type=PerimeterBodygroupMeshFile )
    bpy.types.Scene.perimeter_mesh_file_collection_index = bpy.props.IntProperty()
    bpy.types.Scene.qc_bodygroups_found = bpy.props.BoolProperty( default=False)

    bpy.types.Scene.surfaceprops = bpy.props.EnumProperty( items=[ (sprop, sprop, "") for sprop in surface_prop_list ],
                                                default="default" )
    

    bpy.types.Scene.qc_file_selected = bpy.props.BoolProperty( default=False )

    bpy.types.Scene.perimeter_expand_rpak_slots = bpy.props.BoolProperty()
    bpy.types.Scene.perimeter_expand_rpak_slots_advanced = bpy.props.BoolProperty()
    bpy.types.Scene.perimeter_rpak_export_path = bpy.props.StringProperty( subtype="DIR_PATH" )
    bpy.types.Scene.perimeter_empty_cdmaterials = bpy.props.BoolProperty()
    bpy.types.Scene.perimeter_overwrite_maxverts = bpy.props.BoolProperty()

    bpy.types.Scene.test1 = bpy.props.BoolProperty()
    bpy.types.Scene.test2 = bpy.props.BoolProperty()



    


def unregister():
    for cls in classes:
        bpy.utils.unregister_class( cls )
    del bpy.types.Scene.northstar_items
    del bpy.types.Scene.northstar_items_index
    del bpy.types.Scene.compiled_mod_name
    del bpy.types.Scene.material_path
    del bpy.types.Scene.ns_qc_selected
    del bpy.types.Scene.mdlshit_mdl
    del bpy.types.Scene.qc_file_path
    del bpy.types.Scene.qc_model_name
    del bpy.types.Scene.has_exported
    del bpy.types.Scene.northstar_rpak_materials_enabled
    del bpy.types.Scene.perimeter_material_main_collection
    del bpy.types.Scene.perimeter_material_main_collection_index
    del bpy.types.Scene.perimeter_qc_main_collection
    del bpy.types.Scene.perimeter_qc_main_collection_index
    del bpy.types.Scene.perimeter_expand_rpak_slots
    del bpy.types.Scene.perimeter_expand_rpak_slots_advanced
    del bpy.types.Scene.perimeter_rpak_export_path
    del bpy.types.Scene.perimeter_empty_cdmaterials
    del bpy.types.Scene.qc_surfaceprop
    del bpy.types.Scene.qc_maxverts
    del bpy.types.Scene.texturegroup_materials
    del bpy.types.Scene.qc_expand_texturegroups
    del bpy.types.Scene.perimeter_bodygroup_collection
    del bpy.types.Scene.perimeter_bodygroup_collection_index
    del bpy.types.Scene.perimeter_mesh_file_collection
    del bpy.types.Scene.perimeter_mesh_file_collection_index
    del bpy.types.Scene.surfaceprops
    del bpy.types.Scene.test1
    del bpy.types.Scene.test2
    del bpy.types.Scene.qc_file_selected

    
if __name__ == "__main__":
    register()
