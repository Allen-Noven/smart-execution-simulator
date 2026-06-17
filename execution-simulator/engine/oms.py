from alpaca.trading.client import TradingClient

# 你的 API
API_KEY = "PKS775Q3SDJJEI5G5JUOHX5MNZ"
SECRET_KEY = "6ZQr11bvF52WoxT9uheVX3sSMWCALfmCHChhoCaRvFQG"

# 连接 paper trading
trading_client = TradingClient(

    API_KEY,
    SECRET_KEY,

    paper=True
)

# 获取账户信息
account = trading_client.get_account()

# 打印账户状态
print("Account Status:")
print(account)
