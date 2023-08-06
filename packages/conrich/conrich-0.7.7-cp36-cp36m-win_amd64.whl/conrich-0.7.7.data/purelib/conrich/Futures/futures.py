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
from Concord.API.Future.Client.OrderFormat import FOrderNew, FOrderChangePrice, FOrderChangeQty, FOrderDelete

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


class FuturesAPI(ucClient):

    def __init__(self, debug=False):
        self._load()
        self.is_login = False

        # register event handler
        self.OnFBulletinReport += self.bulletin_event_handler
        self.OnFErrorReport += self.error_event_handler
        self.OnFGeneralReport += self.general_event_handler
        self.OnFOrderReport += self.order_report_event_handler

        if debug:
            self.host = "tradeapitest.concords.com.tw"
        else:
            self.host = "tradeapi.concords.com.tw"

    def _load(self):
        global RET_CODE, HEADER, TAG

        with open(os.path.join(dir_path, 'return_code.json'), encoding='utf-8') as f:
            RET_CODE = json.load(f)
        with open(os.path.join(dir_path, 'header.json'), encoding='utf-8') as f:
            HEADER = json.load(f).get('Futures', {})
        with open(os.path.join(dir_path, 'tag.json'), encoding='utf-8') as f:
            TAG = json.load(f)
            self.msg_tag = TAG

        log4net_path = os.path.join(dir_path, 'log4net')
        AppDomain.CurrentDomain.SetData("APP_CONFIG_FILE", log4net_path)

    # 登入
    def login(self, id_no='', pwd='', branch_no='', account_no=''):
        '''
        param in_no:        身分證字號
        param pwd:          密碼
        param branch_no:    分公司代號
        account_no:         帳號
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
        ret, msg = self.FCheckConnect(None)
        logging.debug('[FCheckConnect] ({}) {}'.format(ret, RET_CODE.get(ret,'')))

        return True if int(ret)==102 else False
	
    # 查詢帳號資訊
    def account_info(self):
        ret, msg = self.FQueryAccountInfo(None)
        logging.debug('[FQueryAccountInfo] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['account_info'])
        
        return df.to_dict(orient='records')

    # 查詢是否多帳號登入
    def check_multi_login(self):
        result = self.FQueryMultiFlag()

        return result

    # 查詢期貨商品
    def get_commodity(self):
        ret, msg = self.FQueryCommo(None)
        logging.debug('[FQueryCommo] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['get_commodity'], dtype=object, keep_default_na=False)
        
        return df.to_dict(orient='records')

    # 查詢期貨商品月份
    def get_commodity_by_month(self):
        ret, msg = self.FQueryCommoYM(None)
        logging.debug('[FQueryCommoYM] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg),
                         names=HEADER['get_commodity_by_month'],
                         dtype=object, 
                         parse_dates=["上市日期","下市日期","最後結算日"],
                         date_parser=lambda x: pd.datetime.strptime(x, '%Y%m%d'),
                         keep_default_na=False)

        return df.to_dict(orient='records')

    # def code_convert(self):
    #     regex_format_O = '([A-Z]{2,3})(\\w{1})(\\d{5})([A-Z])(\\d)' #PPTAAAAACC (T:O或A-Z或1-5) 選擇權複式單格式
    #     regex_format_F = '(\\w{2})(\\w{1})([A-Z]{1})(\\d{1})' #PPTCC (T:F或1-9) 期貨複式單格式

    # if args['market'] == 'Option': #選擇權複式單組合規則
    #     product_format = re.match(regex_format_O, args['symbol'])  #Match the profuct string format (tuple type) (['TX', 'O', '05200', 'D', '3'])
    #     product_format_c = re.match(regex_format_O, args['symbol_c'])
    #     list_year = [product_format[4],product_format_c[4]]
    #     list_month = [product_format[3],product_format_c[3]]
    #     #To find out which group is different (=False)
    #     product_compare_diffindex = [product_format.groups().index(x) for x, y in zip(product_format.groups(),product_format_c.groups()) if y != x]
    #     month_diff1, month_diff2 = month_cal(list_year,list_month,month_dict)
    #     if 1 in product_compare_diffindex: #6.週選擇權時間價差(商品為月跟週)，斜線隔開 (TX'O'/TX'4')
    #         if  month_diff1 == month_diff2: #確認兩商品是否為同一個月
    #             if product_format_c[1].isdigit() == True: #判斷後面那個產品是否為週選擇
    #                 symbol = args['symbol'] + '/' + args['symbol_c'][:3]+args['symbol_c'][-2:] if int(product_format_c[1])>3 else args['symbol_c'] + '/' + args['symbol'][:3]+args['symbol'][-2:]
    #                 buy_sell_code = side.get(args['side_c'], '') if int(product_format_c[1])>3 else side.get(args['side'], '')
    #             else:
    #                 symbol = args['symbol_c'] + '/' + args['symbol'][:3]+args['symbol'][-2:] if int(product_format[1])>3 else args['symbol'] + '/' + args['symbol_c'][:3]+args['symbol_c'][-2:]
    #                 buy_sell_code = side.get(args['side'], '') if int(product_format[1])>3 else side.get(args['side_c'], '')
    #         else:#商品不同月，月份比較靠近現在的放前面
    #             symbol = args['symbol'] + '/' + args['symbol_c'][:3] + args['symbol_c'][-2:] if month_diff1<month_diff2 else args['symbol_c'] + '/' + args['symbol'][:3] + args['symbol'][-2:]
    #             buy_sell_code = side.get(args['side_c'], '') if month_diff1<month_diff2 else side.get(args['side'], '')
    #     elif 2 in product_compare_diffindex:  # 1.多空頭價差 4.勒式 (跨買賣權)
    #         if side.get(args['side']) == side.get(args['side_c']): #勒式(同時買、同時賣)，冒號隔開
    #             symbol = args['symbol'] + ':' + args['symbol_c'][3:] if ord(product_format[3])< ord(product_format_c[3]) else args['symbol_c'] + ':' + args['symbol'][3:]
    #             buy_sell_code = side.get(args['side_c'], '') if ord(product_format[3])< ord(product_format_c[3]) else side.get(args['side'], '')
    #         else: #多空頭價差(價格不同)，斜線隔開
    #             if ord(product_format[3])<=76: #為買權時，價高者放前面
    #                 symbol = args['symbol'][:-2] + '/' + args['symbol_c'][3:] if int(product_format[2]) > int(product_format_c[2]) else args['symbol_c'][:-2] + '/' + args['symbol'][3:]
    #                 buy_sell_code = side.get(args['side_c'], '') if int(product_format[2]) > int(product_format_c[2]) else side.get(args['side'], '')
    #             else: #為賣權時，價低者放前面
    #                 symbol = args['symbol'][:-2] + '/' + args['symbol_c'][3:] if int(product_format[2]) < int(product_format_c[2]) else args['symbol_c'][:-2] + '/' + args['symbol'][3:]
    #                 buy_sell_code = side.get(args['side_c'], '') if int(product_format[2]) < int(product_format_c[2]) else side.get(args['side'], '')
    #     else: #2.時間價差 3.跨式 5.轉換組合、逆轉組合
    #         if side.get(args['side']) == side.get(args['side_c']): #跨式(同時買、同時賣)，冒號隔開
    #             symbol = args['symbol'] + ':' + args['symbol_c'][-2:] if ord(product_format[3]) < ord(product_format_c[3]) else args['symbol_c'] + ':' + args['symbol'][-2:]
    #             buy_sell_code = side.get(args['side_c'], '') if ord(product_format[3]) < ord(product_format_c[3]) else side.get(args['side'], '')
    #         elif abs(ord(product_format[3])- ord(product_format_c[3])) < 12: #時間價差(月份不同)，斜線隔開(不會混合買權賣權，故月份不會跨12)
    #             symbol = args['symbol_c'] + '/' + args['symbol'][-2:] if month_diff1 > month_diff2 else args['symbol'] + '/' + args['symbol_c'][-2:]
    #             buy_sell_code = side.get(args['side'], '') if month_diff1 > month_diff2 else side.get(args['side_c'], '')
    #         else: #轉換組合、逆轉組合
    #             symbol = args['symbol'] + '-' + args['symbol_c'][-2:] if ord(product_format[3]) < ord(product_format_c[3]) else args['symbol_c'] + '-' + args['symbol'][-2:]
    #             buy_sell_code = side.get(args['side_c'], '') if ord(product_format[3]) < ord(product_format_c[3]) else side.get(args['side'], '')
    # else: #期貨複式單組合規則
    #     product_format = re.findall(regex_format_F, args['symbol'])[0] #PPTCC ('T5', 'F', 'K', '9')
    #     product_format_c = re.findall(regex_format_F, args['symbol_c'])[0]
    #     list_year = [product_format[4],product_format_c[4]]
    #     list_month = [product_format[3],product_format_c[3]]
    #     month_diff1, month_diff2 = month_cal(list_year,list_month,month_dict)
    #     if product_format[0][0] != 'M': #M小台,非小台狀況下(PPTCC/CC)
    #         symbol = args['symbol'] + '/' + args['symbol_c'][-2:] if month_diff1 < month_diff2 else args['symbol_c'] + '/' + args['symbol'][-2:]
    #         buy_sell_code = side.get(args['side_c'], '') if month_diff1 < month_diff2 else side.get(args['side'], '')
    #     else: #小台格式(PPPCC/PPWDD or PPWDD/PPPCC)
    #         if month_diff1 == month_diff2: #確認是否為同月
    #             if product_format[1].isdigit():
    #                 symbol = args['symbol'] + '/' + args['symbol_c'] if int(product_format[1]) <3 else args['symbol_c'] + '/' + args['symbol']
    #                 buy_sell_code = side.get(args['side_c'], '') if int(product_format[1]) <3 else side.get(args['side'], '')
    #             else:
    #                 symbol = args['symbol_c'] + '/' + args['symbol'] if int(product_format_c[1]) <3 else args['symbol'] + '/' + args['symbol_c']
    #                 buy_sell_code = side.get(args['side'], '') if int(product_format_c[1]) <3 else side.get(args['side_c'], '')
    #         else:
    #             symbol = args['symbol_c'] + '/' + args['symbol'] if month_diff1 > month_diff2 else args['symbol'] + '/' + args['symbol_c']
    #             buy_sell_code = side.get(args['side'], '') if month_diff1 > month_diff2 else side.get(args['side_c'], '')
                
    # return symbol, buy_sell_code

    # 下單
    def order(self, action, branch_no, account_no, market_type, compound_type, commodity, time_in_force, writeoff, order_type, side, quantity, price, orig_net_no='', order_id=''):
        '''
        param action:       OrderNew, OrderChangeQty, OrderChangePrice, OrderDelete
        param branch_no:	分公司代號	例：F029000
        param account_no:	帳號	例：1009991、0000455(含檢查碼)
        param market_type:	市場別	F=期貨、O=選擇權 
        param compound_type:	單複式別	1=期貨單式、2=選擇權單式、3=選擇權複式、4=期貨複式
        param commodity:	    商品代碼	商品代碼
        param time_in_force:	委託條件	F:=FOK、I=IOC、R=ROD
        param writeoff:	    沖銷別(開平倉碼)	0=開倉、1=平倉、2=期貨當沖、空白=自動
        param order_type:	委託方式	M=市價、L=限價、P=一定範圍市價
        param side:	        買賣別	B=買、S=賣
        param quantity:	    委託數量	新增時請輸入委託數量，例：1口=1、10口=10
        param price:	    委託價格	市價委託時請輸入0，例：80.50、8000.00(含小數點+小數兩位)
        param orig_net_no:	原網路單號	
        param order_id:	    委託書號
        '''
        inst = System.Activator.CreateInstance(eval('F{}'.format(action)))
        inst.bhno = branch_no[-3:]
        inst.cseq = account_no
        inst.mtype = market_type
        inst.sflag = compound_type
        inst.commo = commodity
        inst.fir = time_in_force
        inst.rtype = writeoff
        inst.otype = order_type
        inst.bs = side
        inst.qty = int(quantity)
        inst.price = System.Decimal(float(price))

        if action=='OrderNew':  # 單筆下單
            ret, msg, guid = self.FOrderNew(inst, None, None)
        else:
            inst.netno = orig_net_no
            inst.dseq = order_id
            
            if action=='OrderChangeQty': # 改量
                ret, msg, guid = self.FOrderChangeQty(inst, None, None)
            elif action=='OrderChangePrice':   # 改價
                ret, msg, guid = self.FOrderChangePrice(inst, None, None)
            elif action=='OrderDelete': # 刪單
                ret, msg, guid = self.FOrderDelete(inst, None, None)

        logging.debug('[{}] ({}) {}, guid={}'.format(action, ret, RET_CODE.get(ret,''), guid))

        return msg

    def order_recover(self, branch_no, account_no, seq_start=0, seq_end=0): # 回補
        '''
        param branch_no:	分公司代號	例：F029000
        param account_no:	帳號	例：1009991、0000455(含檢查碼)
        param seq_start:    開始序號
        param seq_end:      結束序號
        '''
        ret, msg = self.FOrderRecover(branch_no[-3:], account_no, seq_start, seq_end)
        logging.debug('[FOrderRecover] ({}) {}'.format(ret, RET_CODE.get(ret,'')))

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
            ret, msg = self.FQueryTOrder(branch_no[-3:], account_no, None)
        elif record_type=='Order' and period=='History':
            # 歷史委託回報查詢 
            ret, msg = self.FQueryHOrder(branch_no[-3:], account_no, None)
        elif record_type=='Deal' and period=='Today':
            # 今日成交回報查詢
            ret, msg = self.FQueryTDeal(branch_no[-3:], account_no, None)
        elif record_type=='Deal' and period=='History':
            # 歷史成交回報查詢
            ret, msg = self.FQueryHDeal(branch_no[-3:], account_no, None)

        logging.debug('[{}][{}] ({}) {}'.format(record_type, period, ret, RET_CODE.get(ret,'')))

        return ret, msg

    def margin(self, branch_no, account_no, currency='**', group='', trader=''):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        param currency      查詢幣別	TWD:國內台幣；US$:國內美元；** :約當台幣；ALL:全部
        param group         群組	1.非子帳客戶傳空白 2.查詢子帳客戶所有組別資料傳’***’
        param trader        交易員代號	1.非子帳客戶傳空白 2.查詢子帳客戶所有子帳資料傳"******"
        '''
        ret, msg = self.FQueryMargin(branch_no[-3:], account_no, currency, group, trader, None)
        logging.debug('[FQueryMargin] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['margin'])

        return df.to_dict(orient='records')

    def position(self, branch_no, account_no, group='', trader='', compound_type='3'):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        param group         組別	1.非子帳客戶傳空白 2.查詢子帳客戶所有組別資料傳’***’
        param trader        交易員	1.非子帳客戶傳空白 2.查詢子帳客戶所有子帳資料傳’******’
        param compound_type	查詢類別	1:單式  2:複式  3:全部
        '''
        ret, msg = self.FQueryPosition(branch_no[-3:], account_no, group, trader, compound_type, None)
        logging.debug('[FQueryPosition] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['position'])

        return df.to_dict(orient='records')

    def position_summary(self, branch_no, account_no, compound_type='3'):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        param compound_type	查詢類別	1:單式  2:複式  3:全部
        '''
        ret, msg = self.FQueryPositionSummary(branch_no[-3:], account_no, compound_type)
        logging.debug('[FQueryPositionSummary] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['position_summary'])

        return df.to_dict(orient='records')

    def position_index(self, branch_no, account_no):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FQueryPositionIndex(branch_no[-3:], account_no, None)
        logging.debug('[FQueryPositionIndex] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['position_index'])

        return df.to_dict(orient='records')

    def offset(self, branch_no, account_no):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FQueryOffset(branch_no[-3:], account_no, None)
        logging.debug('[FQueryOffset] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['offset'])

        return df.to_dict(orient='records')

    def offset_history(self, branch_no, account_no, start_date, end_date):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        param strSDate      起始日期	yyyyMMdd
        param strEDate      結束日期	yyyyMMdd
        '''
        ret, msg = self.FQueryHisOffset(branch_no[-3:], account_no, start_date.strftime('YYYYMMDD'), end_date.strftime('YYYYMMDD'), None)
        logging.debug('[FQueryHisOffset] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['offset_history'])

        return df.to_dict(orient='records')

    def deposit(self, branch_no, account_no):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        '''
        ret, msg = self.FQueryDeposit(branch_no[-3:], account_no, None)
        logging.debug('[FQueryDeposit] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['deposit'])

        return df.to_dict(orient='records')

    def deposit_history(self, branch_no, account_no, start_date, end_date):
        '''
        param branch_no     分公司代號	例：F029000
        param account_no	客戶帳號	7碼
        param strSDate      起始日期	yyyyMMdd
        param strEDate      結束日期	yyyyMMdd
        '''
        ret, msg = self.FQueryHisDeposit(branch_no[-3:], account_no, start_date.strftime('YYYYMMDD'), end_date.strftime('YYYYMMDD'), None)
        logging.debug('[FQueryHisDeposit] ({}) {}'.format(ret, RET_CODE.get(ret,'')))
        df = pd.read_csv(StringIO(msg), names=HEADER['deposit_history'])

        return df.to_dict(orient='records')

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


