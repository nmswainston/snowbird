# Snowbird

A companion app for seasonal travelers — helping snowbirds manage life between two homes.

## Problem

Snowbirds — people who spend part of the year in a warmer location — juggle the logistics of two homes, two sets of contacts, seasonal tasks, and travel planning with no tools built specifically for their lifestyle.

## Solution

Snowbird is a web app built with Python and Streamlit that gives seasonal travelers a central hub for tracking tasks, reminders, key contacts, and home management info for both locations.

## Screenshots

> *Add 2–4 screenshots here*

## Tech Stack

- Python
- Streamlit
- Firebase
- GitHub Actions

## Features

- Task and reminder tracking for both home locations
- Firebase authentication for secure access
- Multi-language support via translation files
- GitHub Actions CI/CD pipeline
- Comprehensive test suite
- Detailed setup and contribution documentation

## Installation

```bash
pip install -r requirements.txt
```

Configure Firebase credentials (see [FIREBASE_SETUP.md](FIREBASE_SETUP.md)):

```bash
cp .env.example .env
streamlit run api.py
```

## Lessons Learned

- Streamlit is remarkably fast for building functional web UIs in Python without frontend overhead
- Firebase Authentication handles the hard parts of auth — worth using even for small projects
- Building with real users in mind (snowbirds are a specific, underserved group) makes design decisions clearer

## Future Improvements

- Mobile app for on-the-go access
- Weather integration for both home locations
- Community features for snowbird communities and parks

---

*Built by [nmswainston](https://github.com/nmswainston)*
