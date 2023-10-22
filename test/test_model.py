import matplotlib.pyplot as plt
import sys
sys.path.insert(1, '../')
from model.create_model import *
from model.get_code import userArg

user_argv = userArg()
ticker = user_argv.code


def predict_future():
    future_days = 18
    # Veriyi indir
    downData = downloadData(ticker=ticker, start='2020-03-11', end="2023-10-01")
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
    #last_date = date.today()

    # FİX HERE !!!!!!!!!!!!!!!!!!!!!!!!
    last_date = pd.to_datetime("2023-10-01")
    # FİX HERE !!!!!!!!!!!!!!!!!!!!!!!!
    
    future_dates = [last_date + pd.DateOffset(days=i) for i in range(1, future_days + 1)]

    return future_dates, next_day_prediction

def real_vals():
    downData = downloadData(ticker="ALGYO.IS", start="2023-10-01")
    data = downData.download()

    data = data.filter(["Adj Close"])
    return data

def plot_datas():
    future_dates, next_day_prediction = predict_future()
    data = real_vals()

    plt.plot(data, label='Real Values')
    plt.plot(future_dates, next_day_prediction, label='Predicted')
    plt.legend()
    plt.show()

plot_datas()