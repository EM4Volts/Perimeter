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


import bpy
from bpy.props import StringProperty, CollectionProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences, UIList, Menu
from .shader import *
from .rpak import *


#        _      _____  _____ _______ _____       __  __  __ _____  _____  _____ 
#       | |    |_   _|/ ____|__   __/ ____|     / / |  \/  |_   _|/ ____|/ ____|
#       | |      | | | (___    | | | (___      / /  | \  / | | | | (___ | |     
#       | |      | |  \___ \   | |  \___ \    / /   | |\/| | | |  \___ \| |     
#       | |____ _| |_ ____) |  | |  ____) |  / /    | |  | |_| |_ ____) | |____ 
#       |______|_____|_____/   |_| |_____/  /_/     |_|  |_|_____|_____/ \_____|
                                                                        


shader_list = ['Default', 'uberAddSamp2222_skn', 'uberAoCavDetovrDtmUV200000010Samp22222222_skn', 'uberAoCavDtnDtmUV200000010Samp22222222_skn', 'uberAoCavEmitDetovrDtmEntcolmeUV2000000010Samp222222222_skn', 'uberAoCavEmitDetovrDtmUV2000000010Samp222222222_skn', 'uberAoCavEmitEntcolmeSamp2222222_skn', 'uberAoCavEmitOpamCutSamp22222222_skn', 'uberAoCavEmitOpamDetovrDtmCutUV20000000010Samp2222222222_skn', 'uberAoCavEmitOpamTransEPMATSamp22222222_skn', 'uberAoCavEmitOpamTransSamp22222222_skn', 'uberAoCavEmitSamp2222222_skn', 'uberAoCavOpamCutSamp2222222_skn', 'uberAoCavOpamTransSamp2222222_skn', 'uberAoCavOpamTransTsaadatSamp2222222_skn', 'uberAoCavSamp222222_skn', 'uberAoDetDtnUV20000011Samp2222222_skn', 'uberAoDetovrDtmUV20000010Samp2222222_skn', 'uberAoEmitDetovrDtmEntcolmeUV200000010Samp22222222_skn', 'uberAoEmitDetovrDtmUV200000010Samp22222222_skn', 'uberAoEmitEntcolmeEntcolmdSamp222222_skn', 'uberAoEmitEntcolmeSamp222222_skn', 'uberAoEmitSamp222222_skn', 'uberAoOpamTransSamp222222_skn', 'uberAoSamp22222_skn', 'uberCavOpamTransSamp222222_skn', 'uberCavSamp22222_skn', 'uberCockpit3Samp2222_skn', 'uberCutSamp2222_skn', 'uberDepthUiVcolaCut', 'uberDepthVsmCut', 'uberDepthVsmOpamCut', 'uberDepthVsmOpamovrCut', 'uberDepthVsmUiVcolaCut', 'uberDepthVsmUvs_skn', 'uberDepthVsmVcolUvs_skn', 'uberDepthVsmVcolaCut', 'uberDepthVsm_fix', 'uberDepthVsm_skn', 'uberEmitDetovrDtmEntcolmeUV20000010Samp2222222_skn', 'uberEmitDtnUV2000001Samp222222_skn', 'uberEmitEmulEefUv1sUv1atUV2000001Samp222222_skn', 'uberEmitEmulUv1atUV2000001Samp222222_skn', 'uberEmitEntcolmeSamp22222_skn', 'uberEmitOpamTransSamp222222_skn', 'uberEmitSamp22222_skn', 'uberEmitTransSamp22222_skn', 'uberInstDecal_wld', 'uberInstDepthUvs_skn', 'uberInstDepthVcolUvs_skn', 'uberInstDepth_gen', 'uberInstDepth_skn', 'uberInstEef_skn', 'uberInstUnlitAef_skn', 'uberInstUnlitUiVcolNofog_skn', 'uberInstUnlitVcolAdfAefNoTsaa_skn', 'uberInstUnlitVcolAdfEef_skn', 'uberInstUnlitVcolAefEef_skn', 'uberInstUnlitVcolAef_skn', 'uberInstUnlitVcolNofog_gen', 'uberInstUnlitVcol_gen', 'uberInstUnlitVcol_skn', 'uberInstUnlitVcol_wld', 'uberInstUnlit_skn', 'uberInstVcolAef_skn', 'uberInstVcolDecal_skn', 'uberInstVcolDecal_wld', 'uberInstVcol_skn', 'uberInst_skn', 'uberLyrDetallOpamDetDtnTransUV4010002200000Samp222222222222_skn', 'uberOpamAddSamp22222_skn', 'uberOpamCutSamp22222_skn', 'uberOpamTransSamp22222_skn', 'uberOpamTransUV210111Samp22222_skn', 'uberSamp2222_skn', 'uberTransSamp2222_skn', 'uberTransSamp2222_wld', 'uberUV20100Samp2222_skn', 'uberUnlitAoCavEmitDetAefAddUv1sUv1atUv2sUv2atUV300001002Samp22222222', 'uberUnlitAvgfrmcolmdSamp2222', 'uberUnlitEef_skn', 'uberUnlitEmitSamp22', 'uberUnlitTransSamp2', 'uberUnlitUiNofogSamp2', 'uberUnlitUiTransNofogSamp2', 'uberUnlitUiVcolNofog_gen', 'uberUnlitUiVcolaAddNofogSamp2', 'uberUnlitUiVcolaTransNofogEPMATSamp2', 'uberUnlitUiVcolaTransNofogSamp2222', 'uberUnlitUiVcoltVcolaAddNofogEPMATSamp2', 'uberUnlitUiVcoltVcolaAddNofogSamp2', 'uberUnlitUiVcoltVcolaCutNofogSamp2', 'uberUnlitUiVcoltVcolaDetTransNofogEPMATUv1atUv2atUV312Samp22', 'uberUnlitVcol_skn', 'uberUnlitVcoltUv1atUV21000Samp2222', 'uberUnlitVcoltVcolaAdfAefAddNoCocNoTsaaSamp2', 'uberUnlitVcoltVcolaEmitEmulEntcolmeEntcolmdAdfEefAddUvd1Uvd2Uv1sUv1dUv1atUv2dUv2atUV401203Samp22222', 'uberUnlitVcoltVcolaEmitEmulEntcolmeEntcolmdTransUvd2Uv1sUv1dUv1atUv2sUv2dUv2atUV31210Samp2222', 'uberUnlitVcoltVcolaEmitEmulOpamEntcolmeEntcolmdAefAddUvd1Uvd2Uv1dUv1atUv2dUv2atUV3111121Samp222222', 'uberUnlitVcoltVcolaEmitEntcolmeEntcolmdAdfEefAddUvd1Uvd2Uv1sUv1dUv1atUV30102Samp2222', 'uberUnlitVcoltVcolaEntcolmdAddSamp2', 'uberUnlitVcoltVcolaEntcolmdTransDofaifSamp2', 'uberUnlit_skn', 'uberVcolaAoOpamTransSamp222222_skn', 'uberVcolaAoOpamTransSamp222222_wld', 'uberVcolaOpamTransSamp22222_skn', 'uberVcolaOpamTransSamp22222_wld', 'uberVcolaTransSamp2222_skn', 'uberVcolaTransSamp2222_wld', 'uberVcolaoAoCavDetovrDtmUV200000010Samp22222222_skn', 'uberVcolaoAoCavEmitEntcolmeSamp2222222_skn', 'uberVcolaoAoCavSamp222222_skn', 'uberVcolaoEmitSamp22222_skn', 'uberVcolaoSamp2222_skn', 'uberVcolaoVcolaAoEntcolmdAefTransSamp22222_skn', 'uberVcoltAoCavDetovrDtmUV200000010Samp22222222_skn', 'uberVcoltAoCavSamp222222_skn', 'uberVcoltAoOpamTransSamp222222_skn', 'uberVcoltAoSamp22222_skn', 'uberVcoltCavSamp22222_skn', 'uberVcoltEmitEntcolmeSamp22222_skn', 'uberVcoltEmitSamp22222_skn', 'uberVcoltOpamCutSamp22222_skn', 'uberVcoltSamp2222_skn', 'uberVcoltVcolaCutSamp2222_skn', 'uberVcoltVcolaEmitAddSamp22222_skn']

#MAIN COLLECTION FOR MATERIAL MANAGEMENT
class PerimeterMaterialMainCollection( bpy.types.PropertyGroup ):
    name: bpy.props.StringProperty() #raw name of material without its path, SHOULD NOT BE USER EDITABLE, SHOULD NEVER CHANGE //bump

    blender_material: bpy.props.PointerProperty( type=bpy.types.Material ) #pointer to the material in blenders material list, has to be updated each time material name or path is changed DO NOT MAKE USER EDITABLE //bump

    #       ____ ___  ____ _  _    ____ ____ _  _ ____ ___     ____ ___ _  _ ____ ____
    #       |__/ |__] |__| |_/     [__  |__| |  | |___ |  \    [__   |  |  | |___ |___
    #       |  \ |    |  | | \_    ___] |  |  \/  |___ |__/    ___]  |  |__| |    | 


    rpak_shader_is_set: bpy.props.BoolProperty( default=False ) #whether or not the rpak shader is set

    rpak_asset_path: bpy.props.StringProperty(default="") #path to the material in the rpak, used for exporting the rpak map

    export_rpak: bpy.props.BoolProperty( default=False) #whether or not to export the material to the rpak

    advanced_rpak_options: bpy.props.BoolProperty( default=False ) #whether or not to show the advanced rpak options

    rpak_preset: bpy.props.EnumProperty( items=[ ("default", "Default", "")
                                                 ], 
                                                default="default" ) #preset for the rpak

    rpak_shaderset: bpy.props.EnumProperty( items=[ (shader, shader, "") for shader in shader_list ], 
                                                default="Default" ) #shaderset for the rpak
    
    rpak_enable_manual_shaderset: bpy.props.BoolProperty( default=False ) #whether or not to use a manual shaderset for the rpak

    rpak_manual_shaderset: bpy.props.StringProperty( default="" ) #manual shaderset for the rpak
    
    rpak_faceflags: bpy.props.IntProperty( default=6 ) #face flags for the material

    rpak_visibilityflags: bpy.props.EnumProperty( items=[ 
                                                        ("opaque", "Opaque", ""), 
                                                        ("transparent", "Transparent", "") 
                                                        ], 
                                                        default="opaque" ) #visibility flags for the material
    
    rpak_surfacetype: bpy.props.StringProperty( default="default" ) #surface type for the material
    rpak_subtype: bpy.props.StringProperty( default="viewmodel" ) #subtype for the material
    rpak_type: bpy.props.StringProperty( default="skn" ) #type for the material
    
    rpak_flag_1: bpy.props.StringProperty( default="" ) #flag 1 for the material
    rpak_flag_2: bpy.props.StringProperty( default="" ) #flag 2 for the material

    rpak_selfillum_enabled: bpy.props.BoolProperty( default=False ) #whether or not selfillum is enabled for the material

    rpak_selfillum: bpy.props.FloatVectorProperty( default=(0.0, 0.0, 0.0), name="Selfillum", subtype="COLOR", min= 0.1, max = 100.0 ) #selfillum for the material

    rpak_slot_1: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_2: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_3: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_4: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_5: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_6: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_7: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_8: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_9: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_10: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_11: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_12: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_13: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_14: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_15: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_16: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_17: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_18: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_19: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_20: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_21: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_22: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_23: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_24: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_25: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_26: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )
    rpak_slot_27: bpy.props.StringProperty( default="None", subtype='FILE_PATH' )

    

    #       _  _ ____ ___ ____ ____ _ ____ _       ____ _  _ ____ ____ ____ _ ___  ____ ____
    #       |\/| |__|  |  |___ |__/ | |__| |       |  | |  | |___ |__/ |__/ | |  \ |___ [__ 
    #       |  | |  |  |  |___ |  \ | |  | |___    |__|  \/  |___ |  \ |  \ | |__/ |___ ___]


    material_override_enabled: bpy.props.BoolProperty( default=False ) #whether or not to override the material

    material_override_path: bpy.props.StringProperty( default="" ) #full material path to override the material with



    #       _  _ _  _ ___    _  _ ____ ___
    #       |  | |\/|  |     |  | |___  | 
    #        \/  |  |  |      \/  |     | 

    material_is_vmt: bpy.props.BoolProperty( default=False ) #whether or not the material is a vmt





#MAIN OPERATOR FOR MATERIAL MANAGEMENT LIST
class PERIMETER_UL_MaterialManagementList( UIList ):
    def draw_item( self, context, layout, data, item, icon, active_data, active_propname, index ):
        split = layout.split(  )
        split.prop( item.blender_material, "name", text="", emboss=False, translate=False, icon="MATERIAL")
        


#        _____        _   _ ______ _            __  __  __ ______ _   _ _    _  _____ 
#       |  __ \ /\   | \ | |  ____| |          / / |  \/  |  ____| \ | | |  | |/ ____|
#       | |__) /  \  |  \| | |__  | |         / /  | \  / | |__  |  \| | |  | | (___  
#       |  ___/ /\ \ | . ` |  __| | |        / /   | |\/| |  __| | . ` | |  | |\___ \ 
#       | |  / ____ \| |\  | |____| |____   / /    | |  | | |____| |\  | |__| |____) |
#       |_| /_/    \_\_| \_|______|______| /_/     |_|  |_|______|_| \_|\____/|_____/ 



class PerimeterMaterialManagementPanel( bpy.types.Panel ):
    bl_idname = "material_management_panel"
    bl_label = "Material Management"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Northstar"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        try:
            selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]
            selected_item_rpak_path = selected_item.blender_material.name.replace("\\", "/").replace("//", "/").split("/")
            selected_item_rpak_path = "/".join( selected_item_rpak_path[:-1] ) + "/"
        except:
            selected_item = None



        col = layout.row()
        split = col.split( factor=0.6 )
        box = split.column().box()
        row = box.column()
        row.operator( "perimeter.add_material", text="Add Material", icon="ADD" )
        if len( bpy.context.scene.perimeter_material_main_collection ) > 0 and selected_item != None:
            row.operator( "perimeter.remove_material", text="Remove Material", icon="REMOVE" )
            row.operator( "perimeter.empty_rpak_shader", text="Setup Empty RPAK Shader for Material", icon="SHADING_TEXTURE" )
            if len( bpy.context.scene.perimeter_material_main_collection ) > 0:
                row = box.row()
                row.label( text="Blender Name:" )
                row.label( text=selected_item.blender_material.name )
                row = box.row()
                row.prop( selected_item, "export_rpak", text="Export in RPAK" )
                if not selected_item.rpak_shader_is_set:
                    row.label( text="RPAK Shader Not Set", icon="ERROR" )
                    row.enabled = False
                else:
                    row.enabled = True

                if selected_item.export_rpak:
                    row = box.row()
                    row.prop( context.scene, "perimeter_rpak_export_path", text="RPAK Export Path" )
                    row = box.row()
                    row.operator( "perimeter.material_management_panel_export_rpak", text="Export RPAK", icon="EXPORT" )
                    row = box.row()
                    row.label( text="RPAK Asset Path (path without material):" )
                    row.label( text=selected_item_rpak_path )
                    row = box.row()
                    row.prop( context.scene, "perimeter_expand_rpak_slots", text="Show Texture Slots")

                    if context.scene.perimeter_expand_rpak_slots:
                        row.prop( context.scene , "perimeter_expand_rpak_slots_advanced", text="Advanced View" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_1", text="1 (col)" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_2", text="2 (nml)" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_3", text="3 (gls/exp)" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_4", text="4 (spc)" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_5", text="5 (ilm)" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_6", text="6" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_7", text="7" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_8", text="8" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_9", text="9" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_10", text="10" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_11", text="11" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_12", text="12 (ao)" )
                        row = box.row()
                        row.prop( selected_item, "rpak_slot_13", text="13 (cav/cvt)" )
                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.prop( selected_item, "rpak_slot_14", text="14 (opa)" )

                        if context.scene.perimeter_expand_rpak_slots_advanced:

                            row = box.row()
                            row.prop( selected_item, "rpak_slot_15", text="15 (detail)" )
    
                            row.prop( selected_item, "rpak_slot_16", text="16 (dm_nml)" )
                            row = box.row()
                            row.prop( selected_item, "rpak_slot_17", text="17 (msk)" )

                            row.prop( selected_item, "rpak_slot_18", text="18" )
                            row = box.row()
                            row.prop( selected_item, "rpak_slot_19", text="19" )

                            row.prop( selected_item, "rpak_slot_20", text="20" )
                            row = box.row()
                            row.prop( selected_item, "rpak_slot_21", text="21" )

                            row.prop( selected_item, "rpak_slot_22", text="22" )
                            row = box.row()
                            row.prop( selected_item, "rpak_slot_23", text="23 (bm)" )

                            row.prop( selected_item, "rpak_slot_24", text="24 (col)" )
                            row = box.row()
                            row.prop( selected_item, "rpak_slot_25", text="25 (nml)" )

                            row.prop( selected_item, "rpak_slot_26", text="26 (gls/exp)" )
                            row = box.row()
                            row.prop( selected_item, "rpak_slot_27", text="27 (spc)" )

                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.operator( "perimeter.refresh_shader", text="Refresh Shader", icon="SHADING_TEXTURE" )




                    row = box.row()
                    row.prop( selected_item, "advanced_rpak_options", text="Advanced RPAK Options" )

                    if selected_item.advanced_rpak_options:
                        row = box.row()
                        row.prop( selected_item, "rpak_preset", text="RPAK Preset" )
                        row = box.row()
                        row.prop( selected_item, "rpak_shaderset", text="RPAK Shaderset" )
                        row = box.row()
                        row.prop( selected_item, "rpak_enable_manual_shaderset", text="Enable Manual Shaderset" )
                        if selected_item.rpak_enable_manual_shaderset:
                            row = box.row()
                            row.prop( selected_item, "rpak_manual_shaderset", text="RPAK Manual Shaderset" )
                        row = box.row()
                        row.prop( selected_item, "rpak_faceflags", text="RPAK Faceflags" )
                        row = box.row()
                        row.prop( selected_item, "rpak_visibilityflags", text="RPAK Visibilityflags", expand=True )
                        row = box.row()
                        row.prop( selected_item, "rpak_surfacetype", text="RPAK Surfacetype" )
                        row = box.row()
                        row.prop( selected_item, "rpak_subtype", text="RPAK Subtype" )
                        row = box.row()
                        row.prop( selected_item, "rpak_type", text="RPAK Type" )
                        row = box.row()
                        row.prop( selected_item, "rpak_flag_1", text="RPAK Flag 1" )
                        row = box.row()
                        row.prop( selected_item, "rpak_flag_2", text="RPAK Flag 2" )
                        row = box.row()
                        row.prop( selected_item, "rpak_selfillum_enabled", text="Enable Selfillum" )
                        row = box.row()
                        if selected_item.rpak_selfillum_enabled:
                            row.prop( selected_item, "rpak_selfillum", text="RPAK Selfillum" )

                row = box.row()
                row.prop( selected_item, "material_override_enabled", text="Override Material" )
                if context.scene.ns_qc_selected == True and context.scene.qc_model_name.endswith( '.mdl"' ):
                    row.enabled = True
                else:
                    row.label( text="QC File Not Selected", icon="ERROR" )
                    row.enabled = False
                
                
                if selected_item.material_override_enabled and row.enabled == True:
                    row = box.row()
                    row.label( text="Material Override Path:" )
                    row = box.row()
                    row.prop( selected_item, "material_override_path", text="" )
                    row = box.row()
                    row.label( text="This will rename the material you selected with your desired material" )
                    row = box.row()
                    row.label( text="$renamematerial line:", icon="INFO" )
                    row = box.row()
                    row.label( text='$renamematerial "' + selected_item.blender_material.name + '" "' + selected_item.material_override_path + '"' )
                    row = box.row()
                    row.label( text="IMPORTANT enter the full material path.", icon="ERROR" )

        box = split.column().box()
        row = box.row()
        row.template_list( "PERIMETER_UL_MaterialManagementList", "", context.scene, "perimeter_material_main_collection", context.scene, "perimeter_material_main_collection_index" )
        
        layout = self.layout
        row = layout.row()
        



#         ____  _____  ______ _____         _______ ____  _____   _____ 
#        / __ \|  __ \|  ____|  __ \     /\|__   __/ __ \|  __ \ / ____|
#       | |  | | |__) | |__  | |__) |   /  \  | | | |  | | |__) | (___  
#       | |  | |  ___/|  __| |  _  /   / /\ \ | | | |  | |  _  / \___ \ 
#       | |__| | |    | |____| | \ \  / ____ \| | | |__| | | \ \ ____) |
#        \____/|_|    |______|_|  \_\/_/    \_\_|  \____/|_|  \_\_____/ 





class PerimeterMaterialManagementRemoveMaterialOperator( bpy.types.Operator ):
    bl_idname = "perimeter.remove_material"
    bl_label = ""
    bl_description = "Removes the currently selected material from the list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]
        bpy.context.scene.perimeter_material_main_collection.remove( selected_index )
        return {'FINISHED'}

class PerimeterMaterialManagementAddMaterialOperator( bpy.types.Operator ):
    bl_idname = "perimeter.add_material"
    bl_label = ""
    bl_description = "Adds the currently selected material to the list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        #get the selected material, check if it is already in the list, if not add it, also check if it is a valid material
        selected_material = bpy.context.active_object.active_material
        
        if selected_material == None:
            self.report( {'ERROR'}, "No material selected" )
            return {'CANCELLED'}
        else:
            #check if the material is already in the list
            for material in bpy.context.scene.perimeter_material_main_collection:
                if material.name == selected_material.name:
                    self.report( {'ERROR'}, "Material already in list" )
                    return {'CANCELLED'}
            item = bpy.context.scene.perimeter_material_main_collection.add()
            item.name = selected_material.name
            item.blender_name = selected_material.name
            item.blender_material = selected_material
            return {'FINISHED'}
        

class PeriimeterMaterialManagementAddEmptyShader( Operator ):
    bl_idname = "perimeter.empty_rpak_shader"
    bl_label = "Empty RPAK Shader"
    bl_description = "Appends the Empty RPAK Ready Shader to the currently selected material"

    def execute( self, context ):
        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]

        setup_shader( selected_item.blender_material, "", False, True, True )
        selected_item.rpak_shader_is_set = True
        selected_item.export_rpak = True

        return {'FINISHED'}



class PerimeterRefreshShader( Operator ):
    bl_idname = "perimeter.refresh_shader"
    bl_label = "Refresh Shader"
    bl_description = "Refreshes the shader for the currently selected material"

    def execute( self, context ):
        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]

        perimeter_make_rpak( context, selected_item )

        return {'FINISHED'}



class PerimeterMaterialManagementPanelExportRPAK( Operator ):
    bl_idname = "perimeter.material_management_panel_export_rpak"
    bl_label = "Export RPAK"
    bl_description = "Exports the currently selected material to an RPAK"

    def execute( self, context ):
        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]

        if selected_item.rpak_shader_is_set:
            if selected_item.export_rpak:
                perimeter_make_rpak( context, selected_item )
            else:
                self.report( {'ERROR'}, "Export RPAK is not enabled for this material" )
                return {'CANCELLED'}
        else:
            self.report( {'ERROR'}, "RPAK Shader is not set for this material" )
            return {'CANCELLED'}

        return {'FINISHED'}



def perimeter_make_rpak( context, material_collection ):


    #get the rpak settings from the material_collection item

    rpak_preset = material_collection.rpak_preset
    rpak_shaderset = material_collection.rpak_shaderset
    rpak_enable_manual_shaderset = material_collection.rpak_enable_manual_shaderset
    rpak_manual_shaderset = material_collection.rpak_manual_shaderset
    rpak_faceflags = material_collection.rpak_faceflags
    rpak_visibilityflags = material_collection.rpak_visibilityflags
    rpak_flag_1 = material_collection.rpak_flag_1
    rpak_flag_2 = material_collection.rpak_flag_2
    rpak_selfillum_enabled = material_collection.rpak_selfillum_enabled
    rpak_selfillum = material_collection.rpak_selfillum
    rpak_surface_type = material_collection.rpak_surfacetype
    rpak_subtype = material_collection.rpak_subtype
    rpak_type = material_collection.rpak_type


    rpak_asset_path = material_collection.blender_material.name.replace("\\", "/").replace("//", "/").split("/")
    rpak_asset_path = "/".join( rpak_asset_path[:-1] ) + "/"


    if rpak_enable_manual_shaderset:
        rpak_shaderset = rpak_manual_shaderset

    if rpak_selfillum_enabled:
        rpak_selfillum = (rpak_selfillum[0] , rpak_selfillum[1], rpak_selfillum[2])
    else :
        rpak_selfillum = (0.0, 0.0, 0.0)

    rpak_material_name = material_collection.blender_material.name.replace("\\", "/").replace("//", "/").split("/")
    rpak_material_name = rpak_material_name[-1]

    rpak_params = { "rpak_export_path": context.scene.perimeter_rpak_export_path, 
                   "rpak_surface_type": rpak_surface_type ,
                   "rpak_subtype": rpak_subtype, 
                   "rpak_type": rpak_type, 
                   "rpak_asset_path": rpak_asset_path, 
                   "rpak_name": rpak_material_name, 
                   "preset": rpak_preset, 
                   "shaderset": rpak_shaderset, 
                   "faceflags": rpak_faceflags, 
                   "visibilityflags": rpak_visibilityflags, 
                   "flag_1": rpak_flag_1, 
                   "flag_2": rpak_flag_2, 
                   "selfillum": rpak_selfillum }

    slots = (
        material_collection.rpak_slot_1,
        material_collection.rpak_slot_2,
        material_collection.rpak_slot_3,
        material_collection.rpak_slot_4,
        material_collection.rpak_slot_5,
        material_collection.rpak_slot_6,
        material_collection.rpak_slot_7,
        material_collection.rpak_slot_8,
        material_collection.rpak_slot_9,
        material_collection.rpak_slot_10,
        material_collection.rpak_slot_11,
        material_collection.rpak_slot_12,
        material_collection.rpak_slot_13,
        material_collection.rpak_slot_14,
        material_collection.rpak_slot_15,
        material_collection.rpak_slot_16,
        material_collection.rpak_slot_17,
        material_collection.rpak_slot_18,
        material_collection.rpak_slot_19,
        material_collection.rpak_slot_20,
        material_collection.rpak_slot_21,
        material_collection.rpak_slot_22,
        material_collection.rpak_slot_23,
        material_collection.rpak_slot_24,
        material_collection.rpak_slot_25,
        material_collection.rpak_slot_26,
        material_collection.rpak_slot_27
        )

    perimeter_make_rpak_map( rpak_params, slots )



"""

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
    
    """