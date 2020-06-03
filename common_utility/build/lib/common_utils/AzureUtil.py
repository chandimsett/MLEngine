from common_utils.MLLogger import MLLogging
import configurations
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
logger=MLLogging.getLog()

class AzureConfiguration(object):
    """Initialize Azure Configuration Object from the project properties file"""
    def __init__(self):
        self.config = configurations.projectConfigurations.config
        self.credentialsConfig=configurations.credentialsConfiguration.config
        if 'Azure' in self.config.keys():
            if 'Azure_local_folder_path' in self.config['Azure'].keys() and self.config['Azure']['Azure_local_folder_path'] is not None:
                self.az_local_folder_path= self.config['Azure']['Azure_local_folder_path']
            if 'storage_account_name' in self.config['Azure'].keys() and self.config['Azure']['storage_account_name'] is not None:
                self.storage_account_name= self.config['Azure']['storage_account_name']
        if 'Azure Credentials' in self.credentialsConfig.keys():
            if 'account_key' in self.credentialsConfig['Azure Credentials'].keys() and self.credentialsConfig['Azure Credentials']['account_key'] is not None:
                self.account_key = self.credentialsConfig['Azure Credentials']['account_key']

class AzureLocalUtility(object):
    def __init__(self):
        try:
            self.azureConfig=AzureConfiguration()
            self.conn_str = 'DefaultEndpointsProtocol=https;AccountName='+self.azureConfig.storage_account_name+';AccountKey='+self.azureConfig.account_key+';EndpointSuffix=core.windows.net'
            self.blob_service_client = BlobServiceClient.from_connection_string(conn_str=self.conn_str)
        except Exception as e:
            msg = "Exception in configuring Azure Local Utility: " + str(type(e).__name__) + " " + str(e)
            logger.error(msg)
            raise Exception(msg)


    def downloadFile(self,container_name,az_file_name,localFileLocation):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=az_file_name)
            logger.info("Downloading from Azure Storage as blob: " + localFileLocation)
            with open(localFileLocation, "wb") as my_blob:
                my_blob.writelines([blob_client.download_blob().readall()])
        except Exception as e:
            msg = "Exception in downloading file via Azure Local Utility: " + str(type(e).__name__) + " " + str(e)
            logger.error(msg)
            raise Exception(msg)

    def uploadFile(self,container_name,az_file_name,localFileLocation):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=az_file_name)
            logger.info("Uploading to Azure Storage as blob: " + localFileLocation)
            with open(localFileLocation, "rb") as data:
                blob_client.upload_blob(data)
        except Exception as e:
            msg = "Exception in uploading file via Azure Local Utility: " + str(type(e).__name__) + " " + str(e)
            logger.error(msg)
            raise Exception(msg)

    def checkIfBlobExist(self,container_name,az_file_name):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=az_file_name)
            logger.info("Checking if Azure Storage blob exists: " )
            try:
                blob_client.get_blob_properties()
                return True
            except ResourceNotFoundError as e:
                return False
        except Exception as e:
            msg = "Exception in checking file existence via Azure Local Utility: " + str(type(e).__name__) + " " + str(e)
            logger.error(msg)
            raise Exception(msg)
