import os, sys

def remove_mid_list(lst, start, end):
    if start < 0 or end >= len(lst) or start > end:
        return lst

    lst = lst[:start] + lst[end + 1:]

    return lst

def return_last_arg( line ):
    return line.split( )[-1].strip( ).replace( '"', '' )

def return_command_arg( lines_list, command_string ):  #returns  the specified commands last argument, if multiple as list if one as single string

    arg_line = [line for line in lines_list if line.lower().startswith( command_string.lower()+ " " )]
    for i in range( len( arg_line ) ):
        arg_line[i] = return_last_arg( arg_line[i].replace( '\n', '' ) )

    if len( arg_line ) == 1:
        arg_line = arg_line[0]

    return arg_line

def return_all_args( line ):
    return line.split( )[1:]

def return_all_args_list( lines_list, command_string ): #returns  the specified commands arguments

    arg_line = [line for line in lines_list if line.lower().startswith( command_string.lower()+ " " )]
    for i in range( len( arg_line ) ):
        arg_line[i] = return_all_args( arg_line[i].replace( '\n', '' ) )

    return arg_line

def return_poseparameters( lines_list ):
    poseparameter_list = []
    for line in lines_list:
        if line.startswith( "$poseparameter" ):
            poseparameter_list.append( POSEPARAMETER( line ) )
    return poseparameter_list

def return_attachements( lines_list ):
    attachements_list = []
    for line in lines_list:
        if line.startswith( "$attachment" ):
            attachements_list.append( ATTACHEMENT( line ) )
    return attachements_list


def return_bones ( lines_list ):
    bone_list = []
    for line in lines_list:
        if line.startswith( "$definebone" ):
            bone_list.append( BONE( line ) )
    return bone_list




def return_bodygroups( lines ): #parse bodygroups, code copied from perimeter slighly altered
        
        bodygroup_dict = {}
        current_bodygroup = ""
        bodygroup_smd_files = []
        bodyroup_found = False
        opening_bracket_found = False
        for line in lines:
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
                    mesh_name = mesh_name.replace( '"', "" )
                    bodygroup_smd_files.append( mesh_name )
                if line.split(  )[0].startswith( "blank" ):
                    bodygroup_smd_files.append( "blank" ) 
            if line.startswith( "}" ) and bodyroup_found and opening_bracket_found:
                opening_bracket_found = False
                bodyroup_found = False
                #add the bodygroup and its smd files to the dict
                bodygroup_dict[current_bodygroup] = bodygroup_smd_files
                bodygroup_smd_files = []
                current_bodygroup = ""
            
        return bodygroup_dict



def write_bodygroups_to_file(qc_file, bodygroup_dict):
    with open(qc_file, 'r') as file:
        lines = file.readlines()

    current_bodygroup = None
    current_studios = []
    bodygroup_lines = []
    i = 0

    # Extract lines before bodygroup definitions
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith('$bodygroup'):
            bodygroup_lines.append(line + '\n')
            del lines[i]
        else:
            break

    # Process the file content
    while i < len(lines):

        line = lines[i].strip()

        if line.startswith('$bodygroup'):
            if current_bodygroup and current_studios:
                current_studios = []
            current_bodygroup = line.split('"')[1]
            del lines[i]

        elif line.startswith('studio'):
            studio = line.split('"')[1]
            current_studios.append(studio)
            del lines[i]

        elif line == '{':
            if current_bodygroup:
                del lines[i]
            else:
                i += 1

        elif line == '}':
            if current_bodygroup and current_studios:
                current_studios = []
                current_bodygroup = None
                del lines[i]  # Remove only closing brace associated with bodygroup
                i -= 1  # Recheck the line after removing the brace
            else:
                i += 1  # Move to the next line without removing the brace

        elif line == 'blank':
            current_studios.append("blank")
            del lines[i]

        else:
            i += 1

    # Reassemble the content
    updated_lines = bodygroup_lines + ['\n']

    # Update the content with the dictionary structure
    for key, value in bodygroup_dict.items():
        updated_lines.append(f'$bodygroup "{key}"\n')
        updated_lines.append('{\n')
        for studio_item in value:
            if studio_item == "blank":
                updated_lines.append(f'\tblank\n')
            else:
                updated_lines.append(f'\tstudio "{studio_item}"\n')
        updated_lines.append('}\n')  # Closing brace for each bodygroup

    updated_lines += lines  # Append remaining content after bodygroups

    with open(qc_file, 'w') as file:
        file.writelines(updated_lines)



def return_texturegroup_materials( lines ):
        
        texture_group_name = ""
        texture_families_list = []
        texturegroup_found = False
        opening_bracket_found = False
        for line in lines:
            line = line.replace( '\n', '' ).strip()
            #test startswith for lowercase and uppercase
            if line.lower(  ).startswith( "$texturegroup" ):
                texturegroup_found = True
                texture_group_name = line.split(  )[1]
                texture_group_name = texture_group_name.replace( '"', "" )
                if line.endswith( "{" ):
                    opening_bracket_found = True
                else:
                    opening_bracket_found = False
            if line.startswith( "{" ) and texturegroup_found:
                opening_bracket_found = True
            if texturegroup_found and opening_bracket_found:
                if line.startswith( "{" ) and line.endswith( "}" ):
                    texture_families_list.append( line.replace("{", "").replace("}", "").strip() ) 
            if line.startswith( "}" ) and texturegroup_found and opening_bracket_found:
                opening_bracket_found = False
                texturegroup_found = False
            
        return texture_group_name, texture_families_list


def write_texturegroup_materials( lines, texgroup_name, qc_file):

    generated_texturegroup_lines = []
    generated_texturegroup_lines.append(f'$texturegroup "{texgroup_name}"')
    generated_texturegroup_lines.append("\n{\n")

    for material_line in lines:
        generated_texturegroup_lines.append("   { " + material_line + " }\n")

    generated_texturegroup_lines.append("}\n")
    
    with open(qc_file, 'r') as file:
        lines = file.readlines()
    
    opening_bracket_found = False
    texture_group_found = False
    texgroup_start_pos = int
    texgroup_end_pos = int
    bracket_count = 0
    closing_bracket_found = False

    while not texture_group_found:
        for i in range(len(lines)):
            if lines[i].lower().startswith('$texturegroup'):
                texture_group_found = True
                texgroup_start_pos = i
    if texture_group_found:
        if lines[texgroup_start_pos].endswith('{'):
            opening_bracket_found = True
        while not opening_bracket_found:  
            for index, line in enumerate(lines[texgroup_start_pos:]):
                if line.startswith('{'):
                    if not opening_bracket_found:
                        opening_bracket_found = True
                if not closing_bracket_found:
                    for letter in line:
                        if letter == '{':
                            bracket_count += 1
                        if letter == '}':
                            bracket_count -= 1
                            if bracket_count == 0:
                                closing_bracket_found = True
                                texgroup_end_pos = texgroup_start_pos + index
                                break

        if closing_bracket_found:
            re_write = remove_mid_list(lines, texgroup_start_pos, texgroup_end_pos)
            new_made = lines[:texgroup_start_pos]
            for line in generated_texturegroup_lines:
                new_made.append(line)
            new_made = re_write[:texgroup_start_pos]
            for line in generated_texturegroup_lines:
                new_made.append(line)
            for line in re_write[texgroup_start_pos:]:
                new_made.append(line)
            with open(qc_file, 'w') as file:
                file.writelines(new_made)


class POSEPARAMETER:
    #$poseparameter "sprintfrac" 0 1 loop 0
    #$poseparameter <$sequence name> <int min> <int max> [loop <int>] [wrap]
    def __init__( self, in_line ):
        #read into above vars
        self.sequence_name      = in_line.split(  )[1]
        self.min                = in_line.split(  )[2] 
        self.max                = in_line.split(  )[3]
        self.loop               = in_line.split(  )[4]
        self.wrap               = in_line.split(  )[5]


class ATTACHEMENT:
    def __init__( self, in_line ):

        self.is_absolute = False

        self.rotate_x           = 0
        self.rotate_y           = 0
        self.rotate_z           = 0

        self.attachement_name   = in_line.split(  )[1]
        self.parent_bone        = in_line.split(  )[2]
        self.offset_x           = in_line.split(  )[3]
        self.offset_y           = in_line.split(  )[4]
        self.offset_z           = in_line.split(  )[5]
        self.arg1               = in_line.split(  )[6]
        if self.arg1 == "absolute":
            self.is_absolute    = True
        if self.arg1 == "rotate":
            self.rotate_x       = in_line.split(  )[7]
            self.rotate_y       = in_line.split(  )[8]
            self.rotate_z       = in_line.split(  )[9]
        
class BONE:
    #$definebone (name) (parent) (X) (Y) (Z) (xr) (yr) (zr) (fixup X) (fixup Y) (fixup Z) (fixup X Rotation) (fixup Y Rotation) (fixup Z Rotation)
    def __init__( self, in_line ):
        self.bone_name          = in_line.split(  )[1]
        self.parent             = in_line.split(  )[2]
        self.pos_x              = in_line.split(  )[3]
        self.pos_y              = in_line.split(  )[4]
        self.pos_z              = in_line.split(  )[5]
        self.rot_x              = in_line.split(  )[6]
        self.rot_y              = in_line.split(  )[7]
        self.rot_z              = in_line.split(  )[8]
        self.fixup_pos_x        = in_line.split(  )[9]
        self.fixup_pos_y        = in_line.split(  )[10]
        self.fixup_pos_z        = in_line.split(  )[11]
        self.fixup_rot_x        = in_line.split(  )[12]
        self.fixup_rot_y        = in_line.split(  )[13]
        self.fixup_rot_z        = in_line.split(  )[14]

        
class QC:

    def __init__( self, in_file ):
        self.qc_file = in_file 

        #we open the file lets go
        with open( self.qc_file, 'r' ) as file:
            lines = file.readlines()
        

        #get all single command lines before going to the more advanced stuff

        self.model_name         = return_command_arg( lines, "$modelname" ) 

        if type(self.model_name) == list:
            
            self.model_name = self.model_name[0]
            

        self.surfaceprop        = return_command_arg( lines, "$surfaceprop" )

        self.contents           = return_command_arg( lines, "$contents" )

        self.cdmaterials        = return_command_arg( lines, "$cdmaterials" )

        self.hboxset            = return_command_arg( lines, "$hboxset" )

        self.bonemerge          = return_command_arg( lines, "$bonemerge" )

        self.includemodel       = return_command_arg( lines, "$includemodel" )

        self.maxverts           = return_command_arg( lines, "$maxverts" )



        #get all multi arg lines

        self.illumposition      = return_all_args_list( lines, "$illumposition" )

        self.cbox               = return_all_args_list( lines, "$cbox" )

        self.bbox               = return_all_args_list( lines, "$bbox" )

        self.hbox               = return_all_args_list( lines, "$hbox")

        for i in self.hbox:
            print(i)

        self.eyeposition        = return_all_args_list( lines, "$eyeposition" )

        self.sectionframes      = return_all_args_list( lines, "$sectionframes" )

        #get the bigger stuff

        self.poseparameters     = return_poseparameters( lines )
        
        self.bodygroups         = return_bodygroups( lines )

        self.texturegroups      = return_texturegroup_materials( lines )

        self.attachements       = return_attachements( lines )

        self.bones              = return_bones( lines )

        
#if name main

if __name__ == "__main__":

#get first arg passed to the file in cmd as var "qc_file"
    
    qc_file = sys.argv[1]

    qc = QC(qc_file)




