from pyShapeshift import api

if __name__ == "__main__":
    print('Available Coins: ', api.get_coins())
    print('BTC LTC Rate', api.get_rate('btc', 'ltc'))
    print('BTC LTC Deposit Limit', api.get_deposit_limit('btc', 'ltc'))

    print(api.get_market_info('btc', 'ltc'))
    print(api.get_recent_tx_list(10))

    btc_addr = '1JVgLgLvWhr8hVy2AKy2T59fVAHhpJ8jT2'
    print(api.create_normal_tx(
        btc_addr,
        'ltc',
        'btc',
    ))
