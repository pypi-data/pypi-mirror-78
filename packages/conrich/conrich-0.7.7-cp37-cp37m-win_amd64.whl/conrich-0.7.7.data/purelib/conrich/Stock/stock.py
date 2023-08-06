# -*- coding: utf-8 -*-
import os, sys, json
import time
import logging
import clr
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
clr.AddReference(os.path.join(dir_path, "ConcordSTradeAPI.dll"))
from System import Enum
from System import AppDomain
from Concord.API.Client.Stock.TradeAPI import TradeAPI, SessionClient
from Concord.API.Client.Stock.TradeAPI.StatusCode import *
from Concord.API.Client.Stock.TradeAPI.RetunClass import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


class StockAPI(TradeAPI):

    def __init__(self, debug=False):
        self._load()
        self.is_login = False
        
        # register event handler
        self.BulletinEvent += self.bulletin_event_handler
        self.GeneralEvent += self.general_event_handler
        self.OrderReportEvent += self.order_report_event_handler
        self.SocketStatusEvent += self.socket_status_event_handler

        if debug:
            self.host = "tradeapitest.concords.com.tw"
        else:
            self.host = "tradeapi.concords.com.tw"
    
    def _load(self):
        global HEADER, TAG

        with open(os.path.join(dir_path, 'header.json'), encoding='utf-8') as f:
            HEADER = json.load(f).get('Stock', {})
        with open(os.path.join(dir_path, 'tag.json'), encoding='utf-8') as f:
            TAG = json.load(f)

        log4net_path = os.path.join(dir_path, 'log4net')
        AppDomain.CurrentDomain.SetData("APP_CONFIG_FILE", log4net_path)
        
    # 登入
    def login(self, id_no, pwd):
        self.is_login = False

        # login
        ret, msg = self.Login(id_no, pwd, self.host, '')
        logging.info('[Login] {} {}'.format(ret, msg))
        for i in range(100):
            if self.is_login:
                break
            time.sleep(0.1)
        
        return ret

    # 交易相關
    def order_recover(self, branch_no, account_no):
        '''
        param branch_no: 客戶分公司代碼
        param account_no: 客戶分帳號
        '''
        ret = self.StockOrderRecover(branch_no, account_no)  # return bool
        logging.info('[OrderRecover]: {}'.format(ret))

        return ret

    def order(self, action, branch_no, account_no, lot_type, order_type, side, day_trade_flag, 
                symbol, quantity, price, price_flag, time_in_force, orig_net_no='', order_id=''):
        '''
        param action:       ['NewOrder','CancelOrder','ModifyQty','ModifyPrice'], 委託種類：新單、刪單、改量、改價
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        param lot_type:     ['RoundLot','BlockLot','OddLot','FixedPrice'], 交易別：整股、鉅額、零股、定價
        param order_type:   ['Ordinary','Margin','Short'], 委託別：現股、自資、自券
        param side:         ['Buy','Sell'], 買賣別：買進、賣出
        param day_trade_flag:   ['Enable', 'Unable'], 現沖註記
        param symbol:       商品代號
        param quantity:     委託數量
        param price:        委託價格 (限價需帶入委託價格)
        param price_flag:   ['Limit','Market','LimitUp','LimitDown','Unchange'], 價格註記：限價、市價、漲停、跌停、平盤
        param time_in_force:    ['ROD', 'IOC', 'FOK'], 委託條件：當盤有效、立即成交其餘刪除、全部立即成交否則刪除
        param orig_net_no:      原網路單號：刪改單時，須帶入被刪改委託單資訊
        param order_id:     委託書號：刪改單時，須帶入被刪改委託單資訊
        '''
        oreder_result = self.StockOrder(Enum.Parse(OrderAction, action),
                                            account_no,
                                            branch_no[-1],  # 分公司碼長度=1
                                            Enum.Parse(OrderLotType, lot_type),
                                            Enum.Parse(OrderType, order_type),
                                            Enum.Parse(SideFlag, side),
                                            Enum.Parse(DayTrade, day_trade_flag), 
                                            symbol,
                                            str(quantity),
                                            str(price),
                                            Enum.Parse(PriceFlag, 'LimitPrice' if price_flag in ('Limit', 'Market') else price_flag),
                                            orig_net_no,
                                            order_id,
                                            Enum.Parse(OrderPriceType, price_flag if price_flag=='Market' else 'Limit'),
                                            Enum.Parse(TimeInForce, time_in_force))
        return {'result'    : oreder_result.ResultType,
                'status'    : oreder_result.StatusCode,
                'desc'      : oreder_result.CodeDesc,
                'order_guid'    : oreder_result.OrderGuid,
                'net_no'    : oreder_result.ClOrdID}

    # 客戶資料查詢
    def accounts_info(self):
        '''
        帳號資訊查詢
        '''
        result = self.QAccountsInfo()
        logging.info('[AccountsInfo] {} {}'.format(result.StatusCode, result.CodeDesc))

        return [dict(zip(HEADER['accounts_info'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def current_delivery(self, branch_no, account_no):
        '''
        即時交割金額試算
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        '''
        result = self.QRealDelivery(branch_no, account_no)
        logging.info('[CurrentDelivery] {} {}'.format(result.StatusCode, result.CodeDesc))
        
        return [dict(zip(HEADER['current_delivery'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def three_days_delivery(self, branch_no, account_no):
        '''
        近3日應收付
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        '''
        result = self.QThreeDayDelivery(branch_no, account_no)
        logging.info('[ThreeDaysDelivery] {} {}'.format(result.StatusCode, result.CodeDesc))
        
        return [dict(zip(HEADER['three_days_delivery'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def history_delivery(self, branch_no, account_no, start_date, end_date):
        '''
        歷史對帳單查詢
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        param start_date:   查詢起始日
        param end_date:     查詢結束日
        '''
        result = self.QHisDelivery(branch_no, account_no, start_date.strftime('YYYYMMDD'), end_date.strftime('YYYYMMDD'))
        logging.info('[HistoryDelivery] {} {}'.format(result.StatusCode, result.CodeDesc))
        
        return [dict(zip(HEADER['history_delivery'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def realized_profit(self, branch_no, account_no, start_date, end_date):
        '''
        已實現損益彙總查詢
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        param start_date:   查詢起始日
        param end_date:     查詢結束日
        '''
        result = self.QRealizedPL(branch_no, account_no, start_date.strftime('YYYYMMDD'), end_date.strftime('YYYYMMDD'))
        logging.info('[RealizedProfit] {} {}'.format(result.StatusCode, result.CodeDesc))
        
        return [dict(zip(HEADER['realized_profit'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def unrealized_profit(self, branch_no, account_no):
        '''
        未實現損益彙總查詢
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        '''
        result = self.QUnrealizedPL(branch_no, account_no)
        logging.info('[UnrealizedProfit] {} {}'.format(result.StatusCode, result.CodeDesc))

        return [dict(zip(HEADER['unrealized_profit'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def maintenance_rate(self, branch_no, account_no):
        '''
        維持率彙總試算查詢
        param branch_no:    客戶分公司代碼
        param account_no:   客戶分帳號
        '''
        result = self.QMaintain(branch_no, account_no)
        logging.info('[MaintenanceRate] {} {}'.format(result.StatusCode, result.CodeDesc))
        
        return [dict(zip(HEADER['maintenance_rate'], r.split(','))) for r in result.Deatils] if result.Deatils else []

    def socket_status_event_handler(self, connect, msg):
        logging.info("[SocketStatusEvent] {} {}".format(Enum.GetName(ConnectionWay, connect), msg))

    def general_event_handler(self, msg):
        if "[註冊成功]" in msg:
            self.is_login = True
        
        logging.info("[GeneralEvent] {}.".format(msg))

    def order_report_event_handler(self, result, msg):
        logging.info("[OrderReport] {}.".format(msg))

        order_result = {'result'    : result.ResultType,
                        'status'    : result.StatusCode,
                        'desc'      : result.CodeDesc,
                        'order_guid'    : result.OrderGuid,
                        'net_no'    : result.ClOrdID
                        }
        logging.debug(order_result)

        if result.ResultType=='1':
            report = result.ExcReport
            exe_report = {'order_id'  : report.OrderID,
                        'orig_net_no'   : report.OrigClOrdID,
                        'execute_status'    : report.ExecType,
                        'account_no'    : report.Account,
                        'symbol'    : report.Symbol,
                        'side'      : report.Side,
                        'quantity'  : report.OrderQty,
                        'price'     : report.Price,
                        'strike_quantity'   : report.LastQty,
                        'strike_price'   : report.LastPx,
                        'transaction_time'  : report.TransactTime}
            logging.debug(exe_report)
        
    def bulletin_event_handler(self, msg):
        logging.info("[BulletinEvent] {}.".format(msg))

    def __del__(self):
        self.Logout()
        logging.debug('[Logout] Success.')

