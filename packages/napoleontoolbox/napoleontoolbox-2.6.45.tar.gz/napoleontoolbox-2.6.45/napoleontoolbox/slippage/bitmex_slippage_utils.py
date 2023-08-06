# Hash
import time
import hashlib
import hmac
from requests.auth import AuthBase
from urllib.parse import urlparse
from urllib import parse

# clients
import bitmex

# Utils
from dateutil import parser
import pytz
import pandas as pd
import math
import requests
import json
from dateutil import parser
from pandas.tseries.offsets import DateOffset
import pickle
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter("ignore")

import os


from napoleontoolbox.file_saver import dropbox_file_saver

# Utils
def convert_unix(ts):
    return dt.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def convert_string(s):
    dt_object = parser.parse(s)
    return dt_object.timestamp()


def assess_rsp(response):
    if response.status_code != 200:
        print('Bad gateway')
    elif isinstance(response.json(), list):
        pass
    # elif response.json()['Response'] != 'Success':
    # raise RuntimeError(response.json()['Message'])


def to_iso(ts):
    if type(ts) == str:
        ts = parser.parse(ts)
        return ts.replace(tzinfo=dt.timezone.utc).isoformat()
    else:
        return dt.datetime.utcfromtimestamp(ts).replace(tzinfo=dt.timezone.utc).isoformat()


def to_unix(s):
    if isinstance(s, str):
        dt_object = parser.parse(s)
    else:
        dt_object = s
    return int(dt_object.replace(tzinfo=dt.timezone.utc).timestamp())


def assess_rsp(response):
    if response.status_code != 200:
        raise RuntimeError('Bad gateway:', response.status_code)
    elif isinstance(response.json(), list) and len(response.json()) == 0:
        raise ValueError('No data')
    # elif response.json()['Response'] != 'Success':
    # raise RuntimeError(response.json()['Message'])


def extract_df(optype, precision, r):
    if optype == 'OHLC':
        try:
            tmp = r.json()['Data']['Data']
            return pd.DataFrame(tmp)
        except KeyError:
            print(r.json()['Message'])
    else:
        return pd.DataFrame(r.json()['Data'])


def convert_to_BitmexTS(s):
    s = parser.parse(s)
    s = s.strftime('%Y-%m-%d%%20%H%%3A%M')
    return s


# CryptoCompare
class CryptoCompare:
    def __init__(self, api_key=None, exchange=None):
        self.api_key = api_key
        self.e = exchange

    def get(self, optype, currency, startdate, enddate, precision):
        timedelta = to_unix(enddate) - to_unix(startdate)
        ts = to_unix(enddate)
        precision_dct = {'1h': 3600, 'hour': 3600, 'minute': 60}  # https://min-api.cryptocompare.com/data/v2/histohour
        endpoint_dct = {'OHLC': {'url': 'https://min-api.cryptocompare.com/data/v2/histo{}'.format(precision),
                                 'params': {'fsym': currency, 'tsym': 'USD', 'limit': '2000', 'aggreggate': '1',
                                            'toTs': ts}},
                        'OBL2': {'url': 'https://min-api.cryptocompare.com/data/ob/l2/snapshot',
                                 'params': {'api_key', self.api_key}},
                        'HVOL': {'url': 'https://min-api.cryptocompare.com/data/symbol/histohour',
                                 'params': {'fsym': currency, 'tsym': 'USD', 'limit': '500', 'toTs': ts}}}

        if optype == 'OHLC' and precision == 'minute':
            endpoint_dct[optype]['params']['api_key'] = '{' + self.api_key + '}'

        runs, rest = divmod(timedelta / precision_dct[precision], int(endpoint_dct[optype]['params']['limit']))
        runs, rest = int(runs), str(int(math.ceil(rest)))
        output = pd.DataFrame()
        for run in range(runs):
            r = requests.request("GET", endpoint_dct[optype]['url'], params=endpoint_dct[optype]['params'])
            assess_rsp(r)
            output = pd.concat([output, extract_df(optype, precision, r)])
            endpoint_dct[optype]['params'].update({'toTs': output.time.min()})

        if rest != '0':
            endpoint_dct[optype]['params'].update({'limit': rest})
            print(endpoint_dct[optype]['params'])
            r = requests.request("GET", endpoint_dct[optype]['url'], params=endpoint_dct[optype]['params'])
            assess_rsp(r)
            output = pd.concat([output, extract_df(optype, precision, r)])

        output['timestamp'] = output.time.apply(lambda x: to_iso(x))
        output = output.set_index('timestamp', drop=True).sort_index().drop_duplicates()
        return output


def generate_signature(secret, verb, url, expires, data):
    """Generate a request signature compatible with BitMEX."""
    # Parse the url so we can remove the base and extract just the path.
    parsedURL = urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query

    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf8')

    # print("Computing HMAC: %s"  % verb + path + str(expires) + data)
    message = verb + path + str(expires) + data

    signature = hmac.new(bytes(secret, 'utf8'), bytes(message, 'utf8'), digestmod=hashlib.sha256).hexdigest()
    return signature


class APIKeyAuthWithExpires:  # (AuthBase):

    """Attaches API Key Authentication to the given Request object. This implementation uses `expires`."""

    def __init__(self, apiKey, apiSecret):
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def __call__(self, r):
        # modify and return the request
        expires = int(round(time.time()) + 5)  # 5s grace period in case of clock skew
        r.headers['api-expires'] = str(expires)
        r.headers['api-key'] = self.apiKey
        r.headers['api-signature'] = generate_signature(self.apiSecret, r.method, r.url, expires, r.data or '')

        return r


def gen_url_BitMEX(optype, currency='', startdate=convert_unix(time.time()), enddate=convert_unix(time.time()),
                   precision='', count=''):  # Ajouter un truc pour le format...
    startdate, enddate = convert_to_BitmexTS(startdate), convert_to_BitmexTS(enddate)
    url_base = 'https://www.bitmex.com/api/v1'
    op_cnvt_runs = {'position': {'endpoint': '/position?',
                                 'params': {'columns': 'account',
                                            'count': '50'}},
                    'stats': {'endpoint': '/stats',
                              'params': None},
                    'OBL2': {'endpoint': '/orderBook/L2?',
                             'params': {'symbol': currency,
                                        'depth': '50'}},
                    'OHLC': {'endpoint': '/trade/bucketed?',
                             'params': {'binSize': precision,
                                        'partial': 'false',
                                        'symbol': currency,
                                        'count': str(count),
                                        'reverse': 'true',
                                        'endTime': enddate}}}

    op_cnvt_rest = {'position': {'endpoint': '/position?',
                                 'params': {'columns': 'account',
                                            'count': '50'}},
                    'stats': {'endpoint': '/stats',
                              'params': None},
                    'OBL2': {'endpoint': '/orderBook/L2?',
                             'params': {'symbol': currency,
                                        'depth': '50'}},
                    'OHLC': {'endpoint': '/trade/bucketed?',
                             'params': {'binSize': precision,
                                        'partial': 'false',
                                        'symbol': currency,
                                        'count': '500',
                                        'reverse': 'true',
                                        'startTime': startdate,
                                        'endTime': enddate}}}

    if count == 500:
        op_cnvt = op_cnvt_runs
    else:
        op_cnvt = op_cnvt_rest

    if op_cnvt[optype]['params'] is not None:
        return url_base + op_cnvt[optype]['endpoint'] + '&'.join(
            ['='.join(list(item)) for item in op_cnvt[optype]['params'].items()])
    else:
        return url_base + op_cnvt[optype]['endpoint']


class BitMEX:

    def __init__(self, api_key, private_key, *args):
        self.api_key = api_key
        self.p_key = private_key
        self.KeyAuth = APIKeyAuthWithExpires(api_key, self.p_key)

    # Where optype = position, stats, funding, orderBook, trade, /user/executionHistory
    # Format we need for startdate, enddate = 2019-04-25T00:00:00.545Z

    def retrieve_and_assess(self, s, url):

        request = self.KeyAuth(requests.Request('GET', url))
        prepped = request.prepare()
        resp = s.send(prepped)
        assess_rsp(resp)
        temp = pd.DataFrame(resp.json())
        return temp

    def get(self, optype, currency='', startdate=convert_unix(time.time()), enddate=convert_unix(time.time()),
            precision='nearest'):

        import tqdm
        s = requests.Session()
        startdate_unix, enddate_unix = convert_string(startdate), convert_string(enddate)
        timedelta = abs(enddate_unix - startdate_unix)
        div_dct = {'daily': 3600 * 24, '1d': 3600 * 24, '1h': 3600, '1m': 60}
        if precision not in div_dct.keys():
            if precision == 'nearest' and optype == 'funding':
                div = 3600 * 8
            else:
                div = 60
        else:
            div = div_dct[precision]
        runs, rest = divmod(timedelta / div, 500)
        runs = int(runs)

        output = pd.DataFrame()
        if (optype != 'OBL2') and (optype != 'stats') and (runs != 0):
            for run in tqdm.tqdm(range(runs)):
                url = gen_url_BitMEX(optype, currency, startdate, enddate, precision, 500)
                output = pd.concat([output, self.retrieve_and_assess(s, url)], ignore_index=True)
                enddate = str(output['timestamp'].iloc[-1])
                time.sleep(3)

            if rest != 0:
                url = gen_url_BitMEX(optype, currency, startdate, enddate, precision)
                output = pd.concat([output, self.retrieve_and_assess(s, url)], ignore_index=True)

        else:
            url = gen_url_BitMEX(optype, currency, startdate, enddate, precision)
            output = self.retrieve_and_assess(s, url)

        output = output.drop_duplicates()
        return output


import numba
from numba import jit


def trades_to_arr(df):
    # Buy = 1
    # Sell = -1
    # XBT = 1
    # ETH = -1
    # Market = 1
    # Limit = 0
    # Funding = 0
    # Limit = 1
    from numba import typed
    df = df.replace('Buy', 1).replace('Sell', -1).replace('ETHUSD', -1).replace('XBTUSD', 1).replace('Limit',
                                                                                                     0).replace(
        'Market', 1).replace('Trade', 1).replace('Funding', 0)
    df = df[['symbol', 'side', 'lastQty', 'lastPx', 'orderQty', 'price', 'execType', 'ordType', 'leavesQty', 'cumQty',
             'avgPx', 'commission', 'execCost', 'execComm', 'homeNotional', 'foreignNotional', 'transactTime']].copy()
    df.transactTime = df.transactTime.apply(lambda x: x.timestamp() * 1000)
    df = df.replace(np.nan, 0)
    df = df.replace({'(.*?)': 0}, regex=True)
    d = typed.Dict()
    for i, k in enumerate(df.columns):
        d[k] = i
    return df.astype(float).values, d


def trades_to_arr(df):
    # Buy = 1
    # Sell = -1
    # XBT = 1
    # ETH = -1
    # Market = 1
    # Limit = 0
    # Funding = 0
    # Limit = 1
    from numba import typed
    df = df.replace('Buy', 1).replace('Sell', -1).replace('ETHUSD', -1).replace('XBTUSD', 1).replace('Limit',
                                                                                                     0).replace(
        'Market', 1).replace('Trade', 1).replace('Funding', 0)
    df = df[['symbol', 'side', 'lastQty', 'lastPx', 'orderQty', 'price', 'execType', 'ordType', 'leavesQty', 'cumQty',
             'avgPx', 'commission', 'execCost', 'execComm', 'homeNotional', 'foreignNotional', 'transactTime']].copy()
    df.transactTime = df.transactTime.apply(lambda x: x.timestamp() * 1000)
    df = df.replace(np.nan, 0)
    df = df.replace({'(.*?)': 0}, regex=True)
    d = typed.Dict()
    for i, k in enumerate(df.columns):
        d[k] = i
    return df.astype(float).values, d


@jit(nopython=True)
def find_lastPx(arr, d):
    lastPxBTC = []
    lastPxETH = []
    for i in range(arr.shape[0]):
        if arr[i, d['symbol']] == 1:
            lastPxBTC.append(arr[i, d['lastPx']])
            t = list(arr[:i, d['symbol']][::-1])
            if -1 not in t:
                lastPxETH.append(np.nan)
            else:
                r = t.index(-1)
                lastPxETH.append(arr[i - r - 1, d['lastPx']])
        else:
            lastPxETH.append(arr[i, d['lastPx']])
            t = list(arr[:i, d['symbol']][::-1])
            if 1 not in t:
                lastPxBTC.append(np.nan)
            else:
                r = t.index(1)
                lastPxBTC.append(arr[i - r - 1, d['lastPx']])

    return np.array(lastPxBTC), np.array(lastPxETH)

    # if len(l[0]) == 0:
    # return np.nan
    # else:
    # return l


@jit(nopython=True)
def get_qtraded(arr, d):
    qtraded_ETH = [187465]  # Faut aller voir dans la feuille de trades sinon c nop
    qtraded_BTC = [620484]
    for i in range(1, arr.shape[0]):
        if (arr[i, d['symbol']] == 1) and (arr[i, d['execType']] == 1):
            qtraded_ETH.append(0)
            qtraded_BTC.append(arr[i, d['lastQty']])
        elif (arr[i, d['symbol']] == -1) and (arr[i, d['execType']] == 1):
            qtraded_BTC.append(0)
            qtraded_ETH.append(arr[i, d['lastQty']])
        else:
            qtraded_BTC.append(0)
            qtraded_ETH.append(0)
    return np.array(qtraded_BTC), np.array(qtraded_ETH)


@jit(nopython=True)
def get_sizes(arr, d):
    size_ETH = []
    size_BTC = []
    for i in range(arr.shape[0]):
        if (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == -1):
            size_ETH.append(arr[i, d['lastPx']] * arr[i, d['lastQty']])
            size_BTC.append(0)
        elif (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == 1):
            size_BTC.append(arr[i, d['lastPx']] * arr[i, d['lastQty']])
            size_ETH.append(0)
        else:
            size_ETH.append(0)
            size_BTC.append(0)
    return np.array(size_BTC), np.array(size_ETH)


@jit(nopython=True)
def get_senses(arr, d):
    sens_ETH = []
    sens_BTC = []
    for i in range(arr.shape[0]):
        if (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == -1) and (arr[i, d['side']] == 1):
            sens_ETH.append(1.)
            sens_BTC.append(0.)
        elif (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == -1) and (arr[i, d['side']] == -1):
            sens_ETH.append(-1.)
            sens_BTC.append(0)
        elif (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == 1) and (arr[i, d['side']] == 1):
            sens_ETH.append(0)
            sens_BTC.append(1.)
        elif (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == 1) and (arr[i, d['side']] == -1):
            sens_ETH.append(0.)
            sens_BTC.append(-1.)
        else:
            sens_ETH.append(0.)
            sens_BTC.append(0.)
    sens_BTC = np.array(sens_BTC)
    sens_ETH = np.array(sens_ETH)
    return sens_BTC, sens_ETH


@jit(nopython=True)
def get_markets(arr, d):
    markets_BTC = []
    markets_ETH = []
    for i in range(arr.shape[0]):
        if (arr[i, d['symbol']] == 1) and (arr[i, d['execType']] == 1) and (arr[i, d['ordType']] == 1):
            markets_BTC.append(arr[i, d['lastQty']])
            markets_ETH.append(0)
        elif (arr[i, d['symbol']] == -1) and (arr[i, d['execType']] == 1) and (arr[i, d['ordType']] == 1):
            markets_ETH.append(arr[i, d['lastQty']])
            markets_BTC.append(0)
        else:
            markets_ETH.append(0)
            markets_BTC.append(0)
    markets_BTC = np.array(markets_BTC)  # .astype(float)
    markets_ETH = np.array(markets_ETH)  # .astype(float)
    return markets_BTC, markets_ETH


@jit(nopython=True)
def _merge_update(arr, d, arrays: list, names: list):
    if len(arrays) != len(names):
        return None
    else:
        last_idx = arr.shape[1] + 1
        for a in arrays:
            t = a.reshape(-1, 1)
            arr = np.hstack((arr, t))
        for _ in names:
            d[_] = int(last_idx)
            last_idx += 1
    return arr, d


@jit(nopython=True)
def numba_compute(arr, d):
    arrays = []
    a, b = find_lastPx(arr, d)
    arrays.extend([a, b])
    a, b = get_qtraded(arr, d)
    arrays.extend([a, b])
    a, b = get_sizes(arr, d)
    arrays.extend([a, b])
    a, b = get_senses(arr, d)
    arrays.extend([a, b])
    a, b = get_markets(arr, d)
    arrays.extend([a, b])
    names = ['lastPxBTC', 'lastPxETH', 'traded_xbt', 'traded_eth', 'size_xbt', 'size_eth', 'sens_trade_xbt',
             'sens_trade_eth', 'markets_BTC', 'markets_ETH']
    arr, d = _merge_update(arr, d, arrays, names)
    #arrays = get_fees(df, d)
    arrays = get_fees(arr, d)

    names = ['funding_fees_xbt_btc', 'funding_fees_eth_btc', 'funding_fees_xbt_usd', 'funding_fees_eth_usd',
             'trading_fees_xbt_btc', 'trading_fees_xbt_usd', 'trading_fees_eth_btc', 'trading_fees_eth_usd']
    arr, d = _merge_update(arr, d, arrays, names)
    return arr, d


@jit(nopython=True)
def get_fees(arr, d):
    if 'lastPxBTC' not in d:
        return None
    else:
        funding_fees_xbt_btc = []
        funding_fees_eth_btc = []
        funding_fees_xbt_usd = []
        funding_fees_eth_usd = []
        trading_fees_xbt_btc = []
        trading_fees_xbt_usd = []
        trading_fees_eth_btc = []
        trading_fees_eth_usd = []
        fold = [funding_fees_xbt_btc, funding_fees_eth_btc, funding_fees_xbt_usd, funding_fees_eth_usd,
                trading_fees_xbt_btc, trading_fees_xbt_usd, trading_fees_eth_btc, trading_fees_eth_usd]
        for i in range(arr.shape[0]):
            if (arr[i, d['execType']] == 0) and (arr[i, d['symbol']] == 1):
                ff = arr[i, d['execComm']] / 100000000
                funding_fees_xbt_btc.append(ff)
                funding_fees_xbt_usd.append(ff * arr[i, d['lastPxBTC']])
                max_l = funding_fees_xbt_btc
            elif (arr[i, d['execType']] == 0) and (arr[i, d['symbol']] == -1):
                ff = arr[i, d['execComm']] / 100000000
                funding_fees_eth_btc.append(ff)
                funding_fees_eth_usd.append(ff * arr[i, d['lastPxBTC']])
                max_l = funding_fees_eth_btc
            elif (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == 1):
                tf = arr[i, d['execComm']] / 100000000
                trading_fees_xbt_btc.append(tf)
                trading_fees_xbt_usd.append(tf * arr[i, d['lastPxBTC']])
                max_l = trading_fees_xbt_btc
            elif (arr[i, d['execType']] == 1) and (arr[i, d['symbol']] == -1):
                tf = arr[i, d['execComm']] / 100000000
                trading_fees_eth_btc.append(tf)
                trading_fees_eth_usd.append(tf * arr[i, d['lastPxBTC']])
                max_l = trading_fees_eth_btc
            for _ in fold:
                if len(_) < len(max_l):
                    _.append(0)

        fold_a = []
        for _ in fold:
            fold_a.append(np.array(_))
        return fold_a

def fetch_all_necessary_data(public_key = None, private_key= None, start_time= None, end_time= None, save_to_dropbox = False, dropbox_token = None, local_root_directory = './'):

    dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=dropbox_token, dropbox_backup=True)

    start_time_stub = start_time.strftime('%d_%b_%Y')
    end_time_stub = end_time.strftime('%d_%b_%Y')
    filename_stub = f'{public_key}_{start_time_stub}_{end_time_stub}_Bitmex'
    #filename_stub = f'{inv_year_dictionary[year]}_{inv_month_dictionary[month]}_{inv_market_dictionary[market]}'


    report_pkl_file_name = f'{filename_stub}_report.pkl'
    trade_pkl_file_name = f'{filename_stub}_trades.pkl'
    ohlc_eth_bm_pkl_file_name = f'{filename_stub}_ohlc_eth_bm.pkl'
    ohlc_btc_bm_pkl_file_name = f'{filename_stub}_ohlc_btc_bm.pkl'
    walletHist_pkl_file_name = f'{filename_stub}_walletHist.pkl'
    ohlc_btc_cc_pkl_file_name = f'{filename_stub}_ohlc_btc_cc.pkl'
    ohlc_eth_cc_pkl_file_name = f'{filename_stub}_ohlc_eth_cc.pkl'

    client = bitmex.bitmex(test=False, config=None, api_key=public_key, api_secret=private_key)
    if isinstance(start_time,dt.datetime) and isinstance(end_time,dt.datetime):
        start_time = start_time.strftime('%Y-%m-%dT%H:%M')
        end_time = end_time.strftime('%Y-%m-%dT%H:%M')


    ce, te = parser.parse(start_time).replace(tzinfo=pytz.UTC), parser.parse(end_time).replace(tzinfo=pytz.UTC)

    ce = ce - dt.timedelta(hours=8)
    trades = pd.DataFrame()
    print('Accessing Trade History...')
    while ce < te:
        print(f'requesting trades between {ce} and {te}')
        tmp = pd.DataFrame(client.Execution.Execution_getTradeHistory(startTime=ce, count=500).result()[0]).sort_values(
            by='timestamp', ascending=True)
        trades = trades.append(tmp)
        time.sleep(4)
        ce = tmp.timestamp.iloc[-1]
    trades = trades[trades.timestamp <= te].copy()
    trades.execComm = - trades.execComm  # logique comptable
    trades = trades.sort_values(by='timestamp', ascending=True).drop_duplicates()
    print('Done.')

    # Get wallet history for a period of time
    ce, te = parser.parse(start_time).replace(tzinfo=pytz.UTC), parser.parse(end_time).replace(tzinfo=pytz.UTC)
    ce = ce - dt.timedelta(hours=8)
    walletHist = pd.DataFrame()
    print('Accessing wallet history...')
    while ce < te:
        print(f'requesting wallet history between {ce} and {te}')
        tmp = pd.DataFrame(client.User.User_getWalletHistory(currency='XBt').result()[0]).sort_values(by='timestamp',
                                                                                                      ascending=True)
        walletHist = walletHist.append(tmp)
        time.sleep(3.5)
        ce = tmp.timestamp.iloc[-1]
    walletHist = walletHist[walletHist.timestamp <= te].copy()
    print('Wallet History retrieved.')

    # Récupérer les OHLC hourly sur Cryptocompare depuis startdate
    cc = CryptoCompare('')
    ohlc_btc_cc = cc.get('OHLC', 'BTC', start_time, end_time, precision='hour')
    ohlc_eth_cc = cc.get('OHLC', 'ETH', start_time, end_time, precision='hour')
    print("OHLC Cryptocompare retrieved.")

    # Récupérer les OHLC hourly sur BM depuis startdate

    bm = BitMEX(public_key, private_key)
    ohlc_btc_bm = bm.get('OHLC', currency='XBT', startdate=start_time, enddate=end_time, precision='1h')
    ohlc_eth_bm = bm.get('OHLC', currency='ETH', startdate=start_time, enddate=end_time, precision='1h')
    print('OHLC BM retrieved.')

    if save_to_dropbox :
        full_path = local_root_directory + trade_pkl_file_name
        trades.to_pickle(full_path)
        print(f'uploading to dropbox {full_path}')
        dbx.upload(fullname=full_path, folder='', subfolder='', name=trade_pkl_file_name, overwrite=True)
        os.remove(full_path)

        full_path = local_root_directory + ohlc_eth_bm_pkl_file_name
        ohlc_eth_bm.to_pickle(full_path)
        print(f'uploading to dropbox {full_path}')
        dbx.upload(fullname=full_path, folder='', subfolder='', name=ohlc_eth_bm_pkl_file_name, overwrite=True)
        os.remove(full_path)

        full_path = local_root_directory + ohlc_btc_bm_pkl_file_name
        ohlc_btc_bm.to_pickle(full_path)
        print(f'uploading to dropbox {full_path}')
        dbx.upload(fullname=full_path, folder='', subfolder='', name=ohlc_btc_bm_pkl_file_name, overwrite=True)
        os.remove(full_path)

        full_path = local_root_directory + walletHist_pkl_file_name
        walletHist.to_pickle(full_path)
        print(f'uploading to dropbox {full_path}')
        dbx.upload(fullname=full_path, folder='', subfolder='', name=walletHist_pkl_file_name, overwrite=True)
        os.remove(full_path)

        full_path = './' + ohlc_btc_cc_pkl_file_name
        ohlc_btc_cc.to_pickle(full_path)
        print(f'uploading to dropbox {full_path}')
        dbx.upload(fullname=full_path, folder='', subfolder='', name=ohlc_btc_cc_pkl_file_name, overwrite=True)
        os.remove(full_path)

        full_path = local_root_directory + ohlc_eth_cc_pkl_file_name
        ohlc_eth_cc.to_pickle(full_path)
        print(f'uploading to dropbox {full_path}')
        dbx.upload(fullname=full_path, folder='', subfolder='', name=ohlc_eth_cc_pkl_file_name, overwrite=True)
        os.remove(full_path)

    # ohlc_btc_bm
    x = ohlc_btc_bm
    x = x.set_index('timestamp')
    x.index = x.index.map(parser.parse)
    x.index = x.index.tz_localize(None)
    x.columns = [y + '_btc_bm' for y in x.columns]
    ohlc_btc_bm = x

    # ohlc_eth_bm
    x = ohlc_eth_bm
    x = x.set_index('timestamp')
    x.index = x.index.map(parser.parse)
    x.index = x.index.tz_localize(None)
    x.columns = [y + '_eth_bm' for y in x.columns]
    ohlc_eth_bm = x

    # ohlc_btc_cc
    x = ohlc_btc_cc
    x.index = x.index.map(parser.parse)
    x.index = x.index.tz_localize(None)
    x.columns = [y + '_btc_cc' for y in x.columns]
    ohlc_btc_cc = x

    # ohlc_eth_cc
    x = ohlc_eth_cc
    x.index = x.index.map(parser.parse)
    x.index = x.index.tz_localize(None)
    x.columns = [y + '_eth_cc' for y in x.columns]
    ohlc_eth_cc = x

    ohlc_eth_cc = ohlc_eth_cc.sort_index(ascending=True).drop_duplicates()
    ohlc_btc_cc = ohlc_btc_cc.sort_index(ascending=True).drop_duplicates()
    ohlc_btc_bm = ohlc_btc_bm.sort_index(ascending=True).drop_duplicates()
    ohlc_eth_bm = ohlc_eth_bm.sort_index(ascending=True).drop_duplicates()

    ##############################
    ##############################
    ##########
    ########## computing, grouping
    ##########
    ##############################
    ##############################

    start = time.time()
    df, d = trades_to_arr(trades)
    df, d = numba_compute(df, d)
    print('Done for', trades.shape[0], 'trades in ', time.time() - start, 'seconds.')

    # Now: Groupby
    df = pd.DataFrame(df, columns=[i for i in d.keys()])
    df['funding_fees_xbt_usd'] = df.funding_fees_xbt_btc * df.lastPxBTC
    df['funding_fees_eth_usd'] = df.funding_fees_eth_btc * df.lastPxBTC
    df['trading_fees_eth_usd'] = df.trading_fees_eth_btc * df.lastPxBTC
    df['trading_fees_xbt_usd'] = df.trading_fees_xbt_btc * df.lastPxBTC
    df.transactTime = df.transactTime.apply(lambda x: dt.datetime.utcfromtimestamp(x / 1000))
    df['dt_floor'] = df.transactTime.dt.floor('H')
    df[
        'total_fees_usd'] = df.trading_fees_xbt_usd + df.trading_fees_eth_usd + df.funding_fees_xbt_usd + df.funding_fees_eth_usd

    print('Grouping by...')
    td = df[['dt_floor', 'traded_eth', 'traded_xbt', 'size_eth', 'size_xbt', 'sens_trade_eth', 'sens_trade_xbt',
             'funding_fees_xbt_usd', 'funding_fees_eth_usd',
             'trading_fees_xbt_btc', 'trading_fees_xbt_usd', 'trading_fees_eth_btc', 'trading_fees_eth_usd',
             'total_fees_usd']].groupby('dt_floor').sum()

    td.index = td.index.tz_localize(None)
    td['avg_eth_price'] = td.size_eth / abs(td.traded_eth)
    td['avg_btc_price'] = td.size_xbt / abs(td.traded_xbt)

    # Join & compute prices for cryptocompare
    td = td.join(ohlc_eth_cc['open_eth_cc']).join(ohlc_btc_cc['open_btc_cc'])
    td['slippage_eth_price_cc'] = (td.avg_eth_price / td.open_eth_cc - 1) * np.sign(td.sens_trade_eth)
    td['slippage_eth_cash_cc'] = td.slippage_eth_price_cc * abs(
        td.traded_eth)  # / 1000000 * td.open_btc_cc * td.open_eth_cc
    td['slippage_btc_price_cc'] = (td.avg_btc_price / td.open_btc_cc - 1) * np.sign(td.sens_trade_xbt)
    td['slippage_btc_cash_cc'] = td.slippage_btc_price_cc * abs(td.traded_xbt)
    # slippage en 100e de millionnième de eth = ratio * cours open * qty * 100
    # slippage en 100e de millionnième de btc = ratio * 1Mo/ cours * 100 * qty

    # Join & compute slippage for bitmex
    td = td.join(ohlc_eth_bm['open_eth_bm']).join(ohlc_btc_bm['open_btc_bm'])
    td['slippage_eth_price_bm'] = (td.avg_eth_price / td.open_eth_bm - 1) * np.sign(td.sens_trade_eth)
    td['slippage_eth_cash_bm'] = td.slippage_eth_price_bm * abs(
        td.traded_eth)  # / 1000000 * td.open_btc_bm * td.open_eth_bm
    td['slippage_btc_price_bm'] = (td.avg_btc_price / td.open_btc_bm - 1) * np.sign(td.sens_trade_xbt)
    td['slippage_btc_cash_bm'] = td.slippage_btc_price_bm * abs(td.traded_xbt)
    print('All done.')

    walletHist = walletHist.set_index('timestamp')
    walletHist.index = walletHist.index.map(lambda x: x.floor('60s'))
    walletHist = walletHist[~walletHist.index.duplicated(keep='first')].sort_index(ascending=True)
    walletHist.index = walletHist.index.tz_localize(None)
    walletHist['walletBalance_xbt'] = walletHist.walletBalance / 100000000
    walletHist = walletHist.join(ohlc_btc_cc['open_btc_cc'])
    walletHist['walletBalance_usd'] = walletHist.walletBalance_xbt * walletHist.open_btc_cc

    # Join to td
    td_h = td.join(walletHist.walletBalance_usd.dropna(), rsuffix='_fromWH')
    td_h.walletBalance_usd = td_h.walletBalance_usd.fillna(method='ffill')

    td_h['traded_eth_usd_a'] = td_h.traded_eth * td_h.avg_eth_price * 0.000001 * td_h.open_btc_bm
    td_h['traded_xbt_usd_a'] = td_h.traded_xbt / td_h.avg_btc_price
    # Usd value = xbt spot * eht usd price * bitcoin multiplier ( 0.000001)

    x = td_h[['traded_eth', 'avg_eth_price', 'traded_eth_usd_a', 'sens_trade_eth', 'trading_fees_eth_usd',
              'funding_fees_eth_usd', 'open_eth_cc', 'open_eth_bm',
              'traded_xbt', 'avg_btc_price', 'traded_xbt_usd_a', 'sens_trade_xbt', 'trading_fees_xbt_usd',
              'funding_fees_xbt_usd', 'open_btc_cc', 'open_btc_bm', 'walletBalance_usd',
              'trading_fees_eth_usd', 'funding_fees_eth_usd', 'slippage_eth_price_cc', 'slippage_eth_cash_cc',
              'trading_fees_xbt_usd', 'funding_fees_xbt_usd', 'slippage_btc_price_cc', 'slippage_btc_cash_cc',
              'trading_fees_eth_usd', 'funding_fees_eth_usd', 'slippage_eth_price_bm', 'slippage_eth_cash_bm',
              'trading_fees_xbt_usd', 'funding_fees_xbt_usd', 'slippage_btc_price_bm', 'slippage_btc_cash_bm']]

    x = x.rename_axis('timestamp')
    x.columns = ['quantity_traded_eth', 'avg_traded_price_eth', 'amount_traded_usd_eth', 'n_trades_eth',
                 'trading_fees_usd_eth', 'funding_fees_usd_eth',
                 'open_eth_cc', 'open_eth_exchange',
                 'quantity_traded_btc', 'avg_traded_price_btc', 'amount_traded_usd_btc', 'n_trades_btc',
                 'trading_fees_usd_btc', 'funding_fees_usd_btc',
                 'open_btc_cc', 'open_btc_exchange',
                 'wallet_amount_usd',
                 'trading_fees_usd_eth', 'funding_fees_usd_eth', 'slippage_eth_price_cc', 'slippage_eth_cash_cc',
                 'trading_fees_usd_btc', 'funding_fees_usd_btc', 'slippage_btc_price_cc', 'slippage_btc_cash_cc',
                 'trading_fees_usd_eth', 'funding_fees_usd_eth', 'slippage_eth_price_bm', 'slippage_eth_cash_bm',
                 'trading_fees_usd_btc', 'funding_fees_usd_btc', 'slippage_btc_price_bm', 'slippage_btc_cash_bm']

    x = x.fillna(0).round(decimals=5)

    full_path = local_root_directory + report_pkl_file_name
    x.to_pickle(full_path)
    print(f'uploading to dropbox {full_path}')
    dbx.upload(fullname=full_path, folder='', subfolder='', name=report_pkl_file_name, overwrite=True)
    os.remove(full_path)

    return x

