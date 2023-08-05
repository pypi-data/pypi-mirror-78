from kumex.marke_data.market_data import MarketData
from kumex.trade.trade import TradeData
from kumex.user.user import UserData
from kumex.ws_token.token import GetToken


class Market(MarketData):
    pass


class User(UserData):
    pass


class Trade(TradeData):
    pass


class WsToken(GetToken):
    pass


