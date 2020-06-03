from common_utils import ServiceHelper
from common_utils.MLLogger import MLLogging
import pandas as pd
from common_utils import S3Util
from common_utils import AzureUtil
from common_utils import NASUtil
s3Config= S3Util.S3Configuration()
azConfig= AzureUtil.AzureConfiguration()
nasConfig= NASUtil.NASConfiguration()
logger=MLLogging.getLog()


def fetchFileviaLocalApiFactory(file,direct=False):
    if file.startswith("/s3hrc-") or file.startswith("s3hrc-"):
        return ServiceHelper.fetchFileFromS3viaLocalApi(file,s3Direct=direct)
    elif file.startswith("/azhrc-") or file.startswith("azhrc-"):
        return ServiceHelper.fetchFileFromAzureviaLocalApi(file,azDirect=direct)
    elif file.startswith("/nas-") or file.startswith("nas-"):
        return ServiceHelper.fetchFileFromNASviaLocalApi(file)
    else:
        return file


def readCsvFactory(fullFilePath,direct=True,**kwargs):
    if fullFilePath.startswith("/s3hrc-") or fullFilePath.startswith("s3hrc-"):
        return ServiceHelper.readCsvFromS3(fullFilePath,s3Direct=direct,**kwargs)
    elif fullFilePath.startswith("/azhrc-") or fullFilePath.startswith("azhrc-"):
        return ServiceHelper.readCsvFromAzure(fullFilePath,azDirect=direct,**kwargs)
    elif fullFilePath.startswith("/nas-") or fullFilePath.startswith("nas-") :
        return ServiceHelper.readCsvFromNAS(fullFilePath,**kwargs)
    else:
        return pd.read_csv(fullFilePath)

def saveDfFactory(df, fullFilePath,**kwargs):
    if fullFilePath.startswith("/s3hrc-") or fullFilePath.startswith("s3hrc-"):
        return ServiceHelper.saveDftoS3(df, fullFilePath,**kwargs)
    elif fullFilePath.startswith("/azhrc-") or fullFilePath.startswith("azhrc-"):
        return ServiceHelper.saveDftoAzure(df, fullFilePath,**kwargs)
    elif fullFilePath.startswith("/nas-") or fullFilePath.startswith("nas-") :
        return ServiceHelper.saveDftoNAS(df, fullFilePath,**kwargs)
    else:
        makeDirectories(fullFilePath)
        df.to_csv(fullFilePath,**kwargs)
        return

def checkIfFileExistFactory(fullFilePath):
    if fullFilePath.startswith("/s3hrc-") or fullFilePath.startswith("s3hrc-"):
        return ServiceHelper.checkIfS3FileExist(fullFilePath)
    elif fullFilePath.startswith("/azhrc-") or fullFilePath.startswith("azhrc-"):
        return ServiceHelper.checkIfAzureFileExist(fullFilePath)
    elif fullFilePath.startswith("/nas-") or fullFilePath.startswith("nas-"):
        return ServiceHelper.checkIfNASFileExist(fullFilePath)
    else:
        return os.path.isfile(fullFilePath)

def getfileLocationFactory(fullFilePath):
    prefix, filePath = ServiceHelper.parsefilePath(fullFilePath)
    if fullFilePath.startswith("/s3-") or fullFilePath.startswith("s3-"):
        localFileLocation = s3Config.s3_local_folder_path + filePath
    elif fullFilePath.startswith("/az-") or fullFilePath.startswith("az-"):
        localFileLocation = azConfig.az_local_folder_path + filePath
    elif fullFilePath.startswith("/nas-") or fullFilePath.startswith("nas-"):
        localFileLocation = nasConfig.nas_local_folder_path + filePath
    else:
        localFileLocation = fullFilePath
    return localFileLocation
