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

from .ioUtils import *
import os, sys

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class BONE:
    def __init__(self, in_file):
        self.bone_file = in_file



class RUI_HEADER:
    def __init__( self, in_file ):
        self.rui_file = in_file
        self.rui_header_offset = self.rui_file.tell()
        self.name_hash = read_uint32(self.rui_file)
        self.rui_mesh_offset = read_uint32(self.rui_file)

class RUI_VERTEX:
    def __init__( self, in_file ):
        self.rui_file = in_file
        self.parent = read_uint32(self.rui_file)
        self.x = read_float(self.rui_file)
        self.y = read_float(self.rui_file)
        self.z = read_float(self.rui_file)
        #print(self.parent, " ", self.x, " ", self.y, " ", self.z)

class RUI_VERTMAP:
    def __init__( self, in_file ):
        self.rui_file = in_file
        self.id0 = read_uint16(self.rui_file)
        self.id1 = read_uint16(self.rui_file)
        self.id2 = read_uint16(self.rui_file)

class RUI_FACEDATA:
    def __init__( self, in_file ):
        self.rui_file = in_file
        self.face_uv_min_x = read_float(self.rui_file)
        self.face_uv_min_y = read_float(self.rui_file)

        self.face_uv_max_x = read_float(self.rui_file)
        self.face_uv_max_y = read_float(self.rui_file)

        self.face_scale_min_x = read_float(self.rui_file)
        self.face_scale_min_y = read_float(self.rui_file)

        self.face_scale_max_x = read_float(self.rui_file)
        self.face_scale_max_y = read_float(self.rui_file)
 
class RUI_MESH:

    def __init__( self, in_file ):
        #RUI HEADER

        self.rui_file = in_file
        self.rui_mesh_start = self.rui_file.tell()
        self.num_parents = read_uint32(self.rui_file)
        self.num_verts = read_uint32(self.rui_file)
        self.num_faces = read_uint32(self.rui_file)
        self.parent_index = read_uint32(self.rui_file)
        self.vertex_index = read_uint32(self.rui_file)
        self.vertmap_index = read_uint32(self.rui_file)
        self.facedata_index = read_uint32(self.rui_file)
        self.unk4 = read_uint32(self.rui_file)
        self.rui_mesh_name = read_string(self.rui_file)

        self.parents = []
        self.verticies = []
        self.vertmap = []
        self.facedata = []
       
        self.rui_file.seek( self.rui_mesh_start + self.parent_index )
        for i in range(self.num_parents):
            parent = read_uint16( self.rui_file )
            self.parents.append( parent )
        
        self.rui_file.seek( self.rui_mesh_start + self.vertex_index )

        for i in range(self.num_verts):
            vert = RUI_VERTEX(self.rui_file)
            self.verticies.append(vert)

        self.rui_file.seek( self.rui_mesh_start + self.vertmap_index )

        for i in range(self.num_faces):
            vert = RUI_VERTMAP(self.rui_file)
            self.vertmap.append(vert)


        self.rui_file.seek( self.rui_mesh_start + self.facedata_index )

        for i in range(self.num_faces):
            vert = RUI_FACEDATA(self.rui_file)
            self.facedata.append(vert)

class MDL53:

    def __init__( self, in_file ):
        self.mdl_file = in_file

        #header
        #header
        #header

        self.hdr_id = read_uint32(self.mdl_file)
        self.hdr_version = read_uint32(self.mdl_file)

        if not self.hdr_version == 53:
            print("Error: Not a valid MDL53 file")
            exit(1)

        self.hdr_checksum = read_uint32(self.mdl_file)
        self.hdr_sznameindex = read_uint32(self.mdl_file)
        self.hdr_model_name = self.mdl_file.read(64).decode("utf-8").rstrip('\0')
        self.hdr_length = read_uint32(self.mdl_file)

        self.hdr_eyeposition = Vector3(read_float(self.mdl_file), read_float(self.mdl_file), read_float(self.mdl_file))

        self.hdr_illumposition = Vector3(read_float(self.mdl_file), read_float(self.mdl_file), read_float(self.mdl_file))

        self.hdr_hull_min = Vector3(read_float(self.mdl_file), read_float(self.mdl_file), read_float(self.mdl_file))
        
        self.hdr_hull_max = Vector3(read_float(self.mdl_file), read_float(self.mdl_file), read_float(self.mdl_file))

        self.hdr_view_bbmin = Vector3(read_float(self.mdl_file), read_float(self.mdl_file), read_float(self.mdl_file))

        self.hdr_view_bbmax = Vector3(read_float(self.mdl_file), read_float(self.mdl_file), read_float(self.mdl_file))

        self.hdr_flags = read_uint32(self.mdl_file)

        self.hdr_bone_count = read_uint32(self.mdl_file)

        self.hdr_bone_offset = read_uint32(self.mdl_file)

        self.hdr_bonecontroller_count = read_uint32(self.mdl_file)

        self.hdr_bonecontroller_offset = read_uint32(self.mdl_file)

        self.hdr_hitbox_count = read_uint32(self.mdl_file)

        self.hdr_hitbox_offset = read_uint32(self.mdl_file)

        self.hdr_localanim_count = read_uint32(self.mdl_file)

        self.hdr_localanim_offset = read_uint32(self.mdl_file)

        self.hdr_localseq_count = read_uint32(self.mdl_file)

        self.hdr_localseq_offset = read_uint32(self.mdl_file)

        self.hdr_activitylistversion = read_uint32(self.mdl_file)

        self.hdr_eventsindexed = read_uint32(self.mdl_file)

        self.hdr_texture_count = read_uint32(self.mdl_file)

        self.hdr_texture_offset = read_uint32(self.mdl_file)

        self.hrd_cdtexture_count = read_uint32(self.mdl_file)

        self.hdr_cdtexture_offset = read_uint32(self.mdl_file)

        self.hdr_skinreference_count = read_uint32(self.mdl_file)

        self.hdr_skinrfamily_count = read_uint32(self.mdl_file)

        self.hdr_skin_offset = read_uint32(self.mdl_file)

        self.hdr_bodypart_count = read_uint32(self.mdl_file)

        self.hdr_bodypart_offset = read_uint32(self.mdl_file)

        self.hdr_attachment_count = read_uint32(self.mdl_file)

        self.hdr_attachment_offset = read_uint32(self.mdl_file)

        self.hdr_localnode_count = read_uint32(self.mdl_file)

        self.hdr_localnode_index = read_uint32(self.mdl_file)

        self.hdr_localnode_name_index = read_uint32(self.mdl_file)

        self.hdr_flexdesc_count = read_uint32(self.mdl_file)

        self.hdr_flexdesc_index = read_uint32(self.mdl_file)

        self.hdr_flexcontroller_count = read_uint32(self.mdl_file)

        self.hdr_flexcontroller_index = read_uint32(self.mdl_file)

        self.hdr_flexrules_count = read_uint32(self.mdl_file)

        self.hdr_flexrules_index = read_uint32(self.mdl_file)

        self.hdr_ikchain_count = read_uint32(self.mdl_file)

        self.hdr_ikchain_index = read_uint32(self.mdl_file)

        self.hdr_rui_mesh_count = read_uint32(self.mdl_file)

        self.hdr_rui_mesh_offset = read_uint32(self.mdl_file)

        self.hdr_localposeparam_count = read_uint32(self.mdl_file)

        self.hdr_localposeparam_index = read_uint32(self.mdl_file)

        self.hdr_surfaceprop_index = read_uint32(self.mdl_file)

        self.hdr_keyvalue_index = read_uint32(self.mdl_file)

        self.hdr_keyvalue_count = read_uint32(self.mdl_file)

        self.hdr_local_ikautoplaylock_count = read_uint32(self.mdl_file)

        self.hdr_local_ikautoplaylock_index = read_uint32(self.mdl_file)

        self.hdr_mass = read_float(self.mdl_file)

        self.hdr_contents = read_uint32(self.mdl_file)

        self.hdr_include_model_count = read_uint32(self.mdl_file)

        self.hdr_include_model_index = read_uint32(self.mdl_file)

        self.hdr_virtual_model = read_uint32(self.mdl_file)

        self.hdr_bbonetable_by_name_index = read_uint32(self.mdl_file)

        self.hdr_constdirectionallightdot = read_uint8(self.mdl_file)

        self.hdr_root_lod = read_uint8(self.mdl_file)

        self.hdr_allowed_root_lod_count = read_uint8(self.mdl_file)

        self.hdr_unused = read_uint8(self.mdl_file)

        self.hdr_fadedistance = read_float(self.mdl_file)

        self.hdr_numflexcontrollerui = read_uint32(self.mdl_file)

        self.hdr_flexcontrollerui_index = read_uint32(self.mdl_file)

        self.hdr_vert_anim_fixed_point_scale = read_float(self.mdl_file)

        self.hdr_surface_prop_lookup = read_uint32(self.mdl_file)

        self.hdr_source_filename = read_uint32(self.mdl_file)

        self.hdr_src_bone_transform_count = read_uint32(self.mdl_file)

        self.hdr_src_bone_transform_index = read_uint32(self.mdl_file)

        self.hdr_illumposition_attachment_index = read_uint32(self.mdl_file)

        self.hdr_linear_bone_offset = read_uint32(self.mdl_file)

        self.hdr_bone_flex_driver_count = read_uint32(self.mdl_file)

        self.hdr_bone_flex_driver_index = read_uint32(self.mdl_file)

        self.hdr_per_triAABBindex = read_uint32(self.mdl_file)

        self.hdr_per_triAABBNodecount = read_uint32(self.mdl_file)

        self.hdr_per_triAABBLeafcount = read_uint32(self.mdl_file)

        self.hdr_per_triAABBVertcount = read_uint32(self.mdl_file)

        self.hdr_unknown_string_index = read_uint32(self.mdl_file)

        self.hdr_vtx_offset = read_uint32(self.mdl_file)

        self.hdr_vvd_offset = read_uint32(self.mdl_file)

        self.hdr_vvc_offset = read_uint32(self.mdl_file)

        self.hdr_vphys_offset = read_uint32(self.mdl_file)

        self.hdr_vtx_size = read_uint32(self.mdl_file)

        self.hdr_vvd_size = read_uint32(self.mdl_file)

        self.hdr_vvc_size = read_uint32(self.mdl_file)

        self.hdr_vphys_size = read_uint32(self.mdl_file)

        self.hdr_unknown_index = read_uint32(self.mdl_file)

        self.hdr_unknown_count = read_uint32(self.mdl_file)

        self.hdr_bone_follower_count = read_uint32(self.mdl_file)

        self.hdr_bone_follower_index = read_uint32(self.mdl_file)

        self.hdr_unknown_60_int = []
        for i in range(0, 60):
            self.hdr_unknown_60_int.append(read_uint32(self.mdl_file))


        self.mdl_file.seek(self.hdr_rui_mesh_offset)

        rui_header = []

        for i in range(self.hdr_rui_mesh_count):

            rui_header.append(RUI_HEADER(self.mdl_file))


        self.mdl_rui_meshes = []

        num_meshes_made = 0

        for ruihead in rui_header:
            self.mdl_file.seek( ruihead.rui_mesh_offset + ruihead.rui_header_offset)
            rui_mesh = RUI_MESH( self.mdl_file )
            self.mdl_rui_meshes.append( rui_mesh )

            num_meshes_made = num_meshes_made + 1

    
def return_blender_rui_mesh(mdl_rui_mesh):

    facedata = []
    vert_list = []
    vertmaps = []
    ruimesh = mdl_rui_mesh
    for vert in ruimesh.facedata:
        new_verts = [vert.face_uv_min_x, vert.face_uv_min_y, vert.face_uv_max_x, vert.face_uv_max_y, vert.face_scale_min_x, vert.face_scale_min_y, vert.face_scale_max_x, vert.face_scale_max_y]
        facedata.append(new_verts)
    for vert in ruimesh.vertmap:
        new_verts = [vert.id0, vert.id1, vert.id2]
        vertmaps.append(new_verts)
    for vert in ruimesh.verticies:
        new_verts = [vert.x, vert.y, vert.z]
        vert_list.append(new_verts)

    return [facedata, vert_list, vertmaps, ruimesh.rui_mesh_name, ruimesh.parents]


def get_mdl_rui_meshes(mdl_file):
    mdl = MDL53(open(mdl_file, "rb"))
    rui_mesh_list = []
    for i in mdl.mdl_rui_meshes:
        rui_mesh_list.append( return_blender_rui_mesh(i) )
    return rui_mesh_list
    



        