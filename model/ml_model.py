import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, ElasticNet
from sklearn.preprocessing import MinMaxScaler
from create_model import downloadData, addFeature, preprocess
from get_code import userArg
from create_model import downloadData
import talib as ta


#    Example of usage: 
#                    python ml_model.py NFLX
#                    python3 ml_model.py NFLX


user_arg = userArg()
download = downloadData(user_arg.code, '2020-03-11', end='2023-10-25')
data = download.download()

def addIndicator(data):
    #RSI
    data["RSI5"] = ta.RSI(data["Close"], 5)
    data["RSI10"] = ta.RSI(data["Close"], 10)
    data["RSI20"] = ta.RSI(data["Close"], 13)

    #MACD
    #Hızlı, Yavaş, Sinyal periyotları
    #12, 26 ve 9: Bu ayarlar, MACD'yi daha hızlı tepki vermesini ve trend değişikliklerini daha doğru bir şekilde belirlemesini sağlar.
    #10, 30 ve 10: Bu ayarlar, MACD'yi daha az gürültülü hale getirmeye yardımcı olur.
    #15, 30 ve 15: Bu ayarlar, MACD'yi daha doğru sinyaller üretmeye yardımcı olur.

    #data["MACD"] = ta.MACD(data["Close"], 12, 26, 9)
    data["Upper"], data["Middle"], data["Lower"] = ta.BBANDS(data['Close'], timeperiod=12, nbdevup=3, nbdevdn=3, matype=0)

    #EMA
    #Kısa vadeli yatırımlar için: 5, 10 veya 20 günlük EMA'lar
    #Uzun vadeli yatırımlar için: 50, 100 veya 200 günlük EMA'lar
    data["EMA"] = ta.EMA(data["Close"], 5)
    data["EMA"] = ta.EMA(data["Close"], 10)
    data["EMA"] = ta.EMA(data["Close"], 20)

    data["Upper"], data["Middle"], data["Lower"] = ta.BBANDS(data["Close"])

    data.drop("Adj Close", axis=1, inplace=True)
    data.dropna(inplace=True)

    print("Necessary Indicators added")

    return data

def createModel(df):
    global scaler
    X = data.drop("Close", axis=1)
    y = data["Close"]

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(scaled, y, test_size=0.2)

    lasso = Lasso()
    elastic = ElasticNet()

    lasso.fit(X_train, y_train)
    elastic.fit(X_train, y_train)
    print("Lasso and ElasticNet Training Completed")

    return lasso, elastic

def makePrediction(df, futureDays):
    """Predicts future prices using the trained model.

    Args:
        futureDays: The number of days in the future to predict prices for.

    Returns:
        A list of predicted prices for the next `futureDays` days.
    """
    # Get the last `futureDays` days of the data.
    X_future = df[-futureDays:]
    X_future = X_future.drop("Close", axis=1)
    # Scale the data using the same scaler that was used to train the model.
    scaled_future = scaler.transform(X_future)

    # Make predictions using the trained model.
    lasso_predictions = lasso.predict(scaled_future)
    elastic_predictions = elasticNet.predict(scaled_future)

    # Return the predictions.
    print("Predictions completed")
    predictions = pd.DataFrame({
    "Date": df.index[-futureDays:],
    "Lasso": lasso_predictions,
    "ElasticNet": elastic_predictions
    })

    # Print the DataFrame.
    print(predictions)
    plt.plot(predictions["Lasso"])
    plt.show()
    #return lasso_predictions, elastic_predictions

if __name__ == "__main__":
    df = addIndicator(data)
    lasso, elasticNet = createModel(df)
    #lassoPrediction, elasticPrediction = makePrediction(df, 14)
    makePrediction(df, 10)

