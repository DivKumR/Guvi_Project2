## Refrence documents 
# https://docs.streamlit.io/develop/concepts/design/custom-classes

import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns




class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.Nifty50_all_df = None

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="dhiviya",  # Replace with your MySQL username
                password="MySQL@25",  # Replace with your MySQL password
                database="Nifty50"
            )
            self.cursor = self.conn.cursor()

            # Query to Select data
            query = "SELECT * FROM nifty50_table;"  # Connect to table nifty50_table
            self.cursor.execute(query)

            Nifty50_all_data = self.cursor.fetchall()  # Fetch all data
            columns = [col[0] for col in self.cursor.description]  # Get column names

            # Convert to DataFrame
            self.Nifty50_all_df = pd.DataFrame(Nifty50_all_data, columns=columns)

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

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class SidebarStyler:
    @staticmethod
    def apply_sidebar_styles():
        """Applies custom styling to sidebar components."""
        st.sidebar.markdown(
            """
            <style>
                .sidebar-title {
                    background-color: #90EE90;
                    color: black; /* Fixed syntax */
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                    text-align: center;
                }
            </style>
            <div class="sidebar-title">Select the stock for market analysis</div>
            """,
            unsafe_allow_html=True
        )

        st.sidebar.markdown(
            """
            <style>
                div.stButton > button {
                    width: 100%;
                    height: 25px;  /* Increased for usability */
                    font-size: 10px;
                    font-weight: bold;
                    color: white;
                    background-color: #154734;
                    border-radius: 5px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    def styled_subheader(text, color="#154734", font_size="20px", bg_color="transparent"):
        """Styles a subheader with custom text color, background color, and font size."""
        st.markdown(
            f'<h3 style="color:{color}; background-color:{bg_color}; font-size:{font_size}; font-weight:bold; text-align:center; padding:10px; border-radius:5px;">{text}</h3>',
            unsafe_allow_html=True
        )
       