def _highest_cost_rate(stock_exchange) -> float:
    if stock_exchange == 'Frankfurt':
        return 1.01089
    elif stock_exchange == 'Shanghai':
        return 1.00402
    else:
        return 3
        
def _transaction_fee(stock_exchange, signal, transaction_amount) -> float:
    '''
    @params:
        stock_exchange:    'Frankfurt' or 'Shanghai';
        signal:             1 for buy; -1 for sell
        transaction_amount: transaction price x shares
    @return:
        total transaction cost
    '''
    if stock_exchange == 'Frankfurt':

        # fees demanded by stock exchange
        transaction_fee = max(0.60, 0.000096 * transaction_amount)
        trading_fee = max(2.52, 0.000504 * transaction_amount)

        # fees demanded by postbank
        if transaction_amount == 0:
            return 0
        elif transaction_amount <= 1200:
            third_party_fee = 9.95
        elif transaction_amount <= 2600:
            third_party_fee = 17.95
        elif transaction_amount <= 5200:
            third_party_fee = 29.95
        elif transaction_amount <= 12500:
            third_party_fee = 39.95
        elif transaction_amount <= 25000:
            third_party_fee = 54.95
        else:
            third_party_fee = 69.95

        return transaction_fee + trading_fee + third_party_fee

    elif stock_exchange == 'Shanghai':
        if transaction_amount == 0:
            return 0
        commision_charge = max(transaction_amount * 0.003, 5)
        transfer_fee = transaction_amount * 0.00002
        stamp_tax = transaction_amount * 0.001

        return commision_charge + transfer_fee + stamp_tax if signal == -1 else commision_charge + transfer_fee
    else:
        return 10000000
    

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


