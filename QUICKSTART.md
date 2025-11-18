# Quick Start Guide

## Prerequisites Check

1. **Python 3.7+** installed
   ```bash
   python --version
   ```

2. **MySQL Server** installed and running
   ```bash
   # Check if MySQL is running (Windows)
   # Or use MySQL Workbench to verify
   ```

3. **pip** installed
   ```bash
   pip --version
   ```

## Installation Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download NLTK Data

```bash
python setup_nltk.py
```

Or manually:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('wordnet'); nltk.download('stopwords')"
```

### Step 3: Configure MySQL

**Option A: Using Environment Variables (Recommended)**
```bash
# Windows PowerShell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_DB="swiftrefund"

# Windows CMD
set MYSQL_HOST=localhost
set MYSQL_USER=root
set MYSQL_PASSWORD=your_password
set MYSQL_DB=swiftrefund

# Linux/Mac
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=swiftrefund
```

**Option B: Edit app.py directly**
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'swiftrefund'
```

### Step 4: Run the Application

```bash
python app.py
```

You should see:
```
Database initialized successfully!
 * Running on http://0.0.0.0:5000
```

### Step 5: Access the Application

- **Home Page**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard
- **API - Reviews**: http://localhost:5000/reviews
- **API - Transactions**: http://localhost:5000/transactions
- **API - Stats**: http://localhost:5000/stats

## Testing the System

### Test 1: Submit a Negative Review

1. Go to http://localhost:5000
2. Enter a negative review like: "This product was terrible and broke immediately. Very disappointed!"
3. Click "Submit Review & Analyze Sentiment"
4. You should see:
   - Sentiment: NEGATIVE
   - ⚡ EXPEDITED REFUND TRIGGERED!

### Test 2: Submit a Positive Review

1. Enter a positive review like: "Great product! Very satisfied with my purchase."
2. Click "Submit Review & Analyze Sentiment"
3. You should see:
   - Sentiment: POSITIVE
   - No refund triggered

### Test 3: View Dashboard

1. Go to http://localhost:5000/dashboard
2. You should see:
   - Statistics (Total Reviews, Transactions, etc.)
   - Recent Reviews table
   - Recent Transactions table

## Troubleshooting

### Issue: "Error initializing database"

**Solution**: 
- Make sure MySQL is running
- Check MySQL credentials
- Ensure MySQL user has CREATE DATABASE privileges

### Issue: "ModuleNotFoundError: No module named 'textblob'"

**Solution**: 
```bash
pip install textblob
```

### Issue: "NLTK data not found"

**Solution**: 
```bash
python setup_nltk.py
```

### Issue: "Can't connect to MySQL server"

**Solution**:
- Verify MySQL is running
- Check host, user, and password
- Try connecting with MySQL Workbench or command line first

## API Testing with curl

### Submit a Review
```bash
curl -X POST http://localhost:5000/submit_review \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer_123",
    "amount": 100.00,
    "review": "This product was terrible!"
  }'
```

### Get All Reviews
```bash
curl http://localhost:5000/reviews
```

### Get Statistics
```bash
curl http://localhost:5000/stats
```

## Next Steps

- Customize sentiment thresholds in `analyze_sentiment()` function
- Add email notifications for expedited refunds
- Integrate with payment gateways for actual refund processing
- Add authentication and user management
- Deploy to production server

