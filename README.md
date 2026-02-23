# 📈 Advanced AI Market Intelligence Tool

An end-to-end Machine Learning application built to predict financial market trends (Stocks & Cryptocurrencies) using real-time data and predictive modeling.

## 🔗 Live Demo
Check out the live app here: [https://ai-market-predictor-mykrsc6zw8qtmnvcdmjqjn.streamlit.app/](https://ai-market-predictor-mykrsc6zw8qtmnvcdmjqjn.streamlit.app/)

## 🚀 Project Overview
This tool leverages **Machine Learning** and **Quantitative Analysis** to provide insights into market movements. It fetches live data via Yahoo Finance, calculates technical indicators, and uses a regression model to forecast the next day's price.

### Key Features:
* **Live Data Integration:** Real-time fetching of market data using `yfinance`.
* **Technical Analysis:** Implemented **Simple Moving Averages (SMA 10, SMA 30)** and **Relative Strength Index (RSI)** to measure market momentum.
* **Predictive AI:** Powered by **Random Forest Regressor** to analyze historical patterns and predict future prices.
* **Accuracy Metrics:** Real-time evaluation using **Mean Absolute Error (MAE)**.
* **Interactive Visualization:** Dynamic charts built with `Matplotlib` to visualize trends over time.



## 🛠️ Tech Stack
* **Language:** Python 3.12
* **ML Library:** Scikit-learn (Random Forest)
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **API:** Yahoo Finance (yfinance)
* **Visualization:** Matplotlib

## 🧠 The Logic
The model follows a standard data science pipeline:
1. **Data Acquisition:** Fetching up to 5 years of historical data.
2. **Feature Engineering:** Generating technical indicators as input features ($X$).
3. **Training:** Splitting data into 80% Training and 20% Testing sets.
4. **Inference:** Predicting the closing price based on the latest market momentum ($RSI$) and trends ($SMA$).



---
Developed by **Rukshan Weerasekara** *Creative Technologist | Animator | AI Developer*
