#!/usr/bin/env python3
"""
FRED Data Downloader for GitHub Actions
Downloads economic data from FRED API and saves to CSV files
"""

import os
import sys
import logging
import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FREDDataDownloader:
    """Downloads FRED data and saves to CSV files"""
    
    def __init__(self, api_key):
        """Initialize with FRED API key"""
        self.fred = Fred(api_key=api_key)
        self.data_dir = "data"
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Default series to download
        self.default_series = [
            'AAA10Y',  # Moody's AAA Corporate Bond Yield vs 10-Year Treasury
            'BAA10Y',  # Moody's BAA Corporate Bond Yield vs 10-Year Treasury
            'DGS10',   # 10-Year Treasury Constant Maturity Rate
            'DGS2',    # 2-Year Treasury Constant Maturity Rate
            'DGS30',   # 30-Year Treasury Constant Maturity Rate
            'DGS3MO',  # 3-Month Treasury Constant Maturity Rate
            'FEDFUNDS', # Federal Funds Rate
            'UNRATE',  # Unemployment Rate
        ]
    
    def download_series(self, series_id, days_back=365):
        """Download a single series and save to CSV"""
        
        try:
            logger.info(f"Downloading {series_id}...")
            
            # Get series info
            series_info = self.fred.get_series_info(series_id)
            title = series_info.get('title', series_id)
            units = series_info.get('units', 'N/A')
            
            logger.info(f"Series: {title}")
            logger.info(f"Units: {units}")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Download data
            data = self.fred.get_series(
                series_id, 
                observation_start=start_date.strftime('%Y-%m-%d')
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            df.columns = ['value']
            df.index.name = 'date'
            df = df.reset_index()
            
            # Save to CSV
            filename = f"{self.data_dir}/{series_id}.csv"
            df.to_csv(filename, index=False)
            
            logger.info(f"✅ Downloaded {len(df)} observations for {series_id}")
            logger.info(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
            logger.info(f"📈 Latest value: {df.iloc[-1]['value']:.2f}")
            logger.info(f"💾 Saved to: {filename}")
            
            return {
                'series_id': series_id,
                'title': title,
                'units': units,
                'observations': len(df),
                'date_range': f"{df['date'].min()} to {df['date'].max()}",
                'latest_value': df.iloc[-1]['value'],
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"❌ Error downloading {series_id}: {e}")
            return None
    
    def download_all_series(self, series_list=None, days_back=365):
        """Download multiple series"""
        
        if series_list is None:
            series_list = self.default_series
        
        logger.info(f"Starting download of {len(series_list)} series...")
        
        results = []
        successful = []
        failed = []
        
        for series_id in series_list:
            result = self.download_series(series_id, days_back)
            
            if result:
                results.append(result)
                successful.append(series_id)
            else:
                failed.append(series_id)
        
        # Create summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_series': len(series_list),
            'successful': len(successful),
            'failed': len(failed),
            'successful_series': successful,
            'failed_series': failed,
            'results': results
        }
        
        # Save summary to JSON
        summary_file = f"{self.data_dir}/download_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"📋 Download summary saved to {summary_file}")
        logger.info(f"✅ Successfully downloaded {len(successful)} series")
        
        if failed:
            logger.warning(f"❌ Failed to download {len(failed)} series: {failed}")
        
        return summary

def main():
    """Main function for GitHub Actions"""
    
    # Get API key from environment variable
    api_key = os.environ.get('FRED_API_KEY')
    
    if not api_key:
        logger.error("❌ FRED_API_KEY environment variable not set")
        sys.exit(1)
    
    # Get series list from environment variable (optional)
    series_list = os.environ.get('FRED_SERIES_IDS')
    if series_list:
        series_list = [s.strip() for s in series_list.split(',')]
    
    # Get days back from environment variable (optional)
    days_back = int(os.environ.get('DAYS_BACK', '365'))
    
    # Initialize downloader
    downloader = FREDDataDownloader(api_key)
    
    # Download all series
    summary = downloader.download_all_series(series_list, days_back)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 FRED DATA DOWNLOAD SUMMARY")
    print("="*60)
    print(f"📅 Timestamp: {summary['timestamp']}")
    print(f"📈 Total series: {summary['total_series']}")
    print(f"✅ Successful: {summary['successful']}")
    print(f"❌ Failed: {summary['failed']}")
    
    if summary['successful_series']:
        print(f"\n✅ Successfully downloaded:")
        for series in summary['successful_series']:
            print(f"   - {series}")
    
    if summary['failed_series']:
        print(f"\n❌ Failed to download:")
        for series in summary['failed_series']:
            print(f"   - {series}")
    
    print(f"\n📁 All files saved in the 'data' directory")
    print("="*60)

if __name__ == "__main__":
    main() 