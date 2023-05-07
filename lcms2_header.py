# Definitions from lcms2.h translated into python

import ctypes as CT
from enum import IntEnum

FLOAT_SH = lambda a: a << 22
COLORSPACE_SH = lambda s: s << 16
CHANNELS_SH = lambda c: c << 3
BYTES_SH = lambda b: b
EXTRA_SH = lambda e: e << 7
SWAPFIRST_SH = lambda s: s << 14

# Formatters colour space code
PT_ANY     = 0    # Don't check colorspace
                  # 1 & 2 are reserved
PT_GRAY    = 3
PT_RGB     = 4
PT_CMY     = 5
PT_CMYK    = 6
PT_YCbCr   = 7
PT_YUV     = 8      # Lu'v'
PT_XYZ     = 9
PT_Lab     = 10
PT_YUVK    = 11     # Lu'v'K
PT_HSV     = 12
PT_HLS     = 13
PT_Yxy     = 14

PT_MCH1    = 15
PT_MCH2    = 16
PT_MCH3    = 17
PT_MCH4    = 18
PT_MCH5    = 19
PT_MCH6    = 20
PT_MCH7    = 21
PT_MCH8    = 22
PT_MCH9    = 23
PT_MCH10   = 24
PT_MCH11   = 25
PT_MCH12   = 26
PT_MCH13   = 27
PT_MCH14   = 28
PT_MCH15   = 29
PT_LabV2   = 30

# Formatters
class FORMATTER(IntEnum):
    TYPE_XYZ_DBL  = (FLOAT_SH(1) |COLORSPACE_SH(PT_XYZ) | CHANNELS_SH(3) | BYTES_SH(0))
    TYPE_Lab_DBL  = (FLOAT_SH(1) |COLORSPACE_SH(PT_Lab) | CHANNELS_SH(3) | BYTES_SH(0))
    TYPE_XYZ_16   = (COLORSPACE_SH(PT_XYZ) | CHANNELS_SH(3) | BYTES_SH(2))
    TYPE_Lab_16   = (COLORSPACE_SH(PT_Lab) | CHANNELS_SH(3) | BYTES_SH(2))
    TYPE_LabV2_16 = (COLORSPACE_SH(PT_LabV2) | CHANNELS_SH(3) | BYTES_SH(2))
    TYPE_RGB_16   = (COLORSPACE_SH(PT_RGB)|CHANNELS_SH(3)|BYTES_SH(2))
    TYPE_XYZ_FLT  = (FLOAT_SH(1)|COLORSPACE_SH(PT_XYZ)|CHANNELS_SH(3)|BYTES_SH(4))
    TYPE_Lab_FLT  = (FLOAT_SH(1)|COLORSPACE_SH(PT_Lab)|CHANNELS_SH(3)|BYTES_SH(4))
    TYPE_RGB_FLT  = (FLOAT_SH(1)|COLORSPACE_SH(PT_RGB)|CHANNELS_SH(3)|BYTES_SH(4))
    TYPE_RGB_DBL  = (FLOAT_SH(1)|COLORSPACE_SH(PT_RGB)|CHANNELS_SH(3)|BYTES_SH(0))
    TYPE_GRAY_FLT = (FLOAT_SH(1)|COLORSPACE_SH(PT_GRAY)|CHANNELS_SH(1)|BYTES_SH(4))

# Get formatter data

T_FLOAT = lambda a: (a>>22) & 1
T_COLORSPACE = lambda s: (s>>16) & 31
T_CHANNELS = lambda c: (c>>3) & 15
T_BYTES = lambda b: b & 7


class ILLUMINANT(IntEnum):
    cmsILLUMINANT_TYPE_UNKNOWN = 0x0000000
    cmsILLUMINANT_TYPE_D50     = 0x0000001
    cmsILLUMINANT_TYPE_D65     = 0x0000002
    cmsILLUMINANT_TYPE_D93     = 0x0000003
    cmsILLUMINANT_TYPE_F2      = 0x0000004
    cmsILLUMINANT_TYPE_D55     = 0x0000005
    cmsILLUMINANT_TYPE_A       = 0x0000006
    cmsILLUMINANT_TYPE_E       = 0x0000007
    cmsILLUMINANT_TYPE_F8      = 0x0000008


# cmsColorSpaceSignature values
cmsColorSpaceSignature = CT.c_uint32
cmsSigXYZData = 'XYZ '   # 0x58595A20
cmsSigLabData = 'Lab '   # 0x4C616220
cmsSigRgbData = 'RGB '   # 0x52474220
cmsSigGrayData = 'GRAY'  # 0x47524159

class cmsCIExyY(CT.Structure):
     _fields_ = [("x", CT.c_double),
                 ("y", CT.c_double),
                 ("Y", CT.c_double)]

class cmsCIEXYZ(CT.Structure):
     _fields_ = [("X", CT.c_double),
                 ("Y", CT.c_double),
                 ("Z", CT.c_double)]


class cmsCIELab(CT.Structure):
     _fields_ = [("L", CT.c_double),
                 ("a", CT.c_double),
                 ("b", CT.c_double)]

class cmsCIEXYZTRIPLE(CT.Structure):
     _fields_ = [ ('Red',   cmsCIEXYZ),
                  ('Green', cmsCIEXYZ),
                  ('Blue',  cmsCIEXYZ)
                ]

# Rendering intents constants
class UsedDirection(IntEnum):
    LCMS_USED_AS_INPUT  = 0
    LCMS_USED_AS_OUTPUT = 1
    LCMS_USED_AS_PROOF  = 2

class Intent(IntEnum):
    INTENT_PERCEPTUAL             = 0
    INTENT_RELATIVE_COLORIMETRIC  = 1
    INTENT_SATURATION             = 2
    INTENT_ABSOLUTE_COLORIMETRIC  = 3

class FLAGS(IntEnum):
    cmsFLAGS_GUESSDEVICECLASS = 0x80
    cmsFLAGS_KEEP_SEQUENCE = 0x20

cmsCIExyYTRIPLE = 3 * cmsCIExyY # Array of 3 cmsCIExyY


class ICC_ags_type(IntEnum):
    cmsSigChromaticityType             = 0x6368726D # 'chrm' 
    cmsSigColorantOrderType            = 0x636C726F     #'clro' 
    cmsSigColorantTableType            = 0x636C7274  #'clrt' 
    cmsSigCrdInfoType                  = 0x63726469  #'crdi' 
    cmsSigCurveType                    = 0x63757276  #'curv' 
    cmsSigDataType                     = 0x64617461  #'data' 
    cmsSigDateTimeType                 = 0x6474696D  #'dtim' 
    cmsSigDeviceSettingsType           = 0x64657673  #'devs' 
    cmsSigLut16Type                    = 0x6d667432  #'mft2' 
    cmsSigLut8Type                     = 0x6d667431  #'mft1' 
    cmsSigLutAtoBType                  = 0x6d414220  #'mAB ' 
    cmsSigLutBtoAType                  = 0x6d424120  #'mBA ' 
    cmsSigMeasurementType              = 0x6D656173  #'meas' 
    cmsSigMultiLocalizedUnicodeType    = 0x6D6C7563  #'mluc' 
    cmsSigMultiProcessElementType      = 0x6D706574  #'mpet' 
    cmsSigNamedColorType               = 0x6E636f6C  #'ncol' 
    cmsSigNamedColor2Type              = 0x6E636C32  #'ncl2' 
    cmsSigParametricCurveType          = 0x70617261  #'para' 
    cmsSigProfileSequenceDescType      = 0x70736571  #'pseq' 
    cmsSigProfileSequenceIdType        = 0x70736964  #'psid' 
    cmsSigResponseCurveSet16Type       = 0x72637332  #'rcs2' 
    cmsSigS15Fixed16ArrayType          = 0x73663332  #'sf32' 
    cmsSigScreeningType                = 0x7363726E  #'scrn' 
    cmsSigSignatureType                = 0x73696720  #'sig ' 
    cmsSigTextType                     = 0x74657874  #'text' 
    cmsSigTextDescriptionType          = 0x64657363  #'desc' 
    cmsSigU16Fixed16ArrayType          = 0x75663332  #'uf32' 
    cmsSigUcrBgType                    = 0x62666420  #'bfd ' 
    cmsSigUInt16ArrayType              = 0x75693136  #'ui16' 
    cmsSigUInt32ArrayType              = 0x75693332  #'ui32' 
    cmsSigUInt64ArrayType              = 0x75693634  #'ui64' 
    cmsSigUInt8ArrayType               = 0x75693038  #'ui08' 
    cmsSigViewingConditionsType        = 0x76696577  #'view' 
    cmsSigXYZType                      = 0x58595A20  #'XYZ '


class cmsTagSignature (IntEnum):
    cmsSigAToB0Tag                           = 0x41324230 # 'A2B0' cmsPipeline              
    cmsSigAToB1Tag                           = 0x41324231 # 'A2B1' cmsPipeline                
    cmsSigAToB2Tag                           = 0x41324232 # 'A2B2' cmsPipeline                
    cmsSigBlueColorantTag                    = 0x6258595A # 'bXYZ' cmsCIEXYZ                  
    cmsSigBlueMatrixColumnTag                = 0x6258595A # 'bXYZ' cmsCIEXYZ                  
    cmsSigBlueTRCTag                         = 0x62545243 # 'bTRC' cmsToneCurve               
    cmsSigBToA0Tag                           = 0x42324130 # 'B2A0' cmsPipeline                
    cmsSigBToA1Tag                           = 0x42324131 # 'B2A1' cmsPipeline                
    cmsSigBToA2Tag                           = 0x42324132 # 'B2A2' cmsPipeline                
    cmsSigCalibrationDateTimeTag             = 0x63616C74 # 'calt' struct tm                  
    cmsSigCharTargetTag                      = 0x74617267 # 'targ' cmsMLU                     
    cmsSigChromaticAdaptationTag             = 0x63686164 # 'chad' cmsCIEXYZ [3]              
    cmsSigChromaticityTag                    = 0x6368726D # 'chrm' cmsCIExyYTRIPLE            
    cmsSigColorantOrderTag                   = 0x636C726F # 'clro' cmsUInt8Number [16]        
    cmsSigColorantTableTag                   = 0x636C7274 # 'clrt' cmsNAMEDCOLORLIST          
    cmsSigColorantTableOutTag                = 0x636C6F74 # 'clot' cmsNAMEDCOLORLIST          
    cmsSigColorimetricIntentImageStateTag    = 0x63696973 # 'ciis'     cmsSignature               
    cmsSigCopyrightTag                       = 0x63707274 # 'cprt' cmsMLU                     
    cmsSigCrdInfoTag                         = 0x63726469 # 'crdi' cmsNAMEDCOLORLIST          
    cmsSigDataTag                            = 0x64617461 # 'data' cmsICCData                 
    cmsSigDateTimeTag                        = 0x6474696D # 'dtim' struct tm                  
    cmsSigDeviceMfgDescTag                   = 0x646D6E64 # 'dmnd' cmsMLU                     
    cmsSigDeviceModelDescTag                 = 0x646D6464 # 'dmdd' cmsMLU                     
    cmsSigDeviceSettingsTag                  = 0x64657673 # 'devs' Not supported*             
    cmsSigDToB0Tag                           = 0x44324230 # 'D2B0' cmsPipeline                
    cmsSigDToB1Tag                           = 0x44324231 # 'D2B1' cmsPipeline                
    cmsSigDToB2Tag                           = 0x44324232 # 'D2B2' cmsPipeline                
    cmsSigDToB3Tag                           = 0x44324233 # 'D2B3' cmsPipeline                
    cmsSigBToD0Tag                           = 0x42324430 # 'B2D0' cmsPipeline                
    cmsSigBToD1Tag                           = 0x42324431 # 'B2D1' cmsPipeline                
    cmsSigBToD2Tag                           = 0x42324432 # 'B2D2' cmsPipeline                
    cmsSigBToD3Tag                           = 0x42324433 # 'B2D3' cmsPipeline                
    cmsSigGamutTag                           = 0x67616D74 # 'gamt' cmsPipeline                
    cmsSigGrayTRCTag                         = 0x6b545243 # 'kTRC' cmsToneCurve               
    cmsSigGreenColorantTag                   = 0x6758595A # 'gXYZ' cmsCIEXYZ                  
    cmsSigGreenMatrixColumnTag               = 0x6758595A # 'gXYZ' cmsCIEXYZ                  
    cmsSigGreenTRCTag                        = 0x67545243 # 'gTRC' cmsToneCurve               
    cmsSigLuminanceTag                       = 0x6C756d69 # 'lumi' cmsCIEXYZ                  
    cmsSigMeasurementTag                     = 0x6D656173 # 'meas' cmsICCMeasurementConditions
    cmsSigMediaBlackPointTag                 = 0x626B7074 # 'bkpt' cmsCIEXYZ         
    cmsSigMediaWhitePointTag                 = 0x77747074 # 'wtpt' cmsCIEXYZ           
    cmsSigNamedColorTag                      = 0x6E636f6C # 'ncol' Not supported*      
    cmsSigNamedColor2Tag                     = 0x6E636C32 # 'ncl2' cmsNAMEDCOLORLIST   
    cmsSigOutputResponseTag                  = 0x72657370 # 'resp' Not supported*      
    cmsSigPerceptualRenderingIntentGamutTag  = 0x72696730 # 'rig0'     cmsSignature        
    cmsSigPreview0Tag                        = 0x70726530 # 'pre0' cmsPipeline         
    cmsSigPreview1Tag                        = 0x70726531 # 'pre1' cmsPipeline         
    cmsSigPreview2Tag                        = 0x70726532 # 'pre2' cmsPipeline         
    cmsSigProfileDescriptionTag              = 0x64657363 # 'desc' cmsMLU
    cmsSigProfileSequenceDescTag             = 0x70736571 # 'pseq' cmsSEQ
    cmsSigProfileSequenceIdTag               = 0x70736964 # 'psid' cmsSEQ        
    cmsSigPs2CRD0Tag                         = 0x70736430 # 'psd0' cmsICCData
    cmsSigPs2CRD1Tag                         = 0x70736431 # 'psd1' cmsICCData
    cmsSigPs2CRD2Tag                         = 0x70736432 # 'psd2' cmsICCData
    cmsSigPs2CRD3Tag                         = 0x70736433 # 'psd3' cmsICCData
    cmsSigPs2CSATag                          = 0x70733273 # 'ps2s' cmsICCData
    cmsSigPs2RenderingIntentTag              = 0x70733269 # 'ps2i' cmsICCData
    cmsSigRedColorantTag                     = 0x7258595A # 'rXYZ' cmsCIEXYZ   
    cmsSigRedMatrixColumnTag                 = 0x7258595A # 'rXYZ' cmsCIEXYZ   
    cmsSigRedTRCTag                          = 0x72545243 # 'rTRC' cmsToneCurve
    cmsSigSaturationRenderingIntentGamutTag  = 0x70733269 # 'ps2i' cmsICCData
    cmsSigScreeningDescTag                   = 0x73637264 # 'scrd' cmsMLU                     
    cmsSigScreeningTag                       = 0x7363726E # 'scrn' cmsScreening         
    cmsSigTechnologyTag                      = 0x74656368 # 'tech'     cmsSignature         
    cmsSigUcrBgTag                           = 0x62666420 # 'bfd ' cmsUcrBg             
    cmsSigViewingCondDescTag                 = 0x76756564 # 'vued' cmsMLU                       
    cmsSigViewingConditionsTag               = 0x76696577 # 'view' cmsICCViewingConditions
    cmsSigMetaTag                            = 0x6D657461 # 'meta' cmsHANDLE (DICT)

cmsTagSignature_type = CT.c_uint32