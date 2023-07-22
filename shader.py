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
import bpy, os

def material_map_finder(directory, material_name, ending):
    try:
        for filename in os.listdir(directory + "/" + material_name):
            if filename.endswith(ending):
                return directory + "/" + material_name + "/" + filename
    except:
        return None
  
def shader_on_material( material, paths, append_textures=True):
    # Set "Use Nodes" for the material
    material.use_nodes = True
    # Clear all existing nodes
    material.node_tree.nodes.clear()
    # Create a Principled BSDF shader node
    principled_node = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (0, 0)  # Adjust the location of the node
    # Create an Image Texture node for the Base Color
    basecolor_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    basecolor_texture_node.location = (-1000, 400)  # Adjust the location of the node
    # Create a MixRGB node for blending colors
    mix_color_node = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_color_node.location = (-700, 300)  # Adjust the location of the node
    mix_color_node.blend_type = 'MIX'
    mix_color_node.inputs['Fac'].default_value = 0.2
    mix_color_node.blend_type = 'MULTIPLY'
    # Set the factor to 1
    mix_color_node.inputs['Fac'].default_value = 1.0
    # Create another Image Texture node
    mix_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    mix_texture_node.location = (-1000, 200)  # Adjust the location of the node
    # Create an Image Texture node for the Roughness
    roughness_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    roughness_texture_node.location = (-1000, -200)  # Adjust the location of the node
    # Create a Combine RGB node
    combine_node = material.node_tree.nodes.new(type='ShaderNodeCombineRGB')
    combine_node.location = (-200, -400)  # Adjust the location of the node
    # Create two Separate RGB nodes
    separate1_node = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
    separate1_node.location = (-700, -400)  # Adjust the location of the node
    separate2_node = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
    separate2_node.location = (-700, -600)  # Adjust the location of the node
    # Create an Invert node for Roughness
    invert_node = material.node_tree.nodes.new(type='ShaderNodeInvert')
    invert_node.location = (-700, -200)  # Adjust the location of the node
    # Create an Image Texture node for the Specular
    specular_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    specular_texture_node.location = (-1000, 0)  # Adjust the location of the node
    # Create Image Texture nodes for Split Color outputs
    image_texture1_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    image_texture1_node.location = (-1000, -400)  # Adjust the location of the node
    image_texture2_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    image_texture2_node.location = (-1000, -600)  # Adjust the location of the node
    # Create a Material Output node
    output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)  # Adjust the location of the node
    # Connect the Image Texture nodes to the MixRGB node
    material.node_tree.links.new(basecolor_texture_node.outputs['Color'], mix_color_node.inputs['Color1'])
    material.node_tree.links.new(mix_texture_node.outputs['Color'], mix_color_node.inputs['Color2'])
    # Connect the MixRGB node to the Principled BSDF node
    material.node_tree.links.new(mix_color_node.outputs['Color'], principled_node.inputs['Base Color'])
    # Connect the Image Texture node for Roughness to the Invert node
    material.node_tree.links.new(roughness_texture_node.outputs['Color'], invert_node.inputs['Color'])
    # Connect the Invert node to the Principled BSDF node for Roughness
    material.node_tree.links.new(invert_node.outputs['Color'], principled_node.inputs['Roughness'])
    # Connect the Separate RGB nodes to the Combine RGB node
    material.node_tree.links.new(separate1_node.outputs['R'], combine_node.inputs['R'])
    material.node_tree.links.new(separate1_node.outputs['G'], combine_node.inputs['G'])
    material.node_tree.links.new(separate2_node.outputs['B'], combine_node.inputs['B'])
    # Connect the Combine RGB node to the shader's Normal input
    material.node_tree.links.new(combine_node.outputs['Image'], principled_node.inputs['Normal'])
    # Connect the Image Texture node for Specular to the Specular input
    material.node_tree.links.new(specular_texture_node.outputs['Color'], principled_node.inputs['Specular'])
    # Connect the Image Texture nodes to the Split Color nodes
    material.node_tree.links.new(image_texture1_node.outputs['Color'], separate1_node.inputs['Image'])
    material.node_tree.links.new(image_texture2_node.outputs['Color'], separate2_node.inputs['Image'])
    # Connect the Principled BSDF node to the Material Output node
    material.node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    emissive_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    emissive_texture_node.location = (-1000, -800)  # Adjust the location of the node
    material.node_tree.links.new(emissive_texture_node.outputs['Color'], principled_node.inputs['Emission'])
    principled_node.inputs['Emission Strength'].default_value = 4.72
    path = material.name
    path = path.replace("/", "|")
    path = path.replace("\\", "|")
    path = path.split("|")
    path = path[-1]
    texcoord_node = material.node_tree.nodes.new(type='ShaderNodeTexCoord')
    texcoord_node.location = (-1500, 0)
    mapping_node = material.node_tree.nodes.new(type='ShaderNodeMapping')
    mapping_node.location = (-1300, 0)
    
    material.node_tree.links.new(texcoord_node.outputs['UV'], mapping_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], basecolor_texture_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], mix_texture_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], roughness_texture_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], specular_texture_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], image_texture1_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], image_texture2_node.inputs['Vector'])
    material.node_tree.links.new(mapping_node.outputs['Vector'], emissive_texture_node.inputs['Vector'])
    
    ACCESS_NODE = material.node_tree.nodes.new(type='NodeReroute')
    ACCESS_NODE.location = (-1300, 400)
    ACCESS_NODE.label = "titanfall2shader"
    NOTICE_NODE = material.node_tree.nodes.new(type='NodeReroute')
    NOTICE_NODE.location = (-1300, 360)
    NOTICE_NODE.label = "DO NOT TOUCH THESE 4 SMALL NODES, SHIT WILL BREAK"
    INSTRUCTIONS_NODE = material.node_tree.nodes.new(type='NodeReroute')
    INSTRUCTIONS_NODE.location = (-1300, 320)
    INSTRUCTIONS_NODE.label = "Simply add textures to the nodes with the same name as the"
    INSTRUCTIONS_NODE2 = material.node_tree.nodes.new(type='NodeReroute')
    INSTRUCTIONS_NODE2.location = (-1300, 280)
    INSTRUCTIONS_NODE2.label = "TF2 texture map names, the exporter will do the rest"
    material.node_tree.links.new(NOTICE_NODE.outputs['Output'], ACCESS_NODE.inputs['Input'])
    material.node_tree.links.new(ACCESS_NODE.outputs['Output'], NOTICE_NODE.inputs['Input'])
    basecolor_texture_node.label = "Col"
    image_texture1_node.label = "Nml"
    roughness_texture_node.label = "Gls"
    specular_texture_node.label = "Spc"
    image_texture2_node.label = "Cav"
    mix_texture_node.label = "Ao"
    emissive_texture_node.label = "Ilm"
    if append_textures == True:
        col = material_map_finder(paths, path, "col.png")
        nml = material_map_finder(paths, path, "nml.png")
        gls = material_map_finder(paths, path, "gls.png")
        spc = material_map_finder(paths, path, "spc.png")
        cav = material_map_finder(paths, path, "cav.png")
        if cav == None:
            cav = material_map_finder(paths, path, "cvt.png")
        ao = material_map_finder(paths, path, "ao.png")
        ems = material_map_finder(paths, path, "ilm.png")
        try:
        
            basecolor_texture_node.image = bpy.data.images.load(col)
        except:
            print("[Perimeter] Error loading col node texture")
        
        #one of these for each : nml, rgh, spc, cav, ao
        try:
            image_texture1_node.image = bpy.data.images.load(nml)
        except:
            print("[Perimeter] Error loading nml node texture")
        try:
            roughness_texture_node.image = bpy.data.images.load(gls)
        except:
            print("[Perimeter] Error loading gls node texture")
        try:
            specular_texture_node.image = bpy.data.images.load(spc)
        except:
            print("[Perimeter] Error loading spc node texture")
        try:
            image_texture2_node.image = bpy.data.images.load(cav)
        except:
            print("[Perimeter] Error loading cav node texture")
        try:
            mix_texture_node.image = bpy.data.images.load(ao)
        except:
            print("[Perimeter] Error loading ao node texture")
            mix_color_node.inputs['Fac'].default_value = 0  
        try:
            emissive_texture_node.image = bpy.data.images.load(ems)
        except:
            print("[Perimeter] Error loading ilm node texture")
    #change the location of all texture nodes to make them be in a nice row horizontal, with a spacing of 250
    basecolor_texture_node.location = (-1000, 400)
    image_texture1_node.location = (-750, 400)
    roughness_texture_node.location = (-500, 400)
    specular_texture_node.location = (-250, 400)
    image_texture2_node.location = (0, 400)
    mix_texture_node.location = (250, 400)
    emissive_texture_node.location = (500, 400)
    #add a reroute above each texture node and label it with the texture name
    basecolor_reroute = material.node_tree.nodes.new(type='NodeReroute')
    basecolor_reroute.location = (-950, 440)
    basecolor_reroute.label = "COL / BASE COLOR MAP / ALBEDO MAP / DIFFUSE MAP"
    nml_reroute = material.node_tree.nodes.new(type='NodeReroute')
    nml_reroute.location = (-700, 440)
    nml_reroute.label = "NML / NORMAL MAP"
    gls_reroute = material.node_tree.nodes.new(type='NodeReroute')
    gls_reroute.location = (-450, 440)
    gls_reroute.label = "INVERTED ROUGHNESS / GLOSS MAP"
    spc_reroute = material.node_tree.nodes.new(type='NodeReroute')
    spc_reroute.location = (-200, 440)
    spc_reroute.label = "SPC / SPECULAR MAP"
    cav_reroute = material.node_tree.nodes.new(type='NodeReroute')
    cav_reroute.location = (50, 440)
    cav_reroute.label = "CAV / CVT / CAVITY MAP"
    ao_reroute = material.node_tree.nodes.new(type='NodeReroute')
    ao_reroute.location = (300, 440)
    ao_reroute.label = "AO / AMBIENT OCCLUSION MAP"
    ilm_reroute = material.node_tree.nodes.new(type='NodeReroute')
    ilm_reroute.location = (550, 440)
    ilm_reroute.label = "ILM / EMISSIVE MAP"
    #add a reroute above the mix node and label it with the texture name
    mix_reroute = material.node_tree.nodes.new(type='NodeReroute')
    mix_reroute.location = (250, 360)
    mix_reroute.label = "Ao"





def setup_shader(mesh, paths, append_textures=True, single_material=False):
    # Check if the object is a mesh
    if mesh.type == 'MESH':
        # Iterate over the material slots
        if single_material == False:
            for slot in mesh.material_slots:
                material = slot.material
                shader_on_material(material, paths, append_textures)
        else:
            material = mesh.active_material
            shader_on_material(material, paths, append_textures)


def setup_diffuse_shader(mesh, paths):
    #shader like above that oinly uses the diffuse texture
    if mesh.type == 'MESH':
        for slot in mesh.material_slots:
            material = slot.material
            material.use_nodes = True
            material.node_tree.nodes.clear()
            principled_node = material.node_tree.nodes.new(type='ShaderNodeBsdfDiffuse')
            principled_node.location = (0, 0)
            #sed specular to 0
            basecolor_texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
            basecolor_texture_node.location = (-300, 0)
            output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
            output_node.location = (200, 0)
            material.node_tree.links.new(basecolor_texture_node.outputs['Color'], principled_node.inputs['Color'])
            material.node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
            path = material.name
            path = path.replace("/", "|")
            path = path.replace("\\", "|")
            path = path.split("|")
            path = path[-1]

            col = material_map_finder(paths, path, "col.png")
            texcoord_node = material.node_tree.nodes.new(type='ShaderNodeTexCoord')
            texcoord_node.location = (-1500, 0)

            mapping_node = material.node_tree.nodes.new(type='ShaderNodeMapping')
            mapping_node.location = (-1300, 0)
            
            basecolor_texture_node.label = "Col"
            material.node_tree.links.new(texcoord_node.outputs['UV'], mapping_node.inputs['Vector'])

            try:
                basecolor_texture_node.image = bpy.data.images.load(col)
            except:
                print("[Perimeter] Error loading col node texture")
            

def return_mesh_maps( context ):
    #returns a dict of each material of each mesh if a node with the label "titanfall2shader" is found in the material
    #the dict is in the format of {material name: {map name: map path}}
    
    materials_dict = {}
    rpak_ready_materials = []

    map_types = ["col", "nml", "gls", "spc", "cav", "ao", "ilm"]

    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            for slot in mesh.material_slots:
                material = slot.material
                if material.use_nodes == True:
                    is_tf2_shader = False

                    for node in material.node_tree.nodes:
                        if node.label == "titanfall2shader":
                            is_tf2_shader = True
                    
                    if is_tf2_shader == True:
                        for node in material.node_tree.nodes:
                            if node.type == "TEX_IMAGE":
                                #all node labels: col, nml, gls, spc, cav, ao, ilm
                                #find the path of each node and add it to the dict 

                                if node.label == "Col":
                                    if node.image:
                                        col = node.image.filepath
                                        
                                    else:
                                        col = None
                                if node.label == "Nml":
                                    if node.image:
                                        nml = node.image.filepath
                                    else:
                                        nml = None
                                if node.label == "Gls":
                                    if node.image:
                                        gls = node.image.filepath
                                    else:
                                        gls = None
                                if node.label == "Spc":
                                    if node.image:
                                        spc = node.image.filepath
                                    else:
                                        spc = None
                                if node.label == "Cav":
                                    if node.image:
                                        cav = node.image.filepath
                                    else:
                                        cav = None
                                if node.label == "Ao":
                                    if node.image:
                                        ao = node.image.filepath
                                    else:
                                        ao = None
                                if node.label == "Ilm":
                                    if node.image:
                                        ilm = node.image.filepath
                                    else:
                                        ilm = None
                                    
                             
                        materials_dict[material.name] = { col, nml, gls, spc, cav, ao, ilm}

    return materials_dict
 