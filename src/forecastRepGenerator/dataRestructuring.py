import pandas as pd 
import datetime as dt 
from src.forecastRepGenerator.dataWithColumnNumMapping import generateDataWithColNoMapping
from openpyxl.utils import get_column_letter, column_index_from_string
from src.typedefs.restructuredData import IRestructuredObj,IRestructuredObjList


def restructureData (df:pd.DataFrame, dataIdentifier:str)-> IRestructuredObjList:
    """take dataframe and return restructured IRestructuredObjList

    Args:
        df (pd.DataFrame): input dataframe(TIME_STAMP, ENTITY_TAG, VALUE)
        dataIdentifier (str): daFor, intraFOr, actDem

    Returns:
        IRestructuredObjList: List of [{'columnNo': columnNo, 'data': data}, similarly for each states]
                            here column number is, column no of raw excel where that entity data to be populted.
    """      

    resData: IRestructuredObjList = []
    columnMapping = generateDataWithColNoMapping()
    # replacing tag with readable names
    df.replace({'ENTITY_TAG' : { 'WRLDCMP.SCADA1.A0047000' : 'WR_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046980' : 'Maharashtra_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046957' : 'Gujarat_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046978' : 'Madhya Pradesh_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046945' : 'Chattisgarh_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046962' : 'Goa_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046948' : 'DD_' + dataIdentifier, 'WRLDCMP.SCADA1.A0046953' : 'DNH_' + dataIdentifier }}, inplace=True)
    #pivoting df and adding identifiers to df columns like Maharashtra_daFor, Maharashtra_intraFor, Maharashtra_actDem
    if dataIdentifier == 'actDem':
        pivotDf= pd.pivot_table(df, values = 'DEMAND_VALUE', index=['TIME_STAMP'], columns = 'ENTITY_TAG').reset_index()
    else:
        pivotDf= pd.pivot_table(df, values = 'FORECASTED_DEMAND_VALUE', index=['TIME_STAMP'], columns = 'ENTITY_TAG').reset_index()
    
    # excluding timestamp column
    pivotDfColumns = pivotDf.columns.tolist()[1:]

    for col in pivotDfColumns:
        # in mapping, column no mentioned in character A, B, BD etc. Converting that to integer
        columnNo = column_index_from_string(columnMapping[col])
        data = pivotDf[col].tolist()
        #iterating through each column and adding obj {column no in raw report, and list of data} to final list
        tempDict:IRestructuredObj = {'columnNo': columnNo, 'data': data}
        resData.append(tempDict)

    return resData