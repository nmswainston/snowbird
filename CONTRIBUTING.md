
# Contributing to Snowbird Financial Assistant

Thank you for your interest in contributing to Snowbird! This document provides guidelines and information for contributors to help maintain code quality and ensure smooth collaboration.

## 🎯 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful, constructive, and professional in all interactions.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/snowbird-app.git
   cd snowbird-app
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install development tools**:
   ```bash
   pip install black flake8 pytest pytest-cov
   ```

### Development Environment

- **Python Version**: 3.9+ (3.11+ recommended)
- **Code Editor**: VS Code, PyCharm, or any editor with Python support
- **Required Tools**: black, flake8, pytest

## 📝 Code Style Guidelines

### Python Code Standards

We follow PEP 8 with specific conventions:

#### Formatting with Black
```bash
# Format all Python files
black .

# Check if files would be formatted
black --check .
```

#### Linting with Flake8
```bash
# Run linting
flake8 .

# Configuration in .flake8 file
```

#### Code Style Requirements

1. **Line Length**: 88 characters (Black default)
2. **Imports**: Group and sort imports logically
3. **Naming Conventions**:
   - Variables and functions: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_CASE`
   - Private methods: `_leading_underscore`

#### Example Code Structure

```python
"""
Module-level docstring explaining the purpose of this module.

This module handles tax residency calculations for multi-state
residents, providing compliance monitoring and risk assessment.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Union

import streamlit as st
from pydantic import BaseModel

from utils.data_models import SnowbirdData


class TaxResidencyCalculator:
    """
    Calculate tax residency status based on days spent in each state.
    
    This class implements the 183-day rule and provides risk assessment
    for users approaching tax residency thresholds.
    """
    
    def __init__(self, threshold_days: int = 183):
        """
        Initialize the tax residency calculator.
        
        Args:
            threshold_days (int): Number of days to trigger tax residency.
                                Default is 183 days per IRS guidelines.
        """
        self.threshold_days = threshold_days
    
    def calculate_status(self, days_in_state: int) -> str:
        """
        Calculate tax residency status for a given state.
        
        Args:
            days_in_state (int): Number of days spent in the state.
            
        Returns:
            str: Status code - 'SAFE', 'CAUTION', 'CRITICAL', or 'TAX_RESIDENT'
            
        Raises:
            ValueError: If days_in_state is negative.
        """
        if days_in_state < 0:
            raise ValueError("Days in state cannot be negative")
        
        # Calculate remaining days until threshold
        remaining_days = self.threshold_days - days_in_state
        
        if days_in_state >= self.threshold_days:
            return 'TAX_RESIDENT'
        elif remaining_days <= 10:  # Critical: within 10 days of threshold
            return 'CRITICAL'
        elif remaining_days <= 30:  # Caution: within 30 days of threshold
            return 'CAUTION'
        else:
            return 'SAFE'
```

### Docstring Conventions

We use Google-style docstrings:

```python
def process_location_data(user_id: str, location_data: Dict[str, int]) -> bool:
    """
    Process and validate location data for a user.
    
    This function takes raw location data, validates it against business rules,
    and updates the user's residency tracking information. It handles duplicate
    date detection and ensures data integrity.
    
    Args:
        user_id (str): Unique identifier for the user.
        location_data (Dict[str, int]): Dictionary mapping state names to day counts.
            Example: {"Arizona": 45, "Minnesota": 23}
    
    Returns:
        bool: True if processing was successful, False otherwise.
        
    Raises:
        ValueError: If location_data contains invalid state names or negative values.
        UserNotFoundError: If user_id does not exist in the system.
        
    Example:
        >>> process_location_data("user123", {"Arizona": 45, "Minnesota": 23})
        True
        
        >>> process_location_data("user123", {"InvalidState": 10})
        ValueError: Invalid state name: InvalidState
    """
    # Implementation here...
```

## 🌿 Branching Workflow

### Branch Naming Convention

- **Feature branches**: `feature/description-of-feature`
- **Bug fixes**: `bugfix/description-of-bug`
- **Documentation**: `docs/description-of-change`
- **Refactoring**: `refactor/description-of-refactor`

### Workflow Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/add-expense-tracking
   ```

2. **Make your changes** following code style guidelines

3. **Write/update tests** for your changes

4. **Run the full test suite**:
   ```bash
   pytest
   black --check .
   flake8 .
   ```

5. **Commit with descriptive messages**:
   ```bash
   git add .
   git commit -m "feat: add expense tracking functionality

   - Add ExpenseTracker component with category support
   - Implement monthly/yearly expense aggregation
   - Add tests for expense calculation logic
   - Update documentation for new features"
   ```

6. **Push and create a Pull Request**:
   ```bash
   git push origin feature/add-expense-tracking
   ```

### Commit Message Format

We follow the Conventional Commits specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(auth): add Firebase authentication support
fix(dashboard): resolve tax calculation edge case
docs(readme): update installation instructions
test(utils): add comprehensive tax logic tests
```

## 🧪 Testing Guidelines

### Writing Tests

1. **Test Location**: Place tests in the `tests/` directory
2. **Test Naming**: Use descriptive names starting with `test_`
3. **Test Structure**: Follow Arrange-Act-Assert pattern

#### Example Test

```python
"""
Tests for tax residency calculation logic.

This module tests the core business logic for determining tax residency
status based on days spent in each state.
"""

import pytest
from utils.tax_calculator import TaxResidencyCalculator


class TestTaxResidencyCalculator:
    """Test cases for TaxResidencyCalculator class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calculator = TaxResidencyCalculator(threshold_days=183)
    
    def test_safe_status_calculation(self):
        """Test that SAFE status is returned for low day counts."""
        # Arrange
        days_in_state = 50
        
        # Act
        status = self.calculator.calculate_status(days_in_state)
        
        # Assert
        assert status == 'SAFE'
    
    def test_tax_resident_status_at_threshold(self):
        """Test that TAX_RESIDENT status is returned at exact threshold."""
        # Arrange
        days_in_state = 183
        
        # Act
        status = self.calculator.calculate_status(days_in_state)
        
        # Assert
        assert status == 'TAX_RESIDENT'
    
    def test_negative_days_raises_error(self):
        """Test that negative days input raises ValueError."""
        # Arrange
        days_in_state = -1
        
        # Act & Assert
        with pytest.raises(ValueError, match="Days in state cannot be negative"):
            self.calculator.calculate_status(days_in_state)
    
    @pytest.mark.parametrize("days,expected_status", [
        (0, 'SAFE'),
        (150, 'CAUTION'),
        (175, 'CRITICAL'),
        (183, 'TAX_RESIDENT'),
        (200, 'TAX_RESIDENT'),
    ])
    def test_status_calculation_parametrized(self, days, expected_status):
        """Test status calculation with multiple input scenarios."""
        status = self.calculator.calculate_status(days)
        assert status == expected_status
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tax_logic.py

# Run with coverage
pytest --cov=utils --cov=components

# Run with verbose output
pytest -v

# Run tests matching a pattern
pytest -k "tax_residency"
```

### Test Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: 95% coverage for tax logic and security features
- **Documentation**: All public functions must have docstring examples that work as doctests

## 📋 Issue Templates

### Bug Report Template

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**
- OS: [e.g. iOS, Windows, Linux]
- Browser: [e.g. chrome, safari]
- Python Version: [e.g. 3.9.7]
- Snowbird Version: [e.g. 1.2.0]

**Additional Context**
Add any other context about the problem here.

**Logs**
```
[Paste any relevant log output here]
```
```

### Feature Request Template

```markdown
**Feature Summary**
A clear and concise description of the feature you'd like to see added.

**Problem Statement**
What problem does this feature solve? Who would benefit from it?

**Proposed Solution**
Describe the solution you'd like to see implemented.

**Alternative Solutions**
Describe any alternative solutions or features you've considered.

**Implementation Details**
If you have ideas about how this could be implemented, share them here.

**Additional Context**
Add any other context, mockups, or examples about the feature request here.

**Acceptance Criteria**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

## 🔄 Pull Request Process

### Before Submitting

1. **Code Quality Checks**:
   ```bash
   black --check .
   flake8 .
   pytest
   ```

2. **Documentation Updates**: Update relevant docs if needed

3. **Test Coverage**: Ensure new code has appropriate test coverage

### Pull Request Template

Your PR description should include:

- **Summary**: Brief description of changes
- **Type of Change**: Bug fix, feature, docs, etc.
- **Testing**: How you tested your changes
- **Checklist**: Completed pre-submission checks

### Review Process

1. **Automated Checks**: CI pipeline must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: All tests must pass
4. **Documentation**: Docs must be updated if needed

## 📚 Development Resources

### Useful Commands

```bash
# Development server
streamlit run main.py --server.port 5000

# Code formatting
black .

# Linting
flake8 .

# Type checking (optional)
mypy utils/ components/

# Security scanning
bandit -r utils/ components/

# Dependency checking
pip-audit
```

### Development Tips

1. **Use type hints** for better code documentation
2. **Write tests first** when fixing bugs (TDD approach)
3. **Keep functions small** and focused on single responsibility
4. **Use meaningful variable names** that explain intent
5. **Comment complex business logic** especially tax calculations

## 🤝 Getting Help

- **GitHub Discussions**: For questions and feature discussions
- **GitHub Issues**: For bug reports and feature requests
- **Code Reviews**: Ask for feedback on approach before implementing large features

Thank you for contributing to Snowbird! Your efforts help make financial management easier for seasonal residents everywhere. 🙏
