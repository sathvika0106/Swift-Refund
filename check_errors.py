"""
Diagnostic script to check for common errors before running the Flask app
"""
import sys

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Current version:", sys.version)
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_imports():
    """Check if all required packages are installed"""
    required_packages = [
        ('flask', 'Flask'),
        ('flask_mysqldb', 'flask-mysqldb'),
        ('textblob', 'TextBlob'),
        ('mysql.connector', 'mysql-connector-python'),
        ('nltk', 'NLTK')
    ]
    
    missing = []
    for module, package_name in required_packages:
        try:
            __import__(module)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is NOT installed")
            missing.append(package_name)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    return True

def check_nltk_data():
    """Check if NLTK data is downloaded"""
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        print("✓ NLTK punkt data found")
        nltk.data.find('corpora/brown')
        print("✓ NLTK brown data found")
        return True
    except LookupError as e:
        print(f"❌ NLTK data missing: {e}")
        print("Run: python setup_nltk.py")
        return False
    except ImportError:
        print("❌ NLTK not installed")
        return False

def check_mysql_connection():
    """Check MySQL connection"""
    import os
    import mysql.connector
    from mysql.connector import Error
    
    host = os.getenv('MYSQL_HOST', 'localhost')
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', 'sath')
    
    print(f"\nAttempting to connect to MySQL...")
    print(f"Host: {host}")
    print(f"User: {user}")
    
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        print("✓ MySQL connection successful")
        conn.close()
        return True
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\nPossible issues:")
        print("1. MySQL server is not running")
        print("2. Incorrect credentials (host, user, password)")
        print("3. MySQL server is not accessible")
        print("\nCheck your MySQL configuration in app.py")
        return False

def check_files():
    """Check if required files exist"""
    import os
    required_files = [
        'app.py',
        'templates/index.html',
        'templates/dashboard.html',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"❌ {file} is missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("=" * 60)
    print("SwiftRefund - Error Diagnostic Tool")
    print("=" * 60)
    
    all_passed = True
    
    print("\n[1/5] Checking Python version...")
    if not check_python_version():
        all_passed = False
    
    print("\n[2/5] Checking required packages...")
    if not check_imports():
        all_passed = False
    
    print("\n[3/5] Checking NLTK data...")
    if not check_nltk_data():
        all_passed = False
    
    print("\n[4/5] Checking MySQL connection...")
    if not check_mysql_connection():
        all_passed = False
    
    print("\n[5/5] Checking required files...")
    if not check_files():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed! You can run the app with: python app.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == '__main__':
    main()

