import pandas as pd
from typing import List
import pysftp

def transferForecastToSftpLocation(configDict: dict, filesNameList:List) -> bool:
    """transfer list of forecast excel report to nldc sftp server

    Args:
        configDict (dict): app config
        filesNameList (List): List of file names ["07_09_2021_WR.xlsx", "08_09_2021_WR.xlsx".... etc]

    Returns:
        bool: return true is transfer successfull
    """    
    
    ftpHost = configDict['ftpHost']
    ftpUsername = configDict['ftpUsername']
    ftpPassword = configDict['ftpPassword']
    ftpFolderPath = configDict['ftpDumpFolder']
    
    # send file via ftp
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(ftpHost, username=ftpUsername, password=ftpPassword, cnopts=cnopts) as sftp:
            sftp.cwd(ftpFolderPath)
            # copy the file to remote ftp folder
            for file in filesNameList:
                sftp.put(file)
        return True
    except Exception as err:
        print(err)
        return False