| Method | 中文說明             | 國內API規格                | 參數             | 說明                                                      |
|--------|------------------|------------------------|----------------|---------------------------------------------------------|
| 系統相關   | 登入               | login                  | in_no          | 身分證字號                                                   |
|        |                  |                        | pwd            | 密碼                                                      |
|        |                  |                        | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        | 檢查連線狀況           | check_connect          |                |                                                         |
| 基本資料   | 查詢帳號資訊           | account_info           |                |                                                         |
|        | 查詢是否多帳號登入        | check_multi_login      |                |                                                         |
|        | 查詢期貨商品           | get_commodity          |                |                                                         |
|        | 查詢期貨商品月份         | get_commodity_by_month |                |                                                         |
| 交易相關   | 單筆下單             | order                  | action         | OrderNew, OrderChangeQty, OrderChangePrice, OrderDelete |
|        |                  |                        | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | market_type    | 市場別 F=期貨、O=選擇權                                          |
|        |                  |                        | compound_type  | 單複式別 1=期貨單式、2=選擇權單式、3=選擇權複式、4=期貨複式                      |
|        |                  |                        | commodity      | 商品代碼                                                    |
|        |                  |                        | time_in_force  | 委託條件 F:=FOK、I=IOC、R=ROD                                 |
|        |                  |                        | writeoff       | 沖銷別(開平倉碼) 0=開倉、1=平倉、2=期貨當沖、空白=自動                        |
|        |                  |                        | order_type     | 委託方式 M=市價、L=限價、P=一定範圍市價                                 |
|        |                  |                        | side           | 買賣別 B=買、S=賣                                             |
|        |                  |                        | quantity       | 委託數量 新增時請輸入委託數量，例：1口=1、10口=10                           |
|        |                  |                        | price          | 委託價格 市價委託時請輸入0，例：80.50、8000.00(含小數點+小數兩位)               |
|        |                  |                        | orig_net_no    | 原網路單號                                                   |
|        |                  |                        | order_id       | 委託書號                                                    |
|        | 回補               | order_recover          | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | seq_start      | 開始序號                                                    |
|        |                  |                        | seq_end        | 結束序號                                                    |
|        | 回報查詢             | query_order            | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | record_type    | 記錄類別    Order, Deal                                     |
|        |                  |                        | period         | 時間區間    History, Today                                  |
| 帳務查詢   | 期貨保證金查詢          | margin                 | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | currency       | 查詢幣別 TWD:國內台幣；US$:國內美元；** :約當台幣；ALL:全部                  |
|        |                  |                        | group          | 群組 1.非子帳客戶傳空白 2.查詢子帳客戶所有組別資料傳’***’                      |
|        |                  |                        | trader         | 交易員代號 1.非子帳客戶傳空白 2.查詢子帳客戶所有子帳資料傳"******"                |
|        | 未平倉查詢 (外期含多貨幣查詢) | position               | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | group          | 組別 1.非子帳客戶傳空白 2.查詢子帳客戶所有組別資料傳’***’                      |
|        |                  |                        | trader         | 交易員 1.非子帳客戶傳空白 2.查詢子帳客戶所有子帳資料傳’******’                  |
|        |                  |                        | compound_type  | 查詢類別 1:單式  2:複式  3:全部                                   |
|        | 未平倉彙總查詢          | position_summary       | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | compound_type  | 查詢類別 1:單式  2:複式  3:全部                                   |
|        | 即時部位查詢           | position_index         | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        | 沖銷明細查詢           | offset                 | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        | 歷史沖銷明細查詢         | offset_history         | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | strSDate       | 起始日期                                                    |
|        |                  |                        | strEDate       | 結束日期                                                    |
|        | 出入金查詢            | deposit                | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        | 歷史出入金查詢          | deposit_history        | branch_no      | 分公司代號 例：F029000                                         |
|        |                  |                        | account_no     | 帳號 例：1009991、0000455(含檢查碼)                              |
|        |                  |                        | strSDate       | 起始日期                                                    |
|        |                  |                        | strEDate       | 結束日期                                                    |

| Event  | 中文說明             | 國內API規格                | 參數             | 說明                                                      |
| 系統相關   | 主動一般通知事件         | OnFGeneralReport       | code           | 代碼                                                      |
|        |                  |                        | msg            | 訊息                                                      |
|        | 主動錯誤通知事件         | OnFErrorReport         | code           | 代碼                                                      |
|        |                  |                        | msg            | 訊息                                                      |
|        | 主動公告通知事件         | OnFBulletinReport      | code           | 代碼                                                      |
|        |                  |                        | msg            | 訊息                                                      |
| 交易相關   | 主動委成回通知事件        | OnFOrderReport         | code           | 代碼                                                      |
|        |                  |                        | msg            | 訊息                                                      |