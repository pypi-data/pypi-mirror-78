"""
IB TWS sometimes does not recognize symbols provided by quandl/sharadar. It is painful experience
when your pipeline crashes due to this reason. In order to overcome this we run exclude routine from
this file which creates local copy (pickle file) of the list containing the exclusions. These exclusions
file is then treated in a due way by sharadar-ext insgest module (see sharadar_ext.py).

However in order to run the excluder you have to have already the copy of sharadar-ext (or whatever
bundle you use) on your local machine. So the proper sequence of actions should be:
1) ingest your bundle to your local machine if you don't have any (zipline just installed)
2) run exclude('your bundle')
3) ingest your bundle once again.
"""

from zipline.data import bundles
from zipline.gens.brokers.ib_broker2 import IBBroker
import pandas as pd
from datetime import datetime
import pytz
import pickle
from zipline.data.bundles.sharadar_ext import EXCLUSIONS_FILE
import os

def exclude_from_local(bundle='sharadar-ext',
                       ):
    from logbook import Logger
    log = Logger(__name__)

    tws_uri = 'localhost:7496:1'
    broker = IBBroker(tws_uri)

    bundle_data = bundles.load(
        bundle,
    )

    all_sids = bundle_data.asset_finder.sids
    all_assets = bundle_data.asset_finder.retrieve_all(all_sids)

    exclusions = []

    for i, asset in enumerate(all_assets):
        live_today = pd.Timestamp(datetime.utcnow().date()).replace(tzinfo=pytz.UTC)
        symbol = asset.symbol
        if asset.to_dict()['end_date'] + pd.offsets.BDay(1) >= live_today:
            print(f'Checking {asset.symbol} symbol ({i+1}/{len(all_assets)})')
            contracts = None
            while contracts is None:
                contracts = broker.reqMatchingSymbols(symbol)

            if symbol not in [c.contract.symbol for c in contracts] and '^' not in symbol:
                log.warning(f'!!!No IB ticker data for {symbol}!!!')
                exclusions.append(symbol)
                continue

            ticker = broker.subscribe_to_market_data(symbol)
            broker.cancelMktData(ticker.contract)

            if pd.isna(ticker.last) and pd.isna(ticker.close) and '^' not in symbol:
                log.warning(f'!!!No IB market data for {symbol}!!!')
                exclusions.append(symbol)
        else:
            log.info(f'Skipping check for {asset.symbol} as it is not traded any more')

    with open(EXCLUSIONS_FILE, 'wb') as f:
        pickle.dump(exclusions, f)

    print(f'{len(exclusions)} exclusions found!')

def exclude_from_web(bundle_module='sharadar_ext',
                     look_for_file=False,
                     ):
    import importlib
    from logbook import Logger
    log = Logger(__name__)

    if look_for_file and os.path.exists(EXCLUSIONS_FILE):
        log.info('No need to run excluder, exclusions file has been found!')
        return

    full_bundle_module_name = 'zipline.data.bundles.' + bundle_module

    bundle_module_ref = importlib.import_module(full_bundle_module_name)
    tws_uri = 'localhost:7496:1'
    broker = IBBroker(tws_uri)

    exclusions = []

    api_key = os.environ.get('QUANDL_API_KEY')
    raw_data = bundle_module_ref.fetch_data_table(api_key=api_key,
                                                  show_progress=True,
                                                  retries=1,
                                                  check_exclusions=False,
                                )
    asset_metadata = bundle_module_ref.gen_asset_metadata(raw_data[['symbol', 'date']],
                                                          True
                                                          )

    for i, asset in asset_metadata.iterrows():
        live_today = pd.Timestamp(datetime.utcnow().date()).replace(tzinfo=pytz.UTC)
        asset_end_date = pd.Timestamp(asset['end_date']).replace(tzinfo=pytz.UTC)
        symbol = asset['symbol']
        if asset_end_date + pd.offsets.BDay(1) >= live_today:
            log.info(f'Checking {symbol} symbol ({i+1}/{len(asset_metadata)})')

            contracts = None
            while contracts is None:
                contracts = broker.reqMatchingSymbols(symbol)

            if symbol not in [c.contract.symbol for c in contracts] and '^' not in symbol:
                log.warning(f'!!!No IB ticker data for {symbol}!!!')
                exclusions.append(symbol)
                continue

            ticker = broker.subscribe_to_market_data(symbol)
            broker.cancelMktData(ticker.contract)

            if pd.isna(ticker.last) and pd.isna(ticker.close) and '^' not in symbol:
                log.warning(f'!!!No IB market data for {symbol}!!!')
                exclusions.append(symbol)

        else:
            log.info(f'Skipping check for {symbol} as it is not traded any more: asset_end_date is {asset_end_date}')

    with open(EXCLUSIONS_FILE, 'wb') as f:
        pickle.dump(exclusions, f)

    log.info(f'{len(exclusions)} exclusions found!')