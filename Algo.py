import pandas as pd
import numpy as np
import yfinance as yf
import time
from binance.client import Client
from binance.enums import *
import time
import yfinance as yf
from binance.client import Client
from binance.enums import *

def fonction2():
    client = Client(api_key='7hfAJlPihlqg8J318lr14wHxl90GMbl3wQg2o4dy29anl0pCaK6u9Oa7IFWvZKdT', api_secret='K3HPFkZEeOkrLPFb48bSFLCiP5EXMvHN3BTHjEAx1oD7ZM2EnOlIBaH7sfGrRAw1')
    client.API_URL = 'https://testnet.binance.vision/api'
    print(client.get_account())

    # Récupérer les données de prix pour le BTC et l'ETH
    btc_data = yf.download('BTC-USD', start='2020-01-01', end='2022-03-22')
    eth_data = yf.download('ETH-USD', start='2020-01-01', end='2022-03-22')

    # Calculer la EMA sur 20 périodes pour le BTC et l'ETH
    btc_ema_20 = btc_data['Close'].ewm(span=20, adjust=False).mean()
    eth_ema_20 = eth_data['Close'].ewm(span=20, adjust=False).mean()

    # Calculer la RSI sur 14 périodes pour le BTC et l'ETH
    btc_delta = btc_data['Close'].diff()
    btc_gain = btc_delta.where(btc_delta > 0, 0)
    btc_loss = -btc_delta.where(btc_delta < 0, 0)
    btc_avg_gain = btc_gain.rolling(window=14).mean()
    btc_avg_loss = btc_loss.rolling(window=14).mean()
    btc_rs = btc_avg_gain / btc_avg_loss
    btc_rsi = 100 - (100 / (1 + btc_rs))

    eth_delta = eth_data['Close'].diff()
    eth_gain = eth_delta.where(eth_delta > 0, 0)
    eth_loss = -eth_delta.where(eth_delta < 0, 0)
    eth_avg_gain = eth_gain.rolling(window=14).mean()
    eth_avg_loss = eth_loss.rolling(window=14).mean()
    eth_rs = eth_avg_gain / eth_avg_loss
    eth_rsi = 100 - (100 / (1 + eth_rs))

    # Ajouter les EMA et RSI aux données de prix
    btc_data['ema_20'] = btc_ema_20
    btc_data['rsi'] = btc_rsi
    eth_data['ema_20'] = eth_ema_20
    eth_data['rsi'] = eth_rsi


    def get_current_price(ticker):
        data = yf.download(ticker, period='1d', interval='1m')
        return data['Close'][-1]

    # Récupérer les données pour BTC et ETH sur Yahoo Finance
    btc_data = yf.download('BTC-USD', period='3mo', interval='1d')
    eth_data = yf.download('ETH-USD', period='3mo', interval='1d')

    # Calculer la EMA sur 20 périodes pour le BTC et l'ETH
    btc_ema_20 = btc_data['Close'].ewm(span=20, adjust=False).mean()
    eth_ema_20 = eth_data['Close'].ewm(span=20, adjust=False).mean()

    # Calculer la RSI sur 14 périodes pour le BTC et l'ETH
    btc_delta = btc_data['Close'].diff()
    btc_gain = btc_delta.where(btc_delta > 0, 0)
    btc_loss = -btc_delta.where(btc_delta < 0, 0)
    btc_avg_gain = btc_gain.rolling(window=14).mean()
    btc_avg_loss = btc_loss.rolling(window=14).mean()
    btc_rs = btc_avg_gain / btc_avg_loss
    btc_rsi = 100 - (100 / (1 + btc_rs))

    eth_delta = eth_data['Close'].diff()
    eth_gain = eth_delta.where(eth_delta > 0, 0)
    eth_loss = -eth_delta.where(eth_delta < 0, 0)
    eth_avg_gain = eth_gain.rolling(window=14).mean()
    eth_avg_loss = eth_loss.rolling(window=14).mean()
    eth_rs = eth_avg_gain / eth_avg_loss
    eth_rsi = 100 - (100 / (1 + eth_rs))

    # Ajouter les EMA et RSI aux données de prix
    btc_data['ema_20'] = btc_ema_20
    btc_data['rsi'] = btc_rsi

    eth_data['ema_20'] = eth_ema_20
    eth_data['rsi'] = eth_rsi

    print(btc_data)
    print(eth_data)

    def place_buy_order(symbol, quantity, price):
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=price
        )
        return order

    def place_sell_order(symbol, quantity, price):
        order = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=price
        )
        return order
        # Lancer le trading en temps réel

        # Récupérer les dernières données de prix d'ETH et BTC
        btc_price = get_current_price('BTC-USD')
        eth_price = get_current_price('ETH-USD')

        # Récupérer les dernières données de l'EMA et de la RSI pour BTC et ETH
        btc_ema_20_last = btc_ema_20[-1]
        btc_rsi_last = btc_rsi[-1]

        eth_ema_20_last = eth_ema_20[-1]
        eth_rsi_last = eth_rsi[-1]

        # Déterminer la décision d'achat ou de vente en fonction des signaux EMA et RSI
        if btc_price > btc_ema_20_last and btc_rsi_last < 30:
            place_buy_order('BTC-USD', 0.1)
        elif btc_price < btc_ema_20_last and btc_rsi_last > 70:
            place_sell_order('BTC-USD', 0.1)

        if eth_price > eth_ema_20_last and eth_rsi_last < 30:
            place_buy_order('ETH-USD', 0.1)
        elif eth_price < eth_ema_20_last and eth_rsi_last > 70:
            place_sell_order('ETH-USD', 0.1)

        # Attendre 5 minutes avant de réexécuter la boucle
        time.sleep(300)