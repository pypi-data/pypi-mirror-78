Requirement:

This library requires greater than 3.6 version of python.

Installment:
First install marketanalyst package from pip so do

pip install marketanalyst
python -m pip install marketanalyst

This will download the package itself and dependencies that is uses.

How to use:

Import the package.
import marketanalyst
Make a client which can be used to call all the other methods.
	client = marketanalyst.client("your api key","your secret key")
The client is ready to use, it can be used to call the below methods.

Methods:

getallsecurities:
df = client.getallsecurities("nasdaq","stock")
or 
df = client.getallsecurities(lookup="aapl")
or
df = client.getallsecurities(master_id="67702,48525")
This will return a dataframe like this:
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



getallindicator:
df = client.getallindicator(lookup="eod")
or
df = client.getallindicator(indicator_category="4")
or
df = client.getallindicator(indicator="1,3")
Return:

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

getuserportfolio:
df = client.getuserportfolio(11)

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

getportfoliodetails:
df = client.getportfoliodetails(11,58)
Return:

  master_id                   name exchange_id exchange_code symbol security_type_id holdings_type holdings
0     61821       NASDAQ Composite           4         INDEX   CCMP               23             0     None
1     61869  DJ Industrial Average           4         INDEX   INDU               23             0     None
2     62384         NYSE Composite           4         INDEX    NYA               23             0     None
3     62870          S&P 500 Index           4         INDEX    SPX               23             0     None

getportfoliodata:
df = client.getportfoliodata(11,58,"371,373")
Return:

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

getdata:
df = client.getdata(["aapl","msft"],"price","2020-01-01,07:00:00","2020-01-05,12:00:00")
Return:

  master_id indicator_id         value data_type     ts_date   ts_hour
0     45406          330  1.357336e+12         0  2020-01-02  00:00:00
1     45406          330  1.344140e+12         0  2020-01-03  00:00:00
2     45406          335  2.509190e+01         0  2020-01-02  00:00:00
3     45406          335  2.484795e+01         0  2020-01-03  00:00:00
4     45406          337  5.330931e+00         0  2020-01-02  00:00:00
5     45406          337  5.279104e+00         0  2020-01-03  00:00:00
6     45406          415  1.025470e-02         0  2020-01-02  00:00:00
7     45406          415  1.035538e-02         0  2020-01-03  00:00:00
8     45406          744  1.532789e+01         0  2020-01-02  00:00:00
9     45406          744  1.517887e+01         0  2020-01-03  00:00:00
0     47070          330  1.226399e+12         0  2020-01-02  00:00:00
1     47070          330  1.211129e+12         0  2020-01-03  00:00:00
2     47070          335  2.996642e+01         0  2020-01-02  00:00:00
3     47070          335  2.959328e+01         0  2020-01-03  00:00:00
4     47070          337  9.445457e+00         0  2020-01-02  00:00:00
5     47070          337  9.327845e+00         0  2020-01-03  00:00:00
6     47070          415  1.145561e-02         0  2020-01-02  00:00:00
7     47070          415  1.160005e-02         0  2020-01-03  00:00:00
8     47070          744  1.156122e+01         0  2020-01-02  00:00:00
9     47070          744  1.141726e+01         0  2020-01-03  00:00:00

getOHLCVData:
df = client.getOHLCVData(["aapl","msft","AAAU"],"2020-01-01,07:00:00","2020-01-30,12:00:00")

Return:

               datetime exchange symbol      open      high       low    close      volume
0   2020-01-02 00:00:00   NASDAQ   AAPL  296.2400  300.6000  295.1900  300.350  33911864.0
1   2020-01-03 00:00:00   NASDAQ   AAPL  297.1500  300.5800  296.5000  297.430  36633878.0
2   2020-01-06 00:00:00   NASDAQ   AAPL  293.7900  299.9600  292.7500  299.800  29644644.0
3   2020-01-07 00:00:00   NASDAQ   AAPL  299.8400  300.9000  297.4800  298.390  27877655.0
4   2020-01-08 00:00:00   NASDAQ   AAPL  297.1600  304.4399  297.1560  303.190  33090946.0
5   2020-01-09 00:00:00   NASDAQ   AAPL  307.2350  310.4300  306.2000  309.630  42621542.0
6   2020-01-10 00:00:00   NASDAQ   AAPL  310.6000  312.6700  308.2500  310.330  35217272.0
7   2020-01-13 00:00:00   NASDAQ   AAPL  311.6400  317.0700  311.1500  316.960  30521722.0
8   2020-01-14 00:00:00   NASDAQ   AAPL  316.7000  317.5700  312.1700  312.680  40653457.0
9   2020-01-15 00:00:00   NASDAQ   AAPL  311.8500  315.5000  309.5500  311.340  30480882.0
10  2020-01-16 00:00:00   NASDAQ   AAPL  313.5900  315.7000  312.0900  315.240  27207254.0
11  2020-01-17 00:00:00   NASDAQ   AAPL  316.2700  318.7400  315.0000  318.730  34454117.0
12  2020-01-21 00:00:00   NASDAQ   AAPL  317.1900  319.0200  316.0000  316.570  27710814.0
13  2020-01-22 00:00:00   NASDAQ   AAPL  318.5800  319.9900  317.3100  317.700  25458115.0
14  2020-01-23 00:00:00   NASDAQ   AAPL  317.9200  319.5600  315.6500  319.230  26117993.0
15  2020-01-24 00:00:00   NASDAQ   AAPL  320.2500  323.3300  317.5188  318.310  36634380.0
16  2020-01-27 00:00:00   NASDAQ   AAPL  310.0600  311.7700  304.8800  308.950  40485005.0
17  2020-01-28 00:00:00   NASDAQ   AAPL  312.6000  318.4000  312.1900  317.690  40558486.0
18  2020-01-29 00:00:00   NASDAQ   AAPL  324.4500  327.8500  321.3800  324.340  54149928.0
19  2020-01-30 00:00:00   NASDAQ   AAPL  320.5435  324.0900  318.7500  323.870  31685808.0
20  2020-01-02 00:00:00   NASDAQ   MSFT  158.7800  160.7300  158.3300  160.620  22634546.0
21  2020-01-03 00:00:00   NASDAQ   MSFT  158.3200  159.9450  158.0600  158.620  21121681.0
22  2020-01-06 00:00:00   NASDAQ   MSFT  157.0800  159.1000  156.5100  159.030  20826702.0
23  2020-01-07 00:00:00   NASDAQ   MSFT  159.3200  159.6700  157.3200  157.580  21881740.0
24  2020-01-08 00:00:00   NASDAQ   MSFT  158.9300  160.8000  157.9491  160.090  27762026.0
25  2020-01-09 00:00:00   NASDAQ   MSFT  161.8350  162.2150  161.0300  162.090  21399951.0
26  2020-01-10 00:00:00   NASDAQ   MSFT  162.8235  163.2200  161.1800  161.340  20733946.0
27  2020-01-13 00:00:00   NASDAQ   MSFT  161.7600  163.3100  161.2600  163.280  21637007.0
28  2020-01-14 00:00:00   NASDAQ   MSFT  163.3900  163.6000  161.7200  162.130  23500783.0
29  2020-01-15 00:00:00   NASDAQ   MSFT  162.6200  163.9400  162.5700  163.180  21417871.0
30  2020-01-16 00:00:00   NASDAQ   MSFT  164.3500  166.2400  164.0300  166.170  23865360.0
31  2020-01-17 00:00:00   NASDAQ   MSFT  167.4200  167.4675  165.4300  167.100  34371659.0
32  2020-01-21 00:00:00   NASDAQ   MSFT  166.6800  168.1900  166.4300  166.500  29517191.0
33  2020-01-22 00:00:00   NASDAQ   MSFT  167.4000  167.4900  165.6800  165.700  24138777.0
34  2020-01-23 00:00:00   NASDAQ   MSFT  166.1900  166.8000  165.2700  166.720  19680766.0
35  2020-01-24 00:00:00   NASDAQ   MSFT  167.5100  167.5300  164.4500  165.040  24918117.0
36  2020-01-27 00:00:00   NASDAQ   MSFT  161.1500  163.3750  160.2000  162.280  32078067.0
37  2020-01-28 00:00:00   NASDAQ   MSFT  163.7800  165.7550  163.0730  165.460  24899940.0
38  2020-01-29 00:00:00   NASDAQ   MSFT  167.8400  168.7500  165.6900  168.040  35127771.0
39  2020-01-30 00:00:00   NASDAQ   MSFT  174.0500  174.0500  170.7900  172.780  51597470.0
40  2020-01-02 00:00:00     AMEX   AAAU   15.2400   15.2750   15.2000   15.250     43147.0
41  2020-01-03 00:00:00     AMEX   AAAU   15.4500   15.4900   15.4179   15.450     53449.0
42  2020-01-06 00:00:00     AMEX   AAAU   15.7600   15.7658   15.5900   15.620     84879.0
43  2020-01-07 00:00:00     AMEX   AAAU   15.6400   15.6999   15.6399   15.680     37083.0
44  2020-01-08 00:00:00     AMEX   AAAU   15.7500   15.7500   15.4865   15.560    136634.0
45  2020-01-09 00:00:00     AMEX   AAAU   15.4800   15.5100   15.4100   15.465     24655.0
46  2020-01-10 00:00:00     AMEX   AAAU   15.5000   15.5700   15.4955   15.570     99055.0
47  2020-01-13 00:00:00     AMEX   AAAU   15.5000   15.5100   15.2600   15.450    170858.0
48  2020-01-14 00:00:00     AMEX   AAAU   15.4000   15.4400   15.3750   15.435     43493.0
49  2020-01-15 00:00:00     AMEX   AAAU   15.5000   15.5400   15.4549   15.520     41800.0
50  2020-01-16 00:00:00     AMEX   AAAU   15.5000   15.5001   15.4500   15.490     78193.0
51  2020-01-17 00:00:00     AMEX   AAAU   15.5300   15.5800   15.5100   15.530     91640.0
52  2020-01-21 00:00:00     AMEX   AAAU   15.4500   15.6700   15.4400   15.550    164200.0
53  2020-01-22 00:00:00     AMEX   AAAU   15.5400   15.5500   15.5100   15.550     28900.0
54  2020-01-23 00:00:00     AMEX   AAAU   15.5400   15.6400   15.5400   15.590    125200.0
55  2020-01-24 00:00:00     AMEX   AAAU   15.5600   15.7200   15.5600   15.680     68600.0
56  2020-01-27 00:00:00     AMEX   AAAU   15.8000   15.8000   15.7400   15.790     56800.0
57  2020-01-28 00:00:00     AMEX   AAAU   15.7200   15.7300   15.6500   15.650     37700.0
58  2020-01-29 00:00:00     AMEX   AAAU   15.6500   15.7400   15.6400   15.730     29700.0
59  2020-01-30 00:00:00     AMEX   AAAU   15.7600   15.8100   15.7000   15.740     87200.0

export_df:
With this method you can export a dataframe to a csv or excel.
client.export_df(df,'excel',r"D:\some_folder\filename")
This example is for windows.