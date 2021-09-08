import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple, Union


class IntradayForecastedDemandFetchRepo():
    """block wise intraday forecasted demand fetch repository for R0A
    """

    def __init__(self, con_string):
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string

    def fetchIntradayForecastedDemand(self, startDate: dt.datetime, endDate: dt.datetime)-> pd.DataFrame:
        """fetch intraday forecast

        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date

        Returns:
            pd.DataFrame: intraday forecast dataframe(TIME_STAMP, ENTITY_TAG, FORECASTED_DEMAND_VALUE)
        """        
        startTime = startDate
        endTime = endDate+dt.timedelta(hours=23, minutes= 59, seconds=59)
        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)
        else:
            try:
                cur = connection.cursor()
                fetch_sql = "SELECT time_stamp, entity_tag, forecasted_demand_value FROM dayahead_demand_forecast WHERE time_stamp BETWEEN TO_DATE(:start_time,'YYYY-MM-DD HH24:MI:SS') and TO_DATE(:end_time,'YYYY-MM-DD HH24:MI:SS') ORDER BY entity_tag, time_stamp"
                cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                intradayForecastedDemandDf = pd.read_sql(fetch_sql, params={
                                 'start_time': startTime, 'end_time': endTime}, con=connection)
                
            except Exception as err:
                print('error while creating a cursor', err)
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
            
        return intradayForecastedDemandDf