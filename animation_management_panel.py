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
from .qcparse import *

#        _      _____  _____ _______ _____       __  __  __ _____  _____  _____
#       | |    |_   _|/ ____|__   __/ ____|     / / |  \/  |_   _|/ ____|/ ____|
#       | |      | | | (___    | | | (___      / /  | \  / | | | | (___ | |
#       | |      | |  \___ \   | |  \___ \    / /   | |\/| | | |  \___ \| |
#       | |____ _| |_ ____) |  | |  ____) |  / /    | |  | |_| |_ ____) | |____
#       |______|_____|_____/   |_| |_____/  /_/     |_|  |_|_____|_____/ \_____|






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


class PerimeterAnimationsPanel( bpy.types.Panel ):
    bl_idname = "perimeter_anim_panel"
    bl_label = "Animation Management"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Perimeter inDev"



    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col.prop( context.scene, "qc_model_name", text="")
        col.label( text="MAXVERTS", icon="GROUP_VERTEX" )




#         ____  _____  ______ _____         _______ ____  _____   _____
#        / __ \|  __ \|  ____|  __ \     /\|__   __/ __ \|  __ \ / ____|
#       | |  | | |__) | |__  | |__) |   /  \  | | | |  | | |__) | (___
#       | |  | |  ___/|  __| |  _  /   / /\ \ | | | |  | |  _  / \___ \
#       | |__| | |    | |____| | \ \  / ____ \| | | |__| | | \ \ ____) |
#        \____/|_|    |______|_|  \_\/_/    \_\_|  \____/|_|  \_\_____/






"""class PerimeterWriteBodygroups(bpy.types.Operator):
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

        return {'FINISHED'}"""

