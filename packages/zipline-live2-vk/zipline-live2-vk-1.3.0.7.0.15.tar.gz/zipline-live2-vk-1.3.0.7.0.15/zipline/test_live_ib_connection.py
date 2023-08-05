import pandas as pd
from zipline.gens.brokers.ib_broker import IBBroker
from zipline import run_algorithm

tws_uri = 'localhost:7496:1236'
brokerobj = IBBroker (tws_uri)

start = pd.to_datetime('2020-06-25').tz_localize('US/Eastern')
end = pd.to_datetime('2020-07-16').tz_localize('US/Eastern')

def initialize(context):
    pass

def handle_data(context, data):
    pass

def before_trading_start(context, data):
    pass

result = run_algorithm(
    start=start,
    end=end,
    initialize=initialize,
    handle_data=handle_data,
    before_trading_start=before_trading_start,
    analyze=None,
    capital_base=10e5,
    data_frequency='minute',
    bundle='sharadar-funds', # whatever your bundle is
    broker=brokerobj,
    state_filename = 'test.state'
)