
from utils.config import settings

def test_config():
    print(f"OPENAI_API_KEY configured: {bool(settings.OPENAI_API_KEY)}")
    print(f"STREAMLIT_PORT: {settings.STREAMLIT_PORT}")
    print(f"STREAMLIT_HOST: {settings.STREAMLIT_HOST}")
    
    # Your assertion test
    assert settings.OPENAI_API_KEY, "Missing OPENAI_API_KEY in .env"
    print("✅ Configuration test passed!")

if __name__ == "__main__":
    test_config()
