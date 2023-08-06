import datetime
import quandl
import os
from zipline.data.bundles.core import load
import pandas as pd
import numpy as np
from zipline.utils.paths import zipline_root
from logbook import Logger, StderrHandler
from zipline.pipeline.factors import CustomFactor
from os import environ
import sys
import pickle


KERNEL_BUNDLE = 'sharadar-prices' # fundamentals are downloaded for symbols from this bundle
DATA_FILE = zipline_root() + '/data/SF1.npy'  # the file name to be used when storing this in ~/.zipline/data
FUNDAMENTAL_FIELDS_FILE = zipline_root() + '/data/SF1.pkl'

log = Logger('quandl_fundamentals.py')

def set_api_key():
    """read QUANDL_API_KEY env variable, and set it."""
    try:
        api_key = environ["QUANDL_API_KEY"]
    except KeyError:
        print("could not read the env variable: QUANDL_API_KEY")
        sys.exit()
    quandl.ApiConfig.api_key = api_key

class SparseDataFactor(CustomFactor):
    """Abstract Base Class to be used for computing sparse data.
    The data is packed and persisted into a NumPy binary data file
    in a previous step.

    This class must be subclassed with class variable 'outputs' set.  The fields
    in 'outputs' should match those persisted."""
    inputs = []
    window_length = 1

    def __init__(self, *args, **kwargs):
        self.time_index = None
        self.curr_date = None     # date for which time_index is accurate
        self.last_date_seen = 0   # earliest date possible
        self.data = None
        self.data_path = "please_specify_.npy_file"

    def bs(self, arr):
        """Binary Search"""
        if len(arr) == 1:
            if self.curr_date < arr[0]:
                return 0
            else: return 1

        mid = int(len(arr) / 2)
        if self.curr_date < arr[mid]:
            return self.bs(arr[:mid])
        else:
            return mid + self.bs(arr[mid:])

    def bs_sparse_time(self, sid):
        """For each security find the best range in the sparse data."""
        dates_for_sid = self.data.date[sid]
        if np.isnan(dates_for_sid[0]):
            return 0

        # do a binary search of the dates array finding the index
        # where self.curr_date will lie.
        non_nan_dates = dates_for_sid[~np.isnan(dates_for_sid)]
        return self.bs(non_nan_dates) - 1

    def cold_start(self, today, assets):
        if self.data is None:
            # need the change allow_pickle=True due to allow_pickle
            # default value change after numpy upgrade
            self.data = np.load(self.data_path, allow_pickle=True)

        self.M = self.data.date.shape[1]

        # for each sid, do binary search of date array to find current index
        # the results can be shared across all factors that inherit from SparseDataFactor
        # this sets an array of ints: time_index
        self.time_index = np.full(self.N, -1, np.dtype('int64'))
        self.curr_date = today.value
        for asset in assets:  # asset is numpy.int64
            self.time_index[asset] = self.bs_sparse_time(asset)

    def update_time_index(self, today, assets):
        """Ratchet update.

        for each asset check if today >= dates[self.time_index]
        if so then increment self.time_index[asset.sid] += 1"""

        ind_p1 = self.time_index.copy()
        np.add.at(ind_p1, ind_p1 != (self.M - 1), 1)
        sids_to_increment = today.value >= self.data.date[np.arange(self.N), ind_p1]
        sids_not_max = self.time_index != (self.M - 1)   # create mask of non-maxed
        self.time_index[sids_to_increment & sids_not_max] += 1

        self.curr_date = today.value

    def compute(self, today, assets, out, *arrays, **params):
        # for each asset in assets determine index from date (today)
        if self.time_index is None or today < self.last_date_seen:
            self.cold_start(today, assets)
        else:
            self.update_time_index(today, assets)
        self.last_date_seen = today

        ti_used_today = self.time_index[assets]

        for field in self.__class__.outputs:
            out[field][:] = self.data[field][assets, ti_used_today]

class Fundamentals(SparseDataFactor):
    params = ('algo_bundle',)

    try:
        with open(FUNDAMENTAL_FIELDS_FILE, 'rb') as f:
            outputs = pickle.load(f)
    except:
        outputs = []

    def __init__(self, *args, **kwargs):
        super(Fundamentals, self).__init__(*args, **kwargs)
        self.data_path = DATA_FILE

        bundle_data = load(KERNEL_BUNDLE)
        self.kernel_sids = bundle_data.asset_finder.sids
        self.kernel_assets = bundle_data.asset_finder.retrieve_all(self.kernel_sids)
        self.N = len(self.kernel_assets)

        self.algo_bundle = kwargs['algo_bundle'] if 'algo_bundle' in kwargs else KERNEL_BUNDLE
        self.alternative_bundle = self.algo_bundle != KERNEL_BUNDLE
        self.kernel_sid_symbol_map = {}
        self.algo_to_kernel_sids = {}

        if self.alternative_bundle:
            for asset in self.kernel_assets:
                self.kernel_sid_symbol_map[asset.symbol] = asset.sid

            bundle_data = load(self.algo_bundle)
            self.algo_sids = bundle_data.asset_finder.sids
            self.algo_assets = bundle_data.asset_finder.retrieve_all(self.algo_sids)

            for asset in self.algo_assets:
                if asset.symbol in self.kernel_sid_symbol_map:
                    self.algo_to_kernel_sids[asset.sid] = self.kernel_sid_symbol_map[asset.symbol]

    def algo_to_kernel_assets(self, assets):
        kernel_assets = [self.algo_to_kernel_sids[asset] for asset in assets if asset in self.algo_to_kernel_sids]
        return pd.Int64Index(kernel_assets)

    def compute(self, today, assets, out, *arrays, **params):
        if self.alternative_bundle:
            algo_to_kernel_assets = self.algo_to_kernel_assets (assets)
            if self.time_index is None or today < self.last_date_seen:
                self.cold_start(today, algo_to_kernel_assets)
            else:
                self.update_time_index(today, algo_to_kernel_assets)
            self.last_date_seen = today

            ti_used_today = self.time_index[algo_to_kernel_assets]

            for field in self.__class__.outputs:
                out[field][algo_to_kernel_assets] = self.data[field][algo_to_kernel_assets, ti_used_today]
        else:
            super(Fundamentals, self).compute(today, assets, out, *arrays, **params)

def get_tickers_from_bundle(bundle_name):
    """Gets a list of tickers from a given bundle"""
    bundle_data = load(bundle_name, os.environ, None)

    # we can request equities or futures separately changing the filters parameter
    all_sids = bundle_data.asset_finder.sids

    # retreive all assets in the bundle
    all_assets = bundle_data.asset_finder.retrieve_all(all_sids)

    return [a.symbol for a in all_assets]

def download_fundamendals_data (bundle,
                                start_date = '2007-01-01',
                                end_date = datetime.datetime.today().strftime('%Y-%m-%d'),
                                tickers = None,
                                dataset = 'SHARADAR/SF1',
                                fields = None,
                                dimensions = None,
                                drop_dimensions = ('MRT', 'MRQ', 'MRY'),
                                data_file = DATA_FILE,
                                ):
    tickers_universe = get_tickers_from_bundle(bundle)
    N = len (tickers_universe)

    tickers = tickers if tickers else tickers_universe

    log.info (f"Downloading data for {len(tickers) if tickers else 'ALL'} tickers")

    header_columns = ['ticker',
                     'dimension',
                     'datekey',
                     'reportperiod',
                     'lastupdated',
                     'calendardate']

    df = quandl.get_table(dataset,
                          calendardate={'gte': start_date, 'lte': end_date},
                          ticker=tickers,
                          qopts={'columns': header_columns + fields} if fields else None,
                          paginate=True)

    df = df.rename(columns={'datekey': 'Date'}).set_index('Date')

    dfs = [None] * N

    fields = [f.upper() for f in df.columns if f not in header_columns]
    dimensions = dimensions if dimensions \
        else [d for d in df['dimension'].unique() if not d in drop_dimensions]

    max_len = -1

    for i, ticker in enumerate (tickers):
        log.info (f"Pre-processing {ticker} ({i+1} / {len (tickers)})...")
        ticker_df = df[df.ticker==ticker]
        ticker_series = []
        for field in fields:
            for dim in dimensions:
                field_dim_series = ticker_df[ticker_df.dimension==dim][field.lower()]
                field_dim_series.name = field + '_' + dim
                ticker_series.append (field_dim_series)

        ticker_processed_df = pd.concat(ticker_series, axis=1)
        max_len = max(max_len, ticker_processed_df.shape[0])
        dfs[tickers_universe.index(ticker)] = ticker_processed_df

    log.info ("Packing data...")
    dtypes = [('date', '<f8')]

    fundamental_fields = [f'{f}_{d}' for f in fields for d in dimensions]

    with open(FUNDAMENTAL_FIELDS_FILE, 'wb') as f:
        pickle.dump(fundamental_fields, f)

    buff = np.full((len(fundamental_fields)+1, N, max_len), np.nan)

    for field in fundamental_fields:
        dtypes.append((field, '<f8'))

    data = np.recarray(shape=(N, max_len), buf=buff, dtype=dtypes)

    for i, df in enumerate(dfs):
        if df is None:
            continue
        else:
            df = pd.DataFrame(df)

        ind_len = df.index.shape[0]
        data.date[i, :ind_len] = df.index
        for field in fundamental_fields:
            data[field][i, :ind_len] = df[field]

    log.info (f"Saving to {data_file}...")
    data.dump(data_file)  # can be read back with np.load()

    log.info ("Done!")
    return data

def download (bundle = KERNEL_BUNDLE,
              start_date = '2013-01-01',
              tickers = None,
              fields = None,
              dimensions = None,
              ):
    """
    this method is a top-level executor of the download
    download volume could be reduced by setting start_date, tickers, fields, dimensions parameters
    with all parameters set as default will need couple of hours to complete the task
    for each field it gets each dimension available - thus returns fields X dimension values
    :param bundle: bundle which to be used to get the universe of tickers, sharadar-prices by default
    :param start_date: first date of the set
    :param tickers: list of tickers, all tickers by default
    :param fields: list of fields, all fields by default
    :param dimensions: list of dimensions, all dimensions by default (skipping MRs)
    """
    log.info(f"Downloading fundamentals data since {start_date}")
    set_api_key()
    data = download_fundamendals_data(bundle = bundle,
                                      start_date = start_date,
                                      tickers = tickers,
                                      fields = fields,
                                      dimensions = dimensions,
                                      )
    return data

def test ():
    start_date = '2015-01-01'

    fields = [
        'netinc',
        'marketcap',
              ]

    dimensions = [
        'ARQ',
                  ]

    tickers = [
        'AAPL',
        'MSFT',
        'PAAS',
              ]

    data = download(tickers = tickers,
                    fields = fields,
                    start_date = start_date,
                    dimensions = dimensions,
                  )
    return data

def download_all (start_date = '2013-01-01'):
    """
    this is the top-level executor of the fundamentals download - just downloads everything since 2007
    you may want to schedule download_all to be executed daily within out-of-market hours
    """
    StderrHandler(bubble=True).push_application()
    data = download(start_date=start_date)
    return data

if __name__ == '__main__':
    download_all()