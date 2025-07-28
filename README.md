
# ❄️ Snowbird: Your Seasonal Financial Assistant 🏖️

*Empowering snowbirds to manage their multi-state lifestyle with confidence and financial clarity*

A comprehensive, mobile-optimized Streamlit web application designed for people who split time between two states (e.g., Arizona and Minnesota). Snowbird helps users track tax residency, manage dual-home budgets, plan seasonal expenses, and get AI-powered financial guidance—all while maintaining compliance with complex multi-state tax regulations.

## 🎯 Who Snowbird Is For

- **Seasonal Residents ("Snowbirds")**: People who split time between warm and cold climates
- **Multi-State Property Owners**: Anyone managing budgets across multiple residences
- **Tax-Conscious Travelers**: Individuals concerned about state tax residency thresholds
- **Financial Planners**: Professionals managing clients with complex residency situations

## 🔷 Core Features

### 📍 **Residency Tracking & Tax Compliance**
- Daily location logging with visual progress tracking
- Real-time tax risk assessment (183-day threshold monitoring)
- Automated alerts for approaching residency limits
- Comprehensive audit trail for tax documentation

### 💰 **Financial Management**
- Dual-home budget tracking (utilities, insurance, HOA fees)
- Seasonal cash flow planning (travel, healthcare, emergency funds)
- Multi-state expense categorization
- Budget variance analysis and alerts

### 🤖 **AI-Powered Assistance**
- Context-aware financial advice using OpenAI GPT-4
- Personalized recommendations based on your residency patterns
- Tax strategy suggestions
- Seasonal financial planning guidance

### 📊 **Analytics & Reporting**
- Downloadable residency reports for tax preparation
- Visual dashboards with key metrics
- Historical trend analysis
- Compliance status monitoring

### 🎨 **Advanced Features**
- **Intelligent Auto-Tracking**: Gmail integration for travel detection
- **Theme Customization**: Winter/Summer themes with advanced styling
- **User Authentication**: Firebase-powered secure profiles
- **Mobile PWA**: Install as native mobile app
- **Admin Dashboard**: System monitoring and user management

## 🚀 Getting Started

### Prerequisites

- **Python 3.9 or higher** (Python 3.11+ recommended)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Internet connection** for AI features and cloud sync

### Quick Installation

1. **Clone or fork this repository**
   ```bash
   git clone https://github.com/yourusername/snowbird-app.git
   cd snowbird-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py --server.port 5000 --server.address 0.0.0.0
   ```

4. **Open your browser** to `http://localhost:5000`

### 🔧 Configuration

#### Environment Variables (.env file)

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Firebase authentication
FIREBASE_SERVICE_ACCOUNT={"type": "service_account", ...}
FIREBASE_CONFIG={"apiKey": "your-api-key", ...}

# Optional: Gmail integration
GMAIL_CREDENTIALS_FILE=path/to/gmail/credentials.json

# Application settings
ENVIRONMENT=development
DEBUG=true
TAX_THRESHOLD=183
```

#### Replit Secrets (Recommended for Replit deployment)

1. Click on **Tools** → **Secrets**
2. Add the following keys:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `FIREBASE_SERVICE_ACCOUNT`: Firebase service account JSON
   - `FIREBASE_CONFIG`: Firebase client configuration JSON

#### Feature Configuration

- **AI Features**: Requires OpenAI API key
- **User Authentication**: Requires Firebase setup
- **Gmail Integration**: Requires Google API credentials
- **All other features**: Work without additional setup

## 🧪 Testing

Snowbird includes a comprehensive test suite covering tax logic, state management, and integration scenarios.

### Run All Tests
```bash
pytest
```

### Run Tests with Detailed Output
```bash
pytest -v --tb=short
```

### Run Tests with Coverage Report
```bash
pytest --cov=utils --cov=components --cov-report=html
```

### Run Specific Test Categories
```bash
# Tax residency logic tests
pytest tests/test_tax_logic.py

# State management tests  
pytest tests/test_state_management.py

# Integration tests
pytest tests/ -k "integration"
```

### Test Coverage Areas

- ✅ **Tax Residency Calculations**: Status determination (SAFE, CAUTION, CRITICAL, TAX RESIDENT)
- ✅ **Day Logging Logic**: State increment, duplicate prevention, bulk operations
- ✅ **Budget Management**: Multi-home budget tracking and validation
- ✅ **Report Generation**: Data export and audit trail verification
- ✅ **Security Features**: Session management and data protection
- ✅ **Error Handling**: Graceful degradation and user feedback

## 🔄 CI/CD Pipeline

Snowbird uses GitHub Actions for automated testing and deployment:

- **[Python Tests Workflow](.github/workflows/python-tests.yml)**: Runs pytest suite on every push
- **[CI Workflow](.github/workflows/ci.yml)**: Linting, formatting, and security checks
- **[Dependency Updates](.github/workflows/dependency-update.yml)**: Automated dependency management
- **[Health Checks](.github/workflows/streamlit-health-check.yml)**: Application monitoring

View workflow status: [![CI](https://github.com/yourusername/snowbird-app/workflows/CI/badge.svg)](https://github.com/yourusername/snowbird-app/actions)

## 📱 Progressive Web App (PWA)

Snowbird is configured as a PWA for mobile-first usage:

1. **Install on mobile**: Open in browser → Share → "Add to Home Screen"
2. **Offline capability**: Core features work without internet
3. **Native feel**: Full-screen experience with app-like navigation

## 🎨 Architecture & Technology Stack

```
Frontend:     Streamlit (Python-based reactive web framework)
Backend:      Python 3.9+ with Pydantic data models
Database:     Firebase Firestore (optional, with local fallback)
Authentication: Firebase Auth (optional, with demo mode)
AI/ML:        OpenAI GPT-4 API integration
Styling:      Custom CSS with theme system
Testing:      Pytest with comprehensive coverage
CI/CD:        GitHub Actions workflows
Deployment:   Replit (recommended) or any Python hosting platform
```

## 📂 Project Structure

```
snowbird-app/
├── components/              # UI components and widgets
│   ├── analytics.py        # Usage tracking and metrics
│   ├── auth_components.py  # Authentication UI
│   ├── dashboard.py        # Main dashboard views
│   ├── day_tracker.py      # Location logging interface
│   ├── styles.py           # CSS styling and themes
│   └── theme_manager.py    # Advanced theming system
├── utils/                  # Business logic and utilities
│   ├── data_models.py      # Pydantic data structures
│   ├── security.py         # Session security and encryption
│   ├── firebase_auth.py    # Firebase integration
│   ├── gmail_parser.py     # Email travel detection
│   └── onboarding.py       # First-time user experience
├── tests/                  # Comprehensive test suite
├── .github/workflows/      # CI/CD automation
├── main.py                # Application entry point
├── config.py              # Configuration management
└── requirements.txt       # Python dependencies
```

## 🎯 First-Time User Experience

Snowbird includes an interactive onboarding carousel that guides new users through key features:

1. **Welcome & Overview**: Introduction to Snowbird's purpose
2. **Location Logging**: How to track your daily location
3. **Budget Management**: Setting up dual-home budgets
4. **AI Assistant**: Getting personalized financial advice

The onboarding appears automatically for first-time users and can be accessed later via the help menu.

## 🤝 Contributing

We welcome contributions! Please see our **[Contributing Guidelines](CONTRIBUTING.md)** for:

- Code style standards (Black, Flake8)
- Development workflow (feature branches, pull requests)
- Testing requirements
- Issue templates and bug reporting

## 🔐 Security & Privacy

- **Data Protection**: All sensitive data encrypted and stored securely
- **Session Security**: Automatic session expiration and CSRF protection
- **Privacy First**: Personal financial data never leaves your control
- **Audit Trail**: Comprehensive logging for tax compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with ❤️ and ❄️ for seasonal residents everywhere. Special thanks to:

- The Streamlit community for the amazing framework
- OpenAI for powering our AI financial assistant
- Firebase for secure authentication and data sync
- The Python testing community for pytest and coverage tools

---

## 📞 Support & Community

- **Documentation**: Full docs available in `/docs` directory
- **Issues**: Report bugs via [GitHub Issues](https://github.com/yourusername/snowbird-app/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/snowbird-app/discussions)
- **Email**: support@snowbird-app.com

**Disclaimer**: This tool provides informational assistance and should not be considered professional tax or financial advice. Always consult qualified professionals for your specific tax situation.

---

*Helping snowbirds fly between seasons with financial confidence* ❄️🏖️
