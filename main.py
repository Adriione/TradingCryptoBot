def fonction1():
        # import des bibliothèques nécessaires
            from binance.client import Client
            from keras.models import Sequential
            from keras.layers import Dense
            import numpy as np
            import telegram
            from telegram import Bot
            import yfinance as yf
            # initialisation du client Binance avec vos identifiants API
            client = Client(api_key='pwbK4DIkCE8l16WKKHPmO86UUkF37VZsGpabkYANjlal8L2xspICpN5Fr1eE3HNC',
                                api_secret='VDJ1oUSbsASgxTSfPFDVr8kgWYi1L2fG2XZ8wtyGr9kExwzpvfaUq6MKH4ob6aKF')
            client.API_URL = 'https://testnet.binance.vision/api'
            print(client.get_account())


            # connect to Telegram API
            telegram_token = '6016951767:AAFomJPQ-yfs-xvwgb5RoI3hs2wGTHg2HWA'
            telegram_chat_id = '744611081'
            bot = Bot(token=telegram_token)

            # collecte des données de marché pour le Bitcoin et l'Ethereum
            btc_data1 = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan, 2019', '21 Mar, 2023')
            eth_data1 = client.get_historical_klines('ETHUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan, 2019', '21 Mar, 2023')
            ticker = "BTC-USD"
            btc_data = yf.download(ticker, start="2019-01-01", end="2023-03-21")
            tricker = "ETH-USD"
            eth_data = yf.download(tricker, start="2019-01-01", end="2023-03-21")
            # nettoyage et prétraitement des données
            btc_prices = []
            for entry in btc_data:
                btc_prices = btc_data["Close"].tolist()
            eth_prices = []
            for entry in eth_data:
                eth_prices = eth_data["Close"].tolist()

            # préparation des données pour l'apprentissage
            look_back = 30
            train_size = int(len(btc_prices) * 0.8)
            test_size = len(btc_prices) - train_size
            btc_train, btc_test = btc_prices[0:train_size], btc_prices[train_size:len(btc_prices)]
            eth_train, eth_test = eth_prices[0:train_size], eth_prices[train_size:len(eth_prices)]

            def create_dataset(dataset, look_back=1):
                dataX, dataY = [], []
                for i in range(len(dataset) - look_back - 1):
                    a = dataset[i:(i + look_back)]
                    dataX.append(a)
                    dataY.append(dataset[i + look_back])
                return np.array(dataX), np.array(dataY)

            # création et entraînement du modèle de prédiction
            btc_trainX, btc_trainY = create_dataset(btc_train, look_back)
            eth_trainX, eth_trainY = create_dataset(eth_train, look_back)
            btc_model = Sequential()
            btc_model.add(Dense(8, input_dim=look_back, activation='relu'))
            btc_model.add(Dense(1))
            btc_model.compile(loss='mean_squared_error', optimizer='adam')
            btc_model.fit(btc_trainX, btc_trainY, epochs=50, batch_size=2, verbose=2)
            eth_model = Sequential()
            eth_model.add(Dense(8, input_dim=look_back, activation='relu'))
            eth_model.add(Dense(1))
            eth_model.compile(loss='mean_squared_error', optimizer='adam')
            eth_model.fit(eth_trainX, eth_trainY, epochs=50, batch_size=2, verbose=2)

            # prédiction des prix futurs
            btc_testX, btc_testY = create_dataset(btc_test, look_back)
            btc_testX = np.reshape(btc_testX, (btc_testX.shape[0], btc_testX.shape[1]))
            eth_testX, eth_testY = create_dataset(eth_test, look_back)
            eth_testX = np.reshape(eth_testX, (eth_testX.shape[0], eth_testX.shape[1]))
            btc_predictions = btc_model.predict(btc_testX)
            eth_predictions = eth_model.predict(eth_testX)

            # trading

            for i in range(len(btc_predictions)):
                btc_price = btc_testY[i]
                btc_prediction = btc_predictions[i]
                eth_price = eth_testY[i]
                eth_prediction = eth_predictions[i]
                if btc_prediction > btc_price:
                    stop_loss_price = btc_price * 0.95
                    take_profit_price = btc_price * 1.05
                    # Passer l'ordre d'achat au prix du marché
                    order = client.order_market_buy(
                        symbol='BTCUSDT',
                        quantity=0.01,
                    )
                    print(f'Bought 0.01 BTC for {order["cummulativeQuoteQty"]}')
                    # Passer l'ordre de stop loss
                    stop_loss_order = client.create_order(
                        symbol='BTCUSDT',
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=0.01,
                        stopPrice=stop_loss_price,
                        price=stop_loss_price,
                    )

                    # Passer l'ordre de take profit
                    take_profit_order = client.create_order(
                        symbol='BTCUSDT',
                        side='SELL',
                        type='TAKE_PROFIT_LIMIT',
                        quantity=0.01,
                        stopPrice=take_profit_price,
                        price=take_profit_price,
                    )



                elif btc_prediction < btc_price:
                    # Calculer les prix stop loss et take profit
                    stop_loss_price = btc_price * 1.05
                    take_profit_price = btc_price * 0.95

                    # Passer l'ordre d'achat au prix du marché
                    order = client.order_market_sell(
                        symbol='BTCUSDT',
                        quantity=0.01,
                    )
                    print(f'Sell 0.01 BTC for {order["cummulativeQuoteQty"]}')
                    # Passer l'ordre de stop loss
                    stop_loss_order = client.create_order(
                        symbol='BTCUSDT',
                        side='BUY',
                        type='STOP_LOSS_LIMIT',
                        quantity=0.01,
                        stopPrice=stop_loss_price,
                        price=stop_loss_price,
                    )

                    # Passer l'ordre de take profit
                    take_profit_order = client.create_order(
                        symbol='BTCUSDT',
                        side='BUY',
                        type='TAKE_PROFIT_LIMIT',
                        quantity=0.01,
                        stopPrice=take_profit_price,
                        price=take_profit_price,
                    )


                if eth_prediction > eth_price:
                    order = client.order_market_buy(symbol='ETHUSDT', quantity=0.1)
                    print(f'Bought 0,01 ETH for {order["cummulativeQuoteQty"]}')
                    # Calculer les prix stop loss et take profit
                    stop_loss_price = eth_price * 0.95
                    take_profit_price = eth_price * 1.05


                    # Passer l'ordre de stop loss
                    stop_loss_order = client.create_order(
                        symbol='ETHUSDT',
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=0.1,
                        stopPrice=stop_loss_price,
                        price=stop_loss_price,
                    )

                    # Passer l'ordre de take profit
                    take_profit_order = client.create_order(
                        symbol='ETHUSDT',
                        side='SELL',
                        type='TAKE_PROFIT_LIMIT',
                        quantity=0.1,
                        stopPrice=take_profit_price,
                        price=take_profit_price,
                    )


                elif eth_prediction < eth_price:
                    order = client.order_market_sell(symbol='ETHUSDT', quantity=0.1)
                    print(f'Sold 0,01 ETH for {order["cummulativeQuoteQty"]}')
                    # Calculer les prix stop loss et take profit
                    stop_loss_price = eth_price * 1.05
                    take_profit_price = eth_price * 0.95

                    # Passer l'ordre de stop loss
                    stop_loss_order = client.create_order(
                        symbol='ETHUSDT',
                        side='BUY',
                        type='STOP_LOSS_LIMIT',
                        quantity=0.1,
                        stopPrice=stop_loss_price,
                        price=stop_loss_price,
                    )

                    # Passer l'ordre de take profit
                    take_profit_order = client.create_order(
                        symbol='ETHUSDT',
                        side='BUY',
                        type='TAKE_PROFIT_LIMIT',
                        quantity=0.1,
                        stopPrice=take_profit_price,
                        price=take_profit_price,
                    )