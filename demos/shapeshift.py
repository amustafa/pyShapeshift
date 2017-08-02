"""
Shapeshift.io API

Implemenets all the API calls on Shapeshift.io

All documentation is taken from https://info.shapeshift.io
"""
import requests


BASE_URL = 'https://shapeshift.io/%s'


def get_coins():
    """
    Gets a list of coins currently supported by Shapeshift.

    url: shapeshift.io/getcoins
    method: GET

    Success Output:

    {
        "SYMBOL1" :
        {
            name: ["Currency Formal Name"],
            symbol: <"SYMBOL1">,
            image: ["https://shapeshift.io/images/coins/coinName.png"],
            status: [available / unavailable]
        }
        (one listing per supported currency)
    }

    The status can be either "available" or "unavailable". Sometimes coins
    become temporarily unavailable during updates or
    unexpected service issues.
    """
    url_path = 'getcoins'
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_rate(input_coin, output_coin):
    """
    Gets the current rate offered by Shapeshift.

    From Shapeshifit:
    url: shapeshift.io/rate/[pair]
    method: GET

    [pair] is any valid coin pair such as btc_ltc or ltc_btc

    Success Output:

    {
        "pair" : "btc_ltc",
        "rate" : "70.1234"
    }
    """
    url_path = "rate/{}_{}".format(input_coin, output_coin)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_deposit_limit(input_coin, output_coin):
    """
    Gets the current deposit limit set by Shapeshift.

    url: shapeshift.io/limit/[pair]
    method: GET

    [pair] is any valid coin pair such as btc_ltc or ltc_btc

    Success Output:
    {
        "pair" : "btc_ltc",
        "limit" : "1.2345"
    }
    """
    url_path = "limit/{}_{}".format(input_coin, output_coin)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_market_info(input_coin, output_coin):
    """
    This gets the market info (pair, rate, limit, minimum limit, miner fee)

    url: shapeshift.io/marketinfo/[pair]
    method: GET

    [pair] (OPTIONAL) is any valid coin pair such as btc_ltc or ltc_btc.
    The pair is not required and if not specified will return an array of all market infos.

    Success Output:
    {
        "pair"     : "btc_ltc",
        "rate"     : 130.12345678,
        "limit"    : 1.2345,
        "min"      : 0.02621232,
        "minerFee" : 0.0001
    }
    """
    url_path = "marketinfo/{}_{}".format(input_coin, output_coin)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_recent_tx_list(max_transactions):
    """
    Get a list of the most recent transactions.

    url: shapeshift.io/recenttx/[max]
    method: GET

    [max] is an optional maximum number of transactions to return.
    If [max] is not specified this will return 5 transactions.
    Also, [max] must be a number between 1 and 50 (inclusive).

    Success Output:
    [
        {
        curIn : [currency input],
        curOut: [currency output],
        amount: [amount],
        timestamp: [time stamp]     //in seconds
        },
        ...
    ]
    """
    assert 1 <= max_transactions <= 50
    url_path = "recenttx/{}".format(max_transactions)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_tx_status(address):
    """
    Gets the status of the most recent transaction to that address.

    url: shapeshift.io/txStat/[address]
    method: GET

    [address] is the deposit address to look up.

    Success Output:  (various depending on status)

    Status: No Deposits Received
    {
        status:"no_deposits",
        address:[address]           //matches address submitted
    }

    Status: Received (we see a new deposit but have not finished processing it)
    {
        status:"received",
        address:[address]           //matches address submitted
    }

    Status: Complete
    {
    status : "complete",
    address: [address],
    withdraw: [withdrawal address],
    incomingCoin: [amount deposited],
    incomingType: [coin type of deposit],
    outgoingCoin: [amount sent to withdrawal address],
    outgoingType: [coin type of withdrawal],
    transaction: [transaction id of coin sent to withdrawal address]
    }

    Status: Failed
    {
    status : "failed",
    error: [Text describing failure]
    }

    """
    url_path = "txStat/{}".format(address)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_time_remaining_on_fixed_tx(address):
    """
    Returns the time remaining on the fixed transaction, since these
    transactions have a 10 minute time limit.

    url: shapeshift.io/timeremaining/[address]
    method: GET

    [address] is the deposit address to look up.

    Success Output:

    {
        status:"pending",
        seconds_remaining: 600
    }

    The status can be either "pending" or "expired".
    If the status is expired then seconds_remaining will show 0.
    """
    url_path = "timeremaining/{}".format(address)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_tx_by_api_key(api_key):
    """
    Allows vendors to get a list of all the transactions performed by
    a particular api key.

    url: shapeshift.io/txbyapikey/[apiKey]
    method: GET

    [apiKey] is the affiliate's PRIVATE api key.

    [
        {
        inputTXID: [Transaction ID of the input coin going into shapeshift],
        inputAddress: [Address that the input coin was paid to for this shift],
        inputCurrency: [Currency type of the input coin],
        inputAmount: [Amount of input coin that was paid in on this shift],
        outputTXID: [Transaction ID of the output coin going out to user],
        outputAddress: [Address that the output coin was sent to for this shift],
        outputCurrency: [Currency type of the output coin],
        outputAmount: [Amount of output coin that was paid out on this shift],
        shiftRate: [The effective rate the user got on this shift.],
        status: [status of the shift]
        }
        (one listing per transaction returned)
    ]

    The status can be  "received", "complete", "returned", "failed".
    """

    url_path = "txbyapikey/{}".format(api_key)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def get_tx_by_address(address, api_key):
    """
    Allows a vendor to look at all the transactions performed at the given address.

    url: shapeshift.io/txbyaddress/[address]/[apiKey]
    method: GET

    [address] the address that output coin was sent to for the shift
    [apiKey] is the affiliate's PRIVATE api key.

    Success Output:

    [
        {
        inputTXID: [Transaction ID of the input coin going into shapeshift],
        inputAddress: [Address that the input coin was paid to for this shift],
        inputCurrency: [Currency type of the input coin],
        inputAmount: [Amount of input coin that was paid in on this shift],
        outputTXID: [Transaction ID of the output coin going out to user],
        outputAddress: [Address that the output coin was sent to for this shift],
        outputCurrency: [Currency type of the output coin],
        outputAmount: [Amount of output coin that was paid out on this shift],
        shiftRate: [The effective rate the user got on this shift.],
        status: [status of the shift]
        }
        (one listing per transaction returned)
    ]

    The status can be  "received", "complete", "returned", "failed".
    """
    url_path = "txbyapikey/{}/{}".format(address, api_key)
    url = BASE_URL % url_path
    response = requests.get(url)
    return response.json()


def validate_address(address, coin_symbol):
    """
    Allows user to verify that the receiving address is valid for the given coin.

    url: shapeshift.io/validateAddress/[address]/[coinSymbol]
    method: GET

    [address] the address that the user wishes to validate
    [coinSymbol] the currency symbol of the coin

    Success Output:


        {
        isValid: [true / false],
        error: [(if isvalid is false, there will be an error message)]
        }


    isValid will either be true or false. If isvalid returns false, an error parameter will be present and will contain a descriptive error message.
    """
    url_path = "validateAddress/{}/{}".format(address, coin_symbol)
    url = BASE_URL % url_path
    print(url)
    response = requests.get(url)
    return response.json()


def create_normal_tx(withdrawal_address, input_coin, output_coin,
            return_address=None,
            destination_tag=None,
            rs_address=None,
            api_key=None):
    """
    This is the primary data input. Creates a deposit address.

    url:  shapeshift.io/shift
    method: POST
    data type: JSON
    data required:
    withdrawal     = the address for resulting coin to be sent to
    pair  = what coins are being exchanged in the form [input coin]_[output coin]  ie btc_ltc
    returnAddress  = (Optional) address to return deposit to if anything goes wrong with exchange
    destTag    = (Optional) Destination tag that you want appended to a Ripple payment to you
    rsAddress  = (Optional) For new NXT accounts to be funded, you supply this on NXT payment to you
    apiKey     = (Optional) Your affiliate PUBLIC KEY, for volume tracking, affiliate payments, split-shifts, etc...

    example data: {"withdrawal":"AAAAAAAAAAAAA", "pair":"btc_ltc", returnAddress:"BBBBBBBBBBB"}

    Success Output:
    {
        deposit: [Deposit Address (or memo field if input coin is BTS / BITUSD)],
        depositType: [Deposit Type (input coin symbol)],
        withdrawal: [Withdrawal Address], //-- will match address submitted in post
        withdrawalType: [Withdrawal Type (output coin symbol)],
        public: [NXT RS-Address pubkey (if input coin is NXT)],
        xrpDestTag : [xrpDestTag (if input coin is XRP)],
        apiPubKey: [public API attached to this shift, if one was given]
    }
    """
    url_path = "shift"
    url = BASE_URL % url_path
    payload = {
        'withdrawal': withdrawal_address,
        'pair': "{}_{}".format(input_coin, output_coin)
    }
    if return_address is not None:
        payload['returnAddress'] = return_address
    if destination_tag is not None:
        payload['destTag'] = destination_tag
    if rs_address is not None:
        payload['rsAddress'] = rs_address
    if api_key is not None:
        payload['apiKey'] = api_key

    response = requests.post(url, data=payload)
    return response.json()


def request_email_receipt(email, tx_id):
    """
    Requests a receipt for a transaction and sends it to the provided email.

    url:  shapeshift.io/mail
    method: POST
    data type: JSON
    data required:
    email    = the address for receipt email to be sent to
    txid       = the transaction id of the transaction TO the user (ie the txid for the withdrawal NOT the deposit)
    example data {"email":"mail@example.com", "txid":"123ABC"}

    Success Output:
    {"email":
    {
        "status":"success",
        "message":"Email receipt sent"
    }
    }
    """
    url_path = "mail"
    url = BASE_URL % url_path
    payload = {
        'email': email,
        'txid': tx_id
    }
    response = requests.post(url, data=payload)
    return response.json()


def create_fixed_amount_tx(amount, withdrawal_address, input_coin, output_coin,
            return_address=None,
            destination_tag=None,
            rs_address=None,
            api_key=None):
    """
    This call allows you to request a fixed amount to be sent to the withdrawal address.

    url: shapeshift.io/sendamount
    method: POST
    data type: JSON

    //1. Send amount request


      Data required:

    amount          = the amount to be sent to the withdrawal address
    withdrawal      = the address for coin to be sent to
    pair            = what coins are being exchanged in the form [input coin]_[output coin]  ie ltc_btc
    returnAddress   = (Optional) address to return deposit to if anything goes wrong with exchange
    destTag         = (Optional) Destination tag that you want appended to a Ripple payment to you
    rsAddress       = (Optional) For new NXT accounts to be funded, supply this on NXT payment to you
    apiKey          = (Optional) Your affiliate PUBLIC KEY, for volume tracking, affiliate payments, split-shifts, etc...

    example data {"amount":123, "withdrawal":"123ABC", "pair":"ltc_btc", returnAddress:"BBBBBBB"}


      Success Output:


    {
     success:
      {
        pair: [pair],
        withdrawal: [Withdrawal Address], //-- will match address submitted in post
        withdrawalAmount: [Withdrawal Amount], // Amount of the output coin you will receive
        deposit: [Deposit Address (or memo field if input coin is BTS / BITUSD)],
        depositAmount: [Deposit Amount], // Exact amount of input coin to send in
        expiration: [timestamp when this will expire],
        quotedRate: [the exchange rate to be honored]
        apiPubKey: [public API attached to this shift, if one was given]
      }
    }




    //2. Quoted Price request


    //Note :  This request will only return information about a quoted rate
    //         This request will NOT generate the deposit address.



      Data required:

    amount  = the amount to be sent to the withdrawal address
    pair    = what coins are being exchanged in the form [input coin]_[output coin]  ie ltc_btc

    example data {"amount":123, "pair":"ltc_btc"}


      Success Output:


    {
     success:
      {
        pair: [pair],
        withdrawalAmount: [Withdrawal Amount], // Amount of the output coin you will receive
        depositAmount: [Deposit Amount], // Exact amount of input coin to send in
        expiration: [timestamp when this will expire],
        quotedRate: [the exchange rate to be honored]
        minerFee: [miner fee for this transaction]
      }
    }
    """

    url_path = "sendamount"
    url = BASE_URL % url_path
    payload = {
        'amount': amount,
        'withdrawal': withdrawal_address,
        'pair': "{}_{}".format(input_coin, output_coin)
    }
    if return_address is not None:
        payload['returnAddress'] = return_address
    if destination_tag is not None:
        payload['destTag'] = destination_tag
    if rs_address is not None:
        payload['rsAddress'] = rs_address
    if api_key is not None:
        payload['apiKey'] = api_key
    response = requests.post(url, data=payload)
    return response.json()


def cancel_tx(address):
    """
    Cancels a pending transaction. Will not work if funds have already
        been sent.

    url: shapeshift.io/cancelpending
    method: POST
    data type: JSON
    data required: address = The deposit address associated with the pending transaction

    Example data : {address : "1HB5XMLmzFVj8ALj6mfBsbifRoD4miY36v"}

    Success Output:

     {  success  : " Pending Transaction cancelled "  }

    Error Output:

     {  error  : {errorMessage}  }
    """
    url_path = "cancelpending"
    url = BASE_URL % url_path
    payload = {
        'address': address,
    }
    response = requests.post(url, data=payload)
    return response.json()


if __name__ == "__main__":
    print('Available Coins: ', get_coins())
    print('BTC LTC Rate', get_rate('btc', 'ltc'))
    print('BTC LTC Deposit Limit', get_deposit_limit('btc', 'ltc'))

    print(get_market_info('btc', 'ltc'))
    print(get_recent_tx_list(10))

    btc_addr = '1JVgLgLvWhr8hVy2AKy2T59fVAHhpJ8jT2'
    print(create_normal_tx(
        btc_addr,
        'ltc',
        'btc',
    ))
