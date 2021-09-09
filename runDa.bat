call project_env\Scripts\activate.bat
call python index_daForecastRepGenerator.py >>DA_log.txt 2>&1
call python index_daNldcSftpTransfer.py >>DA_log.txt 2>&1