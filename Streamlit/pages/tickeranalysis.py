
import streamlit as st 
import pandas as pd 
import mysql.connector 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
from app import Nifty50_df # type: ignore
from class_app import SidebarStyler  # type: ignore

# ** Styling Font**
def styled_subheader(text, color="#154734", font_size="20px"):
    st.markdown(f'<h3 style="color:{color}; font-size:{font_size}; font-weight:bold; text-align:center;">{text}</h3>', unsafe_allow_html=True)
styled_subheader("Insights on the overall market precised for Ticker, Month, Year & Heatmap", color="#darkblue")
styled_subheader("Stock Performance Overview | Heatmap Trends ", color="#007acc")  # Different color example
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://as1.ftcdn.net/v2/jpg/04/16/06/66/1000_F_416066658_S7JYLCOH8vouR1WDkLQUwPeDPVS9pXc7.jpg" 
             width="5000" height="100">
    </div>
    """, 
    unsafe_allow_html=True
)

# "Go Back to Main Page" Button
if st.button("Go Back to Main Page"):
    st.switch_page(r"C:\Users\v-dhramaraj\Desktop\Python\Projects\Assignment2_StockAnalysis\.venv\Scripts\app.py")


# ** Stock trend based on the ticker value clicked **
if "selected_ticker" in st.session_state:
    selected_ticker = st.session_state["selected_ticker"]
    st.title(f"{selected_ticker} Stock Trend Analysis")

 # Filter Data
    ticker_data = Nifty50_df[Nifty50_df["Ticker"] == selected_ticker]

 # Ensure 'Close' is numeric
    ticker_data["close"] = pd.to_numeric(ticker_data["close"], errors="coerce")
    ticker_data = ticker_data.dropna(subset=["close"])

 # **Bar Chart - Monthly Trends**
    monthly_trends = ticker_data.groupby("Month-Year")["close"].mean().reset_index()

    fig_bar = px.bar(monthly_trends, x="Month-Year", y="close",
                     title=f"{selected_ticker} Monthly Trends",
                     labels={"Month-Year": "Month-Year", "close": "Average Close Price"})

    st.plotly_chart(fig_bar)

 # **Heatmap - Date vs Ticker Performance**
    pivot_table = Nifty50_df.pivot_table(values="close", index="date", columns="Ticker")
    fig_heatmap = px.imshow(pivot_table,
                            color_continuous_scale="Viridis",
                            title="Stock Performance Heatmap")

    st.plotly_chart(fig_heatmap)

# Filter data based on selected Year & Month
styled_subheader("Reterive Monthly & Yearly Returns Dynamically", color="#007acc")

# Filters for Year and Month Selection
selected_year = st.selectbox("Select Year:", Nifty50_df["year"].unique())
selected_month = st.selectbox("Select Month:", Nifty50_df["month"].unique())


filtered_data = Nifty50_df[(Nifty50_df["year"] == selected_year) & 
                           (Nifty50_df["month"] == selected_month)]

# Ensure 'open' and 'close' columns are numeric
filtered_data["open"] = pd.to_numeric(filtered_data["open"], errors="coerce")
filtered_data["close"] = pd.to_numeric(filtered_data["close"], errors="coerce")


# Compute Monthly & Yearly Returns Dynamically
filtered_data["monthly_return"] = ((filtered_data["close"] - filtered_data["open"]) / filtered_data["open"])
yearly_returns = filtered_data.groupby("Ticker")["monthly_return"].agg(["mean", "max", "min"]).reset_index()

# Ensure dataframe isn't empty before processing
if not yearly_returns.empty:
    # Top 20 Performers & Worst 20 Stocks (Based on Selected Month & Year)
    top_stocks = yearly_returns.nlargest(20, "mean")
    worst_stocks = yearly_returns.nsmallest(20, "mean")

    # Display Updated Charts
    st.subheader(f"Top-Performing Stocks ({selected_month}-{selected_year})")
    fig_top = px.bar(top_stocks, x="Ticker", y="mean", title="Best Performing Stocks")
    st.plotly_chart(fig_top)

    st.subheader(f"Worst-Performing Stocks ({selected_month}-{selected_year})")
    fig_worst = px.bar(worst_stocks, x="Ticker", y="mean", title="Worst Performing Stocks")
    st.plotly_chart(fig_worst)
else:
    st.warning(f"No data available for {selected_month}-{selected_year}.")

# Sidebar with Clickable Tickers
SidebarStyler.apply_sidebar_styles()
# Initialize session state if not set
if "selected_ticker" not in st.session_state:
    st.session_state["selected_ticker"] = None

# Display available tickers as buttons
selected_ticker = None
for ticker in Nifty50_df['Ticker'].unique():
    if st.sidebar.button(ticker):  # Clicking a ticker updates session state
        st.session_state["selected_ticker"] = ticker
        selected_ticker = ticker  # Assign for immediate use
        st.switch_page(r"C:\Users\v-dhramaraj\Desktop\Python\Projects\Assignment2_StockAnalysis\.venv\Scripts\pages\tickeranalysis.py")
