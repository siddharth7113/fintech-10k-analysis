import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Setup base directory relative to the script location
base_dir = Path(__file__).resolve().parent
# Data paths for textual insights and financial data
text_data = {
    'AAPL': base_dir / 'data/text/AAPL_combined.txt',
    'DELL': base_dir / 'data/text/DELL_combined.txt',
    'GOOGL': base_dir / 'data/text/GOOGL_combined.txt',
    'MSFT': base_dir / 'data/text/MSFT_combined.txt'
}
csv_data = {
    'AAPL': base_dir / 'data/csv/AAPL_combined_financial_data.csv',
    'DELL': base_dir / 'data/csv/DELL_combined_financial_data.csv',
    'GOOGL': base_dir / 'data/csv/GOOGL_combined_financial_data.csv',
    'MSFT': base_dir / 'data/csv/MSFT_combined_financial_data.csv'
}

def load_text_data(company):
    with open(text_data[company], 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Function to load financial data from CSV
def load_financial_data(company):
    df = pd.read_csv(csv_data[company])
    df.columns = [col.strip().title() for col in df.columns]  # Normalize column names
    print("Normalized columns:", df.columns)  # Debugging: print normalized column names
    return df

# Custom CSS for better aesthetics
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading a local CSS file
local_css(base_dir / 'styles/main.css')

# Streamlit app layout
st.sidebar.title('Select Firm')
company = st.sidebar.selectbox('Choose a company:', list(text_data.keys()))

# Main area
st.title('Insights from 10-K from Public Firms')
st.header(f'Important Insights for {company}')
insights = load_text_data(company)
st.text(insights)

# Plotting financial data
# Load and display financial data plots
try:
    financial_data = load_financial_data(company)

    # Check if necessary columns exist before plotting
    if 'Year' in financial_data.columns and 'Revenue' in financial_data.columns:
        fig, ax = plt.subplots()
        ax.plot(financial_data['Year'], financial_data['Revenue'], marker='o', linestyle='-')
        ax.set_title('Revenue Over Years')
        ax.set_xlabel('Year')
        ax.set_ylabel('Revenue ($ in millions)')
        st.pyplot(fig)
    else:
        st.error("The necessary columns for plotting are not available in the CSV file.")
except Exception as e:
    st.error(f"Failed to load or plot data due to: {str(e)}")

st.header('Plots Accompanying the Data')
st.write('These plots are generated from the financial data extracted from the CSV files.')
