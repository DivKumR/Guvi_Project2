# Stock Performance Dashboard
****Stock Performance Dashboard - Assignment 2**
Project Description**
A detailed project description can be found here: https://docs.google.com/document/d/1AYMyK5XXRNyrIoimt4zjSEvVyaMQPXCNnOPwVsgo2IA/edit?tab=t.0#heading=h.dg45ga16ik17

**Summary**

This project focuses on analyzing and visualizing Nifty 50 stock performance over the past year using Python, Streamlit, Power BI, and SQL databases. The workflow includes data extraction, cleaning, transformation, and interactive dashboard creation to help investors and analysts make informed decisions.


**Data Extraction & Transformation**

Method:

- Extracted stock data from YAML files, structured by month and date.
- Transformed the extracted data into CSV format, organizing it by ticker symbols.
  
Output:
- Generated 50 CSV files, each corresponding to a stock symbol for data visulisation and streamlined processing.

**Data Cleaning & Storage**

Process:
- Consolidated multiple CSV datasets into a single structured DataFrame.
- Handled missing values, removed duplicates, and converted stock metrics into a standardized format.
  
Database Integration:
- Stored the cleaned data in a MySQL database for efficient querying.
  Example Code:
insert_query = "INSERT INTO stock_data (ticker, open_price, close_price, volume) VALUES (%s, %s, %s, %s)"
cursor.executemany(insert_query, stock_values)
conn.commit()

**Data Analysis & Visualization Requirements**

1️⃣ Market Overview & Stock Ranking

✅ Identified the top 10 best-performing and top 10 worst-performing stocks based on yearly returns.

✅ Calculated overall percentage of green vs red stocks for market summary insights.

✅ Provided average stock price & trading volume trends.

2️⃣ Volatility Analysis

✔ Measured price fluctuations using standard deviation of daily returns.

✔ Visualized top 10 most volatile stocks using a bar chart representation.

3️⃣ Cumulative Stock Return Trends

🎯 Computed cumulative returns from start to end of the year to assess growth.
🎯 Plotted a line chart tracking stock trends over time.

4️⃣ Sector-Wise Performance

📊 Mapped stocks to industry sectors (e.g., IT, Financials, Energy) for comparative analysis.

📊 Generated bar charts showing average returns per sector.

5️⃣ Stock Price Correlation

🔍 Created a correlation matrix to understand relationships between stock prices.

🔍 Designed a heatmap visualization to highlight strong correlations.

6️⃣ Monthly Gainers & Losers

📅 Tracked top 5 gainers & top 5 losers for each month, visualizing monthly trends.

Technologies Used
🔹 Languages: Python
🔹 Database: MySQL
🔹 Visualization Tools: Streamlit, Power BI, Plotly
🔹 Libraries: Pandas, Matplotlib, SQLAlchemy,saeborn

Deployment
-- Run the project using app.py, located in the Streamlit folder under the Streamlit directory.
-- Ensure the environment is activated before execution.
Example Code: 
Activate the Virtual Environment: In the terminal, run: .\env\Scripts\activate
python -m pip install streamlit
streamlit run app.py

References
- Streamlit API Reference → Streamlit Docs
- Power BI Documentation → Available internally
- GitHub Guide → How to Use GitHub.pptx

Attached Files & Folders

📂 Jupyter Notebooks:

- data_extraction.ipynb → Extracting stock data
- data_cleaning.ipynb → Cleaning and transforming data
- visualization.ipynb → Exploratory stock performance analysis
  
📂 Streamlit Application:

- app.py → Main dashboard script
- tickeranalysis → Subpage 
- class.py → Component & style definitions
  
📂 Data Storage:
- Stock_Data_CSVs/ → Folder containing collected stock CSV files
- MySQL database for stock metrics
  
📂 Documentation:
- Results.pdf → Screenshots showcasing the dashboard and analysis results


