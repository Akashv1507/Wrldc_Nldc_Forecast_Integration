call project_env\Scripts\activate.bat
call python index_intradayForecastRepGenerator.py >>intraday_log.txt 2>&1
call python index_intradayNldcSftpTransfer.py >>intraday_log.txt 2>&1