import os

if not os.path.isdir("./image"):
    os.mkdir("./image")

saving_path_indicator_visualization = "./image/indicator_visualization/"
if not os.path.isdir(saving_path_indicator_visualization):
    os.mkdir(saving_path_indicator_visualization)

saving_path_indicator_signal =  "./image/signal_visualization/"
if not os.path.isdir(saving_path_indicator_signal):
    os.mkdir(saving_path_indicator_signal)

saving_path_trading_records = "./trading_records/"
if not os.path.isdir(saving_path_trading_records):
    os.mkdir(saving_path_trading_records)


TECHNICAL_INDICATORS = ['MACD', 'RSI', 'SO', 'ADX', 'AO']

TEST_SYMBOLS = ["ADS.DE","ZAL.DE"]

pre_start_date = '2020-09-01'
start_date = '2020-11-01'
end_date = '2021-11-01'

# old DAX 30
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


# new DAX 40
# SYMBOLS = [\
# "ADS.DE"
# ,"ALV.DE"
# ,"BAS.DE"
# ,"BAYN.DE"
# ,"BMW.DE"
# ,"CON.DE"
# ,"1COV.DE"
# ,"DAI.DE"
# ,"DHER.DE"
# ,"DBK.DE"
# ,"DB1.DE"
# ,"DPW.DE"
# ,"DTE.DE"
# ,"DWNI.DE"
# ,"EOAN.DE"
# ,"FRE.DE"
# ,"FME.DE"
# ,"HEI.DE"
# ,"HEN3.DE"
# ,"IFX.DE"
# ,"LIN.DE"
# ,"MRK.DE"
# ,"MTX.DE"
# ,"MUV2.DE"
# ,"RWE.DE"
# ,"SAP.DE"
# ,"SIE.DE"
# ,"ENR.DE"
# ,"VOW3.DE"
# ,"VNA.DE"
# ,"AIR.DE"
# ,"PAH3.DE"
# ,"PUM.DE"
# ,"SHL.DE"
# ,"SY1.DE"
# ,"SRT.DE"
# ,"BNR.DE"
# ,"HFG.DE"
# ,"QIA.DE"
# ,"ZAL.DE"
# ]
















