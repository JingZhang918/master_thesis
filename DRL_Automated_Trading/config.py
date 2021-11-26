import os

INITIAL_BALANCE = 1e6
INITIAL_SHARE = 0

saving_path_trading_records = "./trading_records/"
if not os.path.isdir(saving_path_trading_records):
    os.mkdir(saving_path_trading_records)

saving_path_comparison = "./image/"
if not os.path.isdir(saving_path_comparison):
    os.mkdir(saving_path_comparison)

START = "2011-11-01"
END = "2021-11-01"
WINDOW =12*1

# START = "2015-11-01"
# END = "2021-11-01"


SYMBOLS = ["ADS.DE",
           "ALV.DE",
           "BAS.DE",
           "BAYN.DE",
           "BMW.DE",
           "CON.DE",
           # "1COV.DE",
           "DAI.DE",
           # "DHER.DE",
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
           # "ENR.DE",
           "VOW3.DE",
           # "VNA.DE"
          ]


