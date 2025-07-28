
# ❄️ Snowbird: Your Seasonal Financial Assistant

A mobile-optimized Streamlit web application designed for people who split time between two states (e.g., Arizona and Minnesota). Helps users track tax residency, manage dual-home budgets, and plan seasonal expenses with clarity and ease.

## 🔷 Features

- **Residency Tracker**: Log days in different states with visual progress tracking
- **Tax Risk Assessment**: Monitor your proximity to the 183-day tax residency threshold
- **Dual-Home Budgets**: Manage budgets for multiple residences
- **Seasonal Cash Flow**: Plan travel, healthcare, and emergency expenses
- **AI Financial Assistant**: Get personalized financial advice
- **Reports & Export**: Generate downloadable residency reports
- **Migration Checklists**: Organize tasks when moving between homes

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Streamlit
- OpenAI API key (optional, for AI features)

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run main.py --server.port 5000 --server.address 0.0.0.0
   ```

## 🧪 Running Tests

This project uses pytest for testing. The test suite includes:

- **Tax Logic Tests**: Validation of residency status calculations
- **State Management Tests**: Testing of day logging and state tracking
- **Integration Tests**: End-to-end functionality verification

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests with Coverage Report

```bash
pip install pytest-cov
pytest --cov=utils --cov=components --cov-report=html
```

### Run Specific Test Files

```bash
# Test tax residency logic only
pytest tests/test_tax_logic.py

# Test state management only
pytest tests/test_state_management.py
```

### Run Tests in Quiet Mode (CI/CD)

```bash
pytest --maxfail=1 --disable-warnings -q
```

## 📊 Test Coverage

The test suite covers:

- ✅ Tax residency status calculations (SAFE, CAUTION, CRITICAL, TAX RESIDENT)
- ✅ Percentage calculations for residency thresholds
- ✅ Day logging functionality and state increment logic
- ✅ Duplicate date logging prevention
- ✅ Report generation and data structure validation
- ✅ Edge cases and error handling

## 🔧 Development

### Project Structure

```
snowbird-app/
├── components/          # UI components
├── utils/              # Business logic and data models
├── tests/              # Test suite
├── .github/workflows/  # CI/CD pipelines
├── main.py            # Application entry point
└── requirements.txt   # Python dependencies
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📱 Progressive Web App (PWA)

This application is configured as a PWA and can be installed on mobile devices for a native app-like experience.

## 🔐 Security & Privacy

- API keys are managed through environment variables
- No personal financial data is stored permanently
- All data remains in your browser session

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Built with ❤️ and ❄️ for seasonal residents everywhere, helping snowbirds fly south (and north) with confidence.

---

**Disclaimer**: This tool is for informational purposes only and should not be considered professional tax or financial advice. Consult with qualified professionals for your specific situation.
