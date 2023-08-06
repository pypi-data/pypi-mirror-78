import alpaca_trade_api as tradeapi

# Create the api object
api_live = tradeapi.REST(
    key_id='AKKX4ZN1KOXH2ITZ3S3K',
    secret_key='f1Ejw7unlZltOChVKIWy5zWtusW7WPvgb4ILpq8M',
    base_url="https://api.alpaca.markets"
)
# Create the api object
api_paper = tradeapi.REST(
    key_id='PKJM1O6ST2JBEJIYFRU9',
    secret_key='aSbLHh/4703H/4DraSHdtnqwBmfQIqqNiQcVNVGH',
    base_url="https://paper-api.alpaca.markets",
)

poly = api_paper.polygon