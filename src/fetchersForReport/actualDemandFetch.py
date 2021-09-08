import pandas as pd
import datetime as dt
from typing import List, Tuple, TypedDict
from src.fetchersForReport.scadaApiFetcher import ScadaApiFetcher
from utils.printUtils import printWithTs

class ActualDemandFetchFromApi():

    def __init__(self, tokenurl:str, apiBaseUrl:str, clientId:str, clientSecret:str ):
        
        self.tokenUrl: str = tokenurl
        self.apiBaseUrl: str = apiBaseUrl
        self.clientId:str = clientId
        self.clientSecret:str = clientSecret

    def toBlockWiseData(self, demandDf:pd.core.frame.DataFrame, entity:str)->pd.core.frame.DataFrame:
        """convert to blockwise 

        Args:
            demandDf (pd.core.frame.DataFrame): random secondwise dataframe (TIME_STAMP, ENTITY_TAG, DEMAND_VALUE)
            entity (str): entity tag

        Returns:
            pd.core.frame.DataFrame: unfiltered blockwise dataframe(TIME_STAMP, ENTITY_TAG, DEMAND_VALUE)
        """         
        try:
            # to minwise
            demandDf = demandDf.resample('1min', on='TIME_STAMP').agg({'DEMAND_VALUE': 'first'})# this will set TIME_STAMP as index of dataframe
            # to blockwise
            demandDf= demandDf.resample('15min').mean()   
        except Exception as err:
            printWithTs(err, clr='red')
        demandDf.insert(0, "ENTITY_TAG", entity)                      # inserting column entityName with all values of 96 block = entity
        demandDf.reset_index(inplace=True)
        return demandDf

    def filterAction(self, demandDf :pd.core.frame.DataFrame, minRamp:int)-> pd.DataFrame:
        """filtering action

        Args:
            demandDf (pd.core.frame.DataFrame): demand dataframe (TIME_STAMP, ENTITY_TAG, DEMAND_VALUE)
            minRamp (int): [description]

        Returns:
            pd.DataFrame: filtered actual blockwise demand dataframe(TIME_STAMP, ENTITY_TAG, DEMAND_VALUE)
        """         
         
        for ind in demandDf.index.tolist()[1:]:
            if abs(demandDf['DEMAND_VALUE'][ind]-demandDf['DEMAND_VALUE'][ind-1]) > minRamp :
                demandDf['DEMAND_VALUE'][ind] = demandDf['DEMAND_VALUE'][ind-1]
        return demandDf
        

    def applyFilteringToDf(self, demandDf : pd.core.frame.DataFrame, entity:str)->pd.DataFrame:
        """apply filtering logic

        Args:
            demandDf (pd.core.frame.DataFrame): dataframe(TIME_STAMP, ENTITY_TAG, DEMAND_VALUE)
            entity (str): entity tag

        Returns:
            pd.DataFrame: filtered actual blockwise demand dataframe(TIME_STAMP, ENTITY_TAG, DEMAND_VALUE
        """        
        if entity == 'WRLDCMP.SCADA1.A0046945':
            demandDf = self.filterAction(demandDf, 500)

        if entity == 'WRLDCMP.SCADA1.A0046948' or entity == 'WRLDCMP.SCADA1.A0046962' or entity == 'WRLDCMP.SCADA1.A0046953':
            demandDf = self.filterAction(demandDf, 200)
        
        if entity == 'WRLDCMP.SCADA1.A0046957' or entity == 'WRLDCMP.SCADA1.A0046978' or entity == 'WRLDCMP.SCADA1.A0046980':
            demandDf = self.filterAction(demandDf, 1000)
    
        if entity == 'WRLDCMP.SCADA1.A0047000':
            demandDf = self.filterAction(demandDf, 2000)
        return demandDf


    def fetchDemandDataFromApi(self, startDate: dt.datetime, endDate:dt.datetime)->pd.DataFrame:
        """ fetch actual demand fro scada real time api

        Args:
            startDate (dt.datetime): startDate
            endDate (dt.datetime): endDate

        Returns:
            pd.DataFrame: actual blockwise demand dataframe(TIME_STAMP, ENTITY_TAG, DEMAND_VALUE)
        """        
        startTime = startDate
        endTime = endDate+dt.timedelta(hours=23, minutes= 59, seconds=59)
        
        #initializing temporary empty dataframe that append demand values of all entities
        storageDf = pd.DataFrame(columns = [ 'TIME_STAMP','ENTITY_TAG','DEMAND_VALUE']) 

        #list of all entities
        listOfEntity =['WRLDCMP.SCADA1.A0046945','WRLDCMP.SCADA1.A0046948','WRLDCMP.SCADA1.A0046953','WRLDCMP.SCADA1.A0046957','WRLDCMP.SCADA1.A0046962','WRLDCMP.SCADA1.A0046978','WRLDCMP.SCADA1.A0046980','WRLDCMP.SCADA1.A0047000']
        
        #creating object of ScadaApiFetcher class 
        obj_scadaApiFetcher = ScadaApiFetcher(self.tokenUrl, self.apiBaseUrl, self.clientId, self.clientSecret)

        for entity in listOfEntity:
            # fetching secondwise data from api for each entity(TIME_STAMP,value) and converting to dataframe
            resData = obj_scadaApiFetcher.fetchData(entity, startTime, endTime)
            if len(resData)>0:
                demandDf = pd.DataFrame(resData, columns =['TIME_STAMP','DEMAND_VALUE']) 

                #converting to minutewise and then blockwise data and adding entityName column to dataframe
                demandDf = self.toBlockWiseData(demandDf,entity)
                
                # handling missing values NANs
                demandDf['DEMAND_VALUE'].fillna(method='ffill', inplace= True)
                demandDf['DEMAND_VALUE'].fillna(method='bfill', inplace= True)
                
                #applying filtering logic 
                filteredDemandDf = self.applyFilteringToDf(demandDf,entity)

                #appending blockwise demand data for each entity to tempDf
                storageDf = pd.concat([storageDf,filteredDemandDf ],ignore_index=True)
        
        return storageDf
        