
# Snowbird Development Guide

This guide provides detailed information for developers working on the Snowbird Financial Assistant.

## 🏗️ Architecture Overview

### Application Structure

```
Snowbird Financial Assistant
├── Frontend Layer (Streamlit)
│   ├── Interactive UI Components
│   ├── Real-time Data Visualization  
│   └── Progressive Web App (PWA)
├── Business Logic Layer (Python)
│   ├── Tax Residency Calculations
│   ├── Budget Management
│   ├── Location Tracking
│   └── AI Integration
├── Data Layer
│   ├── Session State Management
│   ├── Firebase Firestore (optional)
│   └── Local Storage Fallback
└── Security Layer
    ├── Session Management
    ├── Data Encryption
    └── Privacy Controls
```

### Core Components

#### 1. Data Models (`utils/data_models.py`)
- **Purpose**: Pydantic models for type safety and validation
- **Key Classes**: 
  - `SnowbirdData`: Main user data container
  - `LocationEntry`: Daily location tracking
  - `BudgetCategory`: Expense categorization
  - `TaxResidencyStatus`: Compliance calculations

#### 2. UI Components (`components/`)
- **Dashboard** (`dashboard.py`): Main overview interface
- **Day Tracker** (`day_tracker.py`): Location logging interface
- **Styles** (`styles.py`): CSS theming and visual design
- **Analytics** (`analytics.py`): User behavior tracking

#### 3. Business Logic (`utils/`)
- **Security** (`security.py`): Session and data protection
- **Firebase Auth** (`firebase_auth.py`): User authentication
- **Gmail Parser** (`gmail_parser.py`): Travel detection
- **Onboarding** (`onboarding.py`): First-time user experience

## 🔧 Development Setup

### Local Development Environment

1. **Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Development Tools**:
   ```bash
   pip install black flake8 pytest pytest-cov mypy
   ```

3. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

4. **Run Development Server**:
   ```bash
   streamlit run main.py --server.port 5000 --server.address 0.0.0.0
   ```

### Replit Development

For Replit-specific development:

1. **Secrets Management**: Use the Secrets tool for API keys
2. **Port Configuration**: Use port 5000 for web applications
3. **File Watching**: Streamlit auto-reloads on file changes
4. **Database**: Firebase Firestore recommended for persistence

## 🎯 Feature Development

### Adding New Features

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow TDD Process**:
   - Write tests first (`tests/test_your_feature.py`)
   - Implement feature logic (`utils/your_feature.py`)
   - Create UI component (`components/your_feature.py`)
   - Integrate into main app (`main.py`)

3. **Example: Adding Expense Tracking**:
   ```python
   # tests/test_expense_tracking.py
   def test_expense_calculation():
       tracker = ExpenseTracker()
       assert tracker.calculate_monthly_total("Arizona") == 450
   
   # utils/expense_tracker.py
   class ExpenseTracker:
       def calculate_monthly_total(self, state: str) -> float:
           # Implementation here
           
   # components/expense_dashboard.py
   def render_expense_dashboard():
       # Streamlit UI here
   ```

### UI Component Guidelines

#### Streamlit Best Practices

1. **State Management**:
   ```python
   # Initialize state
   if 'expense_data' not in st.session_state:
       st.session_state.expense_data = {}
   
   # Update state
   if st.button("Add Expense"):
       st.session_state.expense_data[category] = amount
       st.rerun()  # Trigger re-render
   ```

2. **Form Handling**:
   ```python
   with st.form("expense_form"):
       category = st.selectbox("Category", ["Utilities", "Insurance"])
       amount = st.number_input("Amount", min_value=0.0)
       submitted = st.form_submit_button("Submit")
       
       if submitted:
           save_expense(category, amount)
   ```

3. **Error Handling**:
   ```python
   try:
       result = calculate_taxes()
       st.success("Calculation completed!")
   except ValueError as e:
       st.error(f"Invalid input: {e}")
   except Exception as e:
       st.error("An unexpected error occurred. Please try again.")
       logger.exception("Tax calculation error", exc_info=e)
   ```

### Data Flow Patterns

#### 1. User Input → Validation → Processing → Display

```python
def handle_location_input():
    # 1. User Input
    location = st.selectbox("Location", ["Arizona", "Minnesota"])
    date = st.date_input("Date")
    
    # 2. Validation
    if validate_location_data(location, date):
        # 3. Processing
        result = process_location_entry(location, date)
        # 4. Display
        st.success(f"Logged {location} for {date}")
    else:
        st.error("Invalid location data")
```

#### 2. Async Operations with Loading States

```python
def handle_ai_query():
    query = st.text_input("Ask a question:")
    
    if st.button("Get Answer"):
        with st.spinner("Thinking..."):
            try:
                response = get_ai_response(query)
                st.write(response)
            except Exception as e:
                st.error("AI service unavailable")
```

## 🧪 Testing Strategy

### Test Categories

1. **Unit Tests**: Individual function testing
2. **Integration Tests**: Component interaction testing
3. **End-to-End Tests**: Full user workflow testing
4. **Performance Tests**: Load and responsiveness testing

### Testing Patterns

#### Tax Logic Testing
```python
@pytest.mark.parametrize("days,expected", [
    (0, "SAFE"),
    (150, "CAUTION"), 
    (175, "CRITICAL"),
    (183, "TAX_RESIDENT")
])
def test_residency_status(days, expected):
    status = calculate_residency_status(days)
    assert status == expected
```

#### UI Component Testing
```python
def test_dashboard_rendering():
    # Mock session state
    st.session_state.states = {"Arizona": 45, "Minnesota": 30}
    
    # Render component
    render_dashboard()
    
    # Verify outputs (using Streamlit testing utilities)
    assert "Arizona: 45 days" in st.get_text_content()
```

### Mocking External Services

```python
@pytest.fixture
def mock_openai():
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            'choices': [{'message': {'content': 'Test response'}}]
        }
        yield mock

def test_ai_integration(mock_openai):
    response = get_ai_advice("test question")
    assert response == "Test response"
    mock_openai.assert_called_once()
```

## 🔒 Security Considerations

### Data Protection

1. **Sensitive Data Handling**:
   ```python
   # Encrypt before storage
   encrypted_data = encrypt_user_data(financial_info)
   
   # Use secure session state
   if 'secure_token' not in st.session_state:
       st.session_state.secure_token = generate_secure_token()
   ```

2. **Input Validation**:
   ```python
   def validate_tax_input(days: int) -> bool:
       if not isinstance(days, int):
           raise ValueError("Days must be an integer")
       if days < 0 or days > 365:
           raise ValueError("Days must be between 0 and 365")
       return True
   ```

3. **API Key Management**:
   ```python
   # Use environment variables or Streamlit secrets
   api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
   if not api_key:
       st.warning("API key not configured")
       return
   ```

### Session Security

```python
class SessionSecurity:
    @staticmethod
    def check_session_validity():
        """Check if current session is still valid"""
        if 'session_start' not in st.session_state:
            return False
        
        # Session expires after 24 hours of inactivity
        session_age = time.time() - st.session_state.session_start
        return session_age < 86400  # 24 hours
```

## 📊 Performance Optimization

### Streamlit Performance Tips

1. **Caching Expensive Operations**:
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def calculate_year_summary(location_data):
       # Expensive calculation here
       return summary_data
   ```

2. **Lazy Loading**:
   ```python
   # Only load data when needed
   if st.button("Generate Report"):
       with st.spinner("Generating..."):
           report = generate_detailed_report()
           st.download_button("Download", report)
   ```

3. **State Management**:
   ```python
   # Minimize session state size
   if 'large_dataset' in st.session_state:
       # Process and remove large data
       processed = process_data(st.session_state.large_dataset)
       del st.session_state.large_dataset
       st.session_state.processed_data = processed
   ```

## 🚀 Deployment

### Replit Deployment

1. **Configuration**: Use `.replit` for run commands
2. **Secrets**: Store API keys in Replit Secrets
3. **Dependencies**: Ensure `requirements.txt` is complete
4. **Port**: Use port 5000 for web applications

### Environment Configuration

```python
# config.py
import os
from typing import Optional

class Config:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.tax_threshold = int(os.getenv("TAX_THRESHOLD", "183"))

config = Config()
```

## 📝 Code Style Guide

### Python Standards

1. **Type Hints**:
   ```python
   def calculate_tax_status(days: int, threshold: int = 183) -> str:
       """Calculate tax residency status."""
       return "SAFE" if days < threshold else "TAX_RESIDENT"
   ```

2. **Error Handling**:
   ```python
   def process_user_data(data: Dict[str, Any]) -> Optional[UserProfile]:
       try:
           return UserProfile.parse_obj(data)
       except ValidationError as e:
           logger.warning(f"Invalid user data: {e}")
           return None
       except Exception as e:
           logger.error(f"Unexpected error processing user data: {e}")
           raise
   ```

3. **Documentation**:
   ```python
   def calculate_residency_risk(current_days: int, target_days: int) -> float:
       """
       Calculate the risk of exceeding tax residency threshold.
       
       Args:
           current_days: Days already spent in state
           target_days: Maximum days planned for the year
           
       Returns:
           Risk percentage (0.0 to 1.0)
           
       Raises:
           ValueError: If current_days or target_days is negative
       """
   ```

### Git Workflow

1. **Commit Messages**:
   ```
   feat(dashboard): add expense tracking visualization
   
   - Add pie chart for expense categories
   - Implement monthly/yearly view toggle
   - Add export functionality for expense data
   
   Closes #123
   ```

2. **Branch Naming**:
   - `feature/add-expense-tracking`
   - `bugfix/fix-tax-calculation`
   - `docs/update-readme`

## 🔍 Debugging

### Common Issues

1. **Session State Problems**:
   ```python
   # Debug session state
   st.sidebar.write("Debug Info:")
   st.sidebar.json(dict(st.session_state))
   ```

2. **API Connection Issues**:
   ```python
   # Test API connectivity
   try:
       response = test_api_connection()
       st.success("API connected successfully")
   except Exception as e:
       st.error(f"API connection failed: {e}")
   ```

3. **Performance Issues**:
   ```python
   import time
   
   start_time = time.time()
   expensive_operation()
   execution_time = time.time() - start_time
   st.write(f"Operation took {execution_time:.2f} seconds")
   ```

### Logging Strategy

```python
import logging
from utils.logging_config import get_logger

logger = get_logger(__name__)

def process_financial_data():
    logger.info("Starting financial data processing")
    try:
        # Processing logic
        logger.debug("Processing step 1 complete")
        result = calculate_taxes()
        logger.info("Financial processing completed successfully")
        return result
    except Exception as e:
        logger.error(f"Financial processing failed: {e}", exc_info=True)
        raise
```

## 🤝 Contributing Workflow

1. **Issue First**: Create or find an issue before starting work
2. **Feature Branch**: Create descriptive branch names
3. **Tests First**: Write tests before implementation
4. **Code Review**: All changes require review
5. **Documentation**: Update docs for new features

This development guide should help you contribute effectively to Snowbird. For questions or clarifications, please open an issue or discussion on GitHub.
