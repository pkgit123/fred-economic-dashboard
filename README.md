# FRED Economic Data Dashboard

A complete solution for downloading and visualizing Federal Reserve Economic Data (FRED) with automated data collection and interactive dashboards.

## 🏗️ **Architecture**

This project consists of two integrated applications:

1. **📥 FRED Data Downloader** - Python script for downloading economic data
2. **📊 Streamlit Dashboard** - Interactive web application for data visualization

## 📁 **Project Structure**

```
fred_streamlit/
├── 📄 fred_downloader.py          # Data download application
├── 📄 streamlit_app.py            # Streamlit visualization dashboard
├── 📄 requirements.txt            # Python dependencies
├── 📁 .github/workflows/          # GitHub Actions automation
│   └── 📄 fred_download.yml       # Automated data download workflow
├── 📁 data/                       # Downloaded CSV files (created automatically)
└── 📄 README.md                   # This file
```

## 🚀 **Quick Start**

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Set Up GitHub Repository**
1. Create a new GitHub repository
2. Push this code to your repository
3. Add GitHub Secrets (see setup instructions below)

### **Step 3: Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set the app file to `streamlit_app.py`
4. Deploy!

## ⚙️ **Setup Instructions**

### **GitHub Secrets Configuration**

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

1. **`FRED_API_KEY`**: Your FRED API key
   - Get one at: https://fred.stlouisfed.org/docs/api/api_key.html

2. **`FRED_SERIES_IDS`**: Comma-separated series IDs (optional)
   - Default: `AAA10Y,BAA10Y,DGS10,DGS2,DGS30,DGS3MO,FEDFUNDS,UNRATE`

3. **`DAYS_BACK`**: Number of days to look back (optional)
   - Default: `365`

### **Local Development**

1. **Test Data Downloader**:
   ```bash
   # Set environment variable
   export FRED_API_KEY="your_api_key_here"
   
   # Run downloader
   python fred_downloader.py
   ```

2. **Test Streamlit App**:
   ```bash
   # Run Streamlit app
   streamlit run streamlit_app.py
   ```

## 📊 **Available Data Series**

The default configuration downloads these economic indicators:

| Series ID | Description |
|-----------|-------------|
| `AAA10Y` | Moody's AAA Corporate Bond Yield vs 10-Year Treasury |
| `BAA10Y` | Moody's BAA Corporate Bond Yield vs 10-Year Treasury |
| `DGS10` | 10-Year Treasury Constant Maturity Rate |
| `DGS2` | 2-Year Treasury Constant Maturity Rate |
| `DGS30` | 30-Year Treasury Constant Maturity Rate |
| `DGS3MO` | 3-Month Treasury Constant Maturity Rate |
| `FEDFUNDS` | Federal Funds Rate |
| `UNRATE` | Unemployment Rate |

## 🎯 **Features**

### **Data Downloader (`fred_downloader.py`)**
- ✅ Downloads multiple FRED series automatically
- ✅ Configurable date ranges and series selection
- ✅ Comprehensive error handling and logging
- ✅ Generates download summary with statistics
- ✅ Saves data in standardized CSV format

### **Streamlit Dashboard (`streamlit_app.py`)**
- ✅ Interactive time series charts
- ✅ Real-time metrics and statistics
- ✅ Series comparison charts
- ✅ Date range filtering
- ✅ Data table with download functionality
- ✅ Responsive design for mobile/desktop
- ✅ Professional styling and layout

### **GitHub Actions Automation**
- ✅ Daily automated data downloads
- ✅ Manual trigger capability
- ✅ Automatic commit and push of new data
- ✅ Comprehensive logging and error reporting

## 🔧 **Configuration Options**

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `FRED_API_KEY` | Your FRED API key | Required |
| `FRED_SERIES_IDS` | Comma-separated series IDs | See default list above |
| `DAYS_BACK` | Number of days to look back | 365 |

### **Customizing Series**

To download different series, modify the `default_series` list in `fred_downloader.py`:

```python
self.default_series = [
    'YOUR_SERIES_ID_1',
    'YOUR_SERIES_ID_2',
    # Add more series as needed
]
```

## 📈 **Dashboard Features**

### **Interactive Charts**
- **Time Series Charts**: Individual charts for each series
- **Comparison Charts**: Overlay multiple series for comparison
- **Hover Information**: Detailed data on hover
- **Zoom and Pan**: Interactive chart controls

### **Data Analysis**
- **Key Metrics**: Latest values with change indicators
- **Statistics**: Min, max, mean, standard deviation
- **Date Filtering**: Select custom date ranges
- **Series Selection**: Choose which series to display

### **Data Export**
- **CSV Download**: Export filtered data as CSV
- **Raw Data Table**: View all data in tabular format
- **Pivot Table**: Side-by-side comparison of series

## 🚀 **Deployment**

### **Streamlit Cloud Deployment**

1. **Connect Repository**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select your repository

2. **Configure App**:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.9
   - **Requirements file**: `requirements.txt`

3. **Deploy**:
   - Click "Deploy"
   - Your dashboard will be live at `https://your-app-name.streamlit.app`

### **GitHub Actions Automation**

The workflow automatically:
- Runs daily at 9 AM EST
- Downloads fresh FRED data
- Commits and pushes to repository
- Triggers Streamlit Cloud redeployment

## 📊 **Monitoring and Maintenance**

### **Check Data Updates**
- View GitHub Actions logs for download status
- Check `data/download_summary.json` for statistics
- Monitor Streamlit Cloud for deployment status

### **Troubleshooting**
- **API Key Issues**: Verify FRED API key is valid
- **Data Not Loading**: Check if GitHub Actions completed successfully
- **Chart Display Issues**: Verify CSV files exist in `data/` directory

## 💰 **Cost**

- **GitHub Actions**: Free for public repositories
- **Streamlit Cloud**: Free for public apps
- **FRED API**: Free with API key
- **Total Cost**: $0

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 **License**

This project is open source and available under the MIT License.

## 🆘 **Support**

- **FRED API Documentation**: https://fred.stlouisfed.org/docs/api/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **GitHub Actions Documentation**: https://docs.github.com/en/actions

## 🎉 **What You Get**

After setup, you'll have:
- ✅ **Automated daily data collection** from FRED
- ✅ **Professional interactive dashboard** with real-time data
- ✅ **Zero maintenance** - everything runs automatically
- ✅ **Free hosting** - no ongoing costs
- ✅ **Mobile-responsive** design
- ✅ **Data export capabilities**
- ✅ **Comprehensive error handling**

Your economic data dashboard will be live and automatically updated daily! 