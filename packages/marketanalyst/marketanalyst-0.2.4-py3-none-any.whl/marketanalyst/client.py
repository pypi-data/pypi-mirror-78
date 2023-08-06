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
    # this is a new comment added 0.2.4
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

    def getportfoliodata(self,user,portfolio,inidicators):
        params = {"user":user,"portfolio":portfolio,"inidicators":inidicators}
        portfolio_url = self.base_url + "/get_portfolio_data"
        response = requests.get(portfolio_url, params=params)
        try:
            return pd.DataFrame.from_dict(response.json()["security_values"])
        except:
            raise ValueError(response.text)

    def get_indicator_category_id(self,indicator="",indicator_category="",lookup=""):
        params = {"format":"json"}
        if indicator:
            params["indicator"] = indicator
        if indicator_category:
            params["indicator_category"] = indicator_category
        if lookup:
            params["lookup"] = lookup
        response = requests.get(self.base_url + "/get_indicator",params=params)
        try:
            indicator_data = response.json()
            indicator_category_id = indicator_data[0]["indicator_category_id"]
            return indicator_category_id
        except:
            raise ValueError(response.text)

    def getdata(self,symbol,indicator,date_start,date_end,master_id="",indicator_id="",order="",no_cols=""):
        self.validate_date(date_start)
        self.validate_date(date_end)
        start_date_object = datetime.datetime.strptime(date_start, '%Y-%m-%d,%H:%M:%S')
        end_date_object = datetime.datetime.strptime(date_end, '%Y-%m-%d,%H:%M:%S')
        if end_date_object < start_date_object:
            raise ValueError("end date is before start date")
        try:
            indicator_category_id = self.get_indicator_category_id(lookup=indicator)
        except:
            indicator_category_id = None
        if indicator_category_id == None:
            raise ValueError("did not find indicator")
        main_symbol_object = {}
        for temp_symbol in symbol:
            symbol_param = {"lookup":temp_symbol.split(":")[-1],"format":"json"}
            response = requests.get(self.base_url + "/get_master" ,params=symbol_param)
            symbol_data = response.json()
            for temp_symbol_data in symbol_data:
                exchange_id = temp_symbol_data["exchange_id"]
                security_type_id = temp_symbol_data["security_type_id"]
                master_id = temp_symbol_data["master_id"]
                exchange_code = temp_symbol_data["exchange_code"]
                symbol_code = temp_symbol_data["symbol"]
                main_symbol_object[temp_symbol] = {"exchange_id":exchange_id,"security_type_id":security_type_id,"master_id":master_id,"exchange_code":exchange_code,"symbol_code":symbol_code}
        return_df = pd.DataFrame(columns = ['master_id',"indicator_id",'value','data_type','ts_date','ts_hour'])
        for main_symbol in main_symbol_object:
            params = {"exchange":main_symbol_object[main_symbol]["exchange_id"],"security_type":main_symbol_object[main_symbol]["security_type_id"],"indicator_category":indicator_category_id,"date_start":date_start,"format":"csv"}
            params["date_end"] = date_end
            params["master_id"] = main_symbol_object[main_symbol]["master_id"]
            main_request = requests.get(self.base_url + "/get_data",params=params)
            try:
                symbol_df = pd.read_csv(StringIO(main_request.text))
                return_df = return_df.append(symbol_df)
            except:
                pass
        return return_df

    def getOHLCVData(self,symbol,date_start,date_end):
        self.validate_date(date_start)
        self.validate_date(date_end)
        start_date_object = datetime.datetime.strptime(date_start, '%Y-%m-%d,%H:%M:%S')
        end_date_object = datetime.datetime.strptime(date_end, '%Y-%m-%d,%H:%M:%S')
        if end_date_object < start_date_object:
            raise ValueError("end date is before start date")
        main_symbol_object = {}
        for temp_symbol in symbol:
            symbol_param = {"lookup":temp_symbol.split(":")[-1],"format":"json"}
            response = requests.get(self.base_url + "/get_master" ,params=symbol_param)
            symbol_data = response.json()
            for temp_symbol_data in symbol_data:
                exchange_id = temp_symbol_data["exchange_id"]
                security_type_id = temp_symbol_data["security_type_id"]
                master_id = temp_symbol_data["master_id"]
                exchange_code = temp_symbol_data["exchange_code"]
                symbol_code = temp_symbol_data["symbol"]
                main_symbol_object[temp_symbol] = {"exchange_id":exchange_id,"security_type_id":security_type_id,"master_id":master_id,"exchange_code":exchange_code,"symbol_code":symbol_code}
        return_df = pd.DataFrame(columns = ['datetime',"exchange",'symbol','open','high','low','close','volume'])
        for main_symbol in main_symbol_object:
            params = {"exchange":main_symbol_object[main_symbol]["exchange_id"],"security_type":main_symbol_object[main_symbol]["security_type_id"],"indicator_category":1,"date_start":date_start,"format":"csv"}
            params["date_end"] = date_end
            params["master_id"] = main_symbol_object[main_symbol]["master_id"]
            params["indicator_id"] = "371,373,375,377,379"
            main_request = requests.get(self.base_url + "/get_data",params=params)
            try:
                return_symbol = main_symbol_object[main_symbol]["symbol_code"]
                return_exchange = main_symbol_object[main_symbol]["exchange_code"]
                symbol_df = pd.read_csv(StringIO(main_request.text))
                symbol_df["new_date"] = symbol_df["ts_date"] + " " + symbol_df["ts_hour"]
                for ticker_group_name, ticker_group_df in symbol_df.groupby("new_date"):
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
                    return_entry = [datetime_df['new_date'].unique()[0],return_exchange,return_symbol,open_value,high_value,low_value,close_value,volume_value]
                    return_df.loc[len(return_df)] = return_entry
            except:
                pass
        return return_df

    def export_df(self,df,file_format,path): # export a dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Please provide a dataframe")
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