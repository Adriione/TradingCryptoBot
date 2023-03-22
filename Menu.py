import Algo
import main
while True:
    print("Menu:")
    print("1 - Bot Forecast par Machine Learning")
    print("2 - Bot Indicateurs d'Opportunité")
    print("0 - Quitter")

    choice = input("Entrez votre choix : ")

    if choice == "1":
        main.fonction1().run()
    elif choice == "2":
        Algo.fonction2().run()
    elif choice == "0":
        break
    else:
        print("Choix invalide. Veuillez choisir à nouveau.")

'''import QuantConnect
import tensorflow as tf
import numpy as np
import pandas as pd
from binance.client import Client

# Configurez votre clé API et votre secret API pour la plateforme de trading Binance
key = 'votre_clé_API'
secret = 'votre_secret_API'

# Configurez votre stratégie de trading en Deep Learning ici
class StockPredictionStrategy(QCAlgorithm):

    def Initialize(self):
        self.api_key = 'votre_clé_API_binance'
        self.api_secret = 'votre_secret_API_binance'
        self.client = Client(self.api_key, self.api_secret)
        self.symbol = "ETHUSDT"
        self.market = tf.keras.models.load_model("D:\dts papier\modeleETH.h5")

    def OnData(self, data):
        # Obtenez les informations sur le marché actuel
        market_data = self.client.get_historical_klines(self.symbol, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")
        market_data = np.array(market_data)
        market_data = market_data[:, 1:5].astype(float)
        market_data = pd.DataFrame(data=market_data, columns=["open", "high", "low", "close"])
        market_data = market_data.iloc[::-1]
        market_data = market_data.reset_index(drop=True)

        # Préparez les données de marché pour l'entrée du modèle
        market_data = np.array(market_data).reshape(1, 96, 4)

        # Utilisez votre stra1
        tégie de trading basée sur l'apprentissage automatique pour décider quoi faire
        predicted_price = self.market.predict(market_data)
        current_price = self.client.get_ticker(symbol=self.symbol)['lastPrice']
        action = "buy" if predicted_price > current_price else "sell"

        # Si votre stratégie recommande un achat, passez un ordre d'achat
        if action == 'buy':
            quantity = 0.01
            price = self.client.get_ticker(symbol=self.symbol)['lastPrice']
            order = self.client.create_order(
                symbol=self.symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity)

        # Si votre stratégie recommande une vente, passez un ordre de vente
        elif action == 'sell':
            quantity = 0.01
            price = self.client.get_ticker(symbol=self.symbol)['lastPrice']
            order = self.client.create_order(
                symbol=self.symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity)

# Connectez-vous à la plateforme de trading Binance en utilisant Lean
engine = QuantConnect.Lean.Engine(
   'BinanceBrokerage',
   key,
   secret,
   'https://api.binance.com',
   'ethusdt',
   'live',
   log_level='debug')

# Configurez et exécutez votre stratégie de trading
strategy = StockPredictionStrategy(engine)
lean.run(strategy)'''