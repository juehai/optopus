# -*- coding: utf-8 -*-
from collections import OrderedDict
import datetime
from enum import Enum
from typing import List
from optopus.utils import nan, is_nan
from optopus.currency import Currency
from optopus.settings import CURRENCY


class DataSource(Enum):
    IB = 'IB'
    Quandl = 'Quandl'


class AssetType(Enum):
    Stock = 'STK'
    Option = 'OPT'
    Future = 'FUT'
    Forex = 'CASH'
    Index = 'IND'
    CFD = 'CFD'
    Bond = 'BOND'
    Commodity = 'CMDTY'
    FuturesOption = 'FOP'
    MutualFund = 'FUND'
    Warrant = 'IOPT'


class StrategyType(Enum):
    SellNakedPut = 'SNP'


class OrderType(Enum):
    Market = 'MTK'
    Limit = 'LMT'
    Stop = 'STP'


class RightType(Enum):
    Call = 'C'
    Put = 'P'


class OptionMoneyness(Enum):
    AtTheMoney = 'ATM'
    InTheMoney = 'ITM'
    OutTheMoney = 'OTM'
    NA = 'NA'


class OwnershipType(Enum):
    Buyer = 'BUY'
    Seller = 'SELL'


class OrderRol(Enum):
    NewLeg = 'NL'
    TakeProfit = 'TP'
    StopLoss = 'SL'


class OrderStatus(Enum):
    APIPending = 'API pending'
    PendingSubmit = 'Pending submit'
    PendingCancel = 'Pending cancel'
    PreSubmitted = 'Presubmitted'
    Submitted = 'Submitted'
    APICancelled = 'API cancelled'
    Cancelled = 'Cancelled'
    Filled = 'Filled'
    Inactive = 'Inactive'


class Asset():
    def __init__(self,
                 code: str,
                 asset_type: AssetType,
                 data_source: DataSource = DataSource.IB,
                 currency: Currency = CURRENCY) -> None:
        self.code = code
        self.asset_type = asset_type
        self.data_source = data_source
        self.currency = CURRENCY
        self._data = None
        self._contract = None
        self._historical_data = None
        self._historical_IV_data = None
        self._historical_updated = None
        self._historical_IV_updated = None
        self._option_chain = None

    @property
    def current(self):
        return self._data

    @current.setter
    def current(self, values):
        self._data = values

    @property
    def historical(self):
        return self._historical_data

    @historical.setter
    def historical(self, values):
        self._historical_data = values
        self._historical_data_updated = datetime.datetime.now()

    @property
    def historical_IV(self):
        return self._historical_IV_data

    @historical_IV.setter
    def historical_IV(self, values):
        self._historical_IV_data = values
        self._historical_data_updated = datetime.datetime.now()

    @property
    def market_price(self):
        return self._data.market_price

    def historical_is_updated(self) -> bool:
        if self._historical_updated:
            delta = datetime.datetime.now() - self._historical_updated
            if delta.days:
                return True
            else:
                return False
        else:
            return False

    def historical_IV_is_updated(self) -> bool:
        if self._historical_IV_updated:
            delta = datetime.datetime.now() - self._historical_IV_updated
            if delta.days:
                return True
            else:
                return False
        else:
            return False


class AssetData():
    def __init__(self,
                 code: str,
                 asset_type: AssetType,
                 high: float = nan,
                 low: float = nan,
                 close: float = nan,
                 bid: float = nan,
                 bid_size: float = nan,
                 ask: float = nan,
                 ask_size: float = nan,
                 last: float = nan,
                 last_size: float = nan,
                 volume: float = nan,
                 time: datetime.datetime = None) -> None:
        self.code = code
        self.asset_type = asset_type
        self.high = high
        self.low = low
        self.close = close
        self.bid = bid
        self.bid_size = bid_size
        self.ask = ask
        self.ask_size = ask_size
        self.last = last
        self.last_size = last_size
        self.time = time
        self.volume = volume
        self.IV_h = None
        self.IV_rank_h = None
        self.IV_percentile_h = None
        self.volume_h = None
        self.stdev = None
        self.beta = None
        self.one_month_return = None
        self.correlation = None
        self.midpoint = (self.bid + self.ask) / 2

        # market_price is the first available one of:
        # - last price if within current bid/ask;
        # - average of bid and ask (midpoint);
        # - close price.
        self.market_price = nan
        if (is_nan(self.midpoint) or self.bid <= self.last <= self.ask):
            self.market_price = self.last

        if is_nan(self.market_price):
            self.market_price = self.midpoint
        if is_nan(self.market_price) or self.market_price == -1:
            self.market_price = self.close


class OptionData():
    def __init__(self,
                 code: str,
                 expiration: datetime.date,
                 strike: float,
                 right: RightType,
                 high: float = nan,
                 low: float = nan,
                 close: float = nan,
                 bid: float = nan,
                 bid_size: float = nan,
                 ask: float = nan,
                 ask_size: float = nan,
                 last: float = nan,
                 last_size: float = nan,
                 option_price: float = nan,
                 volume: float = nan,
                 delta: float = nan,
                 gamma: float = nan,
                 theta: float = nan,
                 vega: float = nan,
                 implied_volatility: float = nan,
                 underlying_price: float = nan,
                 underlying_dividends: float = nan,
                 moneyness: float = nan,
                 intrinsic_value: float = nan,
                 extrinsic_value: float = nan,
                 time: datetime.datetime = None)-> None:
        self.code = code
        self.asset_type = AssetType.Option
        self.expiration = expiration
        self.strike = strike
        self.right = right
        self.high = high
        self.low = low
        self.close = close
        self.bid = bid
        self.bid_size = bid_size
        self.ask = ask
        self.ask_size = ask_size
        self.last = last
        self.last_size = last_size
        self.option_price = option_price
        self.volume = volume
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.implied_volatility = implied_volatility
        self.underlying_price = underlying_price
        self.underlying_dividends = underlying_dividends
        self.moneyness = moneyness
        self.intrinsic_value = intrinsic_value
        self.extrinsic_value = extrinsic_value
        self.time = time
        self.DTE = (self.expiration - datetime.datetime.now().date()).days


class BarDataType(Enum):
    Trades = 'TRADES'
    IV = 'IMPLIED_VOLATILITY'


class BarData():
    def __init__(self,
                 code: str,
                 bar_time: float = nan,
                 bar_open: float = nan,
                 bar_high: float = nan,
                 bar_low: float = nan,
                 bar_close: float = nan,
                 bar_average: float = nan,
                 bar_volume: float = nan,
                 bar_count: float = nan) -> None:
        self.code = code
        self.bar_time = bar_time
        self.bar_open = bar_open
        self.bar_high = bar_high
        self.bar_low = bar_low
        self.bar_close = bar_close
        self.bar_average = bar_average
        self.bar_volume = bar_volume
        self.bar_count = bar_count


class PositionData():
    def __init__(self,
                 code: str,
                 asset_type: AssetType,
                 ownership: OwnershipType,
                 quantity: int,
                 expiration: datetime.date,
                 strike: float,
                 right: RightType,
                 average_cost: float = None) -> None:

        self.code = code
        self.asset_type = asset_type
        self.ownership = ownership
        self.expiration = expiration
        self.strike = strike
        self.right = right
        self.quantity = quantity
        self.position_id = self.code + ' ' + self.ownership.value + ' ' + self.right.value + ' ' + str(round(self.strike, 1)) + ' ' + self.expiration.strftime('%d-%m-%Y')
        
        self.average_cost = average_cost
        #self.trades = []
        self.option_price = None
        self.trade_price = None
        self.trade_time = None
        self.underlying_price = None
        self.beta = None
        self.delta = None
        self.algorithm = None
        self.strategy = None
        self.rol = None
        self.DTE = None

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.__dict__})')


class OrderData():
    def __init__(self,
                 asset: Asset,
                 rol: OrderRol,
                 ownership: OwnershipType,
                 quantity: int,
                 price: float,
                 order_type: OrderType,
                 expiration: datetime.date,
                 strike: float,
                 right: RightType,
                 reference: str,
                 contract):

        self.asset = asset
        self.rol = rol
        self.ownership = ownership
        self.quantity = quantity
        self.price = price
        self.order_type = order_type

        self.expiration = expiration
        self.strike = strike
        self.right = right
        self.created = datetime.datetime.now()
        self.updated = self.created
        self.status = OrderStatus.APIPending

        self.order_id = reference + '_' + self.rol.value + ' ' + self.created.strftime('%d-%m-%Y %H:%M:%S')
        self.contract = contract

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.__dict__})')


# https://interactivebrokers.github.io/tws-api/order_submission.html
class TradeData:
    def __init__(self,
                 order_id: str,
                 status: OrderStatus,
                 remaining: int,
                 commission: float):
        self.order_id = order_id
        self.status = status
        self.remaining = remaining
        self.commission = commission

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.__dict__})')


class Leg:
    def __init__(self,
                 asset: Asset,
                 ownership: OwnershipType,
                 right: RightType,
                 expiration: datetime.date,
                 strike: float,
                 multiplier: int,
                 strategy_price: float,
                 ratio: int,
                 currency: Currency,
                 take_profit_factor: float,
                 stop_loss_factor: float,
                 contract: object) -> None:
        self.asset = asset
        self.ownership = ownership
        self.right = right
        self.expiration = expiration
        self.strike = strike
        self.multiplier = multiplier
        self.strategy_price = strategy_price
        self.ratio = ratio
        self.order_price = None
        self.quantity = None
        self.currency = currency
        self.contract = contract
        self.take_profit_factor = take_profit_factor
        self.stop_loss_factor = stop_loss_factor
        self.created = datetime.datetime.now()
        self.filled = None
        self.commission = None
        #self.orders = {}
        self.leg_id = self.asset.code + ' ' + self.ownership.value + ' ' + self.right.value + ' ' + str(round(self.strike, 1)) + ' ' + self.expiration.strftime('%d-%m-%Y')
        self.option = None

    def __repr__(self):
        return(f'{self.__class__.__name__}('
               f'{self.asset.code, self.ownership.value, self.right.value, self.strike, self.expiration, self.multiplier, self.currency, self.strategy_quantity})')
        

class Strategy:
    def __init__(self,
                 asset: Asset,
                 strategy_type: StrategyType,
                 legs: List[Leg]):
        self.asset = asset
        self.strategy_type = strategy_type
        self.legs = {}
        for leg in legs:
            self.legs[leg.leg_id] = leg
        self.created = datetime.datetime.now()
        self.updated = self.created
        self.strategy_id = self.asset.code + ' ' + self.created.strftime('%d-%m-%Y %H:%M:%S')

    def __repr__(self):
        return(f'{self.__class__.__name__}('
               f'{self.asset.code, self.strategy_type.value, self.created}'
               f'\n{self.legs!r}')



class AccountData:
    """Class representing a broker account"""

    def __init__(self) -> None:
        self._id = None

        # The basis for determining the price of the assets in your account.
        # Total cash value + stock value + options value + bond value
        self.net_liquidation = None
        # Buying power serves as a measurement of the dollar value of 
        # securities that one may purchase in a securities account without
        # depositing additional funds
        self.buying_power = None
        # Cash recognized at the time of trade + futures PNL
        self.cash = None
        # This value tells what you have available for trading
        self.funds = None
        # The Number of Open/Close trades a user could put on before 
        # Pattern Day Trading is detected. A value of "-1" means that the user
        # can put on unlimited day trades.
        # Number of Open/Close trades in a day
        self.max_day_trades = None
        # Initial Margin requirement of whole portfolio
        self.initial_margin = None       
        #  Maintenance Margin requirement of whole portfolio
        self.maintenance_margin = None
        # This value shows your margin cushion, before liquidation
        self.excess_liquidity = None
        # Excess liquidity as a percentage of net liquidation value
        self.cushion = None
        # The sum of the absolute value of all stock and equity option positions
        # Leverage = GrossPositionValue / NetLiquidation
        self.gross_position_value = None
        # Forms the basis for determining whether a client has the 
        # necessary assets to either initiate or maintain security positions. 
        # Cash + stocks + bonds + mutual funds
        self.equity_with_loan = None
        # Special Memorandum Account: Line of credit created when the market 
        # value of securities in a Regulation T account increase in value
        self.SMA = None
