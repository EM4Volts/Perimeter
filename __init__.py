bl_info = {
    "name": "Perimeter",
    "author": "EM4V",
    "version": ( 1, 1152 ),
    "blender": ( 2, 80, 0),
    "location": "Sidebar > Perimeter",
    "description": "Addon for managing Northstar settings",
    "category": "Scene",
    "wiki_url": "https://github.com/EM4Volts/Perimeter",
    "tracker_url": "https://github.com/EM4Volts/Perimeter/issues"
}

import bpy
from bpy.props import StringProperty, CollectionProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences, UIList
import os, ast, json, subprocess, shutil
from subprocess import Popen, CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS, run, call
from io_scene_valvesource.export_smd import SmdExporter
from io_scene_valvesource.GUI import SMD_MT_ExportChoice
from .shader import *
from .animationporting import *
from .lib_qc import *
from .rpak import *
icons_dict = bpy.utils.previews.new( )

icons_dir = "icons"

icons_dict.load( "logo_icon", os.path.join( icons_dir, "logo.png"), 'IMAGE' )
icons_dict.load( "northstar_icon", os.path.join( icons_dir, "NorthstarLOGO.png" ), 'IMAGE' )

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
        refresh_rpak_export_list( self, context )       
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
            row.operator( "northstar.launch", text="Launch Northstar", icon_value=icons_dict["northstar_icon"].icon_id )
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
            new_col.label( text="Perimeter v" + version, icon_value=icons_dict["logo_icon"].icon_id )
        else:
            layout = self.layout
            row = layout.row()
            layout.label( text="Perimeter Panel Disabled, enable in settings!", icon="CANCEL" )



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

class NSEmptyRpakShaderOperator( Operator ):
    bl_idname = "northstar.empty_rpak_shader"
    bl_label = "Empty RPAK Shader"
    bl_description = "Appends the Empty RPAK Ready Shader to the currently selected material"

    def execute( self, context ):
        
        
        obj = bpy.context.active_object

        if obj and obj.type == 'MESH' and obj.material_slots:
            setup_shader( obj, "", False, True )
        else:
            self.report( {'ERROR'}, "No Mesh Selected!" )

        
        refresh_rpak_export_list( self, context )            
        return {'FINISHED'}


class NSAutoRepakOperator( Operator ):
    bl_idname = "northstar.auto_repak"
    bl_label = "Export RPAKs"
    bl_description = "Automatically make an RPAK for all materials setup for repak in the scene" 

    def execute( self, context ):
        
        all_rpak_materials = return_mesh_maps( context )
        for rpak_material in context.scene.northstar_rpak_materials:
            if rpak_material.do_export:
                addon_prefs = context.preferences.addons[__name__].preferences

                pack_all_batfile = r'for %%i in ("%~dp0maps\*") do "%~dp0RePak.exe" "%%i"'


                #get the material name
                material_name = rpak_material.name
                #get the material path
                material_path = rpak_material.rpak_asset_path
                #get the material textures
                material_textures = all_rpak_materials[rpak_material.name]
                #get the repak path
                repak_path = addon_prefs.repak_path

    
                #check if repak_path/maps/ exists, if not create it
                if not os.path.exists( repak_path + "/maps/" ):
                    os.makedirs( os.path.dirname(repak_path) + "/maps/", exist_ok=True)
                make_rpak_map( material_name, material_path, list(material_textures), os.path.dirname(repak_path) )
                #check if repak_path/assets/<material_path> exists, if not create it and copy the textures over
                if not os.path.exists( repak_path + "/assets/" + material_path ):
                    os.makedirs( os.path.dirname(repak_path) + "/assets/" + material_path, exist_ok=True)
                    for texture in material_textures:
                        if texture != None:
                            shutil.copy( texture, os.path.dirname(repak_path) + "/assets/" + material_path )

                #use convert_textures to convert all textures in the repak_path/assets/<material_path> folder
                convert_textures( addon_prefs.texconv_path, os.path.dirname(repak_path) + "/assets/" + material_path )

                #make an pack_all.bat file in the repak_path folder
                with open(  os.path.dirname(repak_path) + "/pack_all.bat", "w" ) as f:
                    f.write( pack_all_batfile )

                pack_all_path =  os.path.dirname(repak_path) + "/pack_all.bat"
                call( [pack_all_path], shell=True )      
                
        return {'FINISHED'}
    
class NSRpakListItem( bpy.types.PropertyGroup ):
    name: bpy.props.StringProperty()
    do_export: bpy.props.BoolProperty( default=True )
    rpak_asset_path: bpy.props.StringProperty( default="" )
    original_material_name: bpy.props.StringProperty( default="" )


class NS_UL_RpakMaterialList( UIList ):
    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        split = layout.split(  )
        split.label( text=item.rpak_asset_path, icon="LONGDISPLAY")
        split.label( text=item.name, icon="EXPORT" if item.do_export else "CANCEL" )

class NSToggleRpakExportOperator( Operator ):
    bl_idname = "northstar.toggle_rpak_export"
    bl_label = "Toggle Material RPAK Export"
    bl_description = "Toggles wether the selected material will be exported in the RPAK"

    def execute( self, context ):
        selected_index = bpy.context.scene.northstar_rpak_materials_index
        selected_item = bpy.context.scene.northstar_rpak_materials[selected_index]
        selected_item.do_export = not selected_item.do_export
        return {'FINISHED'}

class NSSetRpakAssetPathOperator( Operator ):
    #make this a popup
    bl_idname = "northstar.set_rpak_asset_path"
    bl_label = "Set RPAK Asset Path"
    bl_description = "Set the RPAK Asset Path for the selected material"

    text_input: StringProperty( name="Path to the material" )
    change_all: BoolProperty( name="Set for All RPAK Materials", default=False )

    def execute( self, context ):
        selected_index = bpy.context.scene.northstar_rpak_materials_index
        selected_item = bpy.context.scene.northstar_rpak_materials[selected_index]
        text = self.text_input
        if self.change_all:
            for item in bpy.context.scene.northstar_rpak_materials:
                item.rpak_asset_path = text
                #change the material name to the rpak asset path and the material name
                #find the material in the scene
                for material in bpy.data.materials:
                    if material.name == item.original_material_name:
                        if not len(text + "/" + item.original_material_name.split( "/" )[-1]) > 63:
                            material.name = text + "/" + item.original_material_name.split( "/" )[-1]
                            material.name = material.name.replace( "//", "/" ) 
                            item.original_material_name = material.name
                        else:
                            self.report( {'ERROR'}, "Material name too long! Must be less than 63 characters!" )
        else:
            selected_item.rpak_asset_path = text
            #find the material in the scene
            for material in bpy.data.materials:
                if material.name == selected_item.original_material_name:
                    if not len(text + "/" + selected_item.original_material_name.split( "/" )[-1]) > 63:
                        material.name = text + "/" + selected_item.original_material_name.split( "/" )[-1]
                        material.name = material.name.replace( "//", "/" )
                        selected_item.original_material_name = material.name
                    else:
                        self.report( {'ERROR'}, "Material name too long! Must be less than 63 characters!" )

        return {'FINISHED'}

    def invoke( self, context, event ):
        return context.window_manager.invoke_props_dialog( self )

# Panel for the MDLutils tab
class NSMDLUtilsPanel( Panel ):
    bl_idname = "SIDEBAR_PT_ns_mdl_utils"
    bl_label = "Materials / Repak"
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

        repak_box = layout.box( )
        row = repak_box.column( )
        row.label( text="RPAK TOOLS", icon="PACKAGE" )
        row.separator( factor=3.5 )
        row.label( text="Setup Empty Shader For RPAK", icon="PACKAGE" )
        row.operator( "northstar.empty_rpak_shader", text="Setup Empty RPAK Shader for Material", icon="SHADING_TEXTURE" )
        row.separator( factor=3.5 )

        #add rpak list here
        row.template_list( "NS_UL_RpakMaterialList", "", bpy.context.scene, "northstar_rpak_materials", bpy.context.scene, "northstar_rpak_materials_index", sort_lock=True)
        row = repak_box.row()
        row.operator( "northstar.set_rpak_asset_path", text="Set RPAK Asset Path", icon="FILE_FOLDER", depress=True )
        row.operator( "northstar.toggle_rpak_export", text="Toggle RPAK Export", icon="CHECKMARK", depress=True )

        row = repak_box.column()
        row.separator( factor=3.5 )
        row.label( text="Export all RPAK ready Materials in the Scene", icon="EXPORT" )
        row.scale_y = 2.0
        row.operator( "northstar.auto_repak", text="Export RPAKs", icon="EXPORT" )



    

global bg_dict 
bg_dict = {}


class NSQCParserOperator( Operator ):
    bl_idname = "northstar.qc_parser"
    bl_label = "QC Parser"
    bl_description = "Parse QC File"

    filepath: bpy.props.StringProperty( subtype="FILE_PATH" )
    

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        qc_file_path = bpy.path.abspath( self.filepath )
        qc_file_name = get_model_name( qc_file_path )

        #set qc model name in addon prefs
        context.scene.qc_model_name = qc_file_name
        perimeterPrint( qc_file_name )
        global bg_dict
        bg_dict = return_bodygroup_dict( qc_file_path )
        bpy.data.screens['Layout'].areas[3].regions[3].tag_redraw()

        #save the qc file path to the addon prefs
        context.scene.qc_file_path = qc_file_path
        #check if qc was valid and bg_dict is not empty
        if bg_dict != {} and qc_file_name != "No QC file found":
            #set bpy.types.Scene.ns_qc_selected = bpy.props.BoolProperty() to true
            context.scene.ns_qc_selected = True



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


# UIList item
class NSQCListItem( bpy.types.PropertyGroup ):
    name: bpy.props.StringProperty()
    enabled: bpy.props.BoolProperty( default=True )
    override: bpy.props.StringProperty( default="No Override Set!" )

# UIList
class NSQC_UL_MaterialList( UIList ):

    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        row = layout.row()
        row.label( text=item.name, icon="MATSPHERE" )
        row.label( text=item.override, icon="SHADING_TEXTURE" )
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


class NSQCMaterialOverrideQCWriter( Operator ):
    bl_idname = "ns.qc_material_override_qc_writer"
    bl_label = "Write QC File"
    bl_description = "Write QC File"
    #get current qc file
    #get current override material
    #write override material to qc file

    def execute( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        qc_file_path = bpy.path.abspath( context.scene.qc_file_path )

        #get material_path property
        material_path = bpy.context.scene.material_path
        rename_material_list = []
        no_overrides = True

        for i in bpy.context.scene.northstar_materials:
            if i.override != "No Override Set!":    
                no_overrides = False
                renamemat_string = '$renamematerial "' + material_path + "/" + i.name + '" "' + i.override + '"'
                rename_material_list.append( renamemat_string )
        if no_overrides:
            perimeterPrint( "No Overrides Set, Not Writing to QC File!" )
        else:
            
            save_material_override( qc_file_path, rename_material_list )

        return {'FINISHED'}

# Operator for "All in One > Test" button
class NSAllInOneTestOperator( Operator ):
    bl_idname = "northstar.all_in_one_test"
    bl_label = "All in One"
    bl_description = "All in One"
    
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
            print(context.scene.qc_file_path)
            self.report( {'ERROR'}, "No QC File Selected!" )
        else:
            #export model
            perimeterPrint( "Exporting model..." )

            compile_model( context )
            convert_model( context )

            make_testmod( self, context )

            if not context.scene.northstar_rpak_materials_enabled:
                perimeterPrint( "RPAK Materials Disabled, not exporting RPAKs!" )
          
            else:
                
                perimeterPrint( "Exporting RPAKs..." )
                bpy.ops.northstar.auto_repak()
        
        
 
            launch_exe = addon_prefs.ns_launch_exe + "/northstarlauncher.exe"

            perimeterPrint( "Launching Northstar..." )

            proc = Popen( [launch_exe, addon_prefs.launch_args], creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS )


        return {'FINISHED'}


def compile_model( context ):

    #exectue studiomdl.exe with subprocess
    addon_prefs = context.preferences.addons[__name__].preferences
    qc_file_path = bpy.path.abspath( context.scene.qc_file_path )
    qc_file_name = get_model_name( qc_file_path )
    perimeterPrint( qc_file_name )
    #get the studiomdl.exe path
    #make stripped gameinfo path by stripping the file name from the gameinfo path
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
        line = line.strip()
        print( line )
        if line.startswith( "writing" ):
            if line.endswith( ".mdl:" ):
                line= line.replace( "writing ", "" )[:-1]
                mdlshit_line = line.replace( "\\" , "/" )
    if mdlshit_line != "":
        context.scene.mdlshit_mdl = mdlshit_line
        return mdlshit_line


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
        mod_json_dict = {"Name": "Perimeter Test Mod", "description": "This is a test mod made by Perimeter", "version": "1.0.0", "LoadPriority": 3}
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

        #make an "paks" folder in the testmods folder, copy all the files in the rpak_path/rpaks to it that start with "PERIMETER" and end with lowercase "pak"
        if context.scene.northstar_rpak_materials_enabled:
            os.makedirs( os.path.join( mod_folder, "paks" ) )
            for file in os.listdir( os.path.dirname(addon_prefs.repak_path) + "/rpaks" ):
                if file.startswith( "perimeter" ) and file.endswith( "pak" ):
                    shutil.copy( os.path.join( os.path.dirname(addon_prefs.repak_path) + "/rpaks", file ), os.path.join( mod_folder, "paks" ) )
        #make rpak.json in the paks folder, make an entry in the json for each .rpak file in the paks folder like this {"Postload": {"booleangemini.rpak": "common.rpak","booleangemini_decals.rpak": "common.rpak"}}, common.rpak should be existing for each rpak
        if context.scene.northstar_rpak_materials_enabled:
            rpak_json_dict = {"Postload": {}}
            for file in os.listdir( os.path.join( mod_folder, "paks" ) ):
                if file.endswith( "pak" ):
                    rpak_json_dict["Postload"][file] = "common.rpak"
            with open( os.path.join( mod_folder, "paks", "rpak.json" ), 'w' ) as f:
                json.dump( rpak_json_dict, f, indent=4 )


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
    bl_label = "QC File Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Northstar"

    def draw( self, context ):
        addon_prefs = context.preferences.addons[__name__].preferences
        row = self.layout.column()
        row.label( text="QC File Info", icon="FILE" )
        row.operator( "northstar.qc_parser", text="Select QC File", icon="FILE_FOLDER" )
        layout = self.layout
        row = layout.column()
        row.label( text="QC File Info", icon="FILE" )
        qc_file_name = context.scene.qc_model_name
        row.label( text=qc_file_name, icon="OUTLINER_OB_MESH" ) 

        # Iterate over the dictionary
        global bg_dict
        row.label( text="Bodygroup Visibility Switchers", icon="MODIFIER" )
        for name, items in bg_dict.items():
            # Create a button for each name
            cur = row.operator( "ns.qc_bodygroup", text=name )
            cur.item_name = name
            cur.dict_list_string = str( items )
        
        row = layout.row()
        row.label( text="" )
        row = layout.box()
        row.label( text="Material Overrides", icon="MATERIAL_DATA" )

        row.operator( "ns.material_name_popup", text="Set Override", icon="OUTLINER_DATA_GP_LAYER" )
        row.template_list( "NSQC_UL_MaterialList", "", bpy.context.scene, "northstar_materials", bpy.context.scene, "northstar_materials_index" )
        row.scale_y = 0.9
         
        
        row.prop( context.scene.vs ,"material_path", text="Material Path" )
        row.operator( "ns.qc_material_list_refresh", text="Refresh Material List", icon="FILE_REFRESH" )
       
        row = layout.column()
        row.operator( "ns.qc_material_override_qc_writer", text="Update QC File", icon="FILE_REFRESH" )
        row.scale_y = 1.5
    
        compile_box = layout.box()
        row = compile_box.row()
        
        
        row.label( text="QC Compilation", icon="MEMORY" )
        
        row.prop( context.scene, "compiled_mod_name", text="Compiled Name" )
        row = compile_box.row()

        # Button row
        col = compile_box.column( align=True )
        button_row = compile_box.row() # Increase button row height
        row.prop( context.scene.vs, "export_path", text="SMD/DMX Export Path" )
        row = compile_box.row()
        row.label( text="Export Format")
        row.prop( context.scene.vs, "export_format", expand=True)
        row = compile_box.row()



        """
        button_row.operator( SmdExporter.bl_idname, text="Export Model", icon="EXPORT" )
        button_row.operator( "northstar.compile_model", text="Compile Model", icon="FILE_3D" )
        button_row.operator( "northstar.convert_model", text="Convert Model", icon="MOD_WIREFRAME" )
        """

        
        # All in One Test button
        row = compile_box.column()
        row.operator( "northstar.export_model", text="Export", icon="EXPORT" )
        row = compile_box.column()
        if context.scene.has_exported:
            row.enabled = True
        else:
            row.enabled = False
        row.prop( addon_prefs, "testmod_make_rpak", text="Include RPAKs in Testmod" if addon_prefs.testmod_make_rpak else "RPAKs not Exporting into Testmod", icon="CHECKMARK" if addon_prefs.testmod_make_rpak else "CANCEL", expand = False)
        row.operator( "northstar.all_in_one_test", text="Compile, Convert and Test!", icon="PLAY" )
        row.scale_y = 2.0 
        row = compile_box.column()
       
         # Increase button height
        
        #add updateable lables for the qc file path and its informations
        row = compile_box.row()
        

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
    default='portal2',
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
        layout = self.layout
        layout.label( text="Perimeter Settings")
        layout.label( icon_value=icons_dict["logo_icon"].icon_id )
        layout.prop( self, "ns_launch_exe" )
        layout.prop( self, "texture_path" )
        layout.prop( self, "launch_args" )
        layout.prop( self, "perimeter_panel_enabled" )

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
        row.label( text="" )
        #check if io_scene_valvesource is installed, if not, display error
        if "io_scene_valvesource" in bpy.context.preferences.addons:
            row.label( text="Blender Source Tools is installed!", icon="CHECKMARK" )
        else:
            row.label( text="Blender Source Tools is not installed!", icon="CANCEL" )
        row = layout.row()
        row.label( text="For help see the wiki", icon="URL" )
        row.operator( "wm.url_open", text="Github/Wiki", icon="URL" ).url = bl_info["wiki_url"]





classes = ( # classes for the register and unregister functions

    NSAddonPreferences, # Addon Preferences
    NSPreferencesStudiomdlSetup, # preferences setup for studiomdl

    NSManagerPanel, # Perimeter tab
    NSMDLUtilsPanel, # MDLutils tab
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
    NSQCParserOperator, # QC Parser button bl_idname: northstar.qc_parser
    NSQCBodygroupOperator, # QC Bodygroup visiblity switcher button bl_idname: ns.qc_bodygroup
    NSQCListItem, # UIList item for QC Bodygroup visiblity switcher bl_idname: ns.qc_list_item
    NSQC_UL_MaterialList, # UIList for QC Material Overrides bl_idname: ns.qc_material_list
    NSQCMaterilListRefreshOperator, # Refresh QC Material Overrides  bl_idname: ns.qc_material_list_refresh
    NSMaterialNamePopup, # Set Override popup bl_idname: ns.material_name_popup
    NSQCMaterialOverrideQCWriter, # Write QC File button bl_idname: ns.qc_material_override_qc_writer
    NSEmptyRpakShaderOperator, # Empty Rpak Shader button bl_idname: northstar.empty_rpak_shader
    NSAutoRepakOperator, 
    NSRpakListItem,
    NS_UL_RpakMaterialList,
    NSToggleRpakExportOperator,
    NSSetRpakAssetPathOperator,


 )

preview_collections = {}

def register():
    for cls in classes:
        bpy.utils.register_class( cls )


    bpy.types.Scene.northstar_items = CollectionProperty( type=NSListItem )
    bpy.types.Scene.northstar_items_index = bpy.props.IntProperty()
    bpy.types.Scene.northstar_materials = CollectionProperty( type=NSQCListItem )
    bpy.types.Scene.northstar_materials_index = bpy.props.IntProperty()
    bpy.types.Scene.compiled_mod_name = bpy.props.StringProperty()
    bpy.types.Scene.material_path = bpy.props.StringProperty()
    bpy.types.Scene.ns_qc_selected = bpy.props.BoolProperty()
    bpy.types.Scene.mdlshit_mdl = bpy.props.StringProperty()
    bpy.types.Scene.qc_file_path = bpy.props.StringProperty()
    bpy.types.Scene.qc_model_name = bpy.props.StringProperty()
    bpy.types.Scene.has_exported = bpy.props.BoolProperty()
    bpy.types.Scene.northstar_rpak_materials = CollectionProperty( type=NSRpakListItem )
    bpy.types.Scene.northstar_rpak_materials_index = bpy.props.IntProperty()
    bpy.types.Scene.northstar_rpak_materials_enabled = bpy.props.BoolProperty()



def unregister():
    for cls in classes:
        bpy.utils.unregister_class( cls )
    del bpy.types.Scene.northstar_items
    del bpy.types.Scene.northstar_items_index
    del bpy.types.Scene.northstar_materials
    del bpy.types.Scene.northstar_materials_index
    del bpy.types.Scene.compiled_mod_name
    del bpy.types.Scene.material_path
    del bpy.types.Scene.ns_qc_selected
    del bpy.types.Scene.mdlshit_mdl
    del bpy.types.Scene.qc_file_path
    del bpy.types.Scene.qc_model_name
    del bpy.types.Scene.has_exported
    del bpy.types.Scene.northstar_rpak_materials
    del bpy.types.Scene.northstar_rpak_materials_index
    del bpy.types.Scene.northstar_rpak_materials_enabled




if __name__ == "__main__":
    register()