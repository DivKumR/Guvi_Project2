## Refrence documents 
# https://docs.streamlit.io/get-started
# https://docs.streamlit.io/develop/concepts/connections/secrets-management
# https://docs.streamlit.io/develop/concepts/design/custom-classes
"""
Results:
A fully functional dashboard showing the top-performing and worst-performing stocks over the last year.
Insights on the overall market with clear indicators of stock performance trends.
Interactive visualizations using Power BI and Streamlit to make the data easily accessible for users.
"""

import streamlit as st 
import pandas as pd 
import mysql.connector 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
from class_app import SidebarStyler  # type: ignore 

def styled_subheader(text, color="#154734", font_size="20px"):
    st.markdown(f'<h3 style="color:{color}; font-size:{font_size}; font-weight:bold; text-align:center;">{text}</h3>', unsafe_allow_html=True)

# Database Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="dhiviya",  # Replace with your MySQL username
        password="MySQL@25",  # Replace with your MySQL password
        database="Nifty50"
    )
    cursor = conn.cursor()

    # Query to Select data
    query = "SELECT * FROM nifty50_table;"  # Connect to table nifty50_table
    cursor.execute(query)

    Nifty50_all_data = cursor.fetchall()  # Fetch all data
    columns = [col[0] for col in cursor.description]  # Get column names

    # Convert to DataFrame
    Nifty50_all_df = pd.DataFrame(Nifty50_all_data, columns=columns)

except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()

# Copy dataframe for processing
Nifty50_df = Nifty50_all_df.copy()

# Fix: Reference the correct dataframe when transforming date column
Nifty50_df['date'] = pd.to_datetime(Nifty50_df['date'])
Nifty50_df['month'] = Nifty50_df['date'].dt.month
Nifty50_df['year'] = Nifty50_df['date'].dt.year
Nifty50_df['Month-Year'] = Nifty50_df['date'].dt.to_period('M').astype(str)  # Converts to 'YYYY-MM'

# **Market Insights**
styled_subheader("Market Performance Overview",font_size="40px")
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://as1.ftcdn.net/v2/jpg/04/16/06/66/1000_F_416066658_S7JYLCOH8vouR1WDkLQUwPeDPVS9pXc7.jpg" 
             width="5000" height="100">
    </div>
    """, 
    unsafe_allow_html=True
)

# Convert 'close' to numeric and handle errors
Nifty50_df["close"] = pd.to_numeric(Nifty50_df["close"], errors="coerce")

# Drop rows with NaN values after conversion
Nifty50_df = Nifty50_df.dropna(subset=["close"])

# Calculate yearly returns & top/worst stocks
yearly_returns = Nifty50_df.groupby("Ticker")["close"].agg(["mean", "max", "min"]).reset_index()
top_stocks = yearly_returns.nlargest(20, "mean")  # Top 20 performers
worst_stocks = yearly_returns.nsmallest(20, "mean")  # Worst 20 performers

# Get the latest date from the dataset
latest_date = Nifty50_df["date"].max()

# Filter data for the latest date only
latest_data = Nifty50_df[Nifty50_df["date"] == latest_date]

# Function to format ticker display
# Function to format ticker display with correct colors
def format_ticker(row):
    # Convert values to numeric
    open_price = pd.to_numeric(row["open"], errors="coerce")
    close_price = pd.to_numeric(row["close"], errors="coerce")

    # Assign correct icons and colors
    if close_price > open_price:
        trend_icon = "🟢"  # Upward trend
    else:
        trend_icon = "🔻"  # Downward trend

    color_open = "red" if close_price > open_price else "green"
    color_close = "red" if close_price < open_price else "green"

    return (f'<span style="font-size:20px; font-weight:bold;">{row["Ticker"]}: '
            f'<span style="color:{color_open};">{open_price}</span> | '
            f'<span style="color:{color_close};">{close_price} {trend_icon}</span></span>&nbsp;&nbsp;')


# Generate ticker display efficiently
ticker_display = " ".join(latest_data.apply(format_ticker, axis=1))

# Display scrolling ticker with optimized animation
st.markdown(
    f'<marquee behavior="scroll" direction="left">{ticker_display}</marquee>',
    unsafe_allow_html=True
)

# # **Fetch Nifty50 Heatmap from a Reliable Source**
st.markdown(
    """
    <a href="https://portal.tradebrains.in/index/NIFTY/heatmap" target="_blank" style="text-decoration: none;">
        <div style="
            background: linear-gradient(145deg, #ffffff, #d1d1d1);
            border-radius: 10px;
            box-shadow: 5px 5px 10px #b1b1b1, -5px -5px 10px #ffffff;
            padding: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #333;">
            View Live Nifty50 Heatmap (Live Data)
        </div>
    </a>
    """,
    unsafe_allow_html=True
)

# Apply styling to subheaders
styled_subheader("📈 **Top-Performing Stocks**", color="#007acc", font_size="22px")
st.write("")  # Spacing for better layout
fig_top = px.bar(
    top_stocks, 
    x="Ticker", 
    y="mean", 
    title="Best Performing Stocks (Last Year)",
    color="mean",
    color_continuous_scale="Blues"
)
fig_top.update_layout(title_font=dict(size=18, color="#007acc"), xaxis_title_font=dict(size=14, color="#154734"), yaxis_title_font=dict(size=14, color="#154734"))
st.plotly_chart(fig_top)

# Apply styling to worst-performing stocks section
styled_subheader("📉 **Worst-Performing Stocks**", color="#D32F2F", font_size="22px", )

fig_worst = px.bar(
    worst_stocks, 
    x="Ticker", 
    y="mean", 
    title="Worst Performing Stocks (Last Year)",
    color="mean",
    color_continuous_scale="Reds"
)
fig_worst.update_layout(title_font=dict(size=18, color="#D32F2F"), xaxis_title_font=dict(size=14, color="#154734"), yaxis_title_font=dict(size=14, color="#154734"))
st.plotly_chart(fig_worst)


# Sidebar with Clickable Tickers
# Apply sidebar styles
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

# powerbi_url = "https://msit.powerbi.com/groups/me/reports/9505cc0a-0560-43a5-b4a1-013f2c1219ee/ab3e87908c1d040131b3?experience=power-bi"
# st.components.v1.iframe(powerbi_url, width=800, height=600)



# Close the database connection
conn.close()