import requests
import pandas as pd
import requests
import random 
import string
import numpy as np
import socket
import threading
import websocket
import datetime
from io import StringIO

class client:
    def __init__(self,base_url="http://35.184.152.222:9999"):

        self.base_url = base_url

    def validate_date(self,date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d,%H:%M:%S')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD,hh:mm:ss")

    def getallsecurities(self,exchange="",security_type="",master_id="",lookup=""):
        params = {"format":"csv"}
        security_url = self.base_url + "/get_master"
        if exchange:
            params["exchange"] = exchange
        if security_type:
            params["security_type"] = security_type
        if master_id:
            params["master_id"] = master_id
        if lookup:
            params["lookup"] = lookup
        response = requests.get(security_url, params=params)
        try:
            if "[ERROR]" in response.text:
                raise ValueError(response.text)
            else:
                return pd.read_csv(StringIO(response.text))
        except:
            raise ValueError(response.text)

    def getallindicator(self,indicator="",indicator_category="",lookup=""):
        params = {"format":"csv"}
        getallindicator_url = self.base_url + "/get_indicator"
        if indicator:
            params["indicator"] = indicator
        if indicator_category:
            params["indicator_category"] = indicator_category
        if lookup:
            params["lookup"] = lookup
        response = requests.get(getallindicator_url, params=params)
        try:
            if "[ERROR]" in response.text:
                raise ValueError(response.text)
            else:
                return pd.read_csv(StringIO(response.text))
        except:
            raise ValueError(response.text)

    def getuserportfolio(self,user):
        params = {"user":user}
        portfolio_url = self.base_url + "/get_user_portfolio"
        response = requests.get(portfolio_url, params=params)
        try:
            return response.json()
        except:
            raise ValueError(response.text)

    def getportfoliodetails(self,user,portfolio):
        params = {"user":user,"portfolio":portfolio}
        portfolio_url = self.base_url + "/get_portfolio_details"
        response = requests.get(portfolio_url, params=params)
        try:
            return pd.DataFrame.from_dict(response.json()["portfolio_details"])
        except:
            raise ValueError(response.text)

    def getportfoliodata(self,user,portfolio,indicators):
        params = {"user":user,"portfolio":portfolio,"indicators":indicators}
        portfolio_url = self.base_url + "/get_portfolio_data"
        response = requests.get(portfolio_url, params=params)
        try:
            return pd.DataFrame.from_dict(response.json()["security_values"])
        except:
            raise ValueError(response.text)

    def getdata(self,exchange="",security_type="",indicator_category="",date_start="",date_end="",master_id="",indicator_id=""):
        if exchange == "" or exchange == None:
            raise ValueError("Please provice valid exchange")
        if security_type == "" or security_type == None:
            raise ValueError("Please provice valid security_type")
        if indicator_category == "" or indicator_category == None:
            raise ValueError("Please provice valid indicator_category")
        if date_start == "" or date_start == None:
            raise ValueError("Please provice valid date_start")
        if date_end == "" or date_end == None:
            date_end = date_start
        self.validate_date(date_start)
        self.validate_date(date_end)
        start_date_object = datetime.datetime.strptime(date_start, '%Y-%m-%d,%H:%M:%S')
        end_date_object = datetime.datetime.strptime(date_end, '%Y-%m-%d,%H:%M:%S')
        if end_date_object < start_date_object:
            raise ValueError("end date is before start date")
        params = {"format":"csv"}
        params["exchange"] = exchange
        params["security_type"] = security_type
        params["indicator_category"] = indicator_category
        params["date_start"] = date_start
        params["date_end"] = date_end
        if master_id:
            params["master_id"] = master_id
        if indicator_id:
            params["indicator_id"] = indicator_id
        main_request = requests.get(self.base_url + "/get_data",params=params)
        try:
            return pd.read_csv(StringIO(main_request.text))
        except:
            raise ValueError("could not load dataframe")

    def getOHLCVData(self,exchange="",security_type="",date_start="",date_end="",master_id=""):
        df = self.getdata(exchange,security_type,1,date_start,date_end,master_id=master_id)
        return_df = pd.DataFrame(columns = ['datetime',"exchange_id",'master_id','open','high','low','close','volume'])
        try:
            df["new_date"] = df["ts_date"] + " " + df["ts_hour"]
            for group_name, group_df in df.groupby("master_id"):
                ticker_df = group_df.copy()
                for ticker_group_name, ticker_group_df in ticker_df.groupby("new_date"):
                    datetime_df = ticker_group_df.copy()
                    open_price = datetime_df[datetime_df["indicator_id"] == 377]
                    if open_price.empty == False:
                        open_value = open_price["value"].unique()[0]
                    else:
                        open_value = np.nan
                    low_price = datetime_df[datetime_df["indicator_id"] == 375]
                    if low_price.empty == False:
                        low_value = low_price["value"].unique()[0]
                    else:
                        low_value = np.nan
                    high_price = datetime_df[datetime_df["indicator_id"] == 373]
                    if high_price.empty == False:
                        high_value = high_price["value"].unique()[0]
                    else:
                        high_value = np.nan
                    volume = datetime_df[datetime_df["indicator_id"] == 379]
                    if volume.empty == False:
                        volume_value = volume["value"].unique()[0]
                    else:
                        volume_value = np.nan
                    close_price = datetime_df[datetime_df["indicator_id"] == 371]
                    if close_price.empty == False:
                        close_value = close_price["value"].unique()[0]
                    else:
                        close_value = np.nan
                    return_entry = [datetime_df['new_date'].unique()[0],exchange,datetime_df['master_id'].unique()[0],open_value,high_value,low_value,close_value,volume_value]
                    return_df.loc[len(return_df)] = return_entry
            return return_df
        except Exception as e:
            raise ValueError(e)

    def export_df(self,df,file_format,path): # export a dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Please provide a dataframe")
        try:
            if file_format == 'csv':
                if ".csv" == path[-4:]:
                    df.to_csv(path, index = None, header=True)
                else:
                    df.to_csv(path + ".csv", index = None, header=True)
            if file_format == 'excel':
                if ".xlsx" == path[-5:]:
                    df.to_excel(path, index = None, header=True)
                else:
                    df.to_excel(path + ".xlsx", index = None, header=True)
            if file_format == 'json' or file_format == "JSON":
                if ".json" == path[-5:]:
                    df.to_json(path, orient='records')
                else:
                    df.to_json(path + ".json", orient='records')
        except Exception as e:
            raise ValueError(e)