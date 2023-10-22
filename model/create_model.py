from datetime import date
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.optimizers.legacy import Adam
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers.schedules import ExponentialDecay
import matplotlib.pyplot as plt

# Veriyi indirme sınıfı
class downloadData:
    def __init__(self, ticker, start, end=date.today()):
        self.ticker = ticker
        self.start = start
        self.end = end

    def download(self):
        self.data = yf.download(tickers=self.ticker, start=self.start, end=self.end)
        return self.data

# Özellik eklemek için sınıf
class addFeature:
    def __init__(self, data):
        self.data = data

    def addIndicator(self):
        data = self.data

        # Özelliklerin eklenmesi
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
        dataset = df.values
        training_data_len = int(len(dataset) * 0.80)

        return dataset, training_data_len

# Veriyi ön işlemek için sınıf
class preprocess:
    def split_data(self, dataset, training_data_len, test_data_len):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        try:
            scaled_data = self.scaler.fit_transform(dataset)
            
        except:
            print('Check you internet connection')
            # Hata durumunda işlemi durdurabilir veya başka bir işlem uygulayabilirsiniz.
            # return None, None, None, None

        train_data = scaled_data[0:int(training_data_len), :]
        test_data = scaled_data[int(training_data_len) - 60:int(training_data_len) + test_data_len, :]

        x_train, y_train, x_test, y_test = [], [], [], []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])

        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])
            y_test.append(test_data[i, 0])

        x_train, y_train, x_test, y_test = np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        return x_train, y_train, x_test, y_test

    def inverse_transform(self, data):
        # Veriyi ölçeklendirmeyi tersine çevir
        return self.scaler.inverse_transform(data)

# Modeli oluşturmak için sınıf
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
#        checkpoint = ModelCheckpoint('/tmp/best_model.keras', 
#                                      save_weights_only=False, # Save all the model if false, else only saves the weights
#                                      monitor='mape',
#                                      mode='min',
#                                      save_best_only=True)

        model.fit(x=x_train, y=y_train, batch_size=32, epochs=10, shuffle=False, callbacks=[early_stopping])
        return model

# Gelecekteki fiyatları tahmin etmek için sınıf
class FuturePricePredictor:
    def __init__(self, model, dataset):
        self.model = model
        self.dataset = dataset

    def predict_future_prices(self, future_days):
        last_data = self.dataset[-60:]  # Son 60 gün verisini alın
        predicted_prices = []

        for _ in range(future_days):
            next_day_input = last_data[-60:].reshape(1, -1, 1)
            next_day_predictions = []

            for _ in range(10):
                next_day_prediction = self.model.predict(next_day_input)
                next_day_predictions.append(next_day_prediction[0, 0])

            average_prediction = np.mean(next_day_predictions)
            predicted_prices.append(average_prediction)

            last_data = np.append(last_data, average_prediction).reshape(-1, 1)
            last_data = last_data[1:]

        return predicted_prices


# Monte Carlo simulasyonu sınıfı
class MonteCarlo:
    def __init__(self, next_day_prediction, future_days):
        self.next_day_prediction = next_day_prediction
        self.future_days = future_days

    def calculate_monte_carlo(self):
        num_simulations = 1000
        predicted_prices = []

        for _ in range(num_simulations):
            last_data = np.copy(self.next_day_prediction)
            simulation_prices = []

            for _ in range(self.future_days):
                mean = last_data
                std_dev = np.std(self.next_day_prediction)
                adjusted_price = np.random.normal(mean, std_dev)
                simulation_prices.append(adjusted_price)
                last_data = adjusted_price

            predicted_prices.append(simulation_prices)

        return predicted_prices

def main():
    future_days = 7

    gpu = len(tf.config.list_physical_devices('GPU')) > 0
    print("GPU is", "available" if gpu else "NOT AVAILABLE")
    print('System starting..')

    # Veriyi indir
    downData = downloadData('THYAO.IS', '2020-03-11')
    data = downData.download()

    # Özellikleri ekle
    add_feature = addFeature(data)
    dataset, training_data_len = add_feature.addIndicator()

    test_data_len = len(dataset) - training_data_len
    prpro = preprocess()
    x_train, y_train, x_test, y_test = prpro.split_data(dataset, training_data_len, test_data_len)

    create_model = createModel()
    model = create_model.fitModel(x_train, y_train)

    # Gelecekteki 30 günü tahmin et
    
    predictor = FuturePricePredictor(model, dataset)
    next_day_prediction = predictor.predict_future_prices(future_days)
    next_day_prediction = np.array(next_day_prediction).reshape(-1, 1)
    next_day_prediction = prpro.inverse_transform(next_day_prediction)
    # Tahmin edilen fiyatları ve tarihleri kullanarak bir grafik çizin
    last_date = date.today()
    future_dates = [last_date + pd.DateOffset(days=i) for i in range(1, future_days + 1)]

    # Monte Carlo simulasyonu
    monte_carlo = MonteCarlo(next_day_prediction, future_days)
    mc_results = monte_carlo.calculate_monte_carlo()

    #Monte Carlo sonuçlarını tersine çevir ve yazdır
    print("Monte Carlo Results:")
    #tests = {}  # Döngünün dışında bir kez tanımlanmalıdır
    for i in range(5):
        result = np.array(mc_results[i])
        inverted_result = prpro.inverse_transform(result.reshape(-1, 1))

        print(f"Simulation {i + 1} Min Price: {inverted_result.flatten().min()}")
        print(f"Simulation {i + 1} Avg Price: {inverted_result.flatten().mean()}")
        print(f"Simulation {i + 1} Max Price: {inverted_result.flatten().max()}")
        print('-' * 100)

    # Şimdi grafiği çizin
    plt.figure(figsize=(14, 8))
    plt.title('Gelecekteki 30 Günün Fiyat Tahminleri')
    plt.xlabel('Tarih')
    plt.ylabel('Kapanış Fiyatı')
    # colors = ['orange', 'purple', 'cyan', 'red']
    # for i in range(5):
    #     plt.plot(future_dates, tests[f'Test {i}'][:30], label=f'Test {i}', color='blue')
    #     plt.plot(future_dates, tests[f'Test {i} Moving Average'][:30], label=f'Test {i} Moving Average', color='green')

    plt.plot(future_dates, next_day_prediction, label='Tahminler', color='red')
    plt.legend()
    plt.show()

    

if __name__ == "__main__":
    main()
