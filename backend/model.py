# backend/model.py
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import ta
import numpy as np

def train_model():
    # Download historical stock data
    ticker = 'AAPL'
    start_date = '2010-01-01'
    end_date = '2020-12-31'
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # Ensure the Date column is present and reset the index to use Date as a column
    df.reset_index(inplace=True)

    # Feature engineering
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # Technical Indicators
    df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    df['Volume'] = df['Volume']  # include trading volume as a feature

    # Drop rows with NaN values (from SMA and RSI calculations)
    df.dropna(inplace=True)
    
    # Use Day, Month, Year, and technical indicators as features and Close price as the target variable
    X = df[['Day', 'Month', 'Year', 'SMA_20', 'SMA_50', 'RSI', 'Volume']]
    y = df['Close']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 10],
        'min_samples_split': [2, 5, 10]
    }
    model = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    # Best model from GridSearchCV
    best_model = grid_search.best_estimator_

    # Save the scaler and the model to a file
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(best_model, 'model.pkl')

if __name__ == '__main__':
    train_model()
