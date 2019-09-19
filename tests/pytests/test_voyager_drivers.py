import os
import json
import unittest
from unittest.mock import patch

import pytest
import numpy as np
import spiceypy as spice

import ale
from ale.drivers.mro_drivers import MroCtxPds3LabelNaifSpiceDriver, MroCtxIsisLabelNaifSpiceDriver, MroCtxIsisLabelIsisSpiceDriver

from conftest import get_image_kernels, convert_kernels, get_image_label, compare_dicts

image_dict = {
    # Voyager 2 NAC
    'c2065022': {
        'isis': {
            'CameraVersion': 1,
            'NaifKeywords': {'BODY502_RADII': [1564.13, 1561.23, 1560.93],
                             'BODY_FRAME_CODE': 10024,
                             'BODY_CODE': 502,
                             'FRAME_-32101_CLASS_ID': -32101.0,
                             'TKFRAME_-32101_AXES': [1.0, 2.0, 3.0],
                             'TKFRAME_-32101_SPEC': 'ANGLES',
                             'INS-32101_CK_REFERENCE_ID': 2.0,
                             'TKFRAME_-32101_ANGLES': [0.0, 0.0, 0.0],
                             'FRAME_-32101_CENTER': -32.0,
                             'INS-32101_PLATFORM_ID': -32001.0,
                             'TKFRAME_-32101_RELATIVE': 'VG2_SCAN_PLATFORM',
                             'INS-32101_FOCAL_LENGTH': 1503.49,
                             'INS-32101_TRANSX': [0.0, 0.011789473651194, 0.0],
                             'FRAME_-32101_CLASS': 4.0,
                             'INS-32101_TRANSY': [0.0, 0.0, 0.011789473651194],
                             'INS-32101_BORESIGHT': [0.0, 0.0, 1.0],
                             'INS-32101_PIXEL_PITCH': 0.011789473651194,
                             'INS-32101_FOV_SHAPE': 'RECTANGLE',
                             'INS-32101_ITRANSL': [0.0, 0.0, 84.8214288089711],
                             'INS-32101_ITRANSS': [0.0, 84.8214288089711, 0.0],
                             'INS-32101_FOV_BOUNDARY_CORNERS': [0.003700098, 0.003700098, 1.0, -0.003700098, 0.003700098, 1.0, -0.003700098, -0.003700098, 1.0, 0.003700098],
                             'INS-32101_CK_FRAME_ID': -32100.0,
                             'TKFRAME_-32101_UNITS': 'DEGREES',
                             'INS-32101_FOV_FRAME': 'VG2_ISSNA',
                             'INS-32101_CK_TIME_TOLERANCE': 2000.0,
                             'INS-32101_SPK_TIME_BIAS': 0.0,
                             'INS-32101_CK_TIME_BIAS': 0.0,
                             'FRAME_-32101_NAME': 'VG2_ISSNA'},
            'InstrumentPointing': {'TimeDependentFrames': [-32100, 2, 1],
                                   'ConstantFrames': [-32101, -32100],
                                   'ConstantRotation': (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0),
                                   'CkTableStartTime': -646346832.89712,
                                   'CkTableEndTime': -646346832.89712,
                                   'CkTableOriginalSize': 1,
                                   'EphemerisTimes': [-646346832.89712],
                                   'Quaternions': [[0.34057881936764,0.085849252725072,0.69748691965044,-0.62461825983655]]},
            'BodyRotation': {'TimeDependentFrames': [10024, 1],
                             'CkTableStartTime': -646346832.89712,
                             'CkTableEndTime': -646346832.89712,
                             'CkTableOriginalSize': 1,
                             'EphemerisTimes': [-646346832.89712],
                             'Quaternions': [[-0.029536576144092695, 0.010097306192904288, 0.22183794661925513, -0.9745837883512549]]},
            'InstrumentPosition': {'SpkTableStartTime': -646346832.89712,
                                   'SpkTableEndTime': -646346832.89712,
                                   'SpkTableOriginalSize': 1,
                                   'EphemerisTimes': [-646346832.89712],
                                   'Positions': [[133425.48293894,184605.07752753,-3162.2190909154]],
                                   'Velocities': [[-10.722770423744,2.0367821121285,-0.64314600586812]]},
            'SunPosition': {'SpkTableStartTime': -646346832.8971245,
                            'SpkTableEndTime': -646346832.8971245,
                            'SpkTableOriginalSize': 1,
                            'EphemerisTimes': [-646346832.8971245],
                            'Positions': [[588004836.49532,-489060608.67696,-224000895.4511]],
                            'Velocities': [[9.1115543713942,-4.4506204607189,-2.785930492615]]}}},
    # Voyage 2 WAC
    'c2065801' : {
        'isis' : {
            'CameraVersion': 1,
            'NaifKeywords': {'BODY599_RADII': [71492.0, 71492.0, 66854.0],
                             'BODY_FRAME_CODE': 10015,
                             'BODY_CODE': 599,
                             'INS-32102_FOV_SHAPE': 'RECTANGLE',
                             'INS-32102_PLATFORM_ID': -32002.0,
                             'FRAME_-32102_CLASS': 4.0,
                             'INS-32102_CK_REFERENCE_ID': 2.0,
                             'INS-32102_FOV_FRAME': 'VG2_ISSWA',
                             'FRAME_-32102_CLASS_ID': -32102.0,
                             'TKFRAME_-32102_ANGLES': [0.171102, 0.0068, -0.0308],
                             'FRAME_-32102_CENTER': -32.0,
                             'INS-32102_PIXEL_PITCH': 0.0116661644275479,
                             'TKFRAME_-32102_RELATIVE': 'VG2_SCAN_PLATFORM',
                             'TKFRAME_-32102_UNITS': 'DEGREES',
                             'INS-32102_CK_FRAME_ID': -32100.0,
                             'INS-32102_TRANSX': [0.0, 0.0116661644275479, 0.0],
                             'INS-32102_TRANSY': [0.0, 0.0, 0.0116661644275479],
                             'INS-32102_CK_TIME_BIAS': 0.0,
                             'INS-32102_SPK_TIME_BIAS': 0.0,
                             'INS-32102_FOV_BOUNDARY_CORNERS': [0.02765, 0.02765, 1.0, -0.02765, 0.02765, 1.0, -0.02765, -0.02765, 1.0, 0.02765],
                             'FRAME_-32102_NAME': 'VG2_ISSWA',
                             'TKFRAME_-32102_AXES': [3.0, 1.0, 2.0],
                             'TKFRAME_-32102_SPEC': 'ANGLES',
                             'INS-32102_BORESIGHT': [0.0, 0.0, 1.0],
                             'INS-32102_ITRANSL': [0.0, 0.0, 85.7179757931961],
                             'INS-32102_ITRANSS': [0.0, 85.7179757931961, 0.0],
                             'INS-32102_CK_TIME_TOLERANCE': 2000.0,
                             'INS-32102_FOCAL_LENGTH': 200.77},
            'InstrumentPointing': {'TimeDependentFrames': [-32100, 2, 1],
                                   'ConstantFrames': [-32102, -32100],
                                   'ConstantRotation': [0.9999953963536, -0.0029863521854557, -5.37561379938284e-04, 0.0029862887971166, 0.99999553398688, -1.18682388856997e-04, 5.37913406593448e-04, 1.17076528958573e-04, 0.99999984847112],
                                   'CkTableStartTime': -646324849.03313,
                                   'CkTableEndTime': -646324849.03313,
                                   'CkTableOriginalSize': 1,
                                   'EphemerisTimes': [-646324849.03313],
                                   'Quaternions': [[0.3495693057711,0.14569395751119,0.75146963877355,-0.54024804785301]],
                                   'AngularVelocity' : [[0, 0, 0]]},
            'BodyRotation': {'TimeDependentFrames': [10015, 1],
                             'CkTableStartTime': -646324849.03313,
                             'CkTableEndTime': -646324849.03313,
                             'CkTableOriginalSize': 1,
                             'EphemerisTimes': [-646324849.03313],
                             'Quaternions': [[-0.030328300733922,-6.20657627848567e-04,-0.22073570825636,0.97486181382761]],
                             'AngularVelocity' : [[-2.5673165155352e-06,-7.56760295952808e-05,1.58716581044019e-04]]},
            'InstrumentPosition': {'SpkTableStartTime': -646324849.03313,
                                   'SpkTableEndTime': -646324849.03313,
                                   'SpkTableOriginalSize': 1,
                                   'EphemerisTimes': [-646324849.03313],
                                   'Positions': [[505791.09778057,503456.65486597,125565.58221925]],
                                   'Velocities': [[-15.323164993758,12.206477922116,4.8955647678902]]},
            'SunPosition': {'SpkTableStartTime': -646324849.03313,
                            'SpkTableEndTime': -646324849.03313,
                            'SpkTableOriginalSize': 1,
                            'EphemerisTimes': [-646324849.03313],
                            'Positions': [[588848865.61045,-488873362.10683,-223920792.29514]],
                            'Velocities': [[8.9726279013895,8.4018607734375,3.3830218514148]]}}},
    # Voyager 1 NAC
    'c1637937' : {
        'isis' : {
            'CameraVersion': 1,
            'NaifKeywords': {
                'BODY599_RADII': [71492.0, 71492.0, 66854.0],
                'BODY_FRAME_CODE': 10015,
                'BODY_CODE': 599,
                'INS-31101_CK_REFERENCE_ID': 2.0,
                'INS-31101_FOV_FRAME': 'VG1_ISSNA',
                'FRAME_-31101_CLASS_ID': -31101.0,
                'FRAME_-31101_CLASS': 4.0,
                'INS-31101_FOCAL_LENGTH': 1500.19,
                'INS-31101_FOV_BOUNDARY_CORNERS': [0.003700098, 0.003700098, 1.0, -0.003700098, 0.003700098, 1.0, -0.003700098, -0.003700098, 1.0, 0.003700098],
                'INS-31101_SPK_TIME_BIAS': 0.0,
                'TKFRAME_-31101_RELATIVE': 'VG1_SCAN_PLATFORM',
                'INS-31101_PIXEL_PITCH': 0.0117894735849433,
                'TKFRAME_-31101_UNITS': 'DEGREES',
                'INS-31101_CK_FRAME_ID': -31100.0,
                'TKFRAME_-31101_ANGLES': [0.0, 0.0, 0.0],
                'INS-31101_BORESIGHT': [0.0, 0.0, 1.0],
                'FRAME_-31101_CENTER': -31.0,
                'FRAME_-31101_NAME': 'VG1_ISSNA',
                'TKFRAME_-31101_AXES': [1.0, 2.0, 3.0],
                'TKFRAME_-31101_SPEC': 'ANGLES',
                'INS-31101_ITRANSL': [0.0, 0.0, 84.8214292856238],
                'INS-31101_FOV_SHAPE': 'RECTANGLE',
                'INS-31101_ITRANSS': [0.0, 84.8214292856238, 0.0],
                'INS-31101_CK_TIME_TOLERANCE': 2000.0,
                'INS-31101_CK_TIME_BIAS': 0.0,
                'INS-31101_TRANSX': [0.0, 0.0117894735849433, 0.0],
                'INS-31101_TRANSY': [0.0, 0.0, 0.0117894735849433],
                'INS-31101_PLATFORM_ID': -31001.0
            },
            'InstrumentPointing': {'TimeDependentFrames': [-31100, 2, 1],
                                   'ConstantFrames': [-31101, -31100],
                                   'ConstantRotation': [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
                                   'CkTableStartTime': -657272652.12756,
                                   'CkTableEndTime': -657272652.12756,
                                   'CkTableOriginalSize': 1,
                                   'EphemerisTimes': [-657272652.12756],
                                   'Quaternions': [[0.72031433366582,0.41050497282467,0.50142106290735,-0.24740623612725]],
                                   'AngularVelocity' : [[0, 0, 0]]},
            'BodyRotation': {'TimeDependentFrames': [10015, 1],
                             'CkTableStartTime': -657272652.12756,
                             'CkTableEndTime': -657272652.12756,
                             'CkTableOriginalSize': 1,
                             'EphemerisTimes': [-657272652.12756],
                             'Quaternions': [[-0.94178424117164,0.21107549573449,-0.06459036849449,0.25360927127957]],
                             'AngularVelocity' : [[-2.56727928293352e-06,-7.56761359620731e-05,1.58716530917873e-04]]},
            'InstrumentPosition': {'SpkTableStartTime': -657272652.12756,
                                   'SpkTableEndTime': -657272652.12756,
                                   'SpkTableOriginalSize': 1,
                                   'EphemerisTimes': [-657272652.12756],
                                   'Positions': [[621054.17544251,-237768.22251899,-133459.63687226]],
                                   'Velocities': [[-9.0157282204086,18.601529664095,7.8879197923768]]},
            'SunPosition': {'SpkTableStartTime': -657272652.12756,
                            'SpkTableEndTime': -657272652.12756,
                            'SpkTableOriginalSize': 1,
                            'EphemerisTimes': [-657272652.12756],
                            'Positions': [[481854496.7487,-572645660.67701,-257224015.26585]],
                            'Velocities': [[10.526843107335,6.8566245058164,2.6826355466889]]}}},
    # Voyager 1 WAC
    'c1638610' : {
        'isis' : {
            'CameraVersion': 1,
            'NaifKeywords': {
                'BODY599_RADII': [71492.0, 71492.0, 66854.0],
                'BODY_FRAME_CODE': 10015,
                'BODY_CODE': 599,
                'INS-31102_CK_REFERENCE_ID': 2.0,
                'INS-31102_BORESIGHT': [0.0, 0.0, 1.0],
                'INS-31102_ITRANSL': [0.0, 0.0, 84.74864939016786],
                'INS-31102_ITRANSS': [0.0, 84.74864939016786, 0.0],
                'TKFRAME_-31102_UNITS': 'DEGREES',
                'INS-31102_FOV_BOUNDARY_CORNERS': [0.02765, 0.02765, 1.0, -0.02765, 0.02765, 1.0, -0.02765, -0.02765, 1.0, 0.02765],
                'INS-31102_TRANSX': [0.0, 0.0117995980726038, 0.0],
                'INS-31102_TRANSY': [0.0, 0.0, 0.0117995980726038],
                'INS-31102_PIXEL_PITCH': 0.0117995980726038,
                'INS-31102_FOV_SHAPE': 'RECTANGLE',
                'FRAME_-31102_CLASS_ID': -31102.0,
                'INS-31102_CK_FRAME_ID': -31100.0,
                'FRAME_-31102_NAME': 'VG1_ISSWA',
                'TKFRAME_-31102_RELATIVE': 'VG1_SCAN_PLATFORM',
                'INS-31102_FOV_FRAME': 'VG1_ISSWA',
                'TKFRAME_-31102_AXES': [3.0, 1.0, 2.0],
                'TKFRAME_-31102_SPEC': 'ANGLES',
                'INS-31102_CK_TIME_BIAS': 0.0,
                'FRAME_-31102_CLASS': 4.0,
                'INS-31102_CK_TIME_TOLERANCE': 2000.0,
                'INS-31102_FOCAL_LENGTH': 200.465,
                'INS-31102_PLATFORM_ID': -31002.0,
                'TKFRAME_-31102_ANGLES': [0.275, -0.0247, 0.0315],
                'FRAME_-31102_CENTER': -31.0,
                'INS-31102_SPK_TIME_BIAS': 0.0
            },
            'InstrumentPointing': {'TimeDependentFrames': [-31100, 2, 1],
                                   'ConstantFrames': [-31102, -31100],
                                   'ConstantRotation': [0.9999883294118, -0.0047998732944479, 5.49778635595958e-04, 0.0047996365689827, 0.99998838875498, 4.31096311889819e-04, -5.51841459656287e-04, -4.28452543098038e-04, 0.99999975594968],
                                   'CkTableStartTime': -657253835.36655,
                                   'CkTableEndTime': -657253835.36655,
                                   'CkTableOriginalSize': 1,
                                   'EphemerisTimes': [-657253835.36655],
                                   'Quaternions': [[0.46307604735879,0.24654067983613,0.71505811639587,-0.4620283083588]],
                                   'AngularVelocity' : [[0, 0, 0]]},
            'BodyRotation': {'TimeDependentFrames': [10015, 1],
                             'CkTableStartTime': -657253835.36655,
                             'CkTableEndTime': -657253835.36655,
                             'CkTableOriginalSize': 1,
                             'EphemerisTimes': [-657253835.36655],
                             'Quaternions': [[-0.33145588393446,0.082010450701863,0.2049367374262,-0.91728524278656]],
                             'AngularVelocity' : [[-2.56727935591209e-06,-7.56761357895015e-05,1.58716530998994e-04]]},
            'InstrumentPosition': {'SpkTableStartTime': -657253835.36655,
                                   'SpkTableEndTime': -657253835.36655,
                                   'SpkTableOriginalSize': 1,
                                   'EphemerisTimes': [-657253835.36655],
                                   'Positions': [[383694.55065317,122950.66054569,23540.017308183]],
                                   'Velocities': [[-17.802074028598,18.817691029493,8.540401625345]]},
            'SunPosition': {'SpkTableStartTime': -657253835.36655,
                            'SpkTableEndTime': -657253835.36655,
                            'SpkTableOriginalSize': 1,
                            'EphemerisTimes': [-657253835.36655],
                            'Positions': [[482052551.97723,-572516618.3529,-257173526.65669]],
                            'Velocities': [[10.524141391076,6.8590005124774,2.6836839348482]]}}}}

@pytest.fixture(scope='module')
def test_kernels():
    updated_kernels = {}
    binary_kernels = {}
    for image in image_dict.keys():
        kernels = get_image_kernels(image)
        updated_kernels[image], binary_kernels[image] = convert_kernels(kernels)
    yield updated_kernels
    for kern_list in binary_kernels.values():
        for kern in kern_list:
            os.remove(kern)

@pytest.mark.parametrize("label_type", ['isis3'])
@pytest.mark.parametrize("formatter", ['isis'])
@pytest.mark.parametrize("image", image_dict.keys())
# @pytest.mark.skip(reason="Fails due to angular velocity problems")
def test_voyager_load(test_kernels, label_type, formatter, image):
    label_file = get_image_label(image, label_type)

    usgscsm_isd_str = ale.loads(label_file, props={'kernels': test_kernels[image]}, formatter=formatter)
    usgscsm_isd_obj = json.loads(usgscsm_isd_str)
    print(usgscsm_isd_obj)

    assert compare_dicts(usgscsm_isd_obj, image_dict[image][formatter]) == []
