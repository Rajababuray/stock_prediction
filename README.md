# stock_prediction
### Project Description:

The provided code creates a Streamlit web application for real-time stock analysis and provides a basic buy/sell recommendation based on moving averages. It utilizes data from Yahoo Finance (via `yfinance`) to fetch stock information, generates plots using `plotly`, and conducts time series analysis using `statsmodels`.

### Installation Instructions:

To run this Streamlit app locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Rajababuray/stock_prediction.git
    cd <repository_directory>
    ```

2. **Install Dependencies:**
    Ensure you have Python installed. Create a virtual environment and activate it. Then install the required dependencies:
    ```bash
    pip install streamlit yfinance plotly statsmodels
    ```

3. **Run the Application:**
    Execute the Streamlit app file:
    ```bash
    streamlit run stock_prediction.py
    ```
 
### Usage Information:

- Upon running the application, you'll be prompted to select a country exchange and input a stock ticker symbol for analysis.
- Once a valid stock symbol is entered, the app fetches real-time data, displays company information, market trends, moving averages, and volume analysis.
- It provides a basic buy/sell recommendation based on the relationship between the latest closing price and the moving average.
- Additionally, it showcases a real-time stock price plot, volume analysis, and a time series decomposition plot to visualize trends, seasonality, and residuals in the stock data.
![a2](https://github.com/Rajababuray/stock_prediction/assets/130639226/3ca5e6ef-e0f3-4ab1-9130-4d77009f9dcd)

### Contributors (optional):

- Contributors who have contributed to the codebase or project can be listed here with their respective contributions or roles in the project.
- If there are no specific contributors, this section can be omitted or left empty.
