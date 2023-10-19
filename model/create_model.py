from datetime import date, timedelta
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.optimizers.legacy import Adam
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers.schedules import ExponentialDecay
tf.random.set_seed(42)

class downloadData:
    def __init__(self, ticker, start):
        self.ticker = ticker
        self.start = start

    def download(self):
        self.data = yf.download(tickers=self.ticker, start=self.start, end=date.today())
        return self.data

class addFeature:
    def __init__(self, data):
        self.data = data

    def addIndicator(self):
        data = self.data
        #data = data.set_index("Date")

        # Adding indicators
        data['RSI'] = ta.rsi(data.Close, length=15)
        data['EMAF'] = ta.ema(data.Close, length=20)
        data['EMAM'] = ta.ema(data.Close, length=100)
        data['EMAS'] = ta.ema(data.Close, length=150)

        data['Target'] = data['Adj Close'] - data.Open
        data['Target'] = data['Target'].shift(-1)

        data['TargetClass'] = data.apply(lambda row: 1 if row['Target'] > 0 else 0, axis=1)

        data['TargetNextClose'] = data['Adj Close'].shift(-1)

        data.dropna(inplace=True)
        data.reset_index(inplace=True)
        data.drop(['Volume', 'Close'], axis=1, inplace=True)

        df = data.filter(['Adj Close'])
        # Convert the dataframe to a numpy array
        dataset = df.values
        # Get the number of rows to train the model on
        training_data_len = int(len(dataset) * 0.80)

        return dataset, training_data_len

class preprocess:
    def split_data(self, dataset, training_data_len, test_data_len):
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        train_data = scaled_data[0:int(training_data_len), :]
        test_data = scaled_data[int(training_data_len) - 60:int(training_data_len) + test_data_len, :]

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])

        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])
            y_test.append(test_data[i, 0])

        # Convert the x_train, y_train, x_test, and y_test to numpy arrays
        x_train, y_train, x_test, y_test = np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

        # Reshape the data
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        return x_train, y_train, x_test, y_test, scaler



class createModel:
    def __init__(self, model=None):
        self.model = model

    def create(self, x_train):
        np.random.seed(10)
        model = Sequential()
        model.add(LSTM(150, input_shape=(x_train.shape[1], 1), return_sequences=True))
        model.add(LSTM(32, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='linear'))
        return model

    def compile(self, x_train, y_train):
        model = self.create(x_train)
        initial_learning_rate = 0.01
        lr_schedule = ExponentialDecay(
                        initial_learning_rate,
                        decay_steps=5,
                        decay_rate=0.8,
                        staircase=True
                    )
        optimizer = Adam(learning_rate=lr_schedule)
        model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mape'])
        return model

    def fitModel(self, x_train, y_train):
        model = self.compile(x_train, y_train)
        early_stopping = EarlyStopping(monitor='loss', patience=3, verbose=1)
        model.fit(x=x_train, y=y_train, batch_size=32, epochs=10, shuffle=False, callbacks=[early_stopping])
        return model


def main():
    gpu = len(tf.config.list_physical_devices('GPU')) > 0
    print("GPU is", "available" if gpu else "NOT AVAILABLE")
    print('System starting..')

    # Veriyi indir
    downData = downloadData('ALGYO.IS', '2020-03-11')
    data = downData.download()

    # Özellikleri ekle
    add_feature = addFeature(data)
    dataset, training_data_len = add_feature.addIndicator()

    test_data_len = len(dataset) - training_data_len 
    prpro = preprocess()
    x_train, y_train, x_test, y_test, scaler = prpro.split_data(dataset, training_data_len, test_data_len)

    create_model = createModel()
    model = create_model.fitModel(x_train, y_train)

    # Gelecekteki 30 günü tahmin et ve grafik olarak çiz
    future_days = 30  # 30 gün tahmin
    last_data = dataset[-60:]  # Son 60 gün verisini alın
    predicted_prices = []

    for _ in range(future_days):
        # Son verileri kullanarak bir sonraki günü tahmin edin
        next_day_input = last_data[-60:].reshape(1, -1, 1)
        next_day_prediction = model.predict(next_day_input)
        predicted_prices.append(next_day_prediction[0, 0])

        # Tahmin edilen fiyatı son verilere ekleyin ve en eski veriyi çıkarın
        last_data = np.append(last_data, next_day_prediction).reshape(-1, 1)
        last_data = last_data[1:]


    last_date = date.today()
    future_dates = [last_date + pd.DateOffset(days=i) for i in range(1, future_days + 1)]

    # Tahmin edilen fiyatları ve tarihleri kullanarak bir grafik çizin
    plt.figure(figsize=(14, 8))
    plt.title('Gelecekteki 30 Günün Fiyat Tahminleri')
    plt.xlabel('Tarih')
    plt.ylabel('Kapanış Fiyatı')
    #plt.plot(data['Adj Close'], label='Gerçek Veriler', color='blue')
    plt.plot(future_dates, predicted_prices, label='Tahminler', color='red')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()