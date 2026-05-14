# Snowbird

A companion app for snowbirds — helping seasonal travelers manage their away-from-home life.

## Overview

Snowbird is a Python-based web application designed for seasonal travelers (snowbirds) who split their time between two locations. It helps users manage the logistics of being away — tracking tasks, reminders, contacts, and key information for life on the road or in a second home.

## Tech Stack

- Python
- Streamlit
- Firebase (authentication & data)
- GitHub Actions (CI/CD)

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- A Firebase project ([setup guide](FIREBASE_SETUP.md))

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

Copy the example env file and fill in your Firebase credentials:

```bash
cp .env.example .env
```

See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for Firebase configuration steps.

### Running

```bash
streamlit run api.py
```

## Project Structure

```
api.py              # Main Streamlit app entry point
auth_app.py         # Authentication logic
config.py           # App configuration
components/         # UI components
utils/              # Helper utilities
static/             # Static assets
tests/              # Test suite
translations/       # i18n files
docs/               # Documentation
.github/workflows/  # CI/CD pipelines
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

*Built by [nmswainston](https://github.com/nmswainston)*
