import matplotlib
matplotlib.use('Agg')

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM

app = Flask(__name__)
CORS(app)

companies = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc. (Google)',
    'AMZN': 'Amazon.com Inc.',
    'META': 'Meta Platforms Inc. (Facebook)'
}

def prepare_data(data, time_step):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        a = data[i:(i + time_step), 0]
        X.append(a)
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    date_str = data.get('date')
    company = data.get('company', 'AAPL')
    
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    start_date = date_obj - datetime.timedelta(days=365)
    end_date = date_obj
    ticker = company
    
    df = yf.download(ticker, start=start_date, end=end_date)
    
    if df.empty:
        return jsonify({'error': 'No data available for the specified date range and company'}), 400
    
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    
    time_step = 100
    X, Y = prepare_data(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, Y, batch_size=1, epochs=1)
    
    # Predicting up to the selected date
    predicted_prices = []
    for i in range(len(df) - time_step):
        X_test = scaled_data[i:i+time_step]
        X_test = X_test.reshape(1, time_step, 1)
        predicted_price = model.predict(X_test)
        predicted_prices.append(predicted_price[0][0])
    
    predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))

    # Plot historical prices and predicted prices
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'][time_step:], df['Close'][time_step:], label='Historical Close Price')
    plt.plot(df['Date'][time_step:], predicted_prices, label='Predicted Close Price')
    plt.title(f'{companies[company]} Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    
    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return jsonify({
        'prediction': float(predicted_prices[-1].item()),  # Extract the scalar and convert to float for JSON serialization
        'plot': f'/plot?company={company}&date={date_str}'
    })

@app.route('/plot', methods=['GET'])
def plot():
    company = request.args.get('company', 'AAPL')
    date_str = request.args.get('date')

    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    start_date = date_obj - datetime.timedelta(days=365)
    end_date = date_obj
    ticker = company

    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        return jsonify({'error': 'No data available for the specified date range and company'}), 400

    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

    time_step = 100
    X, Y = prepare_data(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, Y, batch_size=1, epochs=1)

    predicted_prices = []
    for i in range(len(df) - time_step):
        X_test = scaled_data[i:i + time_step]
        X_test = X_test.reshape(1, time_step, 1)
        predicted_price = model.predict(X_test)
        predicted_prices.append(predicted_price[0][0])

    predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))

    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'][time_step:], df['Close'][time_step:], label='Historical Close Price')
    plt.plot(df['Date'][time_step:], predicted_prices, label='Predicted Close Price')
    plt.title(f'{companies[company]} Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
