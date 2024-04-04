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


import bpy, time
from bpy.props import StringProperty, CollectionProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences, UIList, Menu

from subprocess import call

from .shader import *
from .rpak import *
from .lib_pma import *


#        _      _____  _____ _______ _____       __  __  __ _____  _____  _____
#       | |    |_   _|/ ____|__   __/ ____|     / / |  \/  |_   _|/ ____|/ ____|
#       | |      | | | (___    | | | (___      / /  | \  / | | | | (___ | |
#       | |      | |  \___ \   | |  \___ \    / /   | |\/| | | |  \___ \| |
#       | |____ _| |_ ____) |  | |  ____) |  / /    | |  | |_| |_ ____) | |____
#       |______|_____|_____/   |_| |_____/  /_/     |_|  |_|_____|_____/ \_____|



surface_prop_list = ['alienflesh', 'arc_grenade', 'boulder', 'cardboard', 'carpet', 'cloth', 'concrete', 'concrete_block', 'default', 'dirt', 'flesh', 'flyerflesh', 'foliage', 'glass', 'glass_breakable', 'glassbottle', 'grass', 'gravel', 'grenade', 'grenade_triple_threat', 'ice', 'metal', 'metal_barrel', 'metal_bouncy', 'metal_box', 'metal_spectre', 'metal_titan', 'metalgrate', 'metalpanel', 'metalvehicle', 'metalvent', 'paper', 'papercup', 'plaster', 'plastic', 'plastic_barrel', 'plastic_barrel_buoyant', 'plastic_box', 'pottery', 'rock', 'rubber', 'rubbertire', 'sand', 'shellcasing_large', 'shellcasing_small', 'solidmetal', 'stone', 'tile', 'upholstery', 'water', 'weapon', 'wood', 'wood_box', 'wood_furniture', 'wood_plank', 'wood_solid', 'xo_shield']

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

    rpak_cpu_toggle: bpy.props.BoolProperty( default=False )

    rpak_unkFlags: bpy.props.IntProperty( default=4 )
    rpak_depthStencilFlags: bpy.props.IntProperty( default=23 )
    rpak_rasterizerFlags: bpy.props.IntProperty( default=6 )

    c_fogColorFactor: bpy.props.FloatProperty( default=1.0000, name="c_fogColorFactor", min= 0.0, max = 100.0 )
    c_layerBlendRamp: bpy.props.FloatProperty( default=0.000000, name="c_layerBlendRamp", min= 0.0, max = 100.0 )
    c_opacity: bpy.props.FloatProperty( default=1.0000, name="c_opacity", min= 0.0, max = 100.0 )
    c_useAlphaModulateSpecular: bpy.props.FloatProperty( default=0.0000, name="c_useAlphaModulateSpecular", min= 0.0, max = 100.0 )
    c_alphaEdgeFadeExponent: bpy.props.FloatProperty( default=0.0000, name="c_alphaEdgeFadeExponent", min= 0.0, max = 100.0 )
    c_alphaEdgeFadeOuter: bpy.props.FloatProperty( default=0.0000, name="c_alphaEdgeFadeOuter", min= 0.0, max = 100.0 )
    c_alphaEdgeFadeInner: bpy.props.FloatProperty( default=0.0000, name="c_alphaEdgeFadeInner", min= 0.0, max = 100.0 )
    c_useAlphaModulateEmissive: bpy.props.FloatProperty( default=1.0000, name="c_useAlphaModulateEmissive", min= 0.0, max = 100.0 )
    c_emissiveEdgeFadeExponent: bpy.props.FloatProperty( default=0.0000, name="c_emissiveEdgeFadeExponent", min= 0.0, max = 100.0 )
    c_emissiveEdgeFadeInner: bpy.props.FloatProperty( default=1.0000, name="c_emissiveEdgeFadeInner", min= 0.0, max = 100.0 )
    c_emissiveEdgeFadeOuter: bpy.props.FloatProperty( default=1.0000, name="c_emissiveEdgeFadeOuter", min= 0.0, max = 100.0 )
    c_alphaDistanceFadeScale: bpy.props.FloatProperty( default=10000.0000, name="c_alphaDistanceFadeScale", min= 0.0, max = 100000.0 )
    c_alphaDistanceFadeBias: bpy.props.FloatProperty( default=0.0000, name="c_alphaDistanceFadeBias", min= 0.0, max = 100.0 )
    c_alphaTestReference: bpy.props.FloatProperty( default=0.0000, name="c_alphaTestReference", min= 0.0, max = 100.0 )
    c_aspectRatioMulV: bpy.props.FloatProperty( default=1.7780, name="c_aspectRatioMulV", min= 0.0, max = 100.0 )
    c_shadowBias: bpy.props.FloatProperty( default=0.0000, name="c_shadowBias", min= 0.0, max = 100.0 )
    c_tsaaDepthAlphaThreshold: bpy.props.FloatProperty( default=0.0000, name="c_tsaaDepthAlphaThreshold", min= 0.0, max = 100.0 )
    c_tsaaMotionAlphaThreshold: bpy.props.FloatProperty( default=0.9000, name="c_tsaaMotionAlphaThreshold", min= 0.0, max = 100.0 )
    c_tsaaMotionAlphaRamp: bpy.props.FloatProperty( default=10.0000, name="c_tsaaMotionAlphaRamp", min= 0.0, max = 100.0 ) = 10.000000;
    c_dofOpacityLuminanceScale: bpy.props.FloatProperty( default=1.0000, name="c_dofOpacityLuminanceScale", min= 0.0, max = 100.0 )

	#Vector3 pad_CBufUberStatic = { -nan, -nan, -nan }; add in byte later on, not visible

    c_perfGloss: bpy.props.FloatProperty( default=1.0000, name="c_perfGloss", min= 0.0, max = 100.0 )
    c_perfSpecColor: bpy.props.FloatVectorProperty( default=(0.030000, 0.030000, 0.030000), name="c_perfSpecColor", subtype="COLOR", min= 0.0, max = 100.0 ) #selfillum for the material

    c_uv1RotScaleX_x: bpy.props.FloatProperty(default=1.0)
    c_uv1RotScaleX_y: bpy.props.FloatProperty(default=0.0)
    c_uv1RotScaleY_x: bpy.props.FloatProperty(default=0.0)
    c_uv1RotScaleY_y: bpy.props.FloatProperty(default=1.0)
    c_uv1Translate_x: bpy.props.FloatProperty(default=0.0)
    c_uv1Translate_y: bpy.props.FloatProperty(default=0.0)
    c_uv2RotScaleX_x: bpy.props.FloatProperty(default=1.0)
    c_uv2RotScaleX_y: bpy.props.FloatProperty(default=0.0)
    c_uv2RotScaleY_x: bpy.props.FloatProperty(default=0.0)
    c_uv2RotScaleY_y: bpy.props.FloatProperty(default=1.0)
    c_uv2Translate_x: bpy.props.FloatProperty(default=0.0)
    c_uv2Translate_y: bpy.props.FloatProperty(default=0.0)
    c_uv3RotScaleX_x: bpy.props.FloatProperty(default=1.0)
    c_uv3RotScaleX_y: bpy.props.FloatProperty(default=0.0)
    c_uv3RotScaleY_x: bpy.props.FloatProperty(default=0.0)
    c_uv3RotScaleY_y: bpy.props.FloatProperty(default=1.0)
    c_uv3Translate_x: bpy.props.FloatProperty(default=0.0)
    c_uv3Translate_y: bpy.props.FloatProperty(default=0.0)
    c_uvDistortionIntensity_x: bpy.props.FloatProperty(default=0.0) 
    c_uvDistortionIntensity_y: bpy.props.FloatProperty(default=0.0) 
    c_uvDistortion2Intensity_x: bpy.props.FloatProperty(default=0.0)
    c_uvDistortion2Intensity_y: bpy.props.FloatProperty(default=0.0)

    rpak_preset: bpy.props.StringProperty( default="") #preset for the rpak https://github.com/EM4Volts/RePak/blob/2098bbf9f446c0bc62a8eee438b6998560b0885e/src/assets/material.cpp#L301

    rpak_enable_blendstates: bpy.props.BoolProperty( default=False ) #whether or not to use a manual shaderset for the rpak

    rpak_manual_shaderset: bpy.props.StringProperty( default="0xBD04CCCC982F8C15" ) #manual shaderset for the rpak

    rpak_faceflags: bpy.props.IntProperty( default=6 ) #face flags for the material
    
    rpak_surfacetype: bpy.props.EnumProperty( items=[ (sprop, sprop, "") for sprop in surface_prop_list ],
                                                default="default" )
    rpak_subtype: bpy.props.StringProperty( default="viewmodel" ) #subtype for the material
    rpak_type: bpy.props.StringProperty( default="skn" ) #type for the material

    rpak_flag_1: bpy.props.StringProperty( default="1D0300" ) #flag 1 for the material
    rpak_flag_2: bpy.props.StringProperty( default="10000056000020" ) #flag 2 for the material

    rpak_selfillum_enabled: bpy.props.BoolProperty( default=False ) #whether or not selfillum is enabled for the material

    rpak_selfillum: bpy.props.FloatVectorProperty( default=(0.0, 0.0, 0.0), name="Emissive Tint", subtype="COLOR", min= 0.0, max = 100.0 ) #selfillum for the material

    rpak_albedoTint: bpy.props.FloatVectorProperty( default=(1.000000, 1.000000, 1.000000), name="Albedo Tint", subtype="COLOR", min= 0.001, max = 100.0 ) #selfillum for the material

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


    rpak_blendState0: bpy.props.StringProperty( default="4027809796" )
    rpak_blendState1: bpy.props.StringProperty( default="4027809796" )
    rpak_blendState2: bpy.props.StringProperty( default="4027809796" )
    rpak_blendState3: bpy.props.StringProperty( default="1277956" )

    #       _  _ ____ ___ ____ ____ _ ____ _       ____ _  _ ____ ____ ____ _ ___  ____ ____
    #       |\/| |__|  |  |___ |__/ | |__| |       |  | |  | |___ |__/ |__/ | |  \ |___ [__
    #       |  | |  |  |  |___ |  \ | |  | |___    |__|  \/  |___ |  \ |  \ | |__/ |___ ___]


    material_override_enabled: bpy.props.BoolProperty( default=False ) #whether or not to override the material

    material_override_path: bpy.props.StringProperty( default="" ) # type: ignore #full material path to override the material with



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



        box = layout.column()

        row = box.column()
        row.operator( "perimeter.add_material", text="Add Material", icon="ADD" )
        if len( bpy.context.scene.perimeter_material_main_collection ) > 0:
            row.operator( "perimeter.remove_material", text="Remove Material", icon="REMOVE" )
            row.operator( "perimeter.empty_rpak_shader", text="Setup Empty RPAK Shader for Material", icon="SHADING_TEXTURE" )
            row.template_list( "PERIMETER_UL_MaterialManagementList", "", context.scene, "perimeter_material_main_collection", context.scene, "perimeter_material_main_collection_index" )

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
                    #row.prop( context.scene, "perimeter_rpak_export_path", text="RPAK Export Path" )
                    row = box.row()
                    row.scale_y = 2.0
                    #row.operator( "perimeter.material_management_panel_export_rpak", text="Export RPAK", icon="EXPORT" )
                    row = box.row()
                    row.label( text="RPAK Asset Path (path without material):" )
                    row.label( text=selected_item_rpak_path )
                    row = box.column()
                    row.prop( context.scene, "perimeter_expand_rpak_slots", text="Show Texture Slots")

                    if context.scene.perimeter_expand_rpak_slots:
                        row.prop( selected_item, "rpak_slot_1", text="1 (col)" )
                        row.prop( selected_item, "rpak_slot_2", text="2 (nml)" )
                        row.prop( selected_item, "rpak_slot_3", text="3 (gls/exp)" )
                        row.prop( selected_item, "rpak_slot_4", text="4 (spc)" )
                        row.prop( selected_item, "rpak_slot_5", text="5 (ilm)" )
                        row.prop( selected_item, "rpak_slot_6", text="6" )
                        row.prop( selected_item, "rpak_slot_7", text="7" )
                        row.prop( selected_item, "rpak_slot_8", text="8" )
                        row.prop( selected_item, "rpak_slot_9", text="9" )
                        row.prop( selected_item, "rpak_slot_10", text="10" )
                        row.prop( selected_item, "rpak_slot_11", text="11" )
                        row.prop( selected_item, "rpak_slot_12", text="12 (ao)" )
                        row.prop( selected_item, "rpak_slot_13", text="13 (cav/cvt)" )
                        row.prop( selected_item, "rpak_slot_14", text="14 (opa)" )
                        row.prop( selected_item, "rpak_slot_15", text="15 (detail)" )
                        row.prop( selected_item, "rpak_slot_16", text="16 (dm_nml)" )  
                        row.prop( selected_item, "rpak_slot_17", text="17 (msk)" )
                        row.prop( selected_item, "rpak_slot_18", text="18" )
                        row.prop( selected_item, "rpak_slot_19", text="19" )
                        row.prop( selected_item, "rpak_slot_20", text="20" )
                        row.prop( selected_item, "rpak_slot_21", text="21" )
                        row.prop( selected_item, "rpak_slot_22", text="22" )
                        row.prop( selected_item, "rpak_slot_23", text="23 (bm)" )
                        row.prop( selected_item, "rpak_slot_24", text="24 (col)" )
                        row.prop( selected_item, "rpak_slot_25", text="25 (nml)" )
                        row.prop( selected_item, "rpak_slot_26", text="26 (gls/exp)" )
                        row.prop( selected_item, "rpak_slot_27", text="27 (spc)" )

                        if not context.scene.perimeter_expand_rpak_slots_advanced:
                            row = box.row()
                        row.operator( "perimeter.refresh_shader", text="Refresh Shader", icon="SHADING_TEXTURE" )



                    #row = box.row()
                    #row.prop( selected_item, "rpak_preset", text="Preset" ) #disabled in favor of PMAT
                    
                    #row = box.row()
                    #row.prop( selected_item, "rpak_shaderset", text="Shaderset" )
                    row = box.column()
                    row.label( text=" " )
                    row.label( text="Material Settings" )
                    row = box.row()
                    #row.prop( selected_item, "rpak_enable_manual_shaderset", text="Enable Manual Shaderset" )
                    row.scale_y = 2.0
                    row.operator( "perimeter.import_pema", text="Import .pma", icon="IMPORT" )
                    row.operator( "perimeter.export_pema", text="Export .pma", icon="EXPORT" )

                    row = box.column()
                    
                    row = box.column()   
                            
                    #row.prop( selected_item, "rpak_preset", text="Repak Internal Preset" )
                    row.prop( selected_item, "rpak_surfacetype", text="Surfacetype" )
                    row.prop( selected_item, "rpak_type", text="Type" )
                    row.prop( selected_item, "rpak_manual_shaderset", text="Shaderset" )
                    row.prop( selected_item, "rpak_flag_1", text="Samplers" )
                    row.prop( selected_item, "rpak_flag_2", text="Flag 2" )
                    row.prop( selected_item, "rpak_unkFlags", text="unkFlags" )
                    row.prop( selected_item, "rpak_depthStencilFlags", text="DepthStencil Flags" )
                    row.prop( selected_item, "rpak_rasterizerFlags", text="Rasterizer Flags" )
                    row.prop( selected_item, "rpak_albedoTint", text="Albedo Tint" )
                    row.prop( selected_item, "rpak_selfillum", text="Emissive Tint" )
                    row.prop( selected_item, "c_perfSpecColor", text="Specular Tint" )

                    row.prop( selected_item, "rpak_enable_blendstates", text="Show Blendstates")

                    if selected_item.rpak_enable_blendstates:
                        row.prop( selected_item, "rpak_blendState0", text="RenderLighting")
                        row.prop( selected_item, "rpak_blendState1", text="RenderAliasing")
                        row.prop( selected_item, "rpak_blendState2", text="RenderDoF")
                        row.prop( selected_item, "rpak_blendState3", text="RenderUnknown")
                    row.prop( selected_item, "rpak_cpu_toggle", text="Shaderproperties")
                    if selected_item.rpak_cpu_toggle:

                        #row.operator( "perimeter.import_cpu", text="Import from CPU file", icon="IMPORT" )
                        #no importer, instead relay values and build cpu file on demand

                        row = box.row()   
                        row.prop( selected_item, "c_uv1RotScaleX_x")
                        row.prop( selected_item, "c_uv1RotScaleX_y")       
                        row = box.row()   
                        row.prop( selected_item, "c_uv1RotScaleY_x")
                        row.prop( selected_item, "c_uv1RotScaleY_y")   
                        row = box.row()   
                        row.prop( selected_item, "c_uv1Translate_x")
                        row.prop( selected_item, "c_uv1Translate_y") 
                        row = box.row()   
                        row.prop( selected_item, "c_uv2RotScaleX_x")
                        row.prop( selected_item, "c_uv2RotScaleX_y") 
                        row = box.row()   
                        row.prop( selected_item, "c_uv2RotScaleY_x")
                        row.prop( selected_item, "c_uv2RotScaleY_y")  
                        row = box.row()   
                        row.prop( selected_item, "c_uv2Translate_x")
                        row.prop( selected_item, "c_uv2Translate_y") 
                        row = box.row()   
                        row.prop( selected_item, "c_uv3RotScaleX_x")
                        row.prop( selected_item, "c_uv3RotScaleX_y")   
                        row = box.row()   
                        row.prop( selected_item, "c_uv3RotScaleY_x")
                        row.prop( selected_item, "c_uv3RotScaleY_y") 
                        row = box.row()   
                        row.prop( selected_item, "c_uv3Translate_x")
                        row.prop( selected_item, "c_uv3Translate_y") 
                        row = box.row()   
                        row.prop( selected_item, "c_uvDistortionIntensity_x")
                        row.prop( selected_item, "c_uvDistortionIntensity_y") 
                        row = box.row()   
                        row.prop( selected_item, "c_uvDistortion2Intensity_x")
                        row.prop( selected_item, "c_uvDistortion2Intensity_y")
                        row = box.column()   
                        row.prop( selected_item, "c_fogColorFactor", text="c_fogColorFactor" )
                        row.prop( selected_item, "c_layerBlendRamp", text="c_layerBlendRamp" )
                        row.prop( selected_item, "c_opacity", text="c_opacity" )
                        row.prop( selected_item, "c_useAlphaModulateSpecular", text="c_useAlphaModulateSpecular" )
                        row.prop( selected_item, "c_alphaEdgeFadeExponent", text="c_alphaEdgeFadeExponent" )
                        row.prop( selected_item, "c_alphaEdgeFadeOuter", text="c_alphaEdgeFadeOuter" )
                        row.prop( selected_item, "c_alphaEdgeFadeInner", text="c_alphaEdgeFadeInner" )
                        row.prop( selected_item, "c_useAlphaModulateEmissive", text="c_useAlphaModulateEmissive" )
                        row.prop( selected_item, "c_emissiveEdgeFadeExponent", text="c_emissiveEdgeFadeExponent" )
                        row.prop( selected_item, "c_emissiveEdgeFadeInner", text="c_emissiveEdgeFadeInner" )
                        row.prop( selected_item, "c_emissiveEdgeFadeOuter", text="c_emissiveEdgeFadeOuter" )
                        row.prop( selected_item, "c_alphaDistanceFadeScale", text="c_alphaDistanceFadeScale" )
                        row.prop( selected_item, "c_alphaDistanceFadeBias", text="c_alphaDistanceFadeBias" )
                        row.prop( selected_item, "c_alphaTestReference", text="c_alphaTestReference" )
                        row.prop( selected_item, "c_aspectRatioMulV", text="c_aspectRatioMulV" )
                        row.prop( selected_item, "c_shadowBias", text="c_shadowBias" )
                        row.prop( selected_item, "c_tsaaDepthAlphaThreshold", text="c_tsaaDepthAlphaThreshold" )
                        row.prop( selected_item, "c_tsaaMotionAlphaThreshold", text="c_tsaaMotionAlphaThreshold" )
                        row.prop( selected_item, "c_tsaaMotionAlphaRamp", text="c_tsaaMotionAlphaRamp" )
                        row.prop( selected_item, "c_dofOpacityLuminanceScale", text="c_dofOpacityLuminanceScale" )
                        row.prop( selected_item, "c_perfGloss", text="c_perfGloss" )
                            

                row = box.row()
                row.prop( selected_item, "material_override_enabled", text="Override Material" )
                if context.scene.qc_file_selected:
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

        layout = self.layout
        row = layout.row()




#         ____  _____  ______ _____         _______ ____  _____   _____
#        / __ \|  __ \|  ____|  __ \     /\|__   __/ __ \|  __ \ / ____|
#       | |  | | |__) | |__  | |__) |   /  \  | | | |  | | |__) | (___
#       | |  | |  ___/|  __| |  _  /   / /\ \ | | | |  | |  _  / \___ \
#       | |__| | |    | |____| | \ \  / ____ \| | | |__| | | \ \ ____) |
#        \____/|_|    |______|_|  \_\/_/    \_\_|  \____/|_|  \_\_____/


class PerimeterMaterialManagementImportPerimeterMaterial(bpy.types.Operator):

    bl_idname = "perimeter.import_pema"
    bl_label = ""
    bl_description = "Imports Perimeter Material (.pma)"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(subtype="FILE_PATH", name="File Path", description="File path for loading the .pma file")
    filename: StringProperty(name="File Name", description="Name of the .pma file to be loaded")

    def execute(self, context):
        selected_index = context.scene.perimeter_material_main_collection_index
        material = context.scene.perimeter_material_main_collection[selected_index]   
        # Combine the file path and the file name
        filepath = bpy.path.ensure_ext(self.filepath, ".pma")
        # Perform load

        loaded_pma = PEMA_FILE
        loaded_pma.read_pema(loaded_pma, filepath)


        material.rpak_unkFlags                = loaded_pma.rpak_unkFlags                          
        material.rpak_depthStencilFlags       = loaded_pma.rpak_depthStencilFlags                 
        material.rpak_rasterizerFlags         = loaded_pma.rpak_rasterizerFlags    
              
        material.rpak_manual_shaderset        = "0x" + hex(loaded_pma.rpak_manual_shaderset).upper()[2:]      
        material.rpak_flag_1                  = hex(loaded_pma.rpak_flag_1)[2:].upper()          
        material.rpak_flag_2                  = hex(loaded_pma.rpak_flag_2)[2:].upper()         

        material.rpak_blendState0             = str(loaded_pma.rpak_blendState0)
        material.rpak_blendState1             = str(loaded_pma.rpak_blendState1)
        material.rpak_blendState2             = str(loaded_pma.rpak_blendState2)
        material.rpak_blendState3             = str(loaded_pma.rpak_blendState3)
        material.rpak_albedoTint[0]           = loaded_pma.rpak_albedoTint.x      
        material.rpak_albedoTint[1]           = loaded_pma.rpak_albedoTint.y
        material.rpak_albedoTint[2]           = loaded_pma.rpak_albedoTint.z  

        material.rpak_selfillum[0]            = loaded_pma.rpak_selfillum.x
        material.rpak_selfillum[1]            = loaded_pma.rpak_selfillum.y
        material.rpak_selfillum[2]            = loaded_pma.rpak_selfillum.z

        material.c_perfSpecColor[0]           = loaded_pma.c_perfSpecColor.x
        material.c_perfSpecColor[1]           = loaded_pma.c_perfSpecColor.y
        material.c_perfSpecColor[2]           = loaded_pma.c_perfSpecColor.z
                 

        material.c_uv1RotScaleX_x             = loaded_pma.c_uv1RotScaleX_x
        material.c_uv1RotScaleX_y             = loaded_pma.c_uv1RotScaleX_y
        material.c_uv1RotScaleY_x             = loaded_pma.c_uv1RotScaleY_x
        material.c_uv1RotScaleY_y             = loaded_pma.c_uv1RotScaleY_y
        material.c_uv1Translate_x             = loaded_pma.c_uv1Translate_x
        material.c_uv1Translate_y             = loaded_pma.c_uv1Translate_y
        material.c_uv2RotScaleX_x             = loaded_pma.c_uv2RotScaleX_x
        material.c_uv2RotScaleX_y             = loaded_pma.c_uv2RotScaleX_y
        material.c_uv2RotScaleY_x             = loaded_pma.c_uv2RotScaleY_x
        material.c_uv2RotScaleY_y             = loaded_pma.c_uv2RotScaleY_y
        material.c_uv2Translate_x             = loaded_pma.c_uv2Translate_x
        material.c_uv2Translate_y             = loaded_pma.c_uv2Translate_y
        material.c_uv3RotScaleX_x             = loaded_pma.c_uv3RotScaleX_x
        material.c_uv3RotScaleX_y             = loaded_pma.c_uv3RotScaleX_y
        material.c_uv3RotScaleY_x             = loaded_pma.c_uv3RotScaleY_x
        material.c_uv3RotScaleY_y             = loaded_pma.c_uv3RotScaleY_y
        material.c_uv3Translate_x             = loaded_pma.c_uv3Translate_x
        material.c_uv3Translate_y             = loaded_pma.c_uv3Translate_y
        material.c_uvDistortionIntensity_x    = loaded_pma.c_uvDistortionIntensity_x
        material.c_uvDistortionIntensity_y    = loaded_pma.c_uvDistortionIntensity_y
        material.c_uvDistortion2Intensity_x   = loaded_pma.c_uvDistortion2Intensity_x
        material.c_uvDistortion2Intensity_y   = loaded_pma.c_uvDistortion2Intensity_y

        material.c_fogColorFactor             = loaded_pma.c_fogColorFactor                
        material.c_layerBlendRamp             = loaded_pma.c_layerBlendRamp                
        material.c_opacity                    = loaded_pma.c_opacity                   
        material.c_useAlphaModulateSpecular   = loaded_pma.c_useAlphaModulateSpecular                          
        material.c_alphaEdgeFadeExponent      = loaded_pma.c_alphaEdgeFadeExponent                         
        material.c_alphaEdgeFadeOuter         = loaded_pma.c_alphaEdgeFadeOuter                        
        material.c_alphaEdgeFadeInner         = loaded_pma.c_alphaEdgeFadeInner                        
        material.c_useAlphaModulateEmissive   = loaded_pma.c_useAlphaModulateEmissive                          
        material.c_emissiveEdgeFadeExponent   = loaded_pma.c_emissiveEdgeFadeExponent                          
        material.c_emissiveEdgeFadeInner      = loaded_pma.c_emissiveEdgeFadeInner                         
        material.c_emissiveEdgeFadeOuter      = loaded_pma.c_emissiveEdgeFadeOuter                         
        material.c_alphaDistanceFadeScale     = loaded_pma.c_alphaDistanceFadeScale                        
        material.c_alphaDistanceFadeBias      = loaded_pma.c_alphaDistanceFadeBias                         
        material.c_alphaTestReference         = loaded_pma.c_alphaTestReference                        
        material.c_aspectRatioMulV            = loaded_pma.c_aspectRatioMulV                       
        material.c_shadowBias                 = loaded_pma.c_shadowBias                        
        material.c_tsaaDepthAlphaThreshold    = loaded_pma.c_tsaaDepthAlphaThreshold                       
        material.c_tsaaMotionAlphaThreshold   = loaded_pma.c_tsaaMotionAlphaThreshold                          
        material.c_tsaaMotionAlphaRamp        = loaded_pma.c_tsaaMotionAlphaRamp                       
        material.c_dofOpacityLuminanceScale   = loaded_pma.c_dofOpacityLuminanceScale                          
        material.c_perfGloss                  = loaded_pma.c_perfGloss                 

        material.rpak_surfacetype             = loaded_pma.rpak_surfacetype        
        material.rpak_type                    = loaded_pma.rpak_type 
        material.rpak_subtype                 = loaded_pma.rpak_subtype 























        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout


    def check(self, context):
        return True
    



class PerimeterMaterialManagementExportPerimeterMaterial(bpy.types.Operator):
    bl_idname = "perimeter.export_pema"
    bl_label = ""
    bl_description = "Exports Perimeter Material (.pma)"

    filepath: StringProperty(subtype="FILE_PATH", name="File Path", description="File path for saving the .pma file")
    filename: StringProperty(name="File Name", description="Name of the .pma file to be saved")

    def execute(self, context):
        selected_index = context.scene.perimeter_material_main_collection_index
        material = context.scene.perimeter_material_main_collection[selected_index]   
        # Combine the file path and the file name
        filepath = bpy.path.ensure_ext(self.filepath, ".pma")
        # Perform save operation here
        self.report({'INFO'}, "File Saved: " + filepath)

        PEMA_FILE.make_material_file_from_blender_material_collection(PEMA_FILE, filepath, material)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        #layout.prop(self, "filepath")
        #layout.prop(self, "filename")

    def check(self, context):
        return True


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

        setup_shader( selected_item.blender_material, "", False, True, True, True)

        selected_item.rpak_shader_is_set = True
        selected_item.export_rpak = True
        selected_item.blender_material.name = selected_item.blender_material.name.replace('\\', '/')


        return {'FINISHED'}



class PerimeterRefreshShader( Operator ):
    bl_idname = "perimeter.refresh_shader"
    bl_label = "Refresh Shader in Viewport"
    bl_description = "Refreshes the shader for the currently selected material"

    def execute( self, context ):
        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]

        for node in selected_item.blender_material.node_tree.nodes:

            if node.type == "TEX_IMAGE":
                if node.label == "Col":
                    if selected_item.rpak_slot_1 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_1 )
                    else:
                        node.image = None

                elif node.label == "Nml":
                    if selected_item.rpak_slot_2 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_2 )
                    else:
                        node.image = None

                elif node.label == "Gls":
                    if selected_item.rpak_slot_3 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_3 )
                    else:
                        node.image = None

                elif node.label == "Spc":
                    if selected_item.rpak_slot_4 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_4 )
                    else:
                        node.image = None

                elif node.label == "Ilm":
                    if selected_item.rpak_slot_5 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_5 )
                    else:
                        node.image = None

                elif node.label == "Ao":
                    if selected_item.rpak_slot_12 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_12 )
                    else:
                        node.image = None

                elif node.label == "Cav":
                    if selected_item.rpak_slot_13 != "None":
                        node.image = bpy.data.images.load( selected_item.rpak_slot_13 )
                    else:
                        node.image = None






        return {'FINISHED'}



class PerimeterMaterialManagementPanelExportRPAK( Operator ):
    bl_idname = "perimeter.material_management_panel_export_rpak"
    bl_label = "Export RPAK"
    bl_description = "Exports the currently selected material to an RPAK"

    def execute( self, context ):
        selected_index = bpy.context.scene.perimeter_material_main_collection_index
        selected_item = bpy.context.scene.perimeter_material_main_collection[selected_index]
        addon_prefs = context.preferences.addons[__package__].preferences


        if selected_item.rpak_shader_is_set:
            if selected_item.export_rpak:
                if addon_prefs.repak_path == "":
                    self.report( {'ERROR'}, "RPAK Export Path not set, set in Preferences" )
                    return {'CANCELLED'}
                else:
                    perimeter_make_refactor_rpak( context, "single_mat" )
            else:
                self.report( {'ERROR'}, "Export RPAK is not enabled for this material" )
                return {'CANCELLED'}
        else:
            self.report( {'ERROR'}, "RPAK Shader is not set for this material" )
            return {'CANCELLED'}

        return {'FINISHED'}



#       ______ _    _ _   _  _____ _______ _____ ____  _   _  _____
#      |  ____| |  | | \ | |/ ____|__   __|_   _/ __ \| \ | |/ ____|
#      | |__  | |  | |  \| | |       | |    | || |  | |  \| | (___
#      |  __| | |  | | . ` | |       | |    | || |  | | . ` |\___ \
#      | |    | |__| | |\  | |____   | |   _| || |__| | |\  |____) |
#      |_|     \____/|_| \_|\_____|  |_|  |_____\____/|_| \_|_____/



def perimeter_make_refactor_rpak( context, mode="all_mats"): #refactor repak map maker


    ######################################
    #                                    #
    #  SUPPORTS [2] MODES                #
    #                                    #
    #  all_mats     | make map for       #
    #                 all materials      #
    #                 in scene with      #
    #                 export enabled     #
    #                                    #
    #  single_mat   | make map for       #
    #                 the currently      #
    #                 selected material  #
    #                                    #
    ######################################

    addon_prefs = context.preferences.addons[__package__].preferences
    # never change 
    repak_path = addon_prefs.repak_path

    rpak_export_path = context.scene.perimeter_rpak_export_path



    if mode == "single_mat":
        selected_index = context.scene.perimeter_material_main_collection_index
        material = context.scene.perimeter_material_main_collection[selected_index]        

    materials_to_export = []
    if mode == "all_mats":
        for material in bpy.context.scene.perimeter_material_main_collection:
            if material.export_rpak:
                materials_to_export.append(material)
        if not len(materials_to_export) == 0:
            map_returned= perimeter_make_refactor_map(materials_to_export)
            map_path = map_returned[0]
            source_png_list = map_returned[1]
            destination_png_list = map_returned[2]
            material_paths_list = map_returned[3]
            cpu_file_queue = map_returned[4]

            for mat_path in material_paths_list:
                mat_path = mat_path.replace("\\", "/").replace("//", "/")
                if not os.path.exists( mat_path ):
                    os.makedirs( mat_path )

            #make cpu files
            for queued_cpu_file in cpu_file_queue:
                make_cpu(queued_cpu_file[0], queued_cpu_file[1])

            if len(source_png_list) == len(destination_png_list):
                for i in range(len(source_png_list)):
                    shutil.copy( source_png_list[i], destination_png_list[i] + ".png")
                    time.sleep(0.1)

            for material_path in material_paths_list:
                convert_textures( addon_prefs.texconv_path, material_path)

        cmd = f'"{repak_path}" "{map_path}"'
    
        call( cmd, shell=True )
    
        os.remove(map_path)
    
        shutil.rmtree(os.path.dirname(repak_path) + "/perimeter_assets/")


def perimeter_return_materialoverrides( context ):
    materialoverrides = []
    for material in bpy.context.scene.perimeter_material_main_collection:
        if material.material_override_enabled:
            override_line = '$renamematerial "' + material.blender_material.name + '" "' + material.material_override_path + '"'
            materialoverrides.append( override_line )
    return materialoverrides