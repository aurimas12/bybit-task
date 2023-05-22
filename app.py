from objects import User, Client
import datetime as dt
import config


if __name__ == "__main__":
    symbol = 'BTCUSD'
    user = User(config)
    client = Client()
    client.logIn_client(user.api_key, user.api_secret)

    client.get_kline_list(symbol, 1, dt.datetime(
        2020, 1, 1), dt.datetime(2020, 2, 1))
    client.get_info(symbol)
    client.read_kline_data(symbol)
