"""
Test script for SwiftRefund API
Run this after starting the Flask application
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_submit_negative_review():
    """Test submitting a negative review (should trigger expedited refund)"""
    print("\n=== Test 1: Submitting Negative Review ===")
    data = {
        "customer_id": "test_customer_1",
        "amount": 150.00,
        "review": "This product was terrible! It broke immediately after I received it. Very disappointed with the quality. Worst purchase ever!"
    }
    
    response = requests.post(f"{BASE_URL}/submit_review", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()
        assert result['sentiment'] == 'negative', "Expected negative sentiment"
        assert result['refund_triggered'] == True, "Expected refund to be triggered"
        print("✓ Test passed: Negative review triggered expedited refund")
        return result.get('transaction_id')
    else:
        print("✗ Test failed")
        return None

def test_submit_positive_review():
    """Test submitting a positive review (should NOT trigger refund)"""
    print("\n=== Test 2: Submitting Positive Review ===")
    data = {
        "customer_id": "test_customer_2",
        "amount": 200.00,
        "review": "Amazing product! Very satisfied with my purchase. Great quality and fast shipping. Highly recommend!"
    }
    
    response = requests.post(f"{BASE_URL}/submit_review", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()
        assert result['sentiment'] == 'positive', "Expected positive sentiment"
        assert result['refund_triggered'] == False, "Expected no refund for positive review"
        print("✓ Test passed: Positive review did not trigger refund")
    else:
        print("✗ Test failed")

def test_submit_neutral_review():
    """Test submitting a neutral review"""
    print("\n=== Test 3: Submitting Neutral Review ===")
    data = {
        "customer_id": "test_customer_3",
        "amount": 75.00,
        "review": "The product is okay. Nothing special, but it works as expected."
    }
    
    response = requests.post(f"{BASE_URL}/submit_review", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()
        assert result['sentiment'] in ['neutral', 'positive', 'negative'], "Expected valid sentiment"
        print("✓ Test passed: Neutral review processed")
    else:
        print("✗ Test failed")

def test_get_reviews():
    """Test getting all reviews"""
    print("\n=== Test 4: Getting All Reviews ===")
    response = requests.get(f"{BASE_URL}/reviews")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        reviews = response.json()
        print(f"Total Reviews: {len(reviews)}")
        print("✓ Test passed: Successfully retrieved reviews")
        return True
    else:
        print("✗ Test failed")
        return False

def test_get_transactions():
    """Test getting all transactions"""
    print("\n=== Test 5: Getting All Transactions ===")
    response = requests.get(f"{BASE_URL}/transactions")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        transactions = response.json()
        print(f"Total Transactions: {len(transactions)}")
        print("✓ Test passed: Successfully retrieved transactions")
        return True
    else:
        print("✗ Test failed")
        return False

def test_get_stats():
    """Test getting statistics"""
    print("\n=== Test 6: Getting Statistics ===")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"Statistics: {json.dumps(stats, indent=2)}")
        print("✓ Test passed: Successfully retrieved statistics")
        return True
    else:
        print("✗ Test failed")
        return False

def test_process_refund(transaction_id):
    """Test processing a refund"""
    if not transaction_id:
        print("\n=== Test 7: Processing Refund ===")
        print("Skipped: No transaction ID available")
        return
    
    print("\n=== Test 7: Processing Refund ===")
    response = requests.post(f"{BASE_URL}/process_refund/{transaction_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Test passed: Refund processed successfully")
    else:
        print("✗ Test failed")

def main():
    """Run all tests"""
    print("=" * 50)
    print("SwiftRefund API Test Suite")
    print("=" * 50)
    print("\nMake sure the Flask application is running on http://localhost:5000")
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("Error: Cannot connect to Flask application")
            print("Please make sure the app is running: python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Flask application")
        print("Please make sure the app is running: python app.py")
        return
    
    # Run tests
    transaction_id = test_submit_negative_review()
    test_submit_positive_review()
    test_submit_neutral_review()
    test_get_reviews()
    test_get_transactions()
    test_get_stats()
    test_process_refund(transaction_id)
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)

if __name__ == '__main__':
    main()

