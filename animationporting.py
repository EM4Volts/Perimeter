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

import bpy, json

def export_animation_lengths(path):
    # Get the selected armature object
    armature_obj = bpy.context.active_object

    # Check if the selected object is an armature
    if armature_obj and armature_obj.type == 'ARMATURE':
        armature_name = armature_obj.name
        anim_lengths = {}

        # Iterate over all animation actions
        for action in bpy.data.actions:
            # Set the current action to the armature
            armature_obj.animation_data.action = action

            # Get the length of the action in frames
            length_frames = action.frame_range[1] - action.frame_range[0] + 1

            # Convert the length to seconds deprecated no longer needed
            length_seconds = length_frames

            # Add the animation name and length to the dictionary
            anim_lengths[action.name] = length_seconds

        # Generate the JSON file path
        json_file_path = path + armature_name + ".json"

        # Save the animation lengths dictionary as a JSON file
        print("[Perimeter] Exporting animation lengths to:", json_file_path)
        with open(json_file_path, 'w') as json_file:
            json.dump(anim_lengths, json_file, indent=4)

        print("[Perimeter] Animation lengths exported to:", json_file_path)
    else:
        print("[Perimeter] No active armature found.")

def import_animation_lengths(path):
    #path is the path to the json file, which is a dict of animation names and lengths load it into a dict
    with open(path) as json_file:
        anim_lengths = json.load(json_file)

    # Get the selected armature
    selected_armature = bpy.context.object
    if selected_armature and selected_armature.type == 'ARMATURE':
        armature = selected_armature.data

        # Iterate through animation actions
        for action in bpy.data.actions:
            if action.name in anim_lengths:
                # Get the desired length from the dictionary
                desired_length = anim_lengths[action.name]

                # Calculate the scale factor based on desired length and current length
                current_length = action.frame_range[-1]
                scale_factor = desired_length / current_length
                # Apply the scale factor to the action
                for fcurve in action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.co.x *= scale_factor

                # Update the action's range to match the desired length
                action.frame_range[-1] = desired_length
                
        print("[Perimeter] Animation scaling completed.")
    else:
        print("[Perimeter] No armature selected.")
    