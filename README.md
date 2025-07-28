
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

Snowbird is fully configured as a Progressive Web App, providing a native app-like experience:

### 🚀 **Installation**
- **Mobile (iOS/Android)**: Open in browser → Menu → "Add to Home Screen" or "Install App"
- **Desktop (Chrome/Edge)**: Click the install icon in the address bar or browser menu
- **Automatic prompts**: The app will suggest installation when criteria are met

### 💾 **Offline Capabilities**
- **Core Features**: Day tracking, budget viewing, and reports work offline
- **Smart Caching**: Frequently used data is cached automatically
- **Offline Indicator**: Visual feedback when connection is lost
- **Auto-Sync**: Data syncs when connection is restored

### 🎨 **Native Experience**
- **Full-Screen Mode**: No browser UI when installed
- **Custom Splash Screen**: Branded loading experience
- **Theme Integration**: Matches your system theme
- **Hardware Integration**: Uses device capabilities where available

### 🔧 **Technical Implementation**
```
/static/
├── manifest.json        # PWA configuration & metadata
├── sw.js               # Service worker for caching
├── pwa-utils.js        # Installation utilities
├── icon-192.png        # App icon (192x192)
├── icon-512.png        # App icon (512x512)
├── offline.html        # Offline fallback page
└── browserconfig.xml   # Windows tile configuration
```

### 📊 **PWA Features**
- ✅ **Web App Manifest**: Defines app name, icons, and theme
- ✅ **Service Worker**: Caches assets for offline use
- ✅ **Responsive Design**: Optimized for all screen sizes
- ✅ **Install Prompts**: Smart installation suggestions
- ✅ **Update Notifications**: Seamless app updates
- ✅ **Offline Fallbacks**: Graceful offline experience

### 🔍 **Usage Tips**
- **First Load**: May take a moment to cache assets
- **Updates**: Refresh the app to get new features
- **Storage**: App data is stored locally and synced to cloud
- **Performance**: Installed apps typically load faster than web versions

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

## 🚩 Feature Flags

Snowbird uses a flexible feature flags system that allows you to enable/disable features without redeploying:

### Configuration Methods

1. **File-based** (`feature_flags.json`):
   ```json
   {
     "ai_assistant": true,
     "analytics": false,
     "onboarding_carousel": true
   }
   ```

2. **Environment Variables** (prefix with `FF_`):
   ```bash
   FF_AI_ASSISTANT=true
   FF_ANALYTICS=false
   ```

3. **Streamlit Secrets** (`.streamlit/secrets.toml`):
   ```toml
   [feature_flags]
   ai_assistant = true
   analytics = false
   ```

### Available Features

- **Core**: `residency_tracker`, `dual_home_budgets`, `seasonal_cash_flow`
- **AI**: `ai_assistant`, `auto_tracker`, `gmail_integration`
- **UX**: `onboarding_carousel`, `pwa_support`, `theme_customization`
- **Admin**: `analytics`, `admin_dashboard`, `auth`
- **Data**: `reports_export`, `export_data`, `import_data`

### Management

- **Admin Interface**: Access via the Admin tab when `admin_dashboard` is enabled
- **Live Updates**: Changes apply immediately without restart
- **Bulk Operations**: Enable/disable feature sets with one click
- **Session Overrides**: Temporary toggles for testing

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
