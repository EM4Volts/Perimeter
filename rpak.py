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

import json, os, sys, shutil, subprocess, bpy

def convert_textures( texconv_path, asset_path ):
     for filename in os.scandir(asset_path):
          if filename.name.endswith("nml.png"):
               os.system(f"{texconv_path} -f BC5_UNORM -srgb -ft dds " + filename.path + " -o " + asset_path)
          else:
               if filename.name.endswith("gls.png"):
                    os.system(f"{texconv_path} -f BC4_UNORM -srgbi -ft dds " + filename.path + " -o " + asset_path)
               else:
                    os.system(f"{texconv_path} -f BC1_UNORM_SRGB -srgbi -ft dds " + filename.path + " -o " + asset_path)


def perimeter_make_rpak_map( rpak_params, rpak_slots, slot_map_names, material_slot_name):

    addon_prefs = bpy.context.preferences.addons[__package__].preferences

    #rpak_params = { "rpak_surface_type": rpak_surface_type ,"rpak_subtype": rpak_subtype, "rpak_type": rpak_type, "rpak_asset_path": rpak_asset_path, "rpak_name": rpak_material_name, "preset": rpak_preset, "shaderset": rpak_shaderset, "faceflags": rpak_faceflags, "visibilityflags": rpak_visibilityflags, "flag_1": rpak_flag_1, "flag_2": rpak_flag_2, "selfillum": rpak_selfillum }

    """
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
    """
    preset_json ={

        "name": "",
        "assetsDir": "../perimeter_assets",
        "outputDir": "../perimeter_rpaks",
        "starpakPath":"",
        "version": 7,
        "visibilityflags": "opaque",
        "faceflags": 6,
        "files":[

        ]
    }

    files_sub_preset_json =   {
            "$type": "matl",
            "visibilityflags": "opaque",
            "faceflags": 6,
            "version": 12,
            "path": "",
            "type": "skn",
            "subtype": "viewmodel",
            "surface": "default",
            "width": 2048,
            "height": 2048,
            "flags": "",
            "flags2": "",
            "shaderset": "",
            "selfillumtint": [
                1.0,
                1.0,
                1.0
            ],
            "textures": [
            ]
        }

    rpak_map_json = preset_json
    rpak_map_json["name"] = rpak_params["rpak_name"]
    rpak_map_json["starpakPath"] = f'{rpak_params["rpak_name"]}.starpak'
    rpak_map_json["visibilityflags"] = rpak_params["visibilityflags"]
    rpak_map_json["faceflags"] = rpak_params["faceflags"]
    rpak_map_json["outputDir"] = rpak_params["rpak_export_path"].replace("//", "/").replace("\\", "/")
    rpak_map_json["assetsDir"] = os.path.dirname(addon_prefs.repak_path) + "/perimeter_assets"

    normalized_slots = []
    for rpak_slot in rpak_slots:
        if rpak_slot == "None":
            normalized_slots.append("")
        else:
            if rpak_slot.endswith(".png"):
                normalized_slot_name = rpak_params["rpak_asset_path"] + "/"+ material_slot_name + slot_map_names[rpak_slots.index(rpak_slot)]

                if normalized_slot_name.startswith("/"):
                    normalized_slot_name = normalized_slot_name[1:]

                normalized_slots.append( normalized_slot_name.replace("//", "/").removesuffix(".png") )
            else:
                normalized_slots.append("")


    for slot in normalized_slots:
        if slot != "":
            rpak_map_json["files"].append( { "$type":"txtr","path":f'{slot}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", ""),"saveDebugName": True} )

    #append this part into the files list of the rpak map json and populate with the right texture paths: 		{"$type":"matl","visibilityflags": "opaque","faceflags": 6,"version":12,"path":"","type": "skn","subtype":"viewmodel","surface": "default","width": 2048,"height": 2048,"selfillumtint": [1.0, 1.0, 1.0],"textures":["col","nml","gls","spc","","","","","","","","ao","cav"]   }


    normalized_selfillum = []
    for selfillum in rpak_params["selfillum"]:
        normalized_selfillum.append( float( str(selfillum)[:4] ) )


    files_sub_preset_json["path"] = f'{rpak_params["rpak_asset_path"]}/{rpak_params["rpak_name"]}'.replace("//", "/")
    files_sub_preset_json["type"] = rpak_params["rpak_type"]
    files_sub_preset_json["subtype"] = rpak_params["rpak_subtype"]
    files_sub_preset_json["surface"] = rpak_params["rpak_surface_type"]
    if not files_sub_preset_json["flags"] == "":
        files_sub_preset_json["flags"] = rpak_params["flag_1"]
    if not files_sub_preset_json["flags2"] == "":
        files_sub_preset_json["flags2"] = rpak_params["flag_2"]
    if not files_sub_preset_json["shaderset"] == "":
        files_sub_preset_json["shaderset"] = rpak_params["shaderset"]
    files_sub_preset_json["selfillumtint"] = normalized_selfillum
    files_sub_preset_json["textures"] = normalized_slots
    files_sub_preset_json["visibilityflags"] = rpak_params["visibilityflags"]

    rpak_map_json["files"].append( files_sub_preset_json )
    

    repak_path = os.path.dirname(addon_prefs.repak_path) 
    json_map_name = f'{repak_path}/perimeter_repak_map_{rpak_params["rpak_name"]}.json'
    json.dump(rpak_map_json, open(f"{json_map_name}", "w"), indent=4)

    return json_map_name