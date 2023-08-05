import tensorflow.keras.utils
from collections import namedtuple

#models = namedtuple('models', ['model_name', 'model_url', 'caffe_model', 'caffe_model_url', 'prototxt_name', 'prototxt_url'])
models = namedtuple('models', ['model_name', 'model_url'])
model_name = 'helmet_detector.h5'
model_url = 'https://github.com/jonfernandes/dxc_helmet/raw/master/download/0.1.0/helmet_detector.h5'
#url = 'https://raw.github.com/jonfernandes/dxc_helmet/raw/master/download/0.1.0/helmet_detector.h5'
caffe_model = 'res10_300x300_ssd_iter_140000.caffemodel'
caffe_model_url = 'https://github.com/jonfernandes/dxc_helmet/blob/master/download/0.1.0/res10_300x300_ssd_iter_140000.caffemodel'
prototxt_name = 'deploy.prototxt'
prototxt_url = 'https://github.com/jonfernandes/dxc_helmet/blob/master/download/0.1.0/deploy.prototxt'
'''
tf_27_Aug = models(model_name=model_name, 
                   model_url=model_url,
                   caffe_model=caffe_model, 
                   caffe_model_url=caffe_model_url,
                   prototxt_name=prototxt_name, 
                   prototxt_url=prototxt_url)
'''
tf_27_Aug = models(model_name=model_name, 
                   model_url=model_url)

def get_model(mod=tf_27_Aug):
    helmet = tensorflow.keras.utils.get_file(
        mod.model_name,
        mod.model_url,
        cache_subdir='models'
    )
    '''
    face_model = tensorflow.keras.utils.get_file(
        mod.caffe_model,
        mod.caffe_model_url,
        cache_subdir='models'
    )
    prototxt = tensorflow.keras.utils.get_file(
        mod.prototxt_name,
        mod.prototxt_url,
        cache_subdir='models'
    )
    '''
