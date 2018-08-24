#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 16:30:25 2018

@author: ilia
"""
import datetime
from typing import List
from collections import OrderedDict
from optopus.account import Account, AccountItem
from optopus.data_manager import DataManager, DataSource
from optopus.data_objects import Asset, BarDataType
from optopus.portfolio_manager import PortfolioManager
from optopus.order_manager import OrderManager
from optopus.watch_list import WATCH_LIST


class Optopus():
    """Class implementing automated trading system"""

    def __init__(self, broker) -> None:
        self._broker = broker
        self._account = Account()

    def start(self) -> None:
        print('[Initializating managers]')
        self._data_manager = DataManager(WATCH_LIST)
        self._data_manager.add_data_adapter(self._broker._data_adapter,
                                            DataSource.IB)
        self._portfolio_manager = PortfolioManager(self._data_manager)
        self._order_manager = OrderManager(self._broker)

        # Events
        self._broker.emit_account_item_event = self._change_account_item
        self._broker.emit_position_event = self._data_manager._position
        self._broker.emit_new_order = self._new_order
        self._broker.emit_order_status = self._order_status
        self._broker.emit_commission_report = self._data_manager._commission_report

        print('[Connecting to IB broker]')
        self._broker.connect()
        self._broker.sleep(1)

        print('[Updating portfolio]')
        self._data_manager.match_trades_positions()

        print('[Adding underlyings]')
        self._data_manager.initialize_assets()
        self._data_manager.update_assets()

        print('\n[Started]\n')

        # self._beat()

    def stop(self) -> None:
        self._broker.disconnect()

    def pause(self, time: float) -> None:
        self._broker.sleep(time)

    def process(self, signals) -> None:
        self._order_manager.process(signals)

    def _new_order(self) -> None:
        pass

    def _order_status(self) -> None:
        pass

    def _change_account_item(self, item: AccountItem) -> None:
        try:
            self._account.update_item_value(item)
        except Exception as e:
            print('Error updating account item', e)

    def _beat(self) -> None:
        # PIECE OF SHIT!!!!
        for t in self._broker._broker.timeRange(datetime.time(0, 0), datetime.datetime(2100, 1, 1, 0), 10):
            print('+')
        # self._data_manager.update_assets()
        # self.dummy.calculate_signals()

    def positions(self) -> object:
        return self._portfolio_manager.positions()

    def assets(self, fields: List[str]) -> List[OrderedDict]:
        return self._data_manager.assets(fields)

    def asset_historic(self, code: str) -> List[OrderedDict]:
        return self._data_manager.asset_historic(code)

    def asset_historic_IV(self, code: str) -> List[OrderedDict]:
        return self._data_manager.asset_historic_IV(code)

    def assets_matrix(self, field: str) -> dict:
        return self._data_manager._assets_matrix(field)

    def update_assets(self):
        return (self._data_manager.update_assets())

    def option_chain(self, code: str, fields: List[str]) -> List[OrderedDict]:
        return (self._data_manager.option_chain(code, fields))
