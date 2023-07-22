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

    start_renamematerials = 0
    if not qc_file_path.endswith( ".qc" ):
        return ""
    else:
        with open( qc_file_path, "r" ) as qc_file:
            qc_file_lines = qc_file.readlines(  )
            #find the line that starts with lowercase $modelname, start writing below that line 
            for line in qc_file_lines:
                if line.startswith( "$modelname" ):
                    start_renamematerials = qc_file_lines.index( line ) + 1
                    break
            qc_file.close(  )
        with open( qc_file_path, "w" ) as qc_file:
            qc_file.writelines( qc_file_lines[:start_renamematerials] )
            qc_file.write( "\n" )
            for str in material_override:
                qc_file.write( str )
                qc_file.write( "\n" )
            qc_file.writelines( qc_file_lines[start_renamematerials:] )
            qc_file.close(  )      

def read_material_override( qc_file_path ):
    material_override = []
    start_renamematerials = 0
    if not qc_file_path.endswith( ".qc" ):
        return ""
    else:
        with open( qc_file_path, "r" ) as qc_file:
            qc_file_lines = qc_file.readlines(  )
            #find the line that starts with lowercase $modelname, start writing below that line 
            for line in qc_file_lines:
                if line.startswith( "$renamematerials" ):
                    start_renamematerials = qc_file_lines.index( line ) + 1
                    break
            qc_file.close(  )
        return material_override