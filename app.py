import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Page Configuration
st.set_page_config(page_title="AI Market Intelligence", layout="wide")

st.title("📊 Advanced AI Market Intelligence Tool")
st.markdown("---")

# Sidebar for User Inputs
st.sidebar.header("Asset Selection")
asset_ticker = st.sidebar.text_input("Enter Ticker (e.g., BTC-USD, NVDA, TSLA)", "BTC-USD").upper()
history_range = st.sidebar.selectbox("Select History Period", ['1y', '2y', '5y'], index=1)

if st.sidebar.button("Run AI Forecast"):
    try:
        # Data Acquisition
        with st.spinner(f"Fetching live data for {asset_ticker}..."):
            df = yf.download(asset_ticker, period=history_range, interval='1d')
        
        if df.empty:
            st.error("Invalid ticker or no data found. Please try again.")
        else:
            # Feature Engineering
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_30'] = df['Close'].rolling(window=30).mean()
            
            # RSI Calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df = df.dropna()

            # AI Training (Random Forest)
            X = df[['SMA_10', 'SMA_30', 'RSI']]
            y = df['Close']
            
            model = RandomForestRegressor(n_estimators=200, random_state=42)
            model.fit(X.values, y.values.ravel())

            # Prediction for the next session
            latest_feat = [[float(df['SMA_10'].iloc[-1]), float(df['SMA_30'].iloc[-1]), float(df['RSI'].iloc[-1])]]
            prediction = model.predict(latest_feat)[0]

            # Results Display
            current_price = float(df['Close'].iloc[-1])
            change = ((prediction - current_price) / current_price) * 100

            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${current_price:,.2f}")
            col2.metric("AI Predicted Price", f"${prediction:,.2f}", f"{change:+.2f}%")
            col3.metric("RSI Status", f"{df['RSI'].iloc[-1]:.2f}")

            # Visualization
            st.subheader(f"Price Trend & Technical Indicators: {asset_ticker}")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df.index[-120:], df['Close'][-120:], label='Market Price', color='#2c3e50', linewidth=2)
            ax.plot(df.index[-120:], df['SMA_10'][-120:], label='Short Trend (10d)', linestyle='--')
            ax.set_ylabel("Price (USD)")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Page Configuration
st.set_page_config(page_title="AI Market Intelligence", layout="wide")

st.title("📊 Advanced AI Market Intelligence Tool")
st.markdown("---")

# Sidebar for User Inputs
st.sidebar.header("Asset Selection")
asset_ticker = st.sidebar.text_input("Enter Ticker (e.g., BTC-USD, NVDA, TSLA)", "BTC-USD").upper()
history_range = st.sidebar.selectbox("Select History Period", ['1y', '2y', '5y'], index=1)

if st.sidebar.button("Run AI Forecast"):
    try:
        # Data Acquisition
        with st.spinner(f"Fetching live data for {asset_ticker}..."):
            df = yf.download(asset_ticker, period=history_range, interval='1d')
        
        if df.empty:
            st.error("Invalid ticker or no data found. Please try again.")
        else:
            # Feature Engineering
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_30'] = df['Close'].rolling(window=30).mean()
            
            # RSI Calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df = df.dropna()

            # AI Training (Random Forest)
            X = df[['SMA_10', 'SMA_30', 'RSI']]
            y = df['Close']
            
            model = RandomForestRegressor(n_estimators=200, random_state=42)
            model.fit(X.values, y.values.ravel())

            # Prediction for the next session
            latest_feat = [[float(df['SMA_10'].iloc[-1]), float(df['SMA_30'].iloc[-1]), float(df['RSI'].iloc[-1])]]
            prediction = model.predict(latest_feat)[0]

            # Results Display
            current_price = float(df['Close'].iloc[-1])
            change = ((prediction - current_price) / current_price) * 100

            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${current_price:,.2f}")
            col2.metric("AI Predicted Price", f"${prediction:,.2f}", f"{change:+.2f}%")
            col3.metric("RSI Status", f"{df['RSI'].iloc[-1]:.2f}")

            # Visualization
            st.subheader(f"Price Trend & Technical Indicators: {asset_ticker}")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df.index[-120:], df['Close'][-120:], label='Market Price', color='#2c3e50', linewidth=2)
            ax.plot(df.index[-120:], df['SMA_10'][-120:], label='Short Trend (10d)', linestyle='--')
            ax.set_ylabel("Price (USD)")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
