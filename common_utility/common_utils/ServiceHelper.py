import importlib
import os
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
sys.stderr = stderr
from common_utils import S3Util
from common_utils import AzureUtil
from common_utils import NASUtil
import pandas as pd
from common_utils.MLLogger import MLLogging
from filelock import FileLock
from threading import Lock

s3Config= S3Util.S3Configuration()
azConfig= AzureUtil.AzureConfiguration()
nasConfig= NASUtil.NASConfiguration()
logger=MLLogging.getLog()

def parsefilePath(filePath):
    """
    Parse the  file Path and extract prefix name and file location.
    s3FilePath Convention: /s3-<bucket-name>/<path/to/file/in/local/and/s3>
    azureFilePath Convention: /az-<container-name>/<path/to/file/in/local/and/azure storage account>
    If it is not parseable it will return the as is filepath as the localFilePath(assuming the string is the S3 object key) and None as the bucketName
    :param filePath: the Complete File Path Location including prefix and the file with directory location
    :return: Splits the string to get prefix name and  file location according to the convention
    """
    prefix = None
    localFilePath = None
    if filePath.startswith("/s3-") or filePath.startswith("/az-"):
        localFilePath = filePath[filePath[1:].index("/") + 2:]
        prefix = filePath[:filePath[1:].index("/") + 1][1:]
    elif filePath.startswith("s3-") or filePath.startswith("az-"):
        localFilePath = filePath[filePath.index("/") + 1:]
        prefix = filePath[:filePath.index("/")]
    else:
        localFilePath = filePath
    return prefix, localFilePath

def makeDirectories(localFileLocation):
    """
    Makes directories in the location of file prior to file creation
    [FORMAT: 'folder1/folder2/filename']
    :param localFileLocation: The location of file where the directories are to be created prior to file creation
    :return: None
    """
    try:
        localFilePath = localFileLocation[:localFileLocation.rindex("/")]
        if not os.path.exists(localFilePath):
            os.makedirs(localFilePath)
    except FileExistsError:
        logger.debug("Folders already Exists")
        pass

def fetchFileFromS3viaLocalApi(s3FullPath,s3Direct=False):
    """
    Takes S3fullPath and downloads the file and return localFileLocation
    :param s3FullPath: S3 file location to download
    :return: localFileLocation of the downloaded file
    """
    try:
        s3util = S3Util.S3LocalUtility()
        bucketName, s3filePath = parsefilePath(s3FullPath)
        localFileLocation = s3util.s3Config.s3_local_folder_path + s3filePath
        logger.info(localFileLocation)
        if os.path.isfile(localFileLocation) and s3Direct is False:
            return localFileLocation
        if bucketName is None:
            raise FileNotFoundError("Bucket not well defined according to format and no file was found in local file system"+str(localFileLocation))
        makeDirectories(localFileLocation)
        with FileLock(str(localFileLocation)+".lock"):
            with Lock():
                if not os.path.isfile(localFileLocation) or s3Direct is True:
                    logger.info("Downloading file from S3: Bucket: " + str(bucketName) + " S3 file path: " + str(s3filePath) + " via Local API")
                    s3util.downloadFileFromS3(s3filePath, localFileLocation, bucketName)
        return localFileLocation
    except Exception as e:
        msg = "Exception While downloading file from S3 Utility: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)


def fetchFileFromAzureviaLocalApi(azFullPath, azDirect=False):
    """
    Takes azFullPath and downloads the file and return localFileLocation
    :param azFullPath: Full path of Azure file
    :return: localFileLocation of the downloaded file
    """
    try:
        containerName, azfilePath = parsefilePath(azFullPath)
        localFileLocation = azConfig.az_local_folder_path + azfilePath
        if os.path.isfile(localFileLocation) and azDirect is False:
            return localFileLocation
        if containerName is None:
            raise FileNotFoundError(
                "File is not found in the local path. No az-hrc bucket configured and incorrect local path was given:" + str(
                    localFileLocation))
        makeDirectories(localFileLocation)
        with configurations.GlobalVariable.ProcessLock(localFileLocation):
            with configurations.GlobalVariable.ThreadLock:
                if not os.path.isfile(localFileLocation) or azDirect is True:
                    logger.info("Downloading file from AZ: Container: " + str(containerName) + " AZ file path: " + str(
                        azfilePath) + " via Local API")
                    azUtil = AzureUtil.AzureLocalUtility()
                    azUtil.downloadFile(containerName, azfilePath, localFileLocation)
        return localFileLocation
    except Exception as e:
        msg = "Exception While downloading file from Azure Utility: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def fetchFileFromNASviaLocalApi(fullFilePath):
    try:
        prefix, filePath = parsefilePath(fullFilePath)
        localFileLocation = nasConfig.nas_local_folder_path + filePath
        logger.debug("Trying to fetch file from NAS: "+str(localFileLocation))
        if os.path.isfile(localFileLocation):
            return localFileLocation
        else:
            raise FileNotFoundError("File is not Found in NAS Storage in "+str(localFileLocation))
    except Exception as e:
        msg = "Exception While loading file from NAS Utility: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def readCsvFromS3(s3FullPath,s3Direct=True,**kwargs):
    """
    Read csv file from S3 given the S3file path
    :param s3FullPath: csv S3 file path
    :param s3Direct: if True always downloads from S3, else searches in local and returns if found
    :param kwargs: arguments to read_csv
    :return: csv file
    """
    try:
        localFileLocation=fetchFileFromS3viaLocalApi(s3FullPath,s3Direct=s3Direct)
        return pd.read_csv(localFileLocation,**kwargs)
    except Exception as e:
        msg = "Exception While reading csv file from S3: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def readCsvFromAzure(azFullPath,azDirect=True,**kwargs):
    try:
        localFileLocation=fetchFileFromAzureviaLocalApi(azFullPath,azDirect=azDirect)
        return pd.read_csv(localFileLocation,**kwargs)
    except Exception as e:
        msg = "Exception While reading csv file from Azure: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def readCsvFromNAS(fullFullPath, **kwargs):
    try:
        localFileLocation=fetchFileFromNASviaLocalApi(fullFullPath)
        return pd.read_csv(localFileLocation,**kwargs)
    except Exception as e:
        msg = "Exception While reading csv file from NAS: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)


def saveDftoS3(df, s3FullPath,**kwargs):
    """
    Saves csv file in S3
    :param df: Dataframe to save to S3
    :param s3FullPath: S3 path to save the csv
    :param kwargs: arguments to save csv
    :return:
    """
    try:
        s3util = S3Util.S3LocalUtility()
        bucketName, s3filePath = parsefilePath(s3FullPath)
        localFileLocation = s3util.s3Config.s3_local_folder_path + s3filePath
        makeDirectories(localFileLocation)
        df.to_csv(localFileLocation,**kwargs)
        s3util.uploadFileToS3(localFileLocation, s3filePath, bucketName)
    except Exception as e:
        msg = "Exception While saving dataframe to csv file and uploading to S3: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def saveDftoAzure(df, azFullPath,**kwargs):
    try:
        azutil = AzureUtil.AzureLocalUtilityy()
        containerName, azfilePath = parsefilePath(azFullPath)
        localFileLocation = azConfig.s3_local_folder_path + azfilePath
        makeDirectories(localFileLocation)
        df.to_csv(localFileLocation,**kwargs)
        azutil.uploadFile(containerName,azfilePath,localFileLocation)
    except Exception as e:
        msg = "Exception While saving dataframe to csv file and uploading to Azure: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def saveDftoNAS(df, fullFullPath, **kwargs):
    try:
        prefix, nasfilePath = parsefilePath(fullFullPath)
        localFileLocation = nasConfig.nas_local_folder_path + nasfilePath
        makeDirectories(localFileLocation)
        df.to_csv(localFileLocation,**kwargs)
    except Exception as e:
        msg = "Exception While saving dataframe to csv file and uploading to NAS: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def checkIfS3FileExist(s3FullPath):
    """
    Check if S3 file exist or not
    :param s3FullPath: S3 file path
    :return: True/False
    """
    s3util = S3Util.S3LocalUtility()
    bucketName, s3filePath = parsefilePath(s3FullPath)
    return s3util.ifS3FileExist(s3filePath,bucketName)

def checkIfS3FileExist(s3FullPath):
    try:
        s3util = S3Util.S3LocalUtility()
        bucketName, s3filePath = parsefilePath(s3FullPath)
        return s3util.ifS3FileExist(s3filePath,bucketName)
    except Exception as e:
        msg = "Exception in checkIfS3FileExist: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def checkIfAzureFileExist(azFullPath):
    try:
        azutil = AzureUtil.AzureLocalUtility()
        containerName, azfilePath = parsefilePath(azFullPath)
        return azutil.checkIfBlobExist(containerName, azfilePath)
    except Exception as e:
        msg = "Exception in checkIfAzureFileExist: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)

def checkIfNASFileExist(hrcFullPath):
    try:
        prefix, nasFilePath = parsefilePath(hrcFullPath)
        localFileLocation = nasConfig.nas_local_folder_path + nasFilePath
        return os.path.isfile(localFileLocation)
    except Exception as e:
        msg = "Exception in checkIfNASFileExist: " + str(type(e).__name__) + " " + str(e)
        logger.error(msg)
        raise Exception(msg)
