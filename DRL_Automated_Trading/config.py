import os

ETF_EXPENSE = 0.0016

# differ with START and END
yearly_trading_days = {2016:43, 2017: 255, 2018: 252, 2019: 251, 2020: 254, 2021: 212}
monthly_trading_days = {
     2016: {11:22,12:21}
    , 2017: {1 :22.0,2 :20.0,3 :23.0,4 :18.0,5 :22.0,6 :22.0,7 :21.0,8 :23.0,9 :21.0,10:22.0,11:22.0,12:19.0}
    , 2018: {1 :22.0,2 :20.0,3 :21.0,4 :20.0,5 :22.0,6 :21.0,7 :22.0,8 :23.0,9 :20.0,10:22.0,11:22.0,12:17.0}
    , 2019: {1:22,2:20,3:21,4:20,5:22,6:19,7:23,8:22,9:21,10:22,11:21,12:18}
    , 2020:{1:22,2:20,3:22,4:20,5:20,6:21,7:23,8:21,9:22,10:22,11:21,12:20}
    , 2021:{1:20,2:20,3:23,4:20,5:20,6:22,7:22,8:22,9:22,10:21
}}

INITIAL_BALANCE = 1e6
INITIAL_SHARE = 0
TRADING_OUTLAY = list()

saving_path_trading_records = "./trading_records/"
if not os.path.isdir(saving_path_trading_records):
    os.mkdir(saving_path_trading_records)

saving_path_images = "./image/"
if not os.path.isdir(saving_path_images):
    os.mkdir(saving_path_images)

START = "2011-11-01"
END = "2021-11-01"
# END = "2018-11-01"

WINDOW =12*1
TRAINING_YEARS = 5



SYMBOLS = ["ADS.DE",
           "ALV.DE",
           "BAS.DE",
           "BAYN.DE",
           "BMW.DE",
           "CON.DE",
           "1COV.DE",
           "DAI.DE",
           "DHER.DE",
           "DBK.DE",
           "DB1.DE",
           "DPW.DE",
           "DTE.DE",
           "DWNI.DE",
           "EOAN.DE",
           "FRE.DE",
           "FME.DE",
           "HEI.DE",
           "HEN3.DE",
           "IFX.DE",
           "LIN.DE",
           "MRK.DE",
           "MTX.DE",
           "MUV2.DE",
           "RWE.DE",
           "SAP.DE",
           "SIE.DE",
           "ENR.DE",
           "VOW3.DE",
           "VNA.DE"
          ]


