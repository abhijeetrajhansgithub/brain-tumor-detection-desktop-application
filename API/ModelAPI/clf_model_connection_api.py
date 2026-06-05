from Models.load_model import GET_MODEL_PATHS__for_btcm_mdl_v01s, GET_MODEL_PATHS__for_btcm_mdl_21ms

def access_h5_model__for_btcm_mdl_v01():
    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_v01s()
    return h5_MODEL_path

def access_keras_model__for_btcm_mdl_21m():
    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_21ms()
    return keras_MODEL_path

def access_keras_model__for_btcm_mdl_v01():
    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_v01s()
    return keras_MODEL_path

def access_h5_model__for_btcm_mdl_21m():
    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_21ms()
    return h5_MODEL_path

def get_current_system_path():
    import os
    return os.path.dirname(os.path.abspath(__file__))

def access_BOTH_models__for_btcm_mdl_v01s():
    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_v01s()
    return h5_MODEL_path, keras_MODEL_path

def access_BOTH_models__for_btcm_mdl_21ms():
    h5_MODEL_path, keras_MODEL_path = GET_MODEL_PATHS__for_btcm_mdl_21ms()
    return h5_MODEL_path, keras_MODEL_path

def CLASSIFY_IMAGE_H5_MODEL(image_path, h5_MODEL_path, keras_MODEL_path):
    pass

def CLASSIFY_IMAGE_KERAS_MODEL(image_path, h5_MODEL_path, keras_MODEL_path):
    pass

def CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s(h5_MODEL_path, keras_MODEL_path, image_path):
    from Models.load_model import CLASSIFY__for_btcm_mdl_v01
    return CLASSIFY__for_btcm_mdl_v01(h5_MODEL_path=h5_MODEL_path, keras_MODEL_path=keras_MODEL_path, image_path=image_path)

def CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_21ms(h5_MODEL_path, keras_MODEL_path, image_path):
    from Models.load_model import CLASSIFY__for_btcm_mdl_21m
    return CLASSIFY__for_btcm_mdl_21m(h5_MODEL_path=h5_MODEL_path, keras_MODEL_path=keras_MODEL_path, image_path=image_path)

def CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_v01s_using_direct_pixmap(h5_MODEL_path, keras_MODEL_path, image_pixmap):
    from Models.load_model import CLASSIFY__for_btcm_mdl_v01_using_direct_pixmap
    return CLASSIFY__for_btcm_mdl_v01_using_direct_pixmap(h5_MODEL_path=h5_MODEL_path, keras_MODEL_path=keras_MODEL_path, pixmap=image_pixmap)

def CLASSIFY_IMAGE_wBOTH_MODELS__for_btcm_mdl_21ms_using_direct_pixmap(h5_MODEL_path, keras_MODEL_path, image_pixmap):
    from Models.load_model import CLASSIFY__for_btcm_mdl_21m_using_direct_pixmap
    return CLASSIFY__for_btcm_mdl_21m_using_direct_pixmap(h5_MODEL_path=h5_MODEL_path, keras_MODEL_path=keras_MODEL_path, pixmap=image_pixmap)