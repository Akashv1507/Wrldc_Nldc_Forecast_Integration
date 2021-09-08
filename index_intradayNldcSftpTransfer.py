import argparse
from datetime import datetime as dt, timedelta
from src.appConfig import loadAppConfig
from src.nldcSftpTransfer import transferForecastToSftpLocation
from utils.printUtils import printWithTs


configDict = loadAppConfig()

startDate = dt.now()
endDate = startDate

# get start and end dates from command line
parser = argparse.ArgumentParser()
parser.add_argument('--start_date', help="Enter start date in yyyy-mm-dd format",
                    default=dt.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter end date in yyyy-mm-dd format",
                    default=dt.strftime(endDate, '%Y-%m-%d'))

args = parser.parse_args()
startDate = dt.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.strptime(args.end_date, '%Y-%m-%d')

startDate = startDate.replace(
    hour=0, minute=0, second=0, microsecond=0)
endDate = endDate.replace(
    hour=0, minute=0, second=0, microsecond=0)

filesNameList = []
currDate = startDate
while currDate <= endDate:
    # creating entire file path
    fileName = configDict['localForecastCsvDumpPath'] + "\\" + dt.strftime(currDate, '%d_%m_%Y') + "_WR.xlsx"
    filesNameList.append(fileName)
    currDate += timedelta(days=1)

res = transferForecastToSftpLocation(configDict, filesNameList)
if res == True:
    printWithTs("Intraday Forecast Report transfer to NLDC via SFTP successfull", clr='green')
else:
    printWithTs("Intraday Forecast Report transfer to NLDC via SFTP unsuccessfull", clr='red')