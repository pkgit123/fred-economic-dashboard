#!/usr/bin/env python3
"""
FRED Data Visualization Dashboard
Streamlit app for visualizing economic data from FRED
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="FRED Economic Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .data-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .refresh-button {
        background-color: #1f77b4;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

def get_data_freshness():
    """Check how fresh the data is"""
    summary_file = os.path.join("data", 'download_summary.json')
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r') as f:
                summary = json.load(f)
                timestamp = datetime.fromisoformat(summary['timestamp'])
                age = datetime.now() - timestamp
                return timestamp, age
        except Exception:
            return None, None
    return None, None

@st.cache_data(ttl=3600)  # Cache for 1 hour instead of indefinitely
def load_data():
    """Load all FRED data files with freshness check"""
    data = {}
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        st.error(f"Data directory '{data_dir}' not found. Please run the data downloader first.")
        return {}
    
    # Load CSV files
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            series_id = filename.replace('.csv', '')
            filepath = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(filepath)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                data[series_id] = df
            except Exception as e:
                st.warning(f"Error loading {filename}: {e}")
    
    # Load summary if available
    summary_file = os.path.join(data_dir, 'download_summary.json')
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r') as f:
                data['summary'] = json.load(f)
        except Exception as e:
            st.warning(f"Error loading summary: {e}")
    
    return data

def create_time_series_chart(df, series_id, title):
    """Create an interactive time series chart"""
    fig = px.line(
        df, 
        x='date', 
        y='value',
        title=title,
        labels={'value': 'Value', 'date': 'Date'},
        template='plotly_white'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    fig.update_traces(
        line=dict(width=2),
        hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
    )
    
    return fig

def create_comparison_chart(data, series_list, title):
    """Create a comparison chart for multiple series"""
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, series_id in enumerate(series_list):
        if series_id in data:
            df = data[series_id]
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['value'],
                    mode='lines',
                    name=series_id,
                    line=dict(color=colors[i % len(colors)], width=2)
                )
            )
    
    fig.update_layout(
        title=title,
        height=500,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def calculate_statistics(df):
    """Calculate basic statistics for a series"""
    if df.empty:
        return {}
    
    latest = df.iloc[-1]['value']
    prev_day = df.iloc[-2]['value'] if len(df) > 1 else latest
    change = latest - prev_day
    change_pct = (change / prev_day * 100) if prev_day != 0 else 0
    
    return {
        'latest': latest,
        'change': change,
        'change_pct': change_pct,
        'min': df['value'].min(),
        'max': df['value'].max(),
        'mean': df['value'].mean(),
        'std': df['value'].std()
    }

def sort_series_by_risk(series_list):
    """Sort series by risk level (least risky to most risky)"""
    # Define risk order: AAA (lowest risk) -> BAA -> High Yield (highest risk)
    risk_order = {
        'AAA10Y': 1,      # AAA-rated bonds (lowest risk)
        'BAA10Y': 2,      # BAA-rated bonds (medium risk)
        'BAMLH0A0HYM2': 3, # High-yield bonds (highest risk)
        'DGS10': 4,       # Treasury bonds (risk-free)
        'DGS2': 5,        # Treasury bonds (risk-free)
        'DGS30': 6,       # Treasury bonds (risk-free)
        'DGS3MO': 7,      # Treasury bonds (risk-free)
        'FEDFUNDS': 8,    # Federal funds rate
        'UNRATE': 9       # Unemployment rate
    }
    
    # Sort by risk order, with unknown series at the end
    return sorted(series_list, key=lambda x: risk_order.get(x, 999))

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 FRED Economic Data Dashboard</h1>', unsafe_allow_html=True)
    
    # Data freshness check and refresh button
    timestamp, age = get_data_freshness()
    
    # Add refresh button in the top right
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🔄 Refresh Data", help="Clear cache and reload data"):
            st.cache_data.clear()
            st.rerun()
    
    # Show data freshness info
    if timestamp and age:
        if age.total_seconds() < 3600:  # Less than 1 hour
            st.success(f"✅ Data is fresh! Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({age.total_seconds()//60} minutes ago)")
        elif age.total_seconds() < 86400:  # Less than 24 hours
            st.info(f"ℹ️ Data is recent. Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({age.days} days, {age.seconds//3600} hours ago)")
        else:
            st.warning(f"⚠️ Data may be stale. Last updated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({age.days} days ago)")
    
    # Load data
    data = load_data()
    
    if not data:
        st.error("No data found. Please ensure the data downloader has been run.")
        return
    
    # Sidebar
    st.sidebar.header("📈 Dashboard Controls")
    
    # Data info
    if 'summary' in data:
        summary = data['summary']
        st.sidebar.markdown("### 📋 Data Information")
        st.sidebar.write(f"**Last Updated:** {summary['timestamp'][:19]}")
        st.sidebar.write(f"**Series Downloaded:** {summary['successful']}/{summary['total_series']}")
        
        if summary['successful_series']:
            st.sidebar.write("**Available Series (by risk level):**")
            sorted_available = sort_series_by_risk(summary['successful_series'])
            for series in sorted_available:
                # Add risk level indicators
                if series == 'AAA10Y':
                    st.sidebar.write(f"• {series} (AAA - Lowest Risk)")
                elif series == 'BAA10Y':
                    st.sidebar.write(f"• {series} (BAA - Medium Risk)")
                elif series == 'BAMLH0A0HYM2':
                    st.sidebar.write(f"• {series} (High Yield - Highest Risk)")
                else:
                    st.sidebar.write(f"• {series}")
    
    # Series selection
    available_series = [s for s in data.keys() if s != 'summary']
    if available_series:
        # Sort series by risk level (least risky to most risky)
        sorted_series = sort_series_by_risk(available_series)
        
        selected_series = st.sidebar.multiselect(
            "Select Series to Display:",
            sorted_series,
            default=sorted_series[:3]  # Default to first 3 series (AAA10Y, BAA10Y, BAMLH0A0HYM2)
        )
        
        # Date range filter
        if selected_series:
            all_dates = []
            for series in selected_series:
                all_dates.extend(data[series]['date'].tolist())
            
            min_date = min(all_dates)
            max_date = max(all_dates)
            
            date_range = st.sidebar.date_input(
                "Date Range:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
    
    # Main content
    if not selected_series:
        st.info("Please select at least one series from the sidebar.")
        return
    
    # Key metrics row
    st.subheader("📊 Key Metrics")
    cols = st.columns(len(selected_series))
    
    for i, series_id in enumerate(selected_series):
        if series_id in data:
            df = data[series_id]
            stats = calculate_statistics(df)
            
            with cols[i]:
                st.metric(
                    label=series_id,
                    value=f"{stats['latest']:.2f}",
                    delta=f"{stats['change']:.2f} ({stats['change_pct']:.1f}%)"
                )
    
    # Time series charts
    st.subheader("📈 Time Series Charts")
    
    # Individual charts
    for series_id in selected_series:
        if series_id in data:
            df = data[series_id]
            
            # Apply date filter
            if len(date_range) == 2:
                start_date, end_date = date_range
                df_filtered = df[(df['date'] >= pd.Timestamp(start_date)) & 
                               (df['date'] <= pd.Timestamp(end_date))]
            else:
                df_filtered = df
            
            # Get series info
            series_info = None
            if 'summary' in data:
                for result in data['summary']['results']:
                    if result['series_id'] == series_id:
                        series_info = result
                        break
            
            title = series_info['title'] if series_info else series_id
            
            fig = create_time_series_chart(df_filtered, series_id, title)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            stats = calculate_statistics(df_filtered)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Min", f"{stats['min']:.2f}")
            with col2:
                st.metric("Max", f"{stats['max']:.2f}")
            with col3:
                st.metric("Mean", f"{stats['mean']:.2f}")
            with col4:
                st.metric("Std Dev", f"{stats['std']:.2f}")
    
    # Comparison chart
    if len(selected_series) > 1:
        st.subheader("🔄 Series Comparison")
        
        # Filter data for comparison
        comparison_data = {}
        for series_id in selected_series:
            if series_id in data:
                df = data[series_id]
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    df_filtered = df[(df['date'] >= pd.Timestamp(start_date)) & 
                                   (df['date'] <= pd.Timestamp(end_date))]
                else:
                    df_filtered = df
                comparison_data[series_id] = df_filtered
        
        fig = create_comparison_chart(comparison_data, selected_series, "Series Comparison")
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 Raw Data")
    
    # Combine selected series into one table
    combined_data = []
    for series_id in selected_series:
        if series_id in data:
            df = data[series_id].copy()
            df['series'] = series_id
            combined_data.append(df)
    
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        
        # Apply date filter
        if len(date_range) == 2:
            start_date, end_date = date_range
            combined_df = combined_df[(combined_df['date'] >= pd.Timestamp(start_date)) & 
                                    (combined_df['date'] <= pd.Timestamp(end_date))]
        
        # Pivot for better display
        pivot_df = combined_df.pivot(index='date', columns='series', values='value')
        st.dataframe(pivot_df, use_container_width=True)
        
        # Download button
        csv = pivot_df.to_csv()
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"fred_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 