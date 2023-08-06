
from enum import Enum

# 委託種類
class Action(Enum):
    NEW_ORDER = 'NewOrder'  # 新單
    CANCEL_ORDER = 'CancelOrder'    # 刪單
    MODIFY_QUANTITY = 'ModifyQty'   # 改量
    MODIFY_PRICE = 'ModifyPrice'    # 改價

# 交易別
class LotType(Enum):
    ROUND_LOT = 'RoundLot'  # 整股
    BLOCK_LOT = 'BlockLot'  # 鉅額
    ODD_LOT = 'OddLot'      # 零股
    FIX_PRICE = 'FixedPrice'    # 定價

# 委託別
class OrderType(Enum):
    ORDINARY = 'Ordinary'   # 現股
    MARGIN  = 'Margin'  # 融資
    SHORT   = 'Short'   # 融券

# 買賣別
class Side(Enum):
    BUY = 'Buy' # 買進
    SELL    = 'Sell'    # 賣出

# 現沖註記
class DayTradeFlag(Enum):
    Y   = 'Enable'
    N   = 'Unable'

# 價格註記(委託方式)
class PriceFlag(Enum):
    FIX = 'Limit'  # 限價
    MARKET  = 'Market'  # 市價
    LIMIT_UP = 'LimitUp'    # 漲停
    LIMIT_DOWN  = 'LimitDown'   # 跌停
    UNCHANGED   = 'Unchange'    # 平盤

# 委託條件
class TimeInForce(Enum):
    ROD = 'ROD' # 當盤有效
    IOC = 'IOC' # 立即成交其餘刪除
    FOK = 'FOK' # 全部立即成交否則刪除