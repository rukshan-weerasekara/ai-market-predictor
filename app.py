import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import numpy as np

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Market Intelligence", layout="wide")

st.title("📈 Advanced AI Market Intelligence Tool")
st.markdown(f"**Developed by Rukshan Weerasekara** | Creative Technologist")
st.markdown("---")

# --- 2. Sidebar for User Inputs ---
st.sidebar.header("Model Configuration")
asset_ticker = st.sidebar.text_input("Enter Ticker (e.g., BTC-USD, TSLA, NVDA):", "BTC-USD").upper()
time_period = st.sidebar.selectbox("Historical Data Period:", ['1y', '2y', '5y'], index=1)

if st.sidebar.button("Generate AI Forecast"):
    try:
        # --- 3. Data Acquisition ---
        with st.spinner(f"Fetching live data for {asset_ticker}..."):
            df = yf.download(asset_ticker, period=time_period, interval='1d')

        if df.empty:
            st.error("Invalid ticker or no data found. Please check the symbol.")
        else:
            # --- 4. Feature Engineering (Technical Indicators) ---
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_30'] = df['Close'].rolling(window=30).mean()

            # Calculating RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            df = df.dropna()

            # Define Features (X) and Target (y)
            X = df[['SMA_10', 'SMA_30', 'RSI']]
            y = df['Close']

            # --- 5. Model Training (Random Forest) ---
            split = int(0.8 * len(df))
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            model = RandomForestRegressor(n_estimators=200, random_state=42)
            model.fit(X_train.values, y_train.values.ravel())

            # --- 6. Prediction & Evaluation ---
            predictions = model.predict(X_test.values)
            mae = mean_absolute_error(y_test, predictions)

            # Predict NEXT day's price
            latest_data = [[float(df['SMA_10'].iloc[-1]), float(df['SMA_30'].iloc[-1]), float(df['RSI'].iloc[-1])]]
            next_day_prediction = model.predict(latest_data)[0]

            # --- 7. Professional UI Output ---
            current_price = float(df['Close'].iloc[-1])
            predicted_val = float(next_day_prediction)
            change_pct = ((predicted_val - current_price) / current_price) * 100

            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"${current_price:,.2f}")
            col2.metric("AI Predicted Price", f"${predicted_val:,.2f}", f"{change_pct:+.2f}%")
            col3.metric("Model Error (MAE)", f"${mae:,.2f}")
            col4.metric("RSI (Momentum)", f"{df['RSI'].iloc[-1]:.2f}")

            st.markdown("---")

            # --- 8. Visualization ---
            st.subheader(f"Price Analysis & AI Forecast: {asset_ticker}")
            fig, ax = plt.subplots(figsize=(15, 7))
            
            # Plotting last 120 days for clarity
            plot_df = df.tail(120)
            ax.plot(plot_df.index, plot_df['Close'], label='Actual Market Price', color='#2c3e50', linewidth=2)
            ax.plot(plot_df.index, plot_df['SMA_10'], label='10-Day Trend', color='#e67e22', linestyle='--')
            
            ax.set_ylabel('Price (USD)')
            ax.legend()
            ax.grid(True, alpha=0.2)
            
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Status Error: {e}")
