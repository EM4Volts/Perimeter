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
import os

#returns the model name from the qc file
def get_model_name( qc_file_path ):
    print( qc_file_path )
    if not qc_file_path.endswith( ".qc" ):
        return "No QC file found"
    else:
        with open( qc_file_path ) as qc_file:
            for line in qc_file:
                #test startswith for lowercase and uppercase
                if line.lower(  ).startswith( "$modelname" ):
                    model_name = line.split(  )[1]
                    return model_name

#returns the bodygroup dictionary from the qc file
def return_bodygroup_dict( qc_file_path ):
    #bodygroup_dict should be a dict of each bodygroup and their smd files, needs to support multiple bodygroups

    if not qc_file_path.endswith( ".qc" ):

        return "No QC file found"

    else:
        bodygroup_dict = {}
        with open( qc_file_path ) as qc_file:
            current_bodygroup = ""
            bodygroup_smd_files = []
            bodyroup_found = False
            opening_bracket_found = False
            for line in qc_file:
                #test startswith for lowercase and uppercase
                if line.lower(  ).startswith( "$bodygroup" ):
                    current_bodygroup = line.split(  )[1]
                    current_bodygroup = current_bodygroup.replace( '"', "" )
                    bodyroup_found = True
                    if line.endswith( "{" ):
                        opening_bracket_found = True
                    else:
                        opening_bracket_found = False

                if line.startswith( "{" ) and bodyroup_found:
                    opening_bracket_found = True

                if bodyroup_found and opening_bracket_found:
                    if line.split(  )[0].startswith( "studio" ):
                        mesh_name = line.split(  )[1]
                        mesh_name = mesh_name.replace( ".smd", "" )
                        mesh_name = mesh_name.replace( ".dmx", "" )
                        mesh_name = mesh_name.replace( '"', "" )
                        bodygroup_smd_files.append( mesh_name )

                if line.startswith( "}" ) and bodyroup_found and opening_bracket_found:
                    opening_bracket_found = False
                    bodyroup_found = False
                    #add the bodygroup and its smd files to the dict
                    bodygroup_dict[current_bodygroup] = bodygroup_smd_files
                    bodygroup_smd_files = []
                    current_bodygroup = ""
            return bodygroup_dict

                    
def save_material_override( qc_file_path, material_override ):

    if not qc_file_path.lower().endswith( ".qc" ):
        return ""
        
    else:
    
        lines_to_remove = []
    
        with open( qc_file_path, "r" ) as qc_file:
            qc_file_lines = qc_file.readlines(  )
            for line in qc_file_lines:
                if line.lower().startswith("$renamematerial"):
                    lines_to_remove.append( line )
            
            for line in lines_to_remove:
                qc_file_lines.remove( line )
            qc_file.close(  )
        with open( qc_file_path, "w" ) as qc_file:
            for line in material_override:
                qc_file_lines.append( line + "\n" )
            qc_file.writelines( qc_file_lines )
            qc_file.close(  )

def remove_cdmaterials( qc_file_path ):
    print("1")
    if not qc_file_path.lower().endswith( ".qc" ):
        print("return null")
        return ""
    else:

        lines_to_remove = []
        #hacky solution incoming

        with open( qc_file_path, "r" ) as qc_file:
            qc_file_lines = qc_file.readlines(  )
            for line in qc_file_lines:
                if line.lower().startswith("$cdmaterials"):
                    print(line)
                    lines_to_remove.append( line )

            for line in lines_to_remove:
                qc_file_lines.remove( line )
                qc_file.close(  )

        with open( qc_file_path, "w" ) as qc_file:
            qc_file.writelines( '$cdmaterials ""\n')
            qc_file.writelines( qc_file_lines )
            qc_file.close(  )


def change_maxverts( qc_file_path ):
    
    if not qc_file_path.lower().endswith( ".qc" ):
        return ""
    else:

        lines_to_remove = [] 
        #hacky solution incoming

        with open( qc_file_path, "r" ) as qc_file:
            qc_file_lines = qc_file.readlines(  )
            for line in qc_file_lines:
                if line.lower().startswith("$maxverts"):
                    lines_to_remove.append( line )

            for line in lines_to_remove:
                qc_file_lines.remove( line )
                qc_file.close(  )

        with open( qc_file_path, "w" ) as qc_file:
            qc_file.writelines( '$maxverts 99900\n')
            qc_file.writelines( qc_file_lines )
            qc_file.close(  )
