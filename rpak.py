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

import json, os, sys, shutil, subprocess, bpy, secrets
from .ioUtils import *



def convert_textures( texconv_path, asset_path ):
     for filename in os.scandir(asset_path):
        if filename.name.endswith("nml.png"):
            tex_conv_args_list = [texconv_path, "-f", "BC5_UNORM", "-srgb", "-ft", "dds", filename.path, "-o", asset_path]
        else:
            if filename.name.endswith("gls.png"):
                tex_conv_args_list = [texconv_path, "-f", "BC4_UNORM", "-srgbi", "-ft", "dds", filename.path, "-o", asset_path]
            else:
                tex_conv_args_list = [texconv_path, "-f", "BC1_UNORM_SRGB", "-srgbi", "-ft", "dds", filename.path, "-o", asset_path]

        subprocess.call( tex_conv_args_list , shell=True )






def perimeter_make_refactor_map(materials):

    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    if bpy.context.scene.compiled_mod_name == "":
        packed_rpak_name = secrets.token_hex(16) #we just generate a long name that hopefully will NEVER collide with another random name (duplicate name rpak loading bad)
    else:
        packed_rpak_name = bpy.context.scene.compiled_mod_name[:12] + "_" + secrets.token_hex(8) #generate somewhat recognizeable name (hoping for uniquenes with secrets)

    preset_json ={

        "name": "",
        "assetsDir": "../perimeter_assets",
        "outputDir": "../perimeter_rpaks",
        "starpakPath":"",
        "version": 7,
        "files":[
        ]
    }

    
    #generate rpak "header"

    rpak_map_header = preset_json

    rpak_map_header["name"] = packed_rpak_name
    rpak_map_header["outputDir"] = bpy.context.scene.perimeter_rpak_export_path
    rpak_map_header["assetsDir"] = os.path.dirname(addon_prefs.repak_path) + "/perimeter_assets"
    rpak_map_header["starpakPath"] = packed_rpak_name + ".starpak" 

    materials_oldname_list = []
    materials_newname_list = []
    materials_paths_list = []
    cpu_file_queue = []


    for material in materials:


        preset_material_sub_json = {
            "$type": "matl",
            "surface": "",
            "path": "",
            "type": "",
            "samplers": "1D0300",
            "flags2": "56000020",
            "cpuPath": "",
            "width": 512,
            "height": 512,
            "shaderset": "0xBD04CCCC982F8C15",
            "unkFlags": "",
            "depthStencilFlags": "",
            "rasterizerFlags": "",
            "blendState0": 0,
            "blendState1": 0,
            "blendState2": 0,
            "blendState3": 0,
            "emissiveTint": [
                1.0,
                1.0,
                1.0
            ],
            "albedoTint": [
                1.0,
                1.0,
                1.0
            ],
            "textures": []
        }
        new_material_json = preset_material_sub_json

        material_path = material.blender_material.name.replace("\\", "/").replace("//", "/").split("/")
        material_path = "/".join( material_path[:-1] ) + "/"

        normalized_selfillum = []
        for selfillum in material.rpak_selfillum:
            normalized_selfillum.append( float( str(selfillum)[:4] ) )

        normalized_albedotint = []
        for albedotint in material.rpak_albedoTint:
            normalized_albedotint.append( float( str(albedotint)[:4] ) )
        material_slots = [
        material.rpak_slot_1, 
        material.rpak_slot_2, 
        material.rpak_slot_3, 
        material.rpak_slot_4, 
        material.rpak_slot_5, 
        material.rpak_slot_6, 
        material.rpak_slot_7, 
        material.rpak_slot_8, 
        material.rpak_slot_9, 
        material.rpak_slot_10, 
        material.rpak_slot_11, 
        material.rpak_slot_12, 
        material.rpak_slot_13, 
        material.rpak_slot_14, 
        material.rpak_slot_15, 
        material.rpak_slot_16, 
        material.rpak_slot_17, 
        material.rpak_slot_18, 
        material.rpak_slot_19, 
        material.rpak_slot_20, 
        material.rpak_slot_21, 
        material.rpak_slot_22, 
        material.rpak_slot_23, 
        material.rpak_slot_24, 
        material.rpak_slot_25, 
        material.rpak_slot_26, 
        material.rpak_slot_27
        ]


        normalized_slots = []
        material_slot_index = 0
        for rpak_slot in material_slots:
            material_slot_index += 1 
            #make rpak map, directories based on name, eg [asset dir] / [material path without mat name] / file names named after [materialname] + 2 byte hex id + slot id
            if rpak_slot == "None":
                normalized_slots.append("")
            else:
                if rpak_slot.endswith(".png"):
                    normalized_slot_name = material.blender_material.name.split("/")[-1] + secrets.token_hex(4) + "_slot_" + str(material_slot_index)

                    if normalized_slot_name.startswith("/"):
                        normalized_slot_name = normalized_slot_name[1:]


                    
                    normalized_slots.append( material_path + normalized_slot_name.replace("//", "/").removesuffix(".png") )
                    materials_newname_list.append( rpak_map_header["assetsDir"] + "/" + material_path + normalized_slot_name.replace("//", "/").removesuffix(".png") )
                    materials_oldname_list.append( rpak_slot )

                else:
                    normalized_slots.append("")
        rpak_material_name = material.blender_material.name.replace("\\", "/").replace("//", "/").split("/")[-1] 
        print(rpak_material_name)
        material_cpu_path = material_path + material.blender_material.name.split("/")[-1] + ".cpu"

 

        new_material_json["surface"] = material.rpak_surfacetype
        new_material_json["path"] = f'{material_path}/{rpak_material_name}'.replace("//", "/")
        new_material_json["type"] = material.rpak_type
        new_material_json["samplers"] = material.rpak_flag_1
        new_material_json["flags2"] = material.rpak_flag_2
        new_material_json["unkFlags"]   = material.rpak_unkFlags
        new_material_json["depthStencilFlags"]  = material.rpak_depthStencilFlags
        new_material_json["rasterizerFlags"]    = material.rpak_rasterizerFlags
        new_material_json["shaderset"] = material.rpak_manual_shaderset
        new_material_json["blendState0"] = int(material.rpak_blendState0)
        new_material_json["blendState1"] = int(material.rpak_blendState1)
        new_material_json["blendState2"] = int(material.rpak_blendState2)
        new_material_json["blendState3"] = int(material.rpak_blendState3)
        new_material_json["cpuPath"] = material_cpu_path
        new_material_json["emissiveTint"] = normalized_selfillum
        new_material_json["albedoTint"] = normalized_albedotint
        for slot in normalized_slots:
            new_material_json["textures"].append(slot.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", ""))

        materials_paths_list.append(os.path.dirname(addon_prefs.repak_path) + "/perimeter_assets/" + material_path)

        cpu_file_queue.append([material_cpu_path, material])
        rpak_map_header["files"].append(new_material_json)

    repak_path = os.path.dirname(addon_prefs.repak_path) 

    json_map_name = f'{repak_path}/{packed_rpak_name}_perimeter_map.json'
    json.dump(rpak_map_header, open(f"{json_map_name}", "w"), indent=4)

#return both the path to the map aswell as a list of all the NEW image names and the path to copy to, returns in right sequence of norm
    return json_map_name, materials_oldname_list, materials_newname_list, materials_paths_list, cpu_file_queue
                       

def make_cpu(path, material): #writes a 224 bytes big cpu struct file to the given path with the given shader properties of [material]
    #make new file
    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    cpu_file = open(os.path.dirname(addon_prefs.repak_path) + "/perimeter_assets/" + path, "wb+")

    cpu_first_skip_segment = [ material.c_uv1RotScaleX_x, 
    material.c_uv1RotScaleX_y, 
    material.c_uv1RotScaleY_x, 
    material.c_uv1RotScaleY_y, 
    material.c_uv1Translate_x, 
    material.c_uv1Translate_y, 
    material.c_uv2RotScaleX_x, 
    material.c_uv2RotScaleX_y, 
    material.c_uv2RotScaleY_x, 
    material.c_uv2RotScaleY_y, 
    material.c_uv2Translate_x, 
    material.c_uv2Translate_y, 
    material.c_uv3RotScaleX_x, 
    material.c_uv3RotScaleX_y, 
    material.c_uv3RotScaleY_x, 
    material.c_uv3RotScaleY_y, 
    material.c_uv3Translate_x, 
    material.c_uv3Translate_y, 
    material.c_uvDistortionIntensity_x, 
    material.c_uvDistortionIntensity_y, 
    material.c_uvDistortion2Intensity_x, 
    material.c_uvDistortion2Intensity_y
    ]

    #write the first part of the cpu that is currently not user changable

    for cpu_part in cpu_first_skip_segment:
        write_float(cpu_file, cpu_part)




    write_float(cpu_file, material.c_fogColorFactor)
    write_float(cpu_file, material.c_layerBlendRamp)



    normalized_albedotint = []
    for albedotint in material.rpak_albedoTint:
        normalized_albedotint.append( float( str(albedotint)[:4] ) )

    #WRITE ALBEDOTINT HERE

    for alb_float in normalized_albedotint:
        write_float(cpu_file, alb_float)

    write_float(cpu_file, material.c_opacity)
    write_float(cpu_file, material.c_useAlphaModulateSpecular)
    write_float(cpu_file, material.c_alphaEdgeFadeExponent)
    write_float(cpu_file, material.c_alphaEdgeFadeInner)
    write_float(cpu_file, material.c_alphaEdgeFadeOuter)
    write_float(cpu_file, material.c_useAlphaModulateEmissive)
    write_float(cpu_file, material.c_emissiveEdgeFadeExponent)
    write_float(cpu_file, material.c_emissiveEdgeFadeInner)
    write_float(cpu_file, material.c_emissiveEdgeFadeOuter)
    write_float(cpu_file, material.c_alphaDistanceFadeScale)
    write_float(cpu_file, material.c_alphaDistanceFadeBias)
    write_float(cpu_file, material.c_alphaTestReference)
    write_float(cpu_file, material.c_aspectRatioMulV)


    normalized_selfillum = []
    for selfillum in material.rpak_selfillum:
        normalized_selfillum.append( float( str(selfillum)[:4] ) )
    #WRITE EMISSIVETINT
    for ems_float in normalized_selfillum:
        write_float(cpu_file, ems_float)

    write_float(cpu_file, material.c_shadowBias)
    write_float(cpu_file, material.c_tsaaDepthAlphaThreshold)
    write_float(cpu_file, material.c_tsaaMotionAlphaThreshold)
    write_float(cpu_file, material.c_tsaaMotionAlphaRamp)

    write_float(cpu_file, 0)

    write_float(cpu_file, material.c_dofOpacityLuminanceScale)

    #Vector3 pad_CBufUberStatic = { -nan, -nan, -nan };
    
    for i in range(3): write_uInt32(cpu_file, 4294967295)

    write_float(cpu_file, material.c_perfGloss)


    normalized_spectint = []
    for speccol in material.c_perfSpecColor:
        normalized_spectint.append( float( str(speccol)[:4] ) )
    #WRITE EMISSIVETINT
    for spec_float in normalized_spectint:
        write_float(cpu_file, spec_float)

    cpu_file.close()
    """
    
    raw CBufUberStatic struct
    Vector2 c_uv1RotScaleX = { 1.000000, 0.000000 };
    Vector2 c_uv1RotScaleY = { -0.000000, 1.000000 };
    Vector2 c_uv1Translate = { 0.000000, 0.000000 };
    Vector2 c_uv2RotScaleX = { 1.000000, 0.000000 };
    Vector2 c_uv2RotScaleY = { -0.000000, 1.000000 };
    Vector2 c_uv2Translate = { 0.000000, 0.000000 };
    Vector2 c_uv3RotScaleX = { 1.000000, 0.000000 };
    Vector2 c_uv3RotScaleY = { -0.000000, 1.000000 };
    Vector2 c_uv3Translate = { 0.000000, 0.000000 };
    Vector2 c_uvDistortionIntensity = { 0.000000, 0.000000 };
    Vector2 c_uvDistortion2Intensity = { 0.000000, 0.000000 };


    float c_fogColorFactor = 1.000000;
    float c_layerBlendRamp = 0.000000;
    Vector3 c_albedoTint = { 1.000000, 1.000000, 1.000000 };
    float c_opacity = 1.000000;
    float c_useAlphaModulateSpecular = 0.000000;
    float c_alphaEdgeFadeExponent = 0.000000;
    float c_alphaEdgeFadeInner = 0.000000;
    float c_alphaEdgeFadeOuter = 0.000000;
    float c_useAlphaModulateEmissive = 1.000000;
    float c_emissiveEdgeFadeExponent = 0.000000;
    float c_emissiveEdgeFadeInner = 0.000000;
    float c_emissiveEdgeFadeOuter = 0.000000;
    float c_alphaDistanceFadeScale = 10000.000000;
    float c_alphaDistanceFadeBias = -0.000000;
    float c_alphaTestReference = 0.000000;
    float c_aspectRatioMulV = 1.778000;
    Vector3 c_emissiveTint = { 0.000000, 0.000000, 0.000000 };
    float c_shadowBias = 0.000000;
    float c_tsaaDepthAlphaThreshold = 0.000000;
    float c_tsaaMotionAlphaThreshold = 0.900000;
    float c_tsaaMotionAlphaRamp = 10.000000;
    char UNIMPLEMENTED_c_tsaaResponsiveFlag[4];
    float c_dofOpacityLuminanceScale = 1.000000;
    Vector3 pad_CBufUberStatic = { -nan, -nan, -nan };
    float c_perfGloss = 1.000000;
    Vector3 c_perfSpecColor = { 0.030000, 0.030000, 0.030000 };"""
   
    #final size in bytes of the finished cpu should be 224