import importlib
import pandas as pd
import sys
import ast
from common_utils import ServiceHelperFactory
from common_utils.MLLogger import MLLogging
import os
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
sys.stderr = stderr
logger=MLLogging.getLog()
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

def loadDataFramesFromDict(fileDict):
    """
    Load the dataframes from a given dictionary of file paths
    :param fileDict: {key: 'filepath'}
    :return:{key: file}
    """
    try:
        dfs={}
        for key in fileDict.keys():
            dfs[key]= ServiceHelperFactory.readCsvFactory(fileDict[key])
        return dfs
    except Exception as e:
        msg ="Unable to load csv file(s) into dataframes: " + str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception()


def loadDataFramesFromList(filePaths):
    """
    Load Dataframes from list
    :param filePaths: list of file paths
    :return: list of files
    """
    try:
        dfs = []
        for i in filePaths:
            df = ServiceHelperFactory.readCsvFactory(i)
            dfs.append(df)
        return dfs
    except Exception as e:
        msg="Unable to load csv file(s) into dataframes: "+str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception(msg)


def moduleClassFunctionInvoke(moduleClassFunctionPath, *arguments):
    """
    Return a function call dynamically from a string function path.
    It applies reflections to load the function from the given class and module from a string
    :param moduleClassFunctionPath: full path of the module-class-function
    :param arguments: arguments to pass to the function
    :return: function invocation with arguments
    """
    try:
        extractPath=moduleClassFunctionPath.rsplit('.', 2)
        module_name,py_class_name,function_name=extractPath[0],extractPath[1],extractPath[2]
        module = importlib.import_module(module_name)
        py_class = getattr(module, py_class_name)()
        return getattr(py_class, function_name)(*arguments)
    except Exception as e:
        msg="Problem in invocation function: "+str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception(msg)


def moduleClassType(moduleClassFunctionPath):
    """
    Returns the type of a function dynamically from a string function path.
    :param moduleClassFunctionPath: full path of the module-class-function
    :return: type of the invoked function
    """
    try:
        extractPath=moduleClassFunctionPath.rsplit('.', 2)
        module_name,py_class_name,function_name=extractPath[0],extractPath[1],extractPath[2]
        module = importlib.import_module(module_name)
        py_class = getattr(module, py_class_name)()
        return type(py_class)
    except Exception as e:
        msg="Problem in invocation function (Class checking failed):  "+str(type(e).__name__) + str(e)
        logger.error(msg)
        raise Exception(msg)