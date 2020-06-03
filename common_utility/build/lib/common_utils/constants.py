class Constants:
    VM_ENVIRONMENT_VARIABLE='HR_ENV'
    CONFIGURATION_FOLDER='configs/'
    CREDENTIALS_PROPERTIES_FILENAME='credentials.properties'
    CONTAINER_ID="HOSTNAME"
    PROJECT_PROPERTIES_FILENAME = 'project.properties'

projectConfigurations= ProjectConfigurations(Constants.VM_ENVIRONMENT_VARIABLE, Constants.CONFIGURATION_FOLDER, Constants.PROJECT_PROPERTIES_FILENAME)
credentialsConfiguration= CredentialsConfigurations(Constants.CONFIGURATION_FOLDER, Constants.CREDENTIALS_PROPERTIES_FILENAME)

