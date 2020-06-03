from keras import models
from sklearn.externals import joblib
from common_utils import ServiceHelperFactory
from common_utils import ServiceHelper
from functools import lru_cache

def getValFromDict(name, data):
    """
    Get the value from the key from a given dictionary and return custom exception messages if not found
    :param name: key to search
    :param data: Dictionary to search from
    :return: value for the given search key
    """
    if name in data and data[name] is not None:
        return data[name]
    elif name not in data:
        raise KeyError(str(name)+" is not defined in the request parameter")
    elif data[name] is None:
        raise TypeError(str(name)+" cannot be None type")

@lru_cache(maxsize=20)
def load_pipeline_cache(fullFilePath):
    """
    Load the file into the memory using a LRU Caching of maxsize by deriving location and appending local S3 storage path with relative s3 file path
    :param fullFilePath: full file location for the model
    :return: Pickle Object
    """
    try:
        localFileLocation=ServiceHelperFactory.getfileLocationFactory(fullFilePath)
        return joblib.load(localFileLocation)
    except Exception as e:
        msg = "Exception While loading the model from a file: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def load_h5_file(fullFilePath):
    """
    Load the Keras specific h5 model file from the local file system
    :param fullFilePath: full file location for the model
    :return: keras model file
    """
    try:
        localFileLocation=ServiceHelperFactory.getfileLocationFactory(fullFilePath)
        return models.load_model(localFileLocation)
    except Exception as e:
        msg = "Exception While loading the keras model configs from a h5 file: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)
