import json, os, sys, shutil, subprocess




def make_rpak_map( material_name, material_path, material_textures, repak_path ):
    preset_json ={

        "name": "",
        "assetsDir": "../assets",
        "outputDir": "../rpaks",
        "starpakPath":"",
        "version": 7,
        "visibilityflags": "opaque",
        "faceflags": 6,
        "files":[

        ]
    }
    rpak_map_json = preset_json
    rpak_map_json["name"] = f'perimeter_{material_name}.rpak'
    rpak_map_json["starpakPath"] = f'perimeter_{material_name}.starpak'

    mtl_texturres_list = [ "", "", "", "", "", "", "", "", "", "", "", "", "" ]  
    
    for texture in material_textures:
        if texture != None:
            rpak_map_json["files"].append( { "$type":"txtr","path":f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", ""),"saveDebugName": True} )
            #replace the empty strings in the mtl_textures_list with the texture names based on the index of the texture in the material_textures list
            #check for index of texture in material_textures list 
            texture_index = material_textures.index(texture)
            if texture_index == 0:
                if not texture == None:
                    mtl_texturres_list[0] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[0] = ""
            elif texture_index == 1:
                if not texture == None:
                    mtl_texturres_list[1] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[1] = ""
            elif texture_index == 2:
                if not texture == None:
                    mtl_texturres_list[2] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[2] = ""
            elif texture_index == 3:
                if not texture == None:
                    mtl_texturres_list[3] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[3] = ""
            elif texture_index == 4:
                if not texture == None:
                    mtl_texturres_list[4] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[4] = ""
            elif texture_index == 5:
                if not texture == None:
                    mtl_texturres_list[11] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[11] = ""
            elif texture_index == 6:
                if not texture == None:
                    mtl_texturres_list[12] = f'{material_path}/{os.path.basename(texture)}'.replace("//", "/").replace(".png", "").replace(".jpg", "").replace(".tga", "")
                else:
                    mtl_texturres_list[12] = ""


    

    #append this part into the files list of the rpak map json and populate with the right texture paths: 		{"$type":"matl","visibilityflags": "opaque","faceflags": 6,"version":12,"path":"","type": "skn","subtype":"viewmodel","surface": "default","width": 2048,"height": 2048,"selfillumtint": [1.0, 1.0, 1.0],"textures":["col","nml","gls","spc","","","","","","","","ao","cav"]   }		
    rpak_map_json["files"].append( { "$type":"matl","visibilityflags": "opaque","faceflags": 6,"version":12,"path":f'{material_path}/{material_name}',"type": "skn","subtype":"viewmodel","surface": "default","width": 2048,"height": 2048,"selfillumtint": [1.0, 1.0, 1.0],"textures":mtl_texturres_list   } )
   
    json.dump(rpak_map_json, open(f"{repak_path}/maps/perimeter_repak_map_{material_name}.json", "w"), indent=4)

def convert_textures( texconv_path, asset_path ):
     for filename in os.scandir(asset_path):
          if filename.name.endswith("nml.png"):
               os.system(f"{texconv_path} -f BC5_UNORM -srgb -ft dds " + filename.path + " -o " + asset_path)
          else:
               if filename.name.endswith("gls.png"):
                    os.system(f"{texconv_path} -f BC4_UNORM -srgbi -ft dds " + filename.path + " -o " + asset_path)
               else:
                    os.system(f"{texconv_path} -f BC1_UNORM_SRGB -srgbi -ft dds " + filename.path + " -o " + asset_path)