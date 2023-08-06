from logbook import Logger
from collections import namedtuple, defaultdict, OrderedDict
from ib_insync import *
import pandas as pd
import numpy as np
import pytz
from zipline.finance.order import (Order as ZPOrder,
                                   ORDER_STATUS as ZP_ORDER_STATUS)
from zipline.finance.execution import (MarketOrder,
                                       LimitOrder,
                                       StopOrder,
                                       StopLimitOrder)
from zipline.api import symbol as symbol_lookup
from zipline.errors import SymbolNotFound
from six import iteritems, itervalues
from zipline.finance.transaction import Transaction
import zipline.protocol as zp
from zipline.protocol import MutableView
from math import fabs
import sys

log = Logger('IB Broker (ib_insync)')

Position = namedtuple('Position', ['contract', 'position', 'market_price',
                                   'market_value', 'average_cost',
                                   'unrealized_pnl', 'realized_pnl',
                                   'account_name'])

symbol_to_exchange = defaultdict(lambda: 'SMART')
symbol_to_exchange['VIX'] = 'CBOE'
symbol_to_exchange['SPX'] = 'CBOE'
symbol_to_exchange['VIX3M'] = 'CBOE'
symbol_to_exchange['VXST'] = 'CBOE'
symbol_to_exchange['VXMT'] = 'CBOE'
symbol_to_exchange['GVZ'] = 'CBOE'
symbol_to_exchange['GLD'] = 'ARCA'
symbol_to_exchange['GDX'] = 'ARCA'
symbol_to_exchange['GPRO'] = 'SMART/NASDAQ'
symbol_to_exchange['MSFT'] = 'SMART/NASDAQ'
symbol_to_exchange['CSCO'] = 'SMART/NASDAQ'

symbol_to_sec_type = defaultdict(lambda: 'STK')
symbol_to_sec_type['VIX'] = 'IND'
symbol_to_sec_type['VIX3M'] = 'IND'
symbol_to_sec_type['VXST'] = 'IND'
symbol_to_sec_type['VXMT'] = 'IND'
symbol_to_sec_type['GVZ'] = 'IND'
symbol_to_sec_type['SPX'] = 'IND'

wait_step = 0.1
max_wait_cycles = 100

class IBBroker(IB):
    def __init__(self, tws_uri, account_id=None, marketDataType=3):
        # watchout - market data type is set to 'delayed' by default!

        super(self.__class__, self).__init__()

        self._tws_uri = tws_uri
        self.host, self.port, self.client_id = self._tws_uri.split(':')

        self._orders = {}
        self._transactions = {}
        self._next_ticker_id = 0
        self._next_order_id = None
        self.symbol_to_ticker_id = {}
        self.ticker_id_to_symbol = {}
        self.metrics_tracker = None
        self.currency = 'USD'
        self.time_skew = None
        self.account_id = None

        self.open_orders = {}
        self.order_statuses = {}
        self.executions = defaultdict(OrderedDict)
        self.commissions = defaultdict(OrderedDict)
        self._execution_to_order_id = {}
        self._subscribed_assets = []

        self.openOrderEvent += self.openOrder
        self.orderStatusEvent += self.orderStatus
        self.execDetailsEvent += self.execDetails
        self.commissionReportEvent += self.commissionReport
        self.errorEvent += self.error

        try:
            self.connect(self.host, self.port, self.client_id)
        except Exception as e:
            log.error(f"Can't connect to TWS")
            return

        self.managed_accounts = self.managedAccounts()
        log.info("Managed accounts: {}".format(self.managed_accounts))
        time = self.reqCurrentTime()
        self.time_skew = (pd.to_datetime('now', utc=True) -
                          time.replace(tzinfo=pytz.utc))
        log.info("Local-Broker Time Skew: {}".format(self.time_skew))

        self.account_id = (self.client.getAccounts()[0] if account_id is None
                           else account_id)

        self.reqMarketDataType(marketDataType)

    def error(self, reqId, errorCode, errorString, contract):
        # this is just the error-handler
        pass
        # log.info(f'{reqId}: {errorCode}: {errorString}' + '' if not contract else f'{contract}')

    def execDetails(self, trade, fill):
        order_id, exec_id = fill.execution.orderId, fill.execution.execId
        self.executions[order_id][exec_id] = dict (req_id = order_id,
                                                   contract = fill.contract,
                                                   exec_detail = fill.execution)
        self._execution_to_order_id[exec_id] = order_id

        log.info(
            "Order-{order_id} executed @ {exec_time}: "
            "{symbol} current: {shares} @ ${price} "
            "total: {cum_qty} @ ${avg_price} "
            "exec_id: {exec_id} by client-{client_id}".format(
                order_id=order_id, exec_id=exec_id,
                exec_time=pd.to_datetime(fill.execution.time),
                symbol=fill.contract.symbol,
                shares=fill.execution.shares,
                price=fill.execution.price,
                cum_qty=fill.execution.cumQty,
                avg_price=fill.execution.avgPrice,
                client_id=fill.execution.clientId))

    def commissionReport(self, trade, fill, commission_report):
        exec_id = commission_report.execId

        # we need this check for the case when IB is sending report for the
        # order which was placed by another session out of market hours
        # in this case current session does not have info on the exec_id
        self.execDetails (trade, fill)

        order_id = self._execution_to_order_id[commission_report.execId]
        self.commissions[order_id][exec_id] = commission_report

        log.debug(
            "Order-{order_id} report: "
            "realized_pnl: ${realized_pnl} "
            "commission: ${commission} yield: {yield_} "
            "exec_id: {exec_id}".format(
                order_id=order_id,
                exec_id=commission_report.execId,
                realized_pnl=commission_report.realizedPNL
                if commission_report.realizedPNL != sys.float_info.max
                else 0,
                commission=commission_report.commission,
                yield_=commission_report.yield_
                if commission_report.yield_ != sys.float_info.max
                else 0)
        )

    def openOrder(self, trade):
        self.open_orders[trade.order.orderId] = dict (state = trade.orderStatus,
                                                      order = trade.order,
                                                      contract = trade.contract,
                                                      order_id = trade.order.orderId,
                                                      )
        log.debug(
            "Order-{order_id} {status}: "
            "{order_action} {order_count} {symbol} with {order_type} order. "
            "limit_price={limit_price} stop_price={stop_price}".format(
                order_id=trade.order.orderId,
                status=trade.orderStatus.status,
                order_action=trade.order.action,
                order_count=trade.order.totalQuantity,
                symbol=trade.contract.symbol,
                order_type=trade.order.orderType,
                limit_price=trade.order.lmtPrice,
                stop_price=trade.order.auxPrice))

    def orderStatus(self, trade):
        self.order_statuses[trade.order.orderId] = dict (why_held = trade.orderStatus.whyHeld,
                                                         client_id=trade.orderStatus.clientId,
                                                         last_fill_price=trade.orderStatus.lastFillPrice,
                                                         parent_id=trade.orderStatus.parentId,
                                                         perm_id=trade.order.permId,
                                                         avg_fill_price=trade.orderStatus.avgFillPrice,
                                                         remaining=trade.orderStatus.remaining,
                                                         filled=trade.orderStatus.filled,
                                                         status=trade.orderStatus.status,
                                                         order_id=trade.order.orderId,
                                                         )

        log.debug(
            "Order-{order_id} {status}: "
            "filled={filled} remaining={remaining} "
            "avg_fill_price={avg_fill_price} "
            "last_fill_price={last_fill_price} ".format(
                order_id=trade.order.orderId,
                status=self.order_statuses[trade.order.orderId]['status'],
                filled=self.order_statuses[trade.order.orderId]['filled'],
                remaining=self.order_statuses[trade.order.orderId]['remaining'],
                avg_fill_price=self.order_statuses[trade.order.orderId]['avg_fill_price'],
                last_fill_price=self.order_statuses[trade.order.orderId]['last_fill_price']))

    @property
    def next_order_id(self):
        order_id = self.client.getReqId()
        return order_id

    def is_alive(self):
        return self.isConnected()

    @property
    def next_ticker_id(self):
        ticker_id = self._next_ticker_id
        self._next_ticker_id += 1
        return ticker_id

    def subscribe_to_market_data (self, symbol, tick_list='232'):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = symbol_to_sec_type[symbol]
        contract.exchange = symbol_to_exchange[symbol]
        contract.currency = self.currency
        ticker = self.reqMktData(contract, tick_list)
        for i in range(0, max_wait_cycles):
            self.sleep(wait_step)
            if not pd.isna(ticker.close) or not pd.isna(ticker.last):
                break

        return ticker

    def get_spot_value(self, assets, field, dt, data_frequency):
        symbol = str(assets.symbol)

        ticker_id = self.next_ticker_id

        self.symbol_to_ticker_id[symbol] = ticker_id
        self.ticker_id_to_symbol[ticker_id] = symbol

        ticker = self.subscribe_to_market_data(symbol)
        self._subscribed_assets.append (assets)

        if not ticker.time:
            log.error(f"No data retrieved on symbol {symbol}!")
            return pd.NaT if field == 'last_traded' else np.NaN

        if field == 'price':
            return ticker.last if not pd.isna(ticker.last) and ticker.last > 0 else ticker.close

        if field == 'last_traded':
            return pd.NaT

        if field == 'open':
            return ticker.open

        if field == 'close':
            return ticker.close

        if field == 'high':
            return ticker.high

        if field == 'low':
            return ticker.low

        if field == 'volume':
            return ticker.volume

    def set_metrics_tracker(self, metrics_tracker):
        self.metrics_tracker = metrics_tracker

    def _update_orders(self):
        def _update_from_order_status(zp_order, ib_order_id):
            if ib_order_id in self.open_orders:
                open_order_state = self.open_orders[ib_order_id]['state']

                zp_status = self._ib_to_zp_status(open_order_state.status)
                if zp_status is None:
                    log.warning(
                        "Order-{order_id}: "
                        "unknown order status: {order_status}.".format(
                            order_id=ib_order_id,
                            order_status=open_order_state.status))
                else:
                    zp_order.status = zp_status

            if ib_order_id in self.order_statuses:
                order_status = self.order_statuses[ib_order_id]

                zp_order.filled = order_status['filled']

                zp_status = self._ib_to_zp_status(order_status['status'])
                if zp_status:
                    zp_order.status = zp_status
                else:
                    log.warning("Order-{order_id}: "
                                "unknown order status: {order_status}."
                                .format(order_id=ib_order_id,
                                        order_status=order_status['status']))

        def _update_from_execution(zp_order, ib_order_id):
            if ib_order_id in self.executions and \
                    ib_order_id not in self.open_orders:
                zp_order.status = ZP_ORDER_STATUS.FILLED
                executions = self.executions[ib_order_id]
                last_exec_detail = \
                    list(executions.values())[-1]['exec_detail']
                zp_order.filled = last_exec_detail.cumQty

        all_ib_order_ids = (set([e.broker_order_id
                                 for e in self._orders.values()]) |
                            set(self.open_orders.keys()) |
                            set(self.order_statuses.keys()) |
                            set(self.executions.keys()) |
                            set(self.commissions.keys()))
        for ib_order_id in all_ib_order_ids:
            zp_order = self._get_or_create_zp_order(ib_order_id)
            if zp_order:
                _update_from_execution(zp_order, ib_order_id)
                _update_from_order_status(zp_order, ib_order_id)

    @property
    def orders(self):
        self._update_orders()
        return self._orders

    @staticmethod
    def _safe_symbol_lookup(symbol):
        try:
            return symbol_lookup(symbol)
        except SymbolNotFound:
            return None

    def _ib_to_zp_order_id(self, ib_order_id):
        return "IB-{date}-{account_id}-{client_id}-{order_id}".format(
            date=str(pd.to_datetime('today').date()),
            account_id=self.account_id,
            client_id=self.client_id,
            order_id=ib_order_id)

    @staticmethod
    def _action_qty_to_amount(action, qty):
        return qty if action == 'BUY' else -1 * qty

    _zl_order_ref_magic = '!ZL'

    @classmethod
    def _create_order_ref(cls, ib_order:Order, dt=pd.to_datetime('now', utc=True)):
        order_type = ib_order.orderType.replace(' ', '_')
        return \
            "A:{action} Q:{qty} T:{order_type} " \
            "L:{limit_price} S:{stop_price} D:{date} {magic}".format(
                action=ib_order.action,
                qty=ib_order.totalQuantity,
                order_type=order_type,
                limit_price=ib_order.lmtPrice,
                stop_price=ib_order.auxPrice,
                date=int(dt.value / 1e9),
                magic=cls._zl_order_ref_magic)

    @classmethod
    def _parse_order_ref(cls, ib_order_ref):
        if not ib_order_ref or \
                not ib_order_ref.endswith(cls._zl_order_ref_magic):
            return None

        try:
            action, qty, order_type, limit_price, stop_price, dt, _ = \
                ib_order_ref.split(' ')

            if not all(
                    [action.startswith('A:'),
                     qty.startswith('Q:'),
                     order_type.startswith('T:'),
                     limit_price.startswith('L:'),
                     stop_price.startswith('S:'),
                     dt.startswith('D:')]):
                return None

            return {
                'action':      action[2:],
                'qty':         int(qty[2:]),
                'order_type':  order_type[2:].replace('_', ' '),
                'limit_price': float(limit_price[2:]),
                'stop_price':  float(stop_price[2:]),
                'dt':          pd.to_datetime(dt[2:], unit='s', utc=True)}

        except ValueError:
            log.warning("Error parsing order metadata: {}".format(
                ib_order_ref))
            return None

    @staticmethod
    def _ib_to_zp_status(ib_status):
        ib_status = ib_status.lower()
        if ib_status == 'submitted':
            return ZP_ORDER_STATUS.OPEN
        elif ib_status in ('pendingsubmit',
                           'pendingcancel',
                           'presubmitted'):
            return ZP_ORDER_STATUS.HELD
        elif ib_status == 'cancelled':
            return ZP_ORDER_STATUS.CANCELLED
        elif ib_status == 'filled':
            return ZP_ORDER_STATUS.FILLED
        elif ib_status == 'inactive':
            return ZP_ORDER_STATUS.REJECTED
        else:
            return None

    def _get_or_create_zp_order(self, ib_order_id,
                                ib_order=None, ib_contract=None):
        zp_order_id = self._ib_to_zp_order_id(ib_order_id)
        if zp_order_id in self._orders:
            return self._orders[zp_order_id]

        # Try to reconstruct the order from the given information:
        # open order state and execution state
        symbol, order_details = None, None

        if ib_order and ib_contract:
            symbol = ib_contract.symbol
            order_details = self._parse_order_ref(ib_order.orderRef)

        if not order_details and ib_order_id in self.open_orders:
            open_order = self.open_orders[ib_order_id]
            symbol = open_order['contract'].symbol
            order_details = self._parse_order_ref(
                open_order['order'].orderRef)

        if not order_details and ib_order_id in self.executions:
            executions = self.executions[ib_order_id]
            last_exec_detail = list(executions.values())[-1]['exec_detail']
            last_exec_contract = list(executions.values())[-1]['contract']
            symbol = last_exec_contract.symbol
            order_details = self._parse_order_ref(last_exec_detail.orderRef)

        asset = self._safe_symbol_lookup(symbol)
        if not asset:
            log.warning(
                "Ignoring symbol {symbol} which has associated "
                "order but it is not registered in bundle".format(
                    symbol=symbol))
            return None

        if order_details:
            amount = self._action_qty_to_amount(order_details['action'],
                                                order_details['qty'])
            stop_price = order_details['stop_price']
            limit_price = order_details['limit_price']
            dt = order_details['dt']
        else:
            dt = pd.to_datetime('now', utc=True)
            amount, stop_price, limit_price = 0, None, None
            if ib_order_id in self.open_orders:
                open_order = self.open_orders[ib_order_id]['order']
                amount = self._action_qty_to_amount(
                    open_order.action, open_order.totalQuantity)
                stop_price = open_order.auxPrice
                limit_price = open_order.lmtPrice

        stop_price = None if stop_price == 0 else stop_price
        limit_price = None if limit_price == 0 else limit_price

        self._orders[zp_order_id] = ZPOrder(
            dt=dt,
            asset=asset,
            amount=amount,
            stop=stop_price,
            limit=limit_price,
            id=zp_order_id)
        self._orders[zp_order_id].broker_order_id = ib_order_id

        return self._orders[zp_order_id]

    @property
    def transactions(self):
        self._update_transactions()
        return self._transactions

    def _update_transactions(self):
        all_orders = list(self.orders.values())

        for ib_order_id, executions in iteritems(self.executions):
            orders = [order
                      for order in all_orders
                      if order.broker_order_id == ib_order_id]

            if not orders:
                log.warning("No order found for executions: {}".format(
                    executions))
                continue

            assert len(orders) == 1
            order = orders[0]

            for exec_id, execution in iteritems(executions):
                if exec_id in self._transactions:
                    continue

                try:
                    commission = self.commissions[ib_order_id][exec_id] \
                        .commission
                except KeyError:
                    log.warning(
                        "Commission not found for execution: {}".format(
                            exec_id))
                    commission = 0

                exec_detail = execution['exec_detail']
                is_buy = order.amount > 0
                amount = (exec_detail.shares if is_buy
                          else -1 * exec_detail.shares)
                tx = Transaction(
                    asset=order.asset,
                    amount=amount,
                    dt=pd.to_datetime(exec_detail.time, utc=True),
                    price=exec_detail.price,
                    order_id=order.id
                )
                self._transactions[exec_id] = tx

    @property
    def positions(self):
        self._get_positions_from_broker()
        return self.metrics_tracker.positions

    @property
    def subscribed_assets(self):
        return self._subscribed_assets

    def _get_positions_from_broker(self):
        """
        get the positions from the broker and update zipline objects ( the ledger )
        should be used once at startup and once every time we want to refresh the positions array
        """
        cur_pos_in_tracker = self.metrics_tracker.positions
        ib_positions = IB.positions(self, self.account_id)
        for ib_position in ib_positions:
            try:
                z_position = zp.Position(zp.InnerPosition(symbol_lookup(ib_position.contract.symbol)))
                editable_position = MutableView(z_position)
            except SymbolNotFound:
                # The symbol might not have been ingested to the db therefore
                # it needs to be skipped.
                log.warning('Wanted to subscribe to %s, but this asset is probably not ingested' % symbol)
                continue
            editable_position._underlying_position.amount = int(ib_position.position)
            editable_position._underlying_position.cost_basis = float(ib_position.avgCost)

            ticker = self.subscribe_to_market_data(ib_position.contract.symbol)
            editable_position._underlying_position.last_sale_price = \
                ticker.last if not pd.isna(ticker.last) and ticker.last > 0 else ticker.close
            editable_position._underlying_position.last_sale_date = \
                ticker.time if len(ticker.ticks)==0 else ticker.ticks[-1].time

            self.metrics_tracker.update_position(z_position.asset,
                                                 amount=z_position.amount,
                                                 last_sale_price=z_position.last_sale_price,
                                                 last_sale_date=z_position.last_sale_date,
                                                 cost_basis=z_position.cost_basis)
        for asset in cur_pos_in_tracker:
            if asset.symbol not in [p.contract.symbol for p in ib_positions]:
            # if asset.symbol not in self.positions:
                # deleting object from the metrcs_tracker as its not in the portfolio
                self.metrics_tracker.update_position(asset,
                                                     amount=0)
        # # for some reason, the metrics tracker has self.positions AND self.portfolio.positions. let's make sure
        # # these objects are consistent
        # # (self.portfolio.positions is self.metrics_tracker._ledger._portfolio.positions)
        # # (self.metrics_tracker.positions is self.metrics_tracker._ledger.position_tracker.positions)
        self.metrics_tracker._ledger._portfolio.positions = self.metrics_tracker.positions

    @property
    def portfolio(self):
        positions = self.positions

        return self.metrics_tracker.portfolio

    def order(self, asset, amount, style):
        contract = Contract()
        contract.symbol = str(asset.symbol)
        contract.currency = self.currency
        contract.exchange = symbol_to_exchange[str(asset.symbol)]
        contract.secType = symbol_to_sec_type[str(asset.symbol)]

        order = Order()
        order.totalQuantity = int(fabs(amount))
        order.action = "BUY" if amount > 0 else "SELL"

        is_buy = (amount > 0)
        order.lmtPrice = style.get_limit_price(is_buy) or 0
        order.auxPrice = style.get_stop_price(is_buy) or 0

        if isinstance(style, MarketOrder):
            order.orderType = "MKT"
        elif isinstance(style, LimitOrder):
            order.orderType = "LMT"
        elif isinstance(style, StopOrder):
            order.orderType = "STP"
        elif isinstance(style, StopLimitOrder):
            order.orderType = "STP LMT"

        # TODO: Support GTC orders both here and at blotter_live
        order.tif = "DAY"
        order.orderRef = self._create_order_ref(order)

        ib_order_id = self.next_order_id
        order.orderId = ib_order_id
        zp_order = self._get_or_create_zp_order(ib_order_id, order, contract)

        log.info(
            "Placing order-{order_id}: "
            "{action} {qty} {symbol} with {order_type} order. "
            "limit_price={limit_price} stop_price={stop_price} {tif}".format(
                order_id=ib_order_id,
                action=order.action,
                qty=order.totalQuantity,
                symbol=contract.symbol,
                order_type=order.orderType,
                limit_price=order.lmtPrice,
                stop_price=order.auxPrice,
                tif=order.tif
            ))

        self.placeOrder(contract, order)

        return zp_order

    def get_last_traded_dt(self, asset):
        ticker = self.subscribe_to_market_data(asset)

        return ticker.time if len(ticker.ticks)==0 else ticker.ticks[-1].time

    def get_realtime_bars(self, assets, frequency):
        if frequency == '1m':
            resample_freq = '1 Min'
        elif frequency == '1d':
            resample_freq = '24 H'
        else:
            raise ValueError("Invalid frequency specified: %s" % frequency)

        df = pd.DataFrame()
        a=self.subscribe_to_market_data('AAWW')
        for asset in assets:
            symbol = str(asset.symbol)
            ticker = self.subscribe_to_market_data(symbol)

            trade_prices = ticker.last
            trade_sizes = ticker.lastSize
            ohlcv = trade_prices.resample(resample_freq).ohlc()
            ohlcv['volume'] = trade_sizes.resample(resample_freq).sum()

            # Add asset as level 0 column; ohlcv will be used as level 1 cols
            ohlcv.columns = pd.MultiIndex.from_product([[asset, ],
                                                        ohlcv.columns])

            df = pd.concat([df, ohlcv], axis=1)

        return df
