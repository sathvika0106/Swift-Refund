# SwiftRefund - Automated Refund System

SwiftRefund is an automated refund processing system that uses sentiment analysis to expedite refunds for customers who leave negative reviews.

## Features

- **Automated Sentiment Analysis**: Uses TextBlob to analyze customer review sentiment
- **Fast Refund Trigger**: Automatically expedites refunds for negative reviews
- **MySQL Database**: Stores reviews, transactions, and sentiment data
- **Web Dashboard**: View reviews, transactions, and statistics
- **RESTful API**: Submit reviews and retrieve data via API endpoints

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **NLP**: TextBlob for sentiment analysis
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd SwiftRefund
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (required for TextBlob)**
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

4. **Configure MySQL**
   - Make sure MySQL is running
   - Update database credentials in `app.py` or set environment variables:
     ```bash
     export MYSQL_HOST=localhost
     export MYSQL_USER=root
     export MYSQL_PASSWORD=your_password
     export MYSQL_DB=swiftrefund
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Home page: http://localhost:5000
   - Dashboard: http://localhost:5000/dashboard
   - API endpoints: http://localhost:5000/reviews, http://localhost:5000/transactions

## Usage

### Submitting a Review

1. Navigate to the home page
2. Enter customer ID (optional)
3. Enter refund amount (optional)
4. Enter the customer review
5. Click "Submit Review & Analyze Sentiment"

The system will:
- Analyze the sentiment of the review
- If negative, automatically create an expedited refund transaction
- Store the review and transaction in the database

### API Endpoints

#### Submit Review
```
POST /submit_review
Content-Type: application/json

{
    "customer_id": "customer_123",
    "amount": 100.00,
    "review": "This product was terrible and broke immediately."
}
```

#### Get All Reviews
```
GET /reviews
```

#### Get All Transactions
```
GET /transactions
```

#### Get Statistics
```
GET /stats
```

#### Process Refund
```
POST /process_refund/<transaction_id>
```

## Database Schema

### Reviews Table
- `id`: Primary key
- `customer_id`: Customer identifier
- `review_text`: The review content
- `sentiment`: positive, negative, or neutral
- `polarity`: Sentiment polarity score (-1 to 1)
- `subjectivity`: Subjectivity score (0 to 1)
- `created_at`: Timestamp

### Transactions Table
- `id`: Primary key
- `customer_id`: Customer identifier
- `amount`: Refund amount
- `status`: Transaction status (pending, processing, completed)
- `refund_status`: Refund status (not_initiated, expedited, processed)
- `review_id`: Foreign key to reviews table
- `priority`: Priority level (normal, high)
- `created_at`: Timestamp
- `processed_at`: Processing timestamp

## Workflow

1. **Data Input**: Customer submits a review through the web interface or API
2. **Sentiment Analysis**: TextBlob analyzes the review text to determine sentiment
3. **Decision Making**: If sentiment is negative, an expedited refund transaction is automatically created
4. **Database Storage**: Review and transaction data are stored in MySQL
5. **Dashboard Monitoring**: Administrators can view all reviews and transactions in the dashboard

## Sentiment Analysis

The system uses TextBlob's sentiment analysis which provides:
- **Polarity**: Ranges from -1 (very negative) to 1 (very positive)
- **Subjectivity**: Ranges from 0 (objective) to 1 (subjective)

Classification:
- **Negative**: polarity < -0.1
- **Neutral**: -0.1 ≤ polarity ≤ 0.1
- **Positive**: polarity > 0.1

## Configuration

You can configure the application by:
1. Setting environment variables (recommended for production)
2. Modifying the configuration in `app.py`
3. Using the `config.py` file for more advanced configurations

## License

This project is open source and available for educational purposes.

