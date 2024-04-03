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


#this file solely should contain functions and tools for interacting with the perimeter material format files
#below will be definitions of said files
#each version will have its own entry signified by the commend starting with #BEGIN FORMAT VERSION[versionnumber] BEGIN FORMAT
#each versions entry will end with #END FORMAT VERSION[versionnumber] END FORMAT


#BEGIN FORMAT VERSION[100]
#BEGIN FORMAT VERSION[100]
#BEGIN FORMAT VERSION[100]

#HEADER
#UINT32 magic "1095583056" "pema"
#UINT16 pma_format_version 
#UINT16 PADDING
#UINT64 PADDING

#UINT32 rpak_unkFlags                     
#UINT16 rpak_depthStencilFlags            
#UINT16 rpak_rasterizerFlags          
#UINT64 rpak_manual_shaderset             
#UINT32 rpak_flag_1                       
#UINT64 rpak_flag_2      

#FLOATVECTOR3 rpak_albedoTint                   
#FLOATVECTOR3 rpak_selfillum                     
#FLOATVECTOR3 c_perfSpecColor                    

#FLOAT c_fogColorFactor                      
#FLOAT c_layerBlendRamp                      
#FLOAT c_opacity                     
#FLOAT c_useAlphaModulateSpecular                                
#FLOAT c_alphaEdgeFadeExponent                               
#FLOAT c_alphaEdgeFadeOuter                              
#FLOAT c_alphaEdgeFadeInner                              
#FLOAT c_useAlphaModulateEmissive                                
#FLOAT c_emissiveEdgeFadeExponent                                
#FLOAT c_emissiveEdgeFadeInner                               
#FLOAT c_emissiveEdgeFadeOuter                               
#FLOAT c_alphaDistanceFadeScale                              
#FLOAT c_alphaDistanceFadeBias                               
#FLOAT c_alphaTestReference                              
#FLOAT c_aspectRatioMulV                             
#FLOAT c_shadowBias                              
#FLOAT c_tsaaDepthAlphaThreshold                             
#FLOAT c_tsaaMotionAlphaThreshold                                
#FLOAT c_tsaaMotionAlphaRamp                             
#FLOAT c_dofOpacityLuminanceScale                                
#FLOAT c_perfGloss   


#UINT32 PADDING                     
#UINT32 PADDING  
#UINT32 PADDING  

#
#           start stringtable
#write string after string after string

#STRING              rpak_surfacetype                  
#STRING              rpak_type                         
#STRING              rpak_subtype                      


#END FORMAT VERSION[100] END FORMAT
#END FORMAT VERSION[100] END FORMAT
#END FORMAT VERSION[100] END FORMAT



#BEGIN FORMAT VERSION[110]
#BEGIN FORMAT VERSION[110]
#BEGIN FORMAT VERSION[110]

#HEADER
#UINT32 magic "1095583056" "pema"
#UINT16 pma_format_version 
#UINT16 PADDING
#UINT64 PADDING

#UINT32 rpak_unkFlags                     
#UINT16 rpak_depthStencilFlags            
#UINT16 rpak_rasterizerFlags          
#UINT64 rpak_manual_shaderset             
#UINT32 rpak_flag_1                       
#UINT64 rpak_flag_2      

#FLOATVECTOR3 rpak_albedoTint                   
#FLOATVECTOR3 rpak_selfillum                     
#FLOATVECTOR3 c_perfSpecColor                    

#FLOAT c_fogColorFactor                      
#FLOAT c_layerBlendRamp                      
#FLOAT c_opacity                     
#FLOAT c_useAlphaModulateSpecular                                
#FLOAT c_alphaEdgeFadeExponent                               
#FLOAT c_alphaEdgeFadeOuter                              
#FLOAT c_alphaEdgeFadeInner                              
#FLOAT c_useAlphaModulateEmissive                                
#FLOAT c_emissiveEdgeFadeExponent                                
#FLOAT c_emissiveEdgeFadeInner                               
#FLOAT c_emissiveEdgeFadeOuter                               
#FLOAT c_alphaDistanceFadeScale                              
#FLOAT c_alphaDistanceFadeBias                               
#FLOAT c_alphaTestReference                              
#FLOAT c_aspectRatioMulV                             
#FLOAT c_shadowBias                              
#FLOAT c_tsaaDepthAlphaThreshold                             
#FLOAT c_tsaaMotionAlphaThreshold                                
#FLOAT c_tsaaMotionAlphaRamp                             
#FLOAT c_dofOpacityLuminanceScale                                
#FLOAT c_perfGloss   


#UINT32 PADDING                     
#UINT32 PADDING  
#UINT32 PADDING  

#
#           start stringtable
#write string after string after string

#STRING              rpak_surfacetype                  
#STRING              rpak_type                         
#STRING              rpak_subtype                      
#STRING              rpak_preset  

#END FORMAT VERSION[110] END FORMAT
#END FORMAT VERSION[110] END FORMAT
#END FORMAT VERSION[110] END FORMAT


#BEGIN FORMAT VERSION[120]
#BEGIN FORMAT VERSION[120]
#BEGIN FORMAT VERSION[120]

#HEADER
#UINT32 magic "1095583056" "pema"
#UINT16 pma_format_version 
#UINT16 PADDING
#UINT64 PADDING

#begin shaderflags

#UINT32 rpak_unkFlags                     
#UINT16 rpak_depthStencilFlags            
#UINT16 rpak_rasterizerFlags          
#UINT64 rpak_manual_shaderset             
#UINT32 rpak_flag_1                       
#UINT64 rpak_flag_2      
#UINT32 rpak_blendState0
#UINT32 rpak_blendState1
#UINT32 rpak_blendState2
#UINT32 rpak_blendState3


#begin tint vectors

#FLOATVECTOR3 rpak_albedoTint                   
#FLOATVECTOR3 rpak_selfillum                     
#FLOATVECTOR3 c_perfSpecColor                    


#begin cpu_file_contents_misc


#FLOAT c_uv1RotScaleX_x
#FLOAT c_uv1RotScaleX_y
#FLOAT c_uv1RotScaleY_x
#FLOAT c_uv1RotScaleY_y
#FLOAT c_uv1Translate_x
#FLOAT c_uv1Translate_y
#FLOAT c_uv2RotScaleX_x
#FLOAT c_uv2RotScaleX_y
#FLOAT c_uv2RotScaleY_x
#FLOAT c_uv2RotScaleY_y
#FLOAT c_uv2Translate_x
#FLOAT c_uv2Translate_y
#FLOAT c_uv3RotScaleX_x
#FLOAT c_uv3RotScaleX_y
#FLOAT c_uv3RotScaleY_x
#FLOAT c_uv3RotScaleY_y
#FLOAT c_uv3Translate_x
#FLOAT c_uv3Translate_y
#FLOAT c_uvDistortionIntensity_x
#FLOAT c_uvDistortionIntensity_y
#FLOAT c_uvDistortion2Intensity_x
#FLOAT c_uvDistortion2Intensity_y  
#FLOAT c_fogColorFactor                      
#FLOAT c_layerBlendRamp                      
#FLOAT c_opacity                     
#FLOAT c_useAlphaModulateSpecular                                
#FLOAT c_alphaEdgeFadeExponent                               
#FLOAT c_alphaEdgeFadeOuter                              
#FLOAT c_alphaEdgeFadeInner                              
#FLOAT c_useAlphaModulateEmissive                                
#FLOAT c_emissiveEdgeFadeExponent                                
#FLOAT c_emissiveEdgeFadeInner                               
#FLOAT c_emissiveEdgeFadeOuter                               
#FLOAT c_alphaDistanceFadeScale                              
#FLOAT c_alphaDistanceFadeBias                               
#FLOAT c_alphaTestReference                              
#FLOAT c_aspectRatioMulV                             
#FLOAT c_shadowBias                              
#FLOAT c_tsaaDepthAlphaThreshold                             
#FLOAT c_tsaaMotionAlphaThreshold                                
#FLOAT c_tsaaMotionAlphaRamp                             
#FLOAT c_dofOpacityLuminanceScale                                
#FLOAT c_perfGloss   

#UINT32 PADDING  

#
#           start stringtable
#write string after string after string

#STRING              rpak_surfacetype                  
#STRING              rpak_type                         
#STRING              rpak_subtype                      

#END FORMAT VERSION[120] END FORMAT
#END FORMAT VERSION[120] END FORMAT
#END FORMAT VERSION[120] END FORMAT







import os
from .ioUtils import *    


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def return_blender_vector3(blend_vec3):
    normalized_blendvec3 = []
    for vec3_float in blend_vec3:
        normalized_blendvec3.append( float( str(vec3_float)[:4] ) )
    return normalized_blendvec3

class PEMA_FILE:  # Class should always be up to date for WRITING the newest pema format and READING all current formats

    def read_pema( self, path_to_load ):

        pma_file = open(path_to_load, "rb")

        if not read_uint32(pma_file) == 1095583056:
            print("[Perimeter] PMA File read, magic false, aborting load")
        else:
            print("[Perimeter] PMA File read, magic true, continuing load")

            self.version = read_uint16(pma_file)

            if self.version == 120:
                pma_file.seek(16)
                
                self.rpak_unkFlags                  = read_uint32(pma_file)     
                self.rpak_depthStencilFlags         = read_uint16(pma_file)       
                self.rpak_rasterizerFlags           = read_uint16(pma_file)   
                self.rpak_manual_shaderset          = read_uint64(pma_file)       
                self.rpak_flag_1                    = read_uint32(pma_file)            
                self.rpak_flag_2                    = read_uint64(pma_file)
                self.rpak_blendState0               = read_uint32(pma_file)
                self.rpak_blendState1               = read_uint32(pma_file)
                self.rpak_blendState2               = read_uint32(pma_file)
                self.rpak_blendState3               = read_uint32(pma_file)


                self.rpak_albedoTint                = Vector3(read_float(pma_file), read_float(pma_file), read_float(pma_file))                   
                self.rpak_selfillum                 = Vector3(read_float(pma_file), read_float(pma_file), read_float(pma_file))                     
                self.c_perfSpecColor                = Vector3(read_float(pma_file), read_float(pma_file), read_float(pma_file))           

                self.c_uv1RotScaleX_x               = read_float(pma_file) 
                self.c_uv1RotScaleX_y               = read_float(pma_file) 
                self.c_uv1RotScaleY_x               = read_float(pma_file) 
                self.c_uv1RotScaleY_y               = read_float(pma_file) 
                self.c_uv1Translate_x               = read_float(pma_file) 
                self.c_uv1Translate_y               = read_float(pma_file) 
                self.c_uv2RotScaleX_x               = read_float(pma_file) 
                self.c_uv2RotScaleX_y               = read_float(pma_file) 
                self.c_uv2RotScaleY_x               = read_float(pma_file) 
                self.c_uv2RotScaleY_y               = read_float(pma_file) 
                self.c_uv2Translate_x               = read_float(pma_file) 
                self.c_uv2Translate_y               = read_float(pma_file) 
                self.c_uv3RotScaleX_x               = read_float(pma_file) 
                self.c_uv3RotScaleX_y               = read_float(pma_file) 
                self.c_uv3RotScaleY_x               = read_float(pma_file) 
                self.c_uv3RotScaleY_y               = read_float(pma_file) 
                self.c_uv3Translate_x               = read_float(pma_file) 
                self.c_uv3Translate_y               = read_float(pma_file) 
                self.c_uvDistortionIntensity_x      = read_float(pma_file) 
                self.c_uvDistortionIntensity_y      = read_float(pma_file) 
                self.c_uvDistortion2Intensity_x     = read_float(pma_file) 
                self.c_uvDistortion2Intensity_y     = read_float(pma_file) 

                self.c_fogColorFactor               = read_float(pma_file)                 
                self.c_layerBlendRamp               = read_float(pma_file)                
                self.c_opacity                      = read_float(pma_file)        
                self.c_useAlphaModulateSpecular     = read_float(pma_file)                              
                self.c_alphaEdgeFadeExponent        = read_float(pma_file)                           
                self.c_alphaEdgeFadeOuter           = read_float(pma_file)                        
                self.c_alphaEdgeFadeInner           = read_float(pma_file)                        
                self.c_useAlphaModulateEmissive     = read_float(pma_file)                              
                self.c_emissiveEdgeFadeExponent     = read_float(pma_file)                              
                self.c_emissiveEdgeFadeInner        = read_float(pma_file)                          
                self.c_emissiveEdgeFadeOuter        = read_float(pma_file)                          
                self.c_alphaDistanceFadeScale       = read_float(pma_file)                          
                self.c_alphaDistanceFadeBias        = read_float(pma_file)                         
                self.c_alphaTestReference           = read_float(pma_file)                     
                self.c_aspectRatioMulV              = read_float(pma_file)                 
                self.c_shadowBias                   = read_float(pma_file)             
                self.c_tsaaDepthAlphaThreshold      = read_float(pma_file)                        
                self.c_tsaaMotionAlphaThreshold     = read_float(pma_file)                           
                self.c_tsaaMotionAlphaRamp          = read_float(pma_file)                  
                self.c_dofOpacityLuminanceScale     = read_float(pma_file)                           
                self.c_perfGloss                    = read_float(pma_file)

                pma_file.seek(272)

                self.rpak_surfacetype       	    = read_string(pma_file)               
                self.rpak_type                      = read_string(pma_file)           
                self.rpak_subtype                   = read_string(pma_file)



        pma_file.close()

    def write_header_to_file(pma_file, header_version):

        write_uInt32(pma_file, 1095583056) #pema magic
        write_uInt16(pma_file, header_version) #version

        #write padding

        write_uInt16(pma_file, 0)
        write_uInt32(pma_file, 0)
        write_uInt32(pma_file, 0)


    def make_material_file_from_blender_material_collection(self, path_to_save, material):
        #material should be the blender material collection 

        pma_file = open(path_to_save, "wb+")
        self.write_header_to_file(pma_file, 120)


        write_uInt32(pma_file, int(material.rpak_unkFlags))
        write_uInt16(pma_file, int(material.rpak_depthStencilFlags))
        write_uInt16(pma_file, int(material.rpak_rasterizerFlags))

        write_uInt64(pma_file, int(material.rpak_manual_shaderset, 16))
        write_uInt32(pma_file, int(material.rpak_flag_1, 16))
        write_uInt64(pma_file, int(material.rpak_flag_2, 16))
    
        write_uInt32(pma_file, int(material.rpak_blendState0))
        write_uInt32(pma_file, int(material.rpak_blendState1))
        write_uInt32(pma_file, int(material.rpak_blendState2))
        write_uInt32(pma_file, int(material.rpak_blendState3))


        for float in return_blender_vector3(material.rpak_albedoTint):
            write_float(pma_file, float)

        for float in return_blender_vector3(material.rpak_selfillum):
            write_float(pma_file, float)

        for float in return_blender_vector3(material.c_perfSpecColor):
            write_float(pma_file, float)

        
        write_float(pma_file, material.c_uv1RotScaleX_x)
        write_float(pma_file, material.c_uv1RotScaleX_y)
        write_float(pma_file, material.c_uv1RotScaleY_x)
        write_float(pma_file, material.c_uv1RotScaleY_y)
        write_float(pma_file, material.c_uv1Translate_x)
        write_float(pma_file, material.c_uv1Translate_y)
        write_float(pma_file, material.c_uv2RotScaleX_x)
        write_float(pma_file, material.c_uv2RotScaleX_y)
        write_float(pma_file, material.c_uv2RotScaleY_x)
        write_float(pma_file, material.c_uv2RotScaleY_y)
        write_float(pma_file, material.c_uv2Translate_x)
        write_float(pma_file, material.c_uv2Translate_y)
        write_float(pma_file, material.c_uv3RotScaleX_x)
        write_float(pma_file, material.c_uv3RotScaleX_y)
        write_float(pma_file, material.c_uv3RotScaleY_x)
        write_float(pma_file, material.c_uv3RotScaleY_y)
        write_float(pma_file, material.c_uv3Translate_x)
        write_float(pma_file, material.c_uv3Translate_y)
        write_float(pma_file, material.c_uvDistortionIntensity_x)
        write_float(pma_file, material.c_uvDistortionIntensity_y)
        write_float(pma_file, material.c_uvDistortion2Intensity_x)
        write_float(pma_file, material.c_uvDistortion2Intensity_y)

        write_float(pma_file, material.c_fogColorFactor)                      
        write_float(pma_file, material.c_layerBlendRamp)                      
        write_float(pma_file, material.c_opacity)                     
        write_float(pma_file, material.c_useAlphaModulateSpecular)                                
        write_float(pma_file, material.c_alphaEdgeFadeExponent)                               
        write_float(pma_file, material.c_alphaEdgeFadeOuter)                              
        write_float(pma_file, material.c_alphaEdgeFadeInner)                              
        write_float(pma_file, material.c_useAlphaModulateEmissive)                                
        write_float(pma_file, material.c_emissiveEdgeFadeExponent)                                
        write_float(pma_file, material.c_emissiveEdgeFadeInner)                               
        write_float(pma_file, material.c_emissiveEdgeFadeOuter)                               
        write_float(pma_file, material.c_alphaDistanceFadeScale)                              
        write_float(pma_file, material.c_alphaDistanceFadeBias)                               
        write_float(pma_file, material.c_alphaTestReference)                              
        write_float(pma_file, material.c_aspectRatioMulV)                             
        write_float(pma_file, material.c_shadowBias)                              
        write_float(pma_file, material.c_tsaaDepthAlphaThreshold)                             
        write_float(pma_file, material.c_tsaaMotionAlphaThreshold)                                
        write_float(pma_file, material.c_tsaaMotionAlphaRamp)                             
        write_float(pma_file, material.c_dofOpacityLuminanceScale)                                
        write_float(pma_file, material.c_perfGloss)   
        
        #write padding for string table
        write_uInt32(pma_file, 0)


        write_string(pma_file, material.rpak_surfacetype)                  
        write_string(pma_file, material.rpak_type)                         
        write_string(pma_file, material.rpak_subtype)  

        pma_file.close()


