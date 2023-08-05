import pysftp

myHostname = "82.223.115.66"
myUsername = "canper"
myPassword = "1234"

# with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:

#     # Define the file that you want to upload from your local directorty
#     # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
#     localFilePath = './TUTORIAL2.txt'

#     # Define the remote path where the file will be uploaded
#     remoteFilePath = '/var/integraweb-db-backups/TUTORIAL2.txt'

#     sftp.put('README.md', 'C:\\Users\\CASA\Desktop\\README.md')


with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    # Define the file that you want to download from the remote directory
    remoteFilePath = 'C:\\Users\\CASA\\icondssdsddfs.exe'

    # Define the local path where the file will be saved
    # or absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
    localFilePath = 'icon.exe'

    sftp.get(remoteFilePath, localFilePath)
