from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
import re
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = '.'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

# Enhanced Category detection keywords
CATEGORY_KEYWORDS = {
    "🥘 Food & Dining": [
        "swiggy", "zomato", "restaurant", "hotel", "cafe", "eatery", "food", 
        "dominos", "pizza hut", "kfc", "mcdonald", "burger king", "paid to",
        "dining", "meal", "lunch", "dinner", "breakfast", "canteen"
    ],
    "🛒 Groceries & Essentials": [
        "blinkit", "bigbasket", "grocery", "kirana", "spencer", "reliance fresh", 
        "dmart", "star bazaar", "meesho", "grofers", "fresh", "market",
        "vegetables", "fruits", "milk", "bread"
    ],
    "🏥 Medical & Healthcare": [
        "pharmacy", "hospital", "medical", "doctor", "clinic", "apollo", 
        "medplus", "1mg", "netmeds", "medicine", "tablet", "health"
    ],
    "🧾 Bills & Utilities": [
        "jio", "airtel", "vodafone", "idea", "bsnl", "recharge", "bill", 
        "electricity", "water", "gas", "dth", "broadband", "wifi"
    ],
    "🛍 Shopping": [
        "google play", "shopping", "flipkart", "amazon", "snapdeal", "myntra", 
        "nykaa", "ajio", "lifestyle", "netflix", "spotify", "subscription"
    ],
    "💵 Transfers & P2P": [
        "sent to", "money sent", "transfer", "upi to", "money given", 
        "to friend", "to family", "pay to"
    ],
    "💰 Money Received": [
        "received from", "payment from", "refund", "cashback", "reversal", 
        "credited", "salary", "income", "bonus"
    ],
    "🚖 Transport & Travel": [
        "uber", "ola", "rapido", "cab", "taxi", "bus", "train", "irctc", 
        "metro", "flight", "petrol", "diesel"
    ],
    "🎬 Entertainment": [
        "bookmyshow", "pvr", "inox", "movie", "cinema", "event", "concert"
    ],
    "🎓 Education": [
        "byjus", "unacademy", "udemy", "coursera", "school", "college", "tuition"
    ],
    "🏦 Banking & Fees": [
        "bank charge", "atm fee", "interest", "emi", "loan", "penalty"
    ],
    "🏠 Rent & Housing": [
        "rent", "maintenance", "society", "housing", "flat", "apartment"
    ],
    "⛽ Fuel": [
        "petrol", "diesel", "fuel", "hpcl", "iocl", "bpcl", "shell"
    ]
}

class TransactionAnalyzer:
    def __init__(self):
        self.df = None
        self.processed_df = None
        
    def load_excel_file(self, filename='data.xlsx'):
        """Load and process Excel file with robust error handling"""
        try:
            logger.info(f"Loading Excel file: {filename}")
            
            # Check if file exists
            if not os.path.exists(filename):
                logger.error(f"File not found: {filename}")
                return False, f"File not found: {filename}"
            
            # Read Excel file
            try:
                self.df = pd.read_excel(filename, engine='openpyxl')
            except Exception as e:
                logger.error(f"Error reading Excel file: {e}")
                return False, f"Could not read Excel file: {str(e)}"
            
            logger.info(f"Successfully loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            logger.info(f"Column names: {list(self.df.columns)}")
            
            # Process the data
            success, message = self._process_data()
            return success, message
            
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            return False, f"Error loading file: {str(e)}"
    
    def _process_data(self):
        """Process and clean the loaded data - FIXED VERSION"""
        try:
            if self.df is None or len(self.df) == 0:
                return False, "No data to process"
            
            # Make a copy for processing
            self.processed_df = self.df.copy()
            
            # Clean column names
            self.processed_df.columns = self.processed_df.columns.str.strip()
            
            # **FIX 1: Handle DateTime columns properly**
            # Look for Date and Time columns separately and combine them
            date_col = None
            time_col = None
            
            for col in self.processed_df.columns:
                col_lower = col.lower().strip()
                if col_lower == 'date':
                    date_col = col
                elif col_lower == 'time':
                    time_col = col
                elif 'datetime' in col_lower:
                    date_col = col
                    break
            
            # Create DateTime column
            if date_col is not None and time_col is not None:
                try:
                    # Combine Date and Time columns
                    date_str = self.processed_df[date_col].astype(str)
                    time_str = self.processed_df[time_col].astype(str)
                    datetime_str = date_str + ' ' + time_str
                    self.processed_df['DateTime'] = pd.to_datetime(datetime_str, errors='coerce')
                    logger.info(f"Combined {date_col} and {time_col} into DateTime")
                except Exception as e:
                    logger.warning(f"Could not combine date/time columns: {e}")
                    self._create_dummy_datetime()
            elif date_col is not None:
                try:
                    self.processed_df['DateTime'] = pd.to_datetime(self.processed_df[date_col], errors='coerce')
                    logger.info(f"Converted {date_col} to DateTime")
                except Exception as e:
                    logger.warning(f"Could not parse date column: {e}")
                    self._create_dummy_datetime()
            else:
                logger.warning("No date column found, creating dummy dates")
                self._create_dummy_datetime()
            
            # **FIX 2: Handle Amount column with proper error checking**
            amount_col = None
            for col in self.processed_df.columns:
                if 'amount' in col.lower():
                    amount_col = col
                    break
            
            if amount_col is not None:
                try:
                    # Clean and convert amount column
                    amount_series = self.processed_df[amount_col].astype(str)
                    # Remove currency symbols and whitespace
                    amount_series = amount_series.str.replace(r'[₹,$,\s]', '', regex=True)
                    # Handle empty strings
                    amount_series = amount_series.replace('', '0')
                    amount_series = amount_series.replace('nan', '0')
                    self.processed_df['Amount'] = pd.to_numeric(amount_series, errors='coerce')
                    # Fill any remaining NaN values with 0
                    self.processed_df['Amount'] = self.processed_df['Amount'].fillna(0)
                    logger.info(f"Converted {amount_col} to numeric Amount")
                except Exception as e:
                    logger.error(f"Error converting amount column: {e}")
                    self.processed_df['Amount'] = 0
            else:
                logger.warning("No amount column found, setting all amounts to 0")
                self.processed_df['Amount'] = 0
            
            # **FIX 3: Handle Transaction Details column**
            details_col = None
            for col in self.processed_df.columns:
                col_lower = col.lower()
                if 'transaction' in col_lower and 'detail' in col_lower:
                    details_col = col
                    break
            
            if details_col is not None:
                self.processed_df['Transaction Details'] = self.processed_df[details_col].astype(str)
            else:
                # Use first available text column or create dummy data
                text_cols = []
                for col in self.processed_df.columns:
                    if self.processed_df[col].dtype == 'object':
                        text_cols.append(col)
                
                if len(text_cols) > 0:
                    self.processed_df['Transaction Details'] = self.processed_df[text_cols[0]].astype(str)
                    logger.info(f"Used {text_cols[0]} as Transaction Details")
                else:
                    self.processed_df['Transaction Details'] = 'Unknown Transaction'
                    logger.warning("No transaction details found, using dummy data")
            
            # Fill missing values
            self.processed_df['Transaction Details'] = self.processed_df['Transaction Details'].fillna('Unknown Transaction')
            
            # **FIX 4: Add derived columns with proper error handling**
            try:
                self.processed_df['Category'] = self.processed_df['Transaction Details'].apply(self._categorize_transaction)
                
                # **FIX 5: Handle Type column with .loc to avoid ambiguity**
                self.processed_df['Type'] = 'Unknown'
                credit_mask = self.processed_df['Amount'] > 0
                debit_mask = self.processed_df['Amount'] < 0
                
                self.processed_df.loc[credit_mask, 'Type'] = 'Credit'
                self.processed_df.loc[debit_mask, 'Type'] = 'Debit'
                
                self.processed_df['AbsAmount'] = self.processed_df['Amount'].abs()
                
                # Add time-based columns
                self.processed_df['Date'] = self.processed_df['DateTime'].dt.date
                self.processed_df['Month'] = self.processed_df['DateTime'].dt.to_period('M').astype(str)
                self.processed_df['Week'] = self.processed_df['DateTime'].dt.to_period('W').astype(str)
                self.processed_df['DayOfWeek'] = self.processed_df['DateTime'].dt.day_name()
                
            except Exception as e:
                logger.error(f"Error adding derived columns: {e}")
                # Set default values
                self.processed_df['Category'] = '🔄 Miscellaneous'
                self.processed_df['Type'] = 'Unknown'
                self.processed_df['AbsAmount'] = 0
            
            logger.info(f"Successfully processed {len(self.processed_df)} transactions")
            return True, "Data processed successfully"
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return False, f"Error processing data: {str(e)}"
    
    def _create_dummy_datetime(self):
        """Create dummy datetime data"""
        try:
            base_date = datetime.now() - timedelta(days=len(self.processed_df))
            self.processed_df['DateTime'] = [
                base_date + timedelta(days=i) 
                for i in range(len(self.processed_df))
            ]
            logger.info("Created dummy datetime data")
        except Exception as e:
            logger.error(f"Error creating dummy dates: {e}")
            self.processed_df['DateTime'] = datetime.now()
    
    def _categorize_transaction(self, details):
        """Categorize transaction based on keywords in details"""
        try:
            if pd.isna(details) or details == '' or str(details).lower() == 'nan':
                return "🔄 Miscellaneous"
            
            details_lower = str(details).lower().strip()
            
            # Check each category
            for category, keywords in CATEGORY_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in details_lower:
                        return category
            
            return "🔄 Miscellaneous"
        except Exception as e:
            logger.error(f"Error categorizing transaction: {e}")
            return "🔄 Miscellaneous"
    
    def get_full_analysis(self):
        """Get complete analysis of the data"""
        try:
            if self.processed_df is None or len(self.processed_df) == 0:
                return {"error": "No data available for analysis"}
            
            # **FIX 6: Use .loc[] to avoid ambiguous boolean operations**
            # Basic statistics
            debit_mask = self.processed_df['Amount'] < 0
            credit_mask = self.processed_df['Amount'] > 0
            
            total_spent = abs(self.processed_df.loc[debit_mask, 'Amount'].sum())
            total_received = self.processed_df.loc[credit_mask, 'Amount'].sum()
            transaction_count = len(self.processed_df)
            
            # Category analysis (only for debit transactions)
            debit_df = self.processed_df.loc[debit_mask].copy()
            if len(debit_df) > 0:
                debit_df['AbsAmount'] = debit_df['Amount'].abs()
                categories = debit_df.groupby('Category')['AbsAmount'].sum().round(2).to_dict()
            else:
                categories = {}
            
            # Trends analysis
            trends = self._calculate_trends()
            
            # Largest transaction
            if len(self.processed_df) > 0:
                largest_idx = self.processed_df['AbsAmount'].idxmax()
                largest_transaction = {
                    "amount": float(self.processed_df.loc[largest_idx, 'Amount']),
                    "details": str(self.processed_df.loc[largest_idx, 'Transaction Details']),
                    "date": self.processed_df.loc[largest_idx, 'DateTime'].strftime('%Y-%m-%d') if pd.notna(self.processed_df.loc[largest_idx, 'DateTime']) else 'Unknown'
                }
            else:
                largest_transaction = {"amount": 0, "details": "No transactions", "date": "Unknown"}
            
            # Prepare filtered data (last 100 transactions)
            filtered_data = self._prepare_transaction_data(limit=100)
            
            result = {
                "totals": {
                    "spent": float(total_spent),
                    "received": float(total_received),
                    "net": float(total_received - total_spent)
                },
                "categories": categories,
                "filtered_data": filtered_data,
                "trends": trends,
                "largest_transaction": largest_transaction,
                "transaction_count": transaction_count,
                "date_range": {
                    "start": self.processed_df['DateTime'].min().strftime('%Y-%m-%d') if pd.notna(self.processed_df['DateTime'].min()) else 'Unknown',
                    "end": self.processed_df['DateTime'].max().strftime('%Y-%m-%d') if pd.notna(self.processed_df['DateTime'].max()) else 'Unknown'
                }
            }
            
            logger.info("Full analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in get_full_analysis: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _calculate_trends(self):
        """Calculate daily, weekly, and monthly trends"""
        try:
            trends = {"daily": [], "weekly": [], "monthly": []}
            
            if self.processed_df is None or len(self.processed_df) == 0:
                return trends
            
            # **FIX 7: Use .loc[] for boolean indexing**
            debit_mask = self.processed_df['Amount'] < 0
            debit_data = self.processed_df.loc[debit_mask]
            
            if len(debit_data) > 0:
                # Daily trends
                try:
                    daily_spending = debit_data.groupby('Date')['Amount'].apply(lambda x: abs(x.sum())).reset_index()
                    daily_spending['Date'] = daily_spending['Date'].astype(str)
                    trends["daily"] = daily_spending.rename(columns={'Date': 'Period', 'Amount': 'Amount'}).to_dict('records')
                except Exception as e:
                    logger.warning(f"Could not calculate daily trends: {e}")
                
                # Weekly trends
                try:
                    weekly_spending = debit_data.groupby('Week')['Amount'].apply(lambda x: abs(x.sum())).reset_index()
                    trends["weekly"] = weekly_spending.rename(columns={'Week': 'Period', 'Amount': 'Amount'}).to_dict('records')
                except Exception as e:
                    logger.warning(f"Could not calculate weekly trends: {e}")
                
                # Monthly trends
                try:
                    monthly_spending = debit_data.groupby('Month')['Amount'].apply(lambda x: abs(x.sum())).reset_index()
                    trends["monthly"] = monthly_spending.rename(columns={'Month': 'Period', 'Amount': 'Amount'}).to_dict('records')
                except Exception as e:
                    logger.warning(f"Could not calculate monthly trends: {e}")
            
            return trends
            
        except Exception as e:
            logger.error(f"Error calculating trends: {e}")
            return {"daily": [], "weekly": [], "monthly": []}
    
    def _prepare_transaction_data(self, limit=None):
        """Prepare transaction data for frontend"""
        try:
            if self.processed_df is None or len(self.processed_df) == 0:
                return []
            
            # Select relevant columns that exist
            required_cols = ['DateTime', 'Transaction Details', 'Category', 'Amount', 'Type']
            available_cols = [col for col in required_cols if col in self.processed_df.columns]
            
            if len(available_cols) == 0:
                return []
            
            df_subset = self.processed_df[available_cols].copy()
            
            # Sort by date (newest first)
            try:
                df_subset = df_subset.sort_values('DateTime', ascending=False)
            except:
                pass  # If sorting fails, continue with unsorted data
            
            if limit and len(df_subset) > limit:
                df_subset = df_subset.head(limit)
            
            # Convert to records
            records = df_subset.to_dict('records')
            
            # Format for JSON serialization
            for record in records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif isinstance(value, (np.integer, np.floating)):
                        record[key] = float(value)
                    elif key == 'DateTime' and hasattr(value, 'strftime'):
                        record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        record[key] = str(value)
            
            return records
            
        except Exception as e:
            logger.error(f"Error preparing transaction data: {e}")
            return []
    
    def apply_filters(self, filters):
        """Apply filters to the data and return filtered analysis"""
        try:
            if self.processed_df is None or len(self.processed_df) == 0:
                return {"error": "No data available"}
            
            filtered_df = self.processed_df.copy()
            
            # **FIX 8: Use .loc[] for all filtering operations**
            # Apply amount filters
            if filters.get('min_amount'):
                try:
                    min_amt = float(filters['min_amount'])
                    amount_mask = filtered_df['AbsAmount'] >= min_amt
                    filtered_df = filtered_df.loc[amount_mask]
                except Exception as e:
                    logger.warning(f"Could not apply min_amount filter: {e}")
            
            if filters.get('max_amount'):
                try:
                    max_amt = float(filters['max_amount'])
                    amount_mask = filtered_df['AbsAmount'] <= max_amt
                    filtered_df = filtered_df.loc[amount_mask]
                except Exception as e:
                    logger.warning(f"Could not apply max_amount filter: {e}")
            
            # Apply date filters
            if filters.get('start_date'):
                try:
                    start_date = pd.to_datetime(filters['start_date'])
                    date_mask = filtered_df['DateTime'] >= start_date
                    filtered_df = filtered_df.loc[date_mask]
                except Exception as e:
                    logger.warning(f"Could not apply start_date filter: {e}")
            
            if filters.get('end_date'):
                try:
                    end_date = pd.to_datetime(filters['end_date']) + timedelta(days=1)
                    date_mask = filtered_df['DateTime'] < end_date
                    filtered_df = filtered_df.loc[date_mask]
                except Exception as e:
                    logger.warning(f"Could not apply end_date filter: {e}")
            
            # Apply category filter
            if filters.get('category') and filters['category'] != 'All':
                try:
                    category_mask = filtered_df['Category'] == filters['category']
                    filtered_df = filtered_df.loc[category_mask]
                except Exception as e:
                    logger.warning(f"Could not apply category filter: {e}")
            
            # Apply keyword search
            if filters.get('keyword'):
                try:
                    keyword = filters['keyword'].lower()
                    keyword_mask = filtered_df['Transaction Details'].str.lower().str.contains(keyword, na=False)
                    filtered_df = filtered_df.loc[keyword_mask]
                except Exception as e:
                    logger.warning(f"Could not apply keyword filter: {e}")
            
            # Calculate filtered statistics
            debit_mask = filtered_df['Amount'] < 0
            credit_mask = filtered_df['Amount'] > 0
            
            total_spent = abs(filtered_df.loc[debit_mask, 'Amount'].sum()) if debit_mask.any() else 0
            total_received = filtered_df.loc[credit_mask, 'Amount'].sum() if credit_mask.any() else 0
            
            # Category analysis for filtered data
            debit_filtered = filtered_df.loc[debit_mask]
            if len(debit_filtered) > 0:
                categories = debit_filtered.groupby('Category')['AbsAmount'].sum().round(2).to_dict()
            else:
                categories = {}
            
            # Prepare filtered transaction data
            filtered_records = []
            if len(filtered_df) > 0:
                required_cols = ['DateTime', 'Transaction Details', 'Category', 'Amount', 'Type']
                available_cols = [col for col in required_cols if col in filtered_df.columns]
                
                if len(available_cols) > 0:
                    subset = filtered_df[available_cols].copy()
                    try:
                        subset = subset.sort_values('DateTime', ascending=False).head(100)
                    except:
                        subset = subset.head(100)
                    
                    filtered_records = subset.to_dict('records')
                    for record in filtered_records:
                        for key, value in record.items():
                            if pd.isna(value):
                                record[key] = None
                            elif isinstance(value, (np.integer, np.floating)):
                                record[key] = float(value)
                            elif key == 'DateTime' and hasattr(value, 'strftime'):
                                record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                record[key] = str(value)
            
            result = {
                "totals": {
                    "spent": float(total_spent),
                    "received": float(total_received),
                    "net": float(total_received - total_spent)
                },
                "categories": categories,
                "filtered_data": filtered_records,
                "trends": {"daily": [], "weekly": [], "monthly": []},  # Simplified for filtered data
                "transaction_count": len(filtered_df)
            }
            
            logger.info(f"Applied filters, {len(filtered_df)} transactions remaining")
            return result
            
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            return {"error": f"Filter application failed: {str(e)}"}

# Global analyzer instance
analyzer = TransactionAnalyzer()

# Flask Routes (unchanged)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/analyze', methods=['GET'])
def analyze_data():
    try:
        success, message = analyzer.load_excel_file('data.xlsx')
        
        if not success:
            return jsonify({"error": f"Could not load data: {message}"}), 400
        
        result = analyzer.get_full_analysis()
        
        if "error" in result:
            return jsonify(result), 400
        
        logger.info("Analysis completed successfully")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_data: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file and file.filename.lower().endswith(('.xlsx', '.xls')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data.xlsx')
            file.save(filepath)
            
            success, message = analyzer.load_excel_file(filepath)
            
            if not success:
                return jsonify({"error": f"Failed to process uploaded file: {message}"}), 400
            
            logger.info(f"File uploaded and processed successfully: {filename}")
            return jsonify({"message": "File uploaded and processed successfully"}), 200
        
        return jsonify({"error": "Invalid file format. Please upload .xlsx or .xls files only."}), 400
        
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/filter', methods=['POST'])
def filter_data():
    try:
        filters = request.json or {}
        result = analyzer.apply_filters(filters)
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in filter_data: {e}")
        return jsonify({"error": f"Filter failed: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info("Starting Transaction Analyzer Flask App")
    app.run(debug=True, host='0.0.0.0', port=5000)
