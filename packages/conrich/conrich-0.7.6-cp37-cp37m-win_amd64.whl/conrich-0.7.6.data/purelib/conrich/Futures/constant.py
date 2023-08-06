
from enum import Enum

# 委託種類
class Action(Enum):
    NEW_ORDER = 'OrderNew'  # 新單
    CANCEL_ORDER = 'OrderDelete'    # 刪單
    MODIFY_QUANTITY = 'OrderChangeQty'   # 改量
    MODIFY_PRICE = 'OrderChangePrice'    # 改價

class Market(Enum):
    FUTURES = 'F'   # 期貨
    OPTION  = 'O'   # 選擇權

# 單複式別
class CompoundType(Enum):
    FUTURES_SINGLE  = '1'   # 期貨單式
    OPTION_SINGLE   = '2'   # 選擇權單式
    OPTION_COMBINE  = '3'   # 選擇權複式
    FUTURES_COMBINE = '4'   # 期貨複式

# 委託條件
class TimeInForce(Enum):
    ROD = 'R' # 當盤有效
    IOC = 'I' # 立即成交其餘刪除
    FOK = 'F' # 全部立即成交否則刪除

# 沖銷別(開平倉碼)
class WriteOff(Enum):
    OPEN    = '0'   # 開倉
    CLOSE   = '1'   # 平倉
    DAY_TRADE   = '2'   # 期貨當沖
    AUTO    = ''    # 自動

# 委託別
class OrderType(Enum):
    MARKET  = 'M'   # 市價
    LIMIT   = 'L'  # 限價
    MWP     = 'P'   # 一定範圍市價

# 外期委託方式
class ForeignOrderType(Enum):
    MARKET  = 'MKT' # 市價
    LINIT   = 'LMT' # 限價
    STOP    = 'STP' # 停損市價
    STOP_LIMIT  = 'SWL' # 停損限價

# 買賣別
class Side(Enum):
    BUY = 'B' # 買進
    SELL    = 'S'    # 賣出

class PutCall(Enum):
    NONE = 'N'  # 期貨
    PUT = 'P'   # 賣權
    CALL = 'C'  # 買權

# 當沖碼
class DayTradeFlag(Enum):
    Y   = 'Y'   # 當沖
    N   = 'N'   # 非當沖

