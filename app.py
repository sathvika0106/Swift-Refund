from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from textblob import TextBlob
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'sath')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'swiftrefund')

def get_db():
    """Get MySQL database connection (Flask 3.0 compatible)"""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            autocommit=False
        )
    return g.db

def get_cursor():
    """Get MySQL cursor with dictionary results"""
    db = get_db()
    return db.cursor(dictionary=True)

@app.teardown_appcontext
def close_db(error):
    """Close database connection at the end of request"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_database():
    """Initialize database and create tables if they don't exist"""
    try:
        # First, connect without database to create it if needed
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD']
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DB']}")
        cursor.close()
        conn.close()
        
        # Now connect to the database to create tables
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        cursor = conn.cursor()
        
        # Create reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id VARCHAR(100),
                review_text TEXT NOT NULL,
                sentiment VARCHAR(20),
                polarity FLOAT,
                subjectivity FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_sentiment (sentiment),
                INDEX idx_created_at (created_at)
            )
        """)
        
        # Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id VARCHAR(100),
                amount DECIMAL(10, 2),
                status VARCHAR(20) DEFAULT 'pending',
                refund_status VARCHAR(20) DEFAULT 'not_initiated',
                review_id INT,
                priority VARCHAR(20) DEFAULT 'normal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP NULL,
                FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE SET NULL,
                INDEX idx_status (status),
                INDEX idx_refund_status (refund_status),
                INDEX idx_priority (priority)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Error as e:
        print(f"Error initializing database: {e}")
        print("Please make sure MySQL is running and credentials are correct.")
        raise  # Re-raise to prevent app from starting with broken database
    except Exception as e:
        print(f"Unexpected error initializing database: {e}")
        raise

def analyze_sentiment(text):
    """Analyze sentiment of the review text using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Classify sentiment based on polarity
    if polarity < -0.1:
        sentiment = 'negative'
    elif polarity > 0.1:
        sentiment = 'positive'
    else:
        sentiment = 'neutral'
    
    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': subjectivity
    }

@app.route('/')
def index():
    """Home page with review submission form"""
    return render_template('index.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    """Submit a customer review and analyze sentiment"""
    try:
        data = request.get_json() if request.is_json else request.form
        customer_id = data.get('customer_id', f'customer_{datetime.now().timestamp()}')
        review_text = data.get('review', '').strip()
        
        if not review_text:
            return jsonify({'error': 'Review text is required'}), 400
        
        # Analyze sentiment
        sentiment_data = analyze_sentiment(review_text)
        
        # Store review in database
        try:
            cur = get_cursor()
            cur.execute("""
                INSERT INTO reviews (customer_id, review_text, sentiment, polarity, subjectivity)
                VALUES (%s, %s, %s, %s, %s)
            """, (customer_id, review_text, sentiment_data['sentiment'], 
                  sentiment_data['polarity'], sentiment_data['subjectivity']))
            
            review_id = cur.lastrowid
            get_db().commit()
        except Exception as db_error:
            get_db().rollback()
            raise Exception(f"Database error: {str(db_error)}")
        finally:
            cur.close()
        
        # If sentiment is negative, trigger expedited refund
        refund_triggered = False
        transaction_id = None
        
        if sentiment_data['sentiment'] == 'negative':
            try:
                # Create expedited refund transaction
                amount = float(data.get('amount', 0))
                cur = get_cursor()
                cur.execute("""
                    INSERT INTO transactions (customer_id, amount, status, refund_status, review_id, priority)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (customer_id, amount, 'processing', 'expedited', review_id, 'high'))
                
                transaction_id = cur.lastrowid
                get_db().commit()
                refund_triggered = True
                cur.close()
            except Exception as db_error:
                get_db().rollback()
                raise Exception(f"Error creating refund transaction: {str(db_error)}")
        
        response = {
            'review_id': review_id,
            'sentiment': sentiment_data['sentiment'],
            'polarity': sentiment_data['polarity'],
            'subjectivity': sentiment_data['subjectivity'],
            'refund_triggered': refund_triggered,
            'message': 'Refund expedited due to negative review' if refund_triggered else 'Review processed successfully'
        }
        
        if transaction_id:
            response['transaction_id'] = transaction_id
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in submit_review: {error_details}")
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500

@app.route('/reviews')
def get_reviews():
    """Get all reviews with their sentiment analysis"""
    try:
        cur = get_cursor()
        cur.execute("""
            SELECT r.*, t.id as transaction_id, t.amount, t.refund_status, t.priority
            FROM reviews r
            LEFT JOIN transactions t ON r.id = t.review_id
            ORDER BY r.created_at DESC
            LIMIT 100
        """)
        reviews = cur.fetchall()
        cur.close()
        
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transactions')
def get_transactions():
    """Get all transactions"""
    try:
        cur = get_cursor()
        cur.execute("""
            SELECT t.*, r.review_text, r.sentiment
            FROM transactions t
            LEFT JOIN reviews r ON t.review_id = r.id
            ORDER BY t.created_at DESC
            LIMIT 100
        """)
        transactions = cur.fetchall()
        cur.close()
        
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard to view reviews and transactions"""
    return render_template('dashboard.html')

@app.route('/process_refund/<int:transaction_id>', methods=['POST'])
def process_refund(transaction_id):
    """Manually process a refund"""
    try:
        cur = get_cursor()
        cur.execute("""
            UPDATE transactions
            SET status = 'completed', refund_status = 'processed', processed_at = NOW()
            WHERE id = %s
        """, (transaction_id,))
        get_db().commit()
        cur.close()
        
        return jsonify({'message': 'Refund processed successfully', 'transaction_id': transaction_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """Get statistics about reviews and refunds"""
    try:
        cur = get_cursor()
        
        # Total reviews
        cur.execute("SELECT COUNT(*) as total FROM reviews")
        total_reviews = cur.fetchone()['total']
        
        # Sentiment distribution
        cur.execute("""
            SELECT sentiment, COUNT(*) as count
            FROM reviews
            GROUP BY sentiment
        """)
        sentiment_dist = {row['sentiment']: row['count'] for row in cur.fetchall()}
        
        # Total transactions
        cur.execute("SELECT COUNT(*) as total FROM transactions")
        total_transactions = cur.fetchone()['total']
        
        # Expedited refunds
        cur.execute("SELECT COUNT(*) as total FROM transactions WHERE priority = 'high'")
        expedited_refunds = cur.fetchone()['total']
        
        # Pending refunds
        cur.execute("SELECT COUNT(*) as total FROM transactions WHERE refund_status != 'processed'")
        pending_refunds = cur.fetchone()['total']
        
        cur.close()
        
        return jsonify({
            'total_reviews': total_reviews,
            'sentiment_distribution': sentiment_dist,
            'total_transactions': total_transactions,
            'expedited_refunds': expedited_refunds,
            'pending_refunds': pending_refunds
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
