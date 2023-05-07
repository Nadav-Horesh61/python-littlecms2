#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
partial interfacte to lcms2 using ctypes
Created on Sun May 14 17:27:53 2017

@author: nadav
"""

from lcms2_header import *
import ctypes as CT
import numpy as np
# import littlecms as LC
import pathlib as pl

# Enable trap of SIG faults

import  faulthandler
faulthandler.enable()
import threading
import platform

UNTRASH=[]

def physical_cpu_cores()->int:
    if platform.system() != 'Linux':
        return 0
    cpuinfo = dict(map(str.strip, line.split(':'))
                   for line in open('/proc/cpuinfo')
                   if ':' in line)

    #return cpuinfo['siblings'] != cpuinfo['cpu cores']
    return int(cpuinfo['cpu cores'])



# functions
# =========
# cmsOpenProfileFromFile(icc-filename:str*, mode:str*)
# cmsCreateTransform(src_icc: cmsHPROFILE, LC.TYPE_RGB_16: uint32,
#                    dst_icc: cmsHPROFILE, LC.TYPE_RGB_16: uint32,
#                                      LC.INTENT_PERCEPTUAL:uint32 , 0:uint32)
# cmsDoTransform(transform: cmsHTRANSFORM, image: void*, out_image:void*, imagesize:uint32)

# Define a dummy buffer pointer type, matby it's work better than void_p

buffer32_t = 32 * CT.c_uint8
pbuffer32_t = CT.POINTER(buffer32_t)

buffer16_t = 16 * CT.c_uint8
pbuffer16_t = CT.POINTER(buffer16_t)

pointer = CT.POINTER(CT.c_char)


cmsHPROFILE = pbuffer32_t # CT.c_void_p
cmsHTRANSFORM = pbuffer16_t # CT.c_void_p
cmsBool = CT.c_int64
# cmsTagSignature = CT.c_uint32
# cmsCIE_colour = 3 * CT.c_double
# cmsCIExyY = cmsCIE_colour


#cmsProfileClassSignature = CT.c_char * 4

def init(lcms2_lib:str='liblcms2.so')->None:
    lib = pl.Path(lcms2_lib)
    # Test if there is /local/lib version and use it if there is.
    if lib.parent == '.':
        lib = pl.Path('/usr/local/lib/'+lcms2_lib)
        if lib.exists():
            lcms2_lib = str(lib)
    _lcms2 = CT.cdll.LoadLibrary(lcms2_lib)

    _lcmsOpenProfileFromFile = _lcms2.cmsOpenProfileFromFile
    _lcmsOpenProfileFromFile.restype = cmsHPROFILE
    
    _lcmsCreateTransform = _lcms2.cmsCreateTransform
    _lcmsCreateTransform.restype = cmsHTRANSFORM
    
    _lcmsCreateMultiprofileTransform = _lcms2.cmsCreateMultiprofileTransform
    _lcmsCreateMultiprofileTransform.restype = cmsHTRANSFORM
    
    _lcmsTransform2DeviceLink =  _lcms2.cmsTransform2DeviceLink
    _lcmsTransform2DeviceLink.restype = cmsHPROFILE
    
    _lcmsGetHeaderModel = _lcms2.cmsGetHeaderModel
    _lcmsGetHeaderModel.restype = CT.c_uint32
    
    _lcmsGetProfileVersion = _lcms2.cmsGetProfileVersion
    _lcmsGetProfileVersion.restype = CT.c_double
    
    _lcmsGetPCS = _lcms2.cmsGetPCS
    _lcmsGetPCS.restype = cmsColorSpaceSignature
    
    _lcmsGetColorSpace = _lcms2.cmsGetColorSpace
    _lcmsGetColorSpace.restype = cmsColorSpaceSignature
    
    _lcmsGetTransformInputFormat = _lcms2.cmsGetTransformInputFormat
    _lcmsGetTransformInputFormat.restype = CT.c_uint32
    
    _lcmsGetTransformOutputFormat = _lcms2.cmsGetTransformOutputFormat
    _lcmsGetTransformOutputFormat.restype = CT.c_uint32
    
    
    #cmsBool cmsSaveProfileToFile(cmsHPROFILE hProfile, const char* FileName);
    _lcmsSaveProfileToFile = _lcms2.cmsSaveProfileToFile
    _lcmsSaveProfileToFile.restype = cmsBool
    
    # Built in profiles  (All gets void as an argument)
    _lcmsCreate_sRGBProfile = _lcms2.cmsCreate_sRGBProfile
    _lcmsCreate_sRGBProfile.restype = cmsHPROFILE
    
    _lcmsCreateLab2Profile = _lcms2.cmsCreateLab2Profile
    _lcmsCreateLab2Profile.restype = cmsHPROFILE
    
    _lcmsCreateLab4Profile = _lcms2.cmsCreateLab4Profile
    _lcmsCreateLab4Profile.restype = cmsHPROFILE
    
    _lcmsCreateXYZProfile =  _lcms2.cmsCreateXYZProfile
    _lcmsCreateXYZProfile.restype = cmsHPROFILE
    
    _lcmsCreateNULLProfile = _lcms2.cmsCreateNULLProfile
    _lcmsCreateNULLProfile.restype = cmsHPROFILE
    
    _lcmsGetHeaderRenderingIntent = _lcms2.cmsGetHeaderRenderingIntent
    _lcmsGetHeaderRenderingIntent.restype = CT.c_uint32
    
    _lcmsIsIntentSupported = _lcms2.cmsIsIntentSupported
    _lcmsIsIntentSupported.restype = CT.c_int
    
    _lcmsGetDeviceClass = _lcms2.cmsGetDeviceClass
    _lcmsGetDeviceClass.restype = CT.c_int
    
    _lcmsGetTransformInputFormat = _lcms2.cmsGetTransformInputFormat
    _lcmsGetTransformInputFormat.restype = CT.c_uint32
    
    _lcmsGetTransformOutputFormat = _lcms2.cmsGetTransformOutputFormat
    _lcmsGetTransformOutputFormat.restype = CT.c_uint32
    
    _lcmsChangeBuffersFormat = _lcms2.cmsChangeBuffersFormat
    _lcmsChangeBuffersFormat.restype = CT.c_int

###     NEED INSTANTIATION PYZTHON FUNCTIONS

    _lcmsIsTag = _lcms2.cmsIsTag #(cmsHPROFILE hProfile, cmsTagSignature sig);
    _lcmsIsTag.restype = cmsBool

    _lcmsReadTag = _lcms2.cmsReadTag #(cmsHPROFILE hProfile, cmsTagSignature sig);
    _lcmsReadTag.restype = pointer

    _lcmsWriteTag = _lcms2.cmsWriteTag # (cmsHPROFILE hProfile, cmsTagSignature sig, const void* data);
    _lcmsWriteTag.restype = cmsBool

    _lcmsWhitePointFromTemp = _lcms2.cmsWhitePointFromTemp # (cmsCIExyY* WhitePoint,cmsFloat64Number TempK);
    _lcmsWhitePointFromTemp.restype = cmsBool


    # A generator for a matrix RGB profile
    #
    #cmsHPROFILEcmsCreateRGBProfile(const cmsCIExyY* WhitePoint,
    #                               const cmsCIExyYTRIPLE* Primaries,
    #                               cmsToneCurve* const TransferFunction[3]);
    _lcmsCreateRGBProfile = _lcms2.cmsCreateRGBProfile
    _lcmsCreateRGBProfile.restype = cmsHPROFILE
    
    _lcmsXYZ2xyY = _lcms2.cmsXYZ2xyY
    _lcmsXYZ2xyY.restype = None  # CT.c_void_p
    
    _lcmsxyY2XYZ = _lcms2.cmsXYZ2xyY
    _lcmsxyY2XYZ.restype = None  # CT.c_void_p
    
    _lcmsD50_XYZ = _lcms2.cmsD50_XYZ
    _lcmsD50_XYZ.restype = CT.POINTER(cmsCIEXYZ)

    _lcmsD50_xyY = _lcms2.cmsD50_xyY
    _lcmsD50_xyY.restype = CT.POINTER(cmsCIExyY)


    
    # The tone curve can be built by either of the functions desribed in the API
    # documentation pages 135-145
    # cmsBool cmsIsToneCurveLinear(const cmsToneCurve* Curve);
    # Release all definitions to the global scope
    globals().update(locals())


def cmsD50_XYZ()->cmsCIEXYZ:
    xyz = _lcmsD50_XYZ()
    return xyz.contents

def cmsD50_xyY()->cmsCIExyY:
    xyY = _lcmsD50_xyY()
    return xyY.contents

def cmsxyY2XYZ(xyY: cmsCIExyY)->cmsCIEXYZ:
    # Looks bogous
    assert type(xyY) is cmsCIExyY
    xyz = cmsCIEXYZ()
    _lcmsxyY2XYZ(CT.pointer(xyz), CT.pointer(xyY))
    return xyz


def cmsXYZ2xyY(xyz: cmsCIEXYZ)->cmsCIExyY:
    assert type(xyz) is cmsCIEXYZ
    xyY = cmsCIExyY()
    _lcmsXYZ2xyY(CT.pointer(xyY), CT.pointer(xyz))
    return xyY



def cmsIsTag(profile:cmsHPROFILE, tag:cmsTagSignature)->bool:
    assert type(profile) is cmsHPROFILE
    assert type(tag) is cmsTagSignature
    result = _lcmsIsTag(profile, cmsTagSignature_type(tag))
    return bool(result)

def lcmsReadTag(profile:cmsHPROFILE, tag:cmsTagSignature)->pointer:
    assert type(profile) is cmsHPROFILE
    assert type(tag) is cmsTagSignature
    result = _lcmsReadTag(profile, cmsTagSignature_type(tag))
    return result

def lcmsWriteTag(profile:cmsHPROFILE, tag:cmsTagSignature, data):
    assert type(profile) is cmsHPROFILE
    assert type(tag) is cmsTagSignature
    # assert type(data) is pointer
    result = _lcmsWriteTag(profile, cmsTagSignature_type(tag), CT.pointer(data))
    return result

# def lcmscmsWhitePointFromTemp(white_point: cmsCIExyY, temperature:float)->bool:
#     assert type(white_point) is cmsCIExyY
#     result = _lcmscmsWhitePointFromTemp(white_point, CT.c_double(temperature))
#     return bool(result)

def lcmsWhitePointFromTemp(temperature:float)->cmsCIExyY:
    white_point = cmsCIExyY()
    result = _lcmsWhitePointFromTemp(CT.pointer(white_point), CT.c_double(temperature))
    return white_point if bool(result) else None


def read_white_point(profile:cmsHPROFILE):
    result_type = CT.POINTER(cmsCIExyY)
    result = lcmsReadTag(profile, cmsTagSignature.cmsSigMediaWhitePointTag)
    return result_type(result.contents).contents

def set_white_point(profile:cmsHPROFILE, white_point: cmsCIExyY):
    return lcmsWriteTag(profile, cmsTagSignature.cmsSigMediaWhitePointTag, white_point)

#
#  Helper functions
#


def int_to_str(num:int, base=256)->str:
    result = []
    while num > 0:
        num, digit = divmod(num, base)
        result.insert(0, digit)
    return ''.join([chr(dig) for dig in result])


def formatter_to_dtype(formatter:FORMATTER):
    assert type(formatter) is FORMATTER, 'formatter must be an item of FORMATTER class defined in lcms2_header.py'
    ftype = formatter.name.split('_')[-1]
    return {'16': np.uint16, 'FLT':np.float32, 'DBL':np.float64}[ftype]

def cmsSaveProfileToFile(profile:cmsHPROFILE, filename:str, overwrite:bool=False)->bool:
    '''
    save a profile to a file
    '''
    assert type(profile) is cmsHPROFILE
    assert type(filename) is str

    fp = pl.Path(filename)
    if fp.suffix not in ('.icc','.ICC', '.icm','.ICM'):
        filename = filename+'.icc'
        fp = fp.Path(filename)
    if fp.exists() and not overwrite:
        raise FileExistsError(f'file "{filename}" exist, specify overwrite to over write it!')
    return _lcmsSaveProfileToFile(profile, filename.encode('ascii'))

def cmsTransform2DeviceLink(transform:cmsHTRANSFORM, icc_version, flags=None)->cmsHPROFILE:
    '''
    Convert a transfrom to a link profile

    parameters
    ==========
    transfrom: A colour transfrom (like to be prodice by cmsCtrateTransfrome)
    icc_version: An ICC version: if an integet must be either 2 or 4, or a float
                between 2 ato 3 or between 4 to 5
    '''
    assert type(transform) is cmsHTRANSFORM
    if type(icc_version) is int :
        assert icc_version in (2,4), "Only versions 2 or 4 are allowed"
        version = CT.c_double(2.3) if icc_version == 2 else CT.c_double(4.2)
    elif type(icc_version) is float:
        assert (2.0 <= icc_version < 3.0) or (4.0 <= icc_version < 5.0)
        version = CT.c_double(icc_version)
    else:
        raise TypeError('icc_verison must be either int or float')

    dw_flags = CT.c_uint32(FLAGS.cmsFLAGS_GUESSDEVICECLASS + FLAGS.cmsFLAGS_KEEP_SEQUENCE) \
               if flags is None else flags
    result = _lcmsTransform2DeviceLink(transform, version, dw_flags)
    return result if bool(result) else None


def cmsOpenProfileFromFile(icc_fn:str, mode:str='r')-> cmsHPROFILE:
    fn = bytes(icc_fn,'ascii')
    md = bytes(mode,'ascii')
    filename = CT.create_string_buffer(fn)
    c_mode = CT.create_string_buffer(md)
    #return cmsHPROFILE(_lcms2.cmsOpenProfileFromFile(filename, c_mode))
    profile = _lcmsOpenProfileFromFile(filename, c_mode)
    # Return the profile or None if the profile is NULL (function failed)
    return profile if bool(profile) else None

def cmsCreateTransform(src_icc:cmsHPROFILE, dst_icc:cmsHPROFILE,
                       src_mode:FORMATTER=FORMATTER.TYPE_RGB_16, 
                       dst_mode:FORMATTER=FORMATTER.TYPE_RGB_16,
                       intent:Intent=Intent.INTENT_PERCEPTUAL)->cmsHTRANSFORM:
    '''
    The only function which that does not comply to the same argument order as the LCMS
    function it wraps, due to the use of default value for src_mode, dst_mode and intent
    '''
    if type(intent) is Intent:
        intent = intent.value
    assert type(src_icc) is cmsHPROFILE, "Source is not a valid profile!"
    assert type(dst_icc) in (cmsHPROFILE, type(None)), "Destination is not a valid profile!"
    assert type(src_mode) is FORMATTER, "src_mode should be a FORMATTER, see lcms2_header.py FORMATTER class"
    assert type(dst_mode) is FORMATTER, "dst_mode should be a FORMATTER, see lcms2_header.py FORMATTER class"

    src_mode = CT.c_uint32(src_mode)
    dst_mode = CT.c_uint32(dst_mode )
    intent = CT.c_uint32(intent)
    zeros = CT.c_uint32(0)
    result = _lcmsCreateTransform(src_icc, src_mode, dst_icc, dst_mode, intent, zeros)
    if bool(result):   # This evaluates to true if a valid transfrom created
        return result
    return None        # and to False if CreateTransform returns a NULL (failure flag)

def cmsDoTransform(transform: cmsHTRANSFORM, image:np.ndarray,
                   output_type:FORMATTER=None, image_out:np.ndarray=None,
                   chek_input_type:bool=True,
                   threads:int=0)->np.ndarray:
    '''
    Follows closely the wrapper (original) cmsDoTransform, but one can set/guess
    the output image type format, and test validity of input image dtype:
    
    output_type:  If provided, it is assumed to be shuch without testing. If it 
                  is None, it is determined from the transform
    chek_input_type: If True, check if the input image dtype matches the 
                     transform expectation
    '''
    assert type(transform) is cmsHTRANSFORM, '"transform" is not a valid transformation profile'
    assert (output_type is None) or (type(output_type) is FORMATTER)
    assert type(image) is np.ndarray
    
    #img_in = image.ctypes.data_as(CT.POINTER(CT.c_uint16))
    image = np.ascontiguousarray(image)
    #  Generate a pointer to the image data to be sent to the lcms transform fuction
    img_in = image.ctypes.data_as(CT.POINTER(CT.c_voidp))
    
    if chek_input_type:
        assert image.dtype == formatter_to_dtype(cmsGetTransformInputFormat(transform)), "Input image and transform formats do not match"
    if output_type is None:
        output_type = cmsGetTransformOutputFormat(transform)
    out_dtype = formatter_to_dtype(output_type)
    if image_out is None:
        image_out = np.empty(image.shape, out_dtype)
    else:
        assert image_out.dtype == out_dtype
    # img_out = image_out.ctypes.data_as(CT.POINTER(CT.c_uint16))
    img_out = image_out.ctypes.data_as(CT.POINTER(CT.c_voidp))
    img_size = CT.c_uint32(image.size//3)
    # print(img_in[0])
    if threads == 0:
        threads = physical_cpu_cores()
        if threads == 0:
            print('Auto identifyting the cpu cores works only on Linux. Must provide number of threads (> 0)') 
    if threads < 2:
        rc = _lcms2.cmsDoTransform(transform, img_in, img_out, img_size)
    else:
        # Multi threaded run
        lines, cols = image.shape[:2]
        chunk =  lines // threads
        chunk -= chunk % 2  # Enshure chunk is even
        residue = lines - chunk * threads
        chunks = [chunk] * threads
        chunks[-1] += residue
        threads_pull = [None] * threads
        for i in range(threads):
            in_chunk = image[i * chunk].ctypes.data_as(CT.POINTER(CT.c_voidp))
            out_chunk = image_out[i * chunk].ctypes.data_as(CT.POINTER(CT.c_voidp))
            chunk_size = chunks[i] * cols
            threads_pull[i] = threading.Thread(target=_lcms2.cmsDoTransform, 
                                               args=(transform, in_chunk, out_chunk, chunk_size))
            
            threads_pull[i].start()
        for thr in threads_pull:
            thr.join()
    return image_out

def cmsCreateMultiprofileTransform(profiles_list:list,
                       src_mode:FORMATTER=FORMATTER.TYPE_RGB_16, 
                       dst_mode:FORMATTER=FORMATTER.TYPE_RGB_16,
                       intent:Intent=Intent.INTENT_PERCEPTUAL)->cmsHTRANSFORM:

    nprofiles = len(profiles_list)
    for p in profiles_list:
        assert type(p) == cmsHPROFILE
        
    hprofiles = (cmsHPROFILE * nprofiles)(*profiles_list)
    UNTRASH.append(hprofiles)  # Keep away from garbage collection

    res = _lcmsCreateMultiprofileTransform(hprofiles, CT.c_int32(nprofiles),
                                           src_mode, dst_mode, intent)
    UNTRASH.append(res)
    return res

def cmsGetHeaderModel(profile:cmsHPROFILE)->int:
    assert type(profile) is cmsHPROFILE
    res = _lcmsGetHeaderModel(profile)
    return res

def cmsGetProfileVersion(profile: cmsHPROFILE)->float:
    assert type(profile) is cmsHPROFILE
    res = _lcmsGetProfileVersion(profile)
    return res

def cmsGetColorSpace(profile: cmsHPROFILE)->str:
    assert type(profile) is cmsHPROFILE
    res = _lcmsGetColorSpace(profile)
    return int_to_str(res, 256)

def cmsGetPCS(profile: cmsHPROFILE)->str:
    assert type(profile) is cmsHPROFILE
    res = _lcmsGetPCS(profile)
    return int_to_str(res, 256)

def cmsIsIntentSupported(profile:cmsHPROFILE, intent:Intent, direction:UsedDirection)->bool:
    assert type(profile) == cmsHPROFILE
    intent = CT.c_uint32(intent) if type(intent) is int else CT.c_uint32(intent.value)
    direction = CT.c_uint32(direction) if type(direction) is int else CT.c_uint32(direction.value)
    return bool(_lcmsIsIntentSupported(profile, intent, direction))

def cmsGetDeviceClass(hProfile: cmsHPROFILE)->int:
    assert type(hProfile) is cmsHPROFILE
    devclass = _lcmsGetDeviceClass(hProfile)
    return int_to_str(devclass)

def cmsGetHeaderRenderingIntent(hProfile: cmsHPROFILE)->Intent:
    assert type(hProfile) is cmsHPROFILE
    return Intent(_lcmsGetHeaderRenderingIntent(hProfile))

def cmsCreate_sRGBProfile()->cmsHPROFILE:
    return _lcmsCreate_sRGBProfile(None)

def cmsCreateLab4Profile()->cmsHPROFILE:
    return _lcmsCreateLab4Profile(None)

def cmsCreateLab2Profile()->cmsHPROFILE:
    return _lcmsCreateLab2Profile(None)

def cmsCreateXYZProfile()->cmsHPROFILE:
    return _lcmsCreateXYZProfile(None)

def cmsCreateNULLProfile()->cmsHPROFILE:
    return _lcmsCreateNULLProfile(None)

def cmsGetTransformInputFormat(transform:cmsHTRANSFORM)->FORMATTER:
    assert type(transform) is cmsHTRANSFORM
    result = _lcmsGetTransformInputFormat(transform)
    # Return None on Error (result == 0)
    return FORMATTER(result) if result else None
    

def cmsGetTransformOutputFormat(transform:cmsHTRANSFORM)->FORMATTER:
    assert type(transform) is cmsHTRANSFORM
    result = _lcmsGetTransformOutputFormat(transform)
    # Return None on Error (result == 0)
    return FORMATTER(result) if result else None

def cmsChangeBuffersFormat(transform:cmsHTRANSFORM,
                           input_format:FORMATTER,
                           output_format:FORMATTER)->bool:
    assert type(transform) is cmsHTRANSFORM
    assert type(input_format) in (int, FORMATTER)
    assert type(output_format) in (int, FORMATTER)
    return bool(_lcmsChangeBuffersFormat(transform, input_format, output_format))

# For debugging purpose: show the content of the first 32 bytes of a buffer pointed by given pointer
def _showptr(p:CT.POINTER)->tuple:
    v = CT.cast(p, CT.POINTER(p)).contents
    numb = [v[i] for i in range(32)]
    chars = ''.join([chr(n) for n in numb])
    return numb, chars
