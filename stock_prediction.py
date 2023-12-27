import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import statsmodels.api as sm

def calculate_moving_average(data, window=20):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    return data


def perform_time_series_analysis(stock_data):
    decomposition = sm.tsa.seasonal_decompose(stock_data['Close'], model='additive', period=30)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    fig_decomposition = go.Figure()
    fig_decomposition.add_trace(go.Scatter(x=stock_data.index, y=trend, mode='lines', name='Trend'))
    fig_decomposition.add_trace(go.Scatter(x=stock_data.index, y=seasonal, mode='lines', name='Seasonal'))
    fig_decomposition.add_trace(go.Scatter(x=stock_data.index, y=residual, mode='lines', name='Residual'))

    fig_decomposition.update_layout(title='Time Series Decomposition',
                                    xaxis_title='Time',
                                    yaxis_title='Value',
                                    xaxis_rangeslider_visible=False)

    return fig_decomposition


# Set the title and description of the app
st.title('Real-Time Stock Analysis & Trading Recommendation')
st.write("Enter the stock ticker symbol and select the country exchange to get real-time analysis and a basic buy/sell recommendation.")

# Select country exchange
country_exchange = st.selectbox(
    "Select Country Exchange:",
    ["India", "USA", "Nepal", "UK", "Australia"]
)

if country_exchange:
    exchange_suffix = {
        "India": ".NS",
        "USA": "",
        "Nepal": ".NP",
        "UK": ".L",
        "Australia": ".AX"
    }.get(country_exchange, "")

    stock_symbol = st.text_input(f"Enter Stock Ticker Symbol for {country_exchange}:")

    if stock_symbol:
        try:
            stock_data = yf.download(stock_symbol + exchange_suffix, period="1y", interval="1d")

            if not stock_data.empty:

                window_size = 20
                stock_data = calculate_moving_average(stock_data, window=window_size)

                stock_info = yf.Ticker(stock_symbol + exchange_suffix).info
                st.subheader(f"Company Information: {stock_info['longName']} ({stock_symbol + exchange_suffix})")
                st.write(f"Industry: {stock_info['industry']}")
                st.write(f"Market Cap: ${stock_info['marketCap']:,}")
                st.write(f"Current Price: ${stock_data['Close'][-1]:,.2f}")

                # Determine Buy/Sell signal based on moving averages
                latest_close_price = stock_data['Close'][-1]
                latest_sma = stock_data['SMA'][-1]
                if latest_close_price > latest_sma:
                    st.write("Recommendation: **Buy**")
                else:
                    st.write("Recommendation: **Sell**")

                # Real-Time Stock Price Plot
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=stock_data.index,
                                             open=stock_data['Open'],
                                             high=stock_data['High'],
                                             low=stock_data['Low'],
                                             close=stock_data['Close'],
                                             name="Candlestick"))

                fig.add_trace(
                    go.Scatter(x=stock_data.index, y=stock_data['SMA'], name="Moving Average", line=dict(color='blue')))
                fig.update_layout(title=f"{stock_symbol} Stock Analysis",
                                  xaxis_title='Time',
                                  yaxis_title='Stock Price ($)',
                                  xaxis_rangeslider_visible=False)

                st.subheader('Real-Time Stock Price Plot')
                st.plotly_chart(fig, use_container_width=True)

                # Volume Analysis
                fig_volume = go.Figure()
                fig_volume.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name="Volume"))
                fig_volume.update_layout(title=f"{stock_symbol} Volume Analysis",
                                         xaxis_title='Time',
                                         yaxis_title='Volume',
                                         xaxis_rangeslider_visible=False)
                st.subheader('Volume Analysis')
                st.plotly_chart(fig_volume, use_container_width=True)

                # Time Series Decomposition
                st.subheader('Time Series Decomposition')
                fig_decomposition = perform_time_series_analysis(stock_data)
                st.plotly_chart(fig_decomposition, use_container_width=True)

            else:
                st.warning("No data found for the given stock symbol. Please enter a valid symbol.")
        except Exception as e:
            st.warning(f"Error: {e}")
