# -*- coding: utf-8 -*-
import os, sys, json
import time
import logging
import clr
import pandas as pd
from io import StringIO
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
clr.AddReference(os.path.join(dir_path, "Concord.API.Future.Client.dll"))
import System
from System.Windows.Forms import Application
from System import AppDomain
from Concord.API.Future.Client import ucClient
from Concord.API.Future.Client.OrderFormat import FFOrderNew, FFOrderChangePrice, FFOrderChangeQty, FFOrderDelete


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

class ForeignFuturesAPI(ucClient):

    def __init__(self, debug=False):
        self._load()
        self.is_login = False

        # register event handler
        self.OnFFBulletinReport += self.bulletin_event_handler
        self.OnFFErrorReport += self.error_event_handler
        self.OnFFGeneralReport += self.general_event_handler
        self.OnFFOrderReport += self.order_report_event_handler

        if debug:
            self.host = "tradeapitest.concords.com.tw"
        else:
            self.host = "tradeapi.concords.com.tw"
    
    def _load(self):
        global RET_CODE, HEADER, TAG

        with open(os.path.join(dir_path, 'return_code.json'), encoding='utf-8') as f:
            RET_CODE = json.load(f)
        with open(os.path.join(dir_path, 'header.json'), encoding='utf-8') as f:
            HEADER = json.load(f).get('ForeignFutures', {})
        with open(os.path.join(dir_path, 'tag.json'), encoding='utf-8') as f:
            TAG = json.load(f)
            self.msg_tag = TAG

        log4net_path = os.path.join(dir_path, 'foreign', 'log4net')
        AppDomain.CurrentDomain.SetData("APP_CONFIG_FILE", log4net_path)

    # 登入
    def login(self, id_no='', pwd='', branch_no='', account_no=''):
        '''
        param in_no:    身分證字號
        param pwd:      密碼
        param branch_no: 分公司代號
        account_no:     帳號
        '''
        self.is_login = False

        if id_no:
            # login
            ret, msg = self.Login(id_no, pwd, self.host, '')
        else:
            # login by account
            ret, msg = self.LoginAccount(branch_no, account_no, pwd, self.host, '')
        logging.info('[Login] ({}) {}'.format(ret, msg))
        time.sleep(0.5)
        Application.DoEvents()
        for i in range(100):
            if self.is_login:
                break
            time.sleep(0.1)

        return True if self.is_login else False

    # 檢查連線狀況
    def check_connect(self):
        ret, msg = self.FFCheckConnect(None)
        logging.debug('[FFCheckConnect] ({}) {}'.format(ret, RET_CODE.get(ret,'')))

        return ret
	
    # 查詢帳號資訊
    def account_info(self):
        ret, msg = self.FFQueryAccountInfo(None)
        logging.debug('[FFQueryAccountInfo] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['account_info'])
        
        return df.to_dict(orient='records') if ret=="000" else []

    # 查詢是否多帳號登入
    def check_multi_login(self):
        result = self.FFQueryMultiFlag()
        logging.debug('[FFQueryMultiFlag] {}'.format(result))

        return result

    # 國外期貨查詢交易所
    def exchange(self):
        ret, msg = self.FFQueryExchange(None)
        logging.debug('[FFQueryExchange] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['exchange'])
        
        return df.to_dict(orient='records') if ret=="000" else []

    # 查詢期貨商品
    def get_commodity(self):
        ret, msg = self.FFQueryCommo(None)
        logging.debug('[FFQueryCommo] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['get_commodity'], dtype=object, keep_default_na=False)
        
        return df.to_dict(orient='records') if ret=="000" else []

    # 查詢期貨商品月份
    def get_commodity_by_month(self):
        ret, msg = self.FFQueryCommoYM(None)
        logging.debug('[FFQueryCommoYM] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg),
                         names=HEADER['get_commodity_by_month'],
                         dtype=object,
                         parse_dates=["最後交易日"],
                         date_parser=lambda x: pd.datetime.strptime(x, '%Y/%m/%d'),
                         keep_default_na=False)

        return df.to_dict(orient='records') if ret=="000" else []

    # 查詢匯率
    def exchange_rate(self):
        ret, msg = self.FFQueryCurrencyRate(None)
        logging.debug('[FFQueryCurrencyRate] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['exchange_rate'])

        return df.to_dict(orient='records')

    # 下單
    def order(self, action, branch_no, account_no, exchange, 
                side1, market_type1, commodity1, commodity_month1, strike_price1, put_call1,
                side2, market_type2, commodity2, commodity_month2, strike_price2, put_call2,
                order_type, price, price_numerator, price_denominator, stop_price, stop_price_numerator, stop_price_denominator,
                quantity, day_trade_flag, writeoff, order_id='', orig_quantity=0):
        '''
        param action:       OrderNew, OrderChangeQty, OrderChangePrice, OrderDelete
        param branch_no	分公司代號	例：F029000
        param account_no	帳號	例：1009991、0000455(含檢查碼)
        param exchange	交易所	
        param side1	買賣別1	B=買、S=賣
        param market_type1	商品類別1	F: 期貨、O: 選擇權
        param commodity1	商品代號1	
        param commodity_month1	商品年月1	yyyyMM
        param strike_price1	履約價1	最大長度(12.12)
        param put_call1	買賣權1	N: 期貨、C: 選擇權Call、P: 選擇權Put
        param side2	買賣別2	B=買、S=賣
        param market_type2	商品類別2	F: 期貨、O: 選擇權
        param commodity2	商品代號2	
        param commodity_month2	商品年月2	YYYYMM
        param strike_price2	履約價2	最大長度(12.12)
        param put_call2	買賣權2	N: 期貨、C: 選擇權Call、P: 選擇權Put
        param order_type	委託方式	MKT: 市價、LMT: 限價、STP: 停損市價、SWL: 停損限價
        param price	限價	最大長度(12.12)
        param price_numerator	限價(分子)	最大長度(4.4)
        param price_denominator	限價(分母)	最大長度(5)
        param stop_price	停損價	最大長度(12.12)
        param stop_price_numerator	停損價(分子)	最大長度(4.4)
        param stop_price_denominator	停損價(分母)	最大長度(5)
        param quantity	委託數量	最大長度(4)
        param writeoff	沖銷別(開平倉碼)	0=開倉、1=平倉、2=期貨當沖
        param order_id    委託書號
        param compound_type   單複式別	N: 非組合
        param orig_quantity   原委託數量
        '''
        inst = System.Activator.CreateInstance(eval('FF{}'.format(action)))
        inst.bhno = branch_no[-3:]
        inst.cseq = account_no
        inst.exchange = exchange
        inst.bs1 = side1
        inst.commtype1 = market_type1
        inst.commo1 = commodity1
        inst.commym1 = commodity_month1
        inst.stkPrice1 = System.Decimal(float(strike_price1))
        inst.cp1 = put_call1
        inst.bs2 = side2
        inst.commtype2 = market_type2
        inst.commo2 = commodity2
        inst.commym2 = commodity_month2
        inst.stkPrice2 = System.Decimal(float(strike_price2))
        inst.cp2 = put_call2
        inst.otype = order_type
        inst.price = System.Decimal(float(price))
        inst.price_numerator = System.Decimal(float(price_numerator)) 
        inst.price_denominator = int( price_denominator)
        inst.stopPrice = System.Decimal(float(stop_price)) 
        inst.stopPrice_numerator = System.Decimal(float(stop_price_numerator)) 
        inst.stopPrice_denominator = int(stop_price_denominator)
        inst.dtFlag = 'Y' if writeoff==2 else 'N'
        inst.rtype = 'N' if writeoff==1 else 'Y'

        if action=='OrderNew':  # 單筆下單
            inst.qty = int(quantity)

            ret, msg, guid = self.FFOrderNew(inst, None, None)
        elif action=='OrderDelete': # 刪單
            inst.dseq = order_id
            inst.oqty = int(orig_quantity)

            ret, msg, guid = self.FFOrderDelete(inst, None, None)
        else:
            inst.dseq = order_id
            inst.qty = int(quantity)
            inst.oqty = int(orig_quantity)

            if action=='OrderChangeQty': # 改量
                ret, msg, guid = self.FFOrderChangeQty(inst, None, None)
            elif action=='OrderChangePrice': # 改價
                ret, msg, guid = self.FFOrderChangePrice(inst, None, None)

        logging.debug('[{}] ({}) {}, guid={}'.format(action, ret, RET_CODE.get(ret,''), guid))

        return msg

    # 回補
    def order_recover(self, branch_no, account_no, seq_start=0, seq_end=0):
        '''
        param branch_no:	分公司代號	例：F029000
        param account_no:	帳號	例：1009991、0000455(含檢查碼)
        param seq_start:    開始序號
        param seq_end:      結束序號
        '''
        ret, msg = self.FFOrderRecover(branch_no[-3:], account_no, seq_start, seq_end)
        logging.debug('[FFOrderRecover] ({}) {}'.format(ret, RET_CODE.get(ret,'')))

        return ret

    def query_order(self, branch_no, account_no, record_type, period):
        '''
        param branch_no:	分公司代號	例：F029000
        param account_no:	帳號	例：1009991、0000455(含檢查碼)
        param record_type:  記錄類別    Order, Deal
        param period:       時間區間    History, Today
        '''
        if record_type=='Order' and period=='Today':
            # 今日委託回報查詢
            ret, msg = self.FFQueryTOrder(branch_no[-3:], account_no, None)
        elif record_type=='Order' and period=='History':
            # 歷史委託回報查詢 
            ret, msg = self.FFQueryHOrder(branch_no[-3:], account_no, None)
        elif record_type=='Deal' and period=='Today':
            # 今日成交回報查詢
            ret, msg = self.FFQueryTDeal(branch_no[-3:], account_no, None)
        elif record_type=='Deal' and period=='History':
            # 歷史成交回報查詢
            ret, msg = self.FFQueryHDeal(branch_no[-3:], account_no, None)

        logging.debug('[{}][{}] ({}) {}'.format(record_type, period, ret, RET_CODE.get(ret,'')))

        return ret, msg

    def margin(self, branch_no, account_no):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FFQueryMargin(branch_no[-3:], account_no, None)
        logging.debug('[FFQueryMargin] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['margin'])

        return df.to_dict(orient='records') if ret=="000" else []

    def position(self, branch_no, account_no):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FFQueryPosition(branch_no[-3:], account_no, None)
        logging.debug('[FFQueryPosition] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['position'])

        return df.to_dict(orient='records') if ret=="000" else []

    def position_index(self, branch_no, account_no):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FFQueryPositionIndex(branch_no[-3:], account_no, None)
        logging.debug('[FFQueryPositionIndex] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['position_index'])

        return df.to_dict(orient='records') if ret=="000" else []

    def offset(self, branch_no, account_no):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FFQueryOffset(branch_no[-3:], account_no, None)
        logging.debug('[FFQueryOffset] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['offset'])

        return df.to_dict(orient='records') if ret=="000" else []

    def offset_history(self, branch_no, account_no, start_date, end_date):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        param strSDate      起始日期	yyyyMMdd
        param strEDate      結束日期	yyyyMMdd
        '''
        ret, msg = self.FFQueryHisOffset(branch_no[-3:], account_no, start_date.strftime('YYYYMMDD'), end_date.strftime('YYYYMMDD'), None)
        logging.debug('[FFQueryHisOffset] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['offset_history'])

        return df.to_dict(orient='records') if ret=="000" else []

    def deposit(self, branch_no, account_no):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FFQueryDeposit(branch_no[-3:], account_no, None)
        logging.debug('[FFQueryDeposit] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['deposit'])

        return df.to_dict(orient='records') if ret=="000" else []

    def deposit_history(self, branch_no, account_no, start_date, end_date):
        '''
        param branch_no     分公司碼	F029000
        param account_no	客戶帳號	7碼
        param strSDate      起始日期	yyyyMMdd
        param strEDate      結束日期	yyyyMMdd
        '''
        ret, msg = self.FFQueryHisDeposit(branch_no[-3:], account_no, start_date.strftime('YYYYMMDD'), end_date.strftime('YYYYMMDD'), None)
        logging.debug('[FFQueryHisDeposit] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['deposit_history'])

        return df.to_dict(orient='records') if ret=="000" else []

    def error_event_handler(self, code, msg):
        logging.info("[ErrorEvent] ({}) {}".format(code, msg))
        Application.DoEvents()

    def general_event_handler(self, code, msg):
        if int(code)==102:
            self.is_login = True
        logging.info("[GeneralEvent] ({}) {}".format(code, msg))
        Application.DoEvents()

    def order_report_event_handler(self, code, msg):
        logging.info("[OrderReport] ({}) {}".format(code, msg))
        # dict_msg = dict((TAG[k], v) for k,v in [tag.split('=') for tag in msg.split('|')])
        # logging.debug(dict_msg)
        Application.DoEvents()
        
    def bulletin_event_handler(self, code, msg):
        logging.info("[BulletinEvent] ({}) {}".format(code, msg))
        # dict_msg = dict((TAG[k], v) for k,v in [tag.split('=') for tag in msg.split('|')])
        # logging.debug(dict_msg)
        Application.DoEvents()

    def __del__(self):
        ret, msg = self.Logout(None)
        logging.debug('[Logout] ({}) {}'.format(ret, msg))

