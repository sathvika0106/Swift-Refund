"""
Setup script to download required NLTK data for TextBlob
Run this script once before using the application
"""
import nltk

def download_nltk_data():
    """Download required NLTK data files"""
    print("Downloading NLTK data files...")
    
    try:
        nltk.download('punkt', quiet=True)
        print("✓ Downloaded punkt")
        
        nltk.download('brown', quiet=True)
        print("✓ Downloaded brown")
        
        nltk.download('wordnet', quiet=True)
        print("✓ Downloaded wordnet")
        
        nltk.download('stopwords', quiet=True)
        print("✓ Downloaded stopwords")
        
        print("\nAll NLTK data downloaded successfully!")
        print("You can now run the Flask application with: python app.py")
        
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        print("Please check your internet connection and try again.")

if __name__ == '__main__':
    download_nltk_data()

