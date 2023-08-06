## requirement

This library requires greater than 3.6 version of python.

## Installment:
First install marketanalyst package from pip so do
```bash
pip install marketanalyst
python -m pip install marketanalyst
```
This will download the package itself and dependencies that is uses.

## How to use:

```python
import marketanalyst
```
Make a client which can be used to call all the other methods.
```python
client = marketanalyst.client()
```
The client is ready to use, it can be used to call the below methods.

## Methods:

All of these methods will return either a string with error message or a dataframe as a success
1) Getallsecurities:
```python
df = client.getallsecurities("nasdaq","stock")
```
OR
```python
df = client.getallsecurities(lookup="aapl")
```
OR
```python
df = client.getallsecurities(master_id="67702,48525")
```
This will return a dataframe like this:
```bash
     exchange_code  exchange_id symbol security_type  security_type_id  master_id  company_id                           name news_function  keyword_id currency country_code
0           NASDAQ            1    AAL         STOCK                 4      45402       45402    American Airlines Group Inc    NASDAQ:AAL         5.0      USD           US
1           NASDAQ            1   AAME         STOCK                 4      45403       45403  Atlantic American Corporation   NASDAQ:AAME         7.0      USD           US
2           NASDAQ            1   AAOI         STOCK                 4      45404       45404    Applied Optoelectronics Inc   NASDAQ:AAOI         9.0      USD           US
3           NASDAQ            1   AAON         STOCK                 4      45405       45405                       AAON Inc   NASDAQ:AAON        10.0      USD           US
4           NASDAQ            1   AAPL         STOCK                 4      45406       45406                      Apple Inc   NASDAQ:AAPL        12.0      USD           US
...            ...          ...    ...           ...               ...        ...         ...                            ...           ...         ...      ...          ...
2274        NASDAQ            1   ZSAN         STOCK                 4      49553       49553      Zosano Pharma Corporation   NASDAQ:ZSAN     15827.0      USD           US
2275        NASDAQ            1   ZUMZ         STOCK                 4      48186       48186                     Zumiez Inc   NASDAQ:ZUMZ      4297.0      USD           US
2276        NASDAQ            1    ZVO         STOCK                 4      43124       43124                      Zovio Inc    NASDAQ:ZVO         NaN      USD           US
2277        NASDAQ            1   ZYNE         STOCK                 4      68720       68720    Zynerba Pharmaceuticals Inc   NASDAQ:ZYNE      4298.0      USD           US
2278        NASDAQ            1   ZYXI         STOCK                 4      71587       71587                      ZYNEX INC   NASDAQ:ZYXI     21454.0      USD           US

[2279 rows x 12 columns]
```

Here title is the name of security and id represents the database id that was assigned to this security.

2) getallcategory:
```python
df = client.getallindicator(lookup="eod")
```
OR
```python
df = client.getallindicator(indicator_category="4")
```
OR
```python
df = client.getallindicator(indicator="1,3")
```
This will return a dataframe like this:
```bash
   indicator_id         indicator  indicator_category_id indicator_category       title                      definition    data_type  data_type_id
0           371  D_EODCLOSE_EXT_1                      1              Price   EOD Close     Close Value of the security  TYPE_NUMBER             0
1           372  D_EODCLOSE_EXT_2                      1              Price   EOD Close     Close Value of the security  TYPE_NUMBER             0
2           373   D_EODHIGH_EXT_1                      1              Price    EOD High      High Value of the security  TYPE_NUMBER             0
3           374   D_EODHIGH_EXT_2                      1              Price    EOD High      High Value of the security  TYPE_NUMBER             0
4           375    D_EODLOW_EXT_1                      1              Price     EOD Low       Low Value of the security  TYPE_NUMBER             0
5           376    D_EODLOW_EXT_2                      1              Price     EOD Low       Low Value of the security  TYPE_NUMBER             0
6           377   D_EODOPEN_EXT_1                      1              Price    EOD Open      Open Value of the security  TYPE_NUMBER             0
7           378   D_EODOPEN_EXT_2                      1              Price    EOD Open      Open Value of the security  TYPE_NUMBER             0
8           379    D_EODVOL_EXT_1                      1              Price  EOD Volume  Volume traded for the security  TYPE_NUMBER             0
9           380    D_EODVOL_EXT_2                      1              Price  EOD Volume  Volume traded for the security  TYPE_NUMBER             0
```
3) getuserportfolio:
```python
df = client.getuserportfolio(11)
```
This will return a dataframe like this:
```bash
{
    "global_portfolio": {
        "portfolio": {
            "AMEX:ADR": "2",
            "AMEX:ETF": "4",
            "AMEX:STOCK": "5",
            "AS:STOCK": "38",
            "AUPVT:STOCK": "42",
            "BATS:ETF": "6",
            "BSE:ETF": "7",
            "BSE:STOCK": "8",
            "CAPVT:STOCK": "43",
            "CHPVT:STOCK": "44",
            "CO:STOCK": "36",
            "COMEX:SPOT": "9",
            "DEPVT:STOCK": "45",
            "FOREX:CROSS": "10",
            "FOREX:SPOT": "11",
            "FRPVT:STOCK": "46",
            "GBPVT:STOCK": "47",
            "HKEX:ETF": "12",
            "HKEX:HSHARES": "29",
            "HKEX:STOCK": "28",
            "INDEX:INDEX": "13",
            "INDMF:MF": "14",
            "KO:STOCK": "31",
            "LSE:STOCK": "40",
            "NASDAQ100": "63",
            "NASDAQ:ADR": "15",
            "NASDAQ:ETF": "16",
            "NASDAQ:STOCK": "17",
            "NSE:ETF": "18",
            "NSE:REIT": "26",
            "NSE:STOCK": "19",
            "NYMEX:SPOT": "20",
            "NYSE:ADR": "21",
            "NYSE:STOCK": "22",
            "PA:STOCK": "34",
            "PORTFOLIO:INDEX": "41",
            "RUSSELL2000": "69",
            "SGX:ETF": "23",
            "SGX:REIT": "24",
            "SGX:STOCK": "27",
            "SHG:STOCK": "33",
            "SP500": "67",
            "SW:STOCK": "30",
            "TO:STOCK": "39",
            "TSE:STOCK": "35",
            "TW:STOCK": "32",
            "USPVT:STOCK": "48",
            "XETRA:STOCK": "37",
            "ZAPVT:STOCK": "49"
        },
        "user_id": "2"
    },
    "user_portfolio": {
        "portfolio": {
            "KRISTAL-GLOBAL-INDICES": "58",
            "KRISTAL-GLOBAL-STOCKS": "57",
            "KRISTAL-INDICES": "59"
        },
        "user_id": "11"
    }
}
```
4) getportfoliodetails:
```python
df = client.getportfoliodetails(11,58)
```
This will return a dataframe like this:
```bash
  master_id                   name exchange_id exchange_code symbol security_type_id holdings_type holdings
0     61821       NASDAQ Composite           4         INDEX   CCMP               23             0     None
1     61869  DJ Industrial Average           4         INDEX   INDU               23             0     None
2     62384         NYSE Composite           4         INDEX    NYA               23             0     None
3     62870          S&P 500 Index           4         INDEX    SPX               23             0     None
```

5) getportfoliodata:
```python
df = client.getportfoliodata(11,58,"371,373")
```
This will return a dataframe like this:

```bash
   master_id indicator_id      value data_type     ts_date   ts_hour
0      61821          371   11939.67         0  2020-09-01  00:00:00
1      61821          373   11945.72         0  2020-09-01  00:00:00
2      61821          375   11794.78         0  2020-09-01  00:00:00
3      61821          377   11844.13         0  2020-09-01  00:00:00
4      61821          379          0         0  2020-09-01  00:00:00
5      61869          371   28645.66         0  2020-09-01  00:00:00
6      61869          373   28659.26         0  2020-09-01  00:00:00
7      61869          375   28290.91         0  2020-09-01  00:00:00
8      61869          377   28439.61         0  2020-09-01  00:00:00
9      61869          379  428663800         0  2020-09-01  00:00:00
10     62384          371   13113.74         0  2020-09-01  00:00:00
11     62384          373   13113.93         0  2020-09-01  00:00:00
12     62384          375   13004.17         0  2020-09-01  00:00:00
13     62384          377   13032.04         0  2020-09-01  00:00:00
14     62384          379          0         0  2020-09-01  00:00:00
15     62870          371    3526.65         0  2020-09-01  00:00:00
16     62870          373    3528.03         0  2020-09-01  00:00:00
17     62870          375     3494.6         0  2020-09-01  00:00:00
18     62870          377    3507.44         0  2020-09-01  00:00:00
19     62870          379          0         0  2020-09-01  00:00:00
```

6) getdata:
```python
df = client.getdata(exchange=1,security_type=4,indicator_category=1,date_start="2020-01-01,07:00:00",date_end="2020-01-05,12:00:00",master_id="45406,45549",indicator_id="377,379")
```
This will return a dataframe like this:
```bash
   master_id  indicator_id         value  data_type     ts_date   ts_hour
0      45406           377  7.406000e+01          0  2020-01-02  00:00:00
1      45406           377  7.429000e+01          0  2020-01-03  00:00:00
2      45406           379  1.354804e+08          0  2020-01-02  00:00:00
3      45406           379  1.463228e+08          0  2020-01-03  00:00:00
4      45549           377  1.875000e+03          0  2020-01-02  00:00:00
5      45549           377  1.864500e+03          0  2020-01-03  00:00:00
6      45549           379  4.035910e+06          0  2020-01-02  00:00:00
7      45549           379  3.766604e+06          0  2020-01-03  00:00:00
```

7) getOHLCVData:
```python
df = client.getOHLCVData(exchange=1,security_type=4,date_start="2020-01-01,07:00:00",date_end="2020-01-31,12:00:00",master_id="45406,45549")
```
This will return a dataframe like this:
```bash
               datetime exchange_id master_id     open       high        low    close       volume
0   2020-01-02 00:00:00           1     45406    74.06    75.1500    73.8000    75.09  135480400.0
1   2020-01-03 00:00:00           1     45406    74.29    75.1400    74.1300    74.36  146322800.0
2   2020-01-06 00:00:00           1     45406    73.45    74.9900    73.1900    74.95  118387200.0
3   2020-01-07 00:00:00           1     45406    74.96    75.2200    74.3700    74.60  108872000.0
4   2020-01-08 00:00:00           1     45406    74.29    76.1100    74.2900    75.80  132079200.0
5   2020-01-09 00:00:00           1     45406    76.81    77.6100    76.5500    77.41  170108400.0
6   2020-01-10 00:00:00           1     45406    77.65    78.1700    77.0600    77.58  140644800.0
7   2020-01-13 00:00:00           1     45406    77.91    79.2700    77.7900    79.24  121532000.0
8   2020-01-14 00:00:00           1     45406    79.18    79.3900    78.0400    78.17  161954400.0
9   2020-01-15 00:00:00           1     45406    77.96    78.8800    77.3900    77.83  121923600.0
10  2020-01-16 00:00:00           1     45406    78.40    78.9300    78.0200    78.81  108829200.0
11  2020-01-17 00:00:00           1     45406    79.07    79.6800    78.7500    79.68  137816400.0
12  2020-01-21 00:00:00           1     45406    79.30    79.7500    79.0000    79.14  110843200.0
13  2020-01-22 00:00:00           1     45406    79.64    80.0000    79.3300    79.43  101832400.0
14  2020-01-23 00:00:00           1     45406    79.48    79.8900    78.9100    79.81  104472000.0
15  2020-01-24 00:00:00           1     45406    80.06    80.8300    79.3800    79.58  146537600.0
16  2020-01-27 00:00:00           1     45406    77.51    77.9400    76.2200    77.24  161940000.0
17  2020-01-28 00:00:00           1     45406    78.15    79.6000    78.0500    79.42  162234000.0
18  2020-01-29 00:00:00           1     45406    81.11    81.9600    80.3500    81.08  216229200.0
19  2020-01-30 00:00:00           1     45406    80.14    81.0200    79.6900    80.97  126743200.0
20  2020-01-31 00:00:00           1     45406    80.23    80.6700    77.0700    77.38  199588400.0
21  2020-01-02 00:00:00           1     45549  1875.00  1898.0100  1864.1500  1898.01    4035910.0
22  2020-01-03 00:00:00           1     45549  1864.50  1886.1966  1864.5000  1874.97    3766604.0
23  2020-01-06 00:00:00           1     45549  1860.00  1903.6900  1860.0000  1902.88    4065698.0
24  2020-01-07 00:00:00           1     45549  1904.50  1913.8900  1892.0434  1906.86    4134010.0
25  2020-01-08 00:00:00           1     45549  1898.04  1910.9998  1886.4448  1891.97    3511966.0
26  2020-01-09 00:00:00           1     45549  1909.89  1917.8200  1895.8038  1901.05    3174962.0
27  2020-01-10 00:00:00           1     45549  1905.37  1906.9400  1880.0000  1883.16    2856959.0
29  2020-01-14 00:00:00           1     45549  1885.88  1887.1100  1858.5500  1869.44    3446381.0
30  2020-01-15 00:00:00           1     45549  1872.25  1878.8600  1855.0900  1862.02    2896592.0
31  2020-01-16 00:00:00           1     45549  1882.99  1885.5900  1866.0200  1877.94    2659493.0
32  2020-01-17 00:00:00           1     45549  1885.89  1886.6400  1857.2500  1864.72    3997340.0
33  2020-01-21 00:00:00           1     45549  1865.00  1894.2700  1860.0000  1892.00    3707785.0
34  2020-01-22 00:00:00           1     45549  1896.09  1902.5000  1883.3400  1887.46    3216257.0
35  2020-01-23 00:00:00           1     45549  1885.11  1889.9750  1872.7600  1884.58    2484613.0
36  2020-01-24 00:00:00           1     45549  1891.37  1894.9900  1847.4400  1861.64    3766181.0
37  2020-01-27 00:00:00           1     45549  1820.00  1841.0000  1815.3400  1828.34    3528509.0
38  2020-01-28 00:00:00           1     45549  1840.50  1858.1100  1830.0200  1853.25    2808040.0
39  2020-01-29 00:00:00           1     45549  1864.00  1874.7500  1855.0200  1858.00    2101390.0
40  2020-01-30 00:00:00           1     45549  1858.00  1872.8700  1850.6100  1870.68    6327438.0
41  2020-01-31 00:00:00           1     45549  2051.47  2055.7200  2002.2700  2008.72   15567283.0
```
8) export_df:
With this method you can export a dataframe to a csv or excel.
```python
client.export_df(df,'excel',r"D:\some_folder\filename")
```
This example is for windows.
For now three formats are supported json,excel,csv.
