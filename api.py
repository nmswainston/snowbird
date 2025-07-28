
"""
Snowbird Financial Assistant - REST API
Exposes core data via REST endpoints for external integrations.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import json
import os
import uvicorn
import threading
import streamlit as st
from utils.data_persistence import load_user_data, save_user_data, get_data_file_info
from utils.logging_config import data_logger
from components.session_state import initialize_session_state

# Initialize FastAPI app
app = FastAPI(
    title="Snowbird Financial Assistant API",
    description="REST API for accessing Snowbird app data and functionality",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class LogEntry(BaseModel):
    """Model for residency log entry"""
    state: str = Field(..., description="State name (e.g., 'Arizona', 'Minnesota')")
    date: str = Field(..., description="Date in ISO format (YYYY-MM-DD)")
    notes: Optional[str] = Field(None, description="Optional notes for the log entry")

class LogResponse(BaseModel):
    """Response model for log operations"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# Global session state management for API
api_session_state = {
    'states': {"Arizona": 0, "Minnesota": 0},
    'home_budgets': {
        "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100, "Maintenance": 75},
        "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90, "Maintenance": 100}
    },
    'seasonal_cash_flow': {
        "Travel": 500, "Healthcare": 400, "Supplemental Insurance": 200, "Emergency Fund": 300
    },
    'day_log': [],
    'tax_threshold': 183
}

def load_api_data():
    """Load data from file system into API session state"""
    try:
        # Load existing data if available
        if os.path.exists("user_data/snowbird_data.json"):
            with open("user_data/snowbird_data.json", 'r') as f:
                data = json.load(f)
                api_session_state.update({
                    'states': data.get('states', api_session_state['states']),
                    'home_budgets': data.get('home_budgets', api_session_state['home_budgets']),
                    'seasonal_cash_flow': data.get('seasonal_cash_flow', api_session_state['seasonal_cash_flow']),
                    'day_log': data.get('day_log', []),
                    'tax_threshold': data.get('tax_threshold', 183)
                })
        data_logger.info("API data loaded successfully")
    except Exception as e:
        data_logger.error(f"Failed to load API data: {e}")

def save_api_data():
    """Save API session state to file system"""
    try:
        os.makedirs("user_data", exist_ok=True)
        with open("user_data/snowbird_data.json", 'w') as f:
            json.dump({
                'states': api_session_state['states'],
                'home_budgets': api_session_state['home_budgets'],
                'seasonal_cash_flow': api_session_state['seasonal_cash_flow'],
                'day_log': api_session_state['day_log'],
                'tax_threshold': api_session_state['tax_threshold'],
                'last_saved': datetime.now().isoformat()
            }, f, indent=2)
        data_logger.info("API data saved successfully")
    except Exception as e:
        data_logger.error(f"Failed to save API data: {e}")

# Initialize data on startup
load_api_data()

@app.on_event("startup")
async def startup_event():
    """Initialize API on startup"""
    data_logger.info("Snowbird API starting up...")
    load_api_data()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return HTMLResponse("""
    <html>
        <head><title>Snowbird Financial Assistant API</title></head>
        <body>
            <h1>❄️ Snowbird Financial Assistant API 🏖️</h1>
            <p>REST API for accessing Snowbird app data</p>
            <ul>
                <li><a href="/docs">API Documentation (Swagger)</a></li>
                <li><a href="/redoc">API Documentation (ReDoc)</a></li>
                <li><a href="/logs">View Residency Logs</a></li>
                <li><a href="/budgets">View Budget Data</a></li>
                <li><a href="/health">Health Check</a></li>
            </ul>
        </body>
    </html>
    """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "data_file_exists": os.path.exists("user_data/snowbird_data.json")
    }

@app.get("/logs")
async def get_logs():
    """
    GET /logs - Returns JSON of all residency logs
    
    Returns:
        - Current state counts (days spent in each state)
        - Detailed log entries with dates and locations
        - Tax residency status based on threshold
    """
    try:
        load_api_data()  # Refresh data from file
        
        # Calculate tax residency status
        tax_status = {}
        for state, days in api_session_state['states'].items():
            tax_status[state] = {
                "days": days,
                "is_tax_resident": days >= api_session_state['tax_threshold'],
                "days_until_threshold": max(0, api_session_state['tax_threshold'] - days),
                "percentage": round((days / 365) * 100, 1)
            }
        
        return {
            "success": True,
            "data": {
                "state_totals": api_session_state['states'],
                "detailed_logs": api_session_state['day_log'],
                "tax_threshold": api_session_state['tax_threshold'],
                "tax_status": tax_status,
                "total_logged_days": sum(api_session_state['states'].values()),
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        data_logger.error(f"Error fetching logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {str(e)}")

@app.get("/budgets")
async def get_budgets():
    """
    GET /budgets - Returns budgets JSON
    
    Returns:
        - Home budgets by property (monthly costs by category)
        - Seasonal cash flow items
        - Total budget calculations and analysis
    """
    try:
        load_api_data()  # Refresh data from file
        
        # Calculate budget totals and analysis
        total_home_budget = sum(sum(budget.values()) for budget in api_session_state['home_budgets'].values())
        total_seasonal = sum(api_session_state['seasonal_cash_flow'].values())
        
        # Budget breakdown by category across all properties
        category_totals = {}
        for home, budget in api_session_state['home_budgets'].items():
            for category, amount in budget.items():
                category_totals[category] = category_totals.get(category, 0) + amount
        
        return {
            "success": True,
            "data": {
                "home_budgets": api_session_state['home_budgets'],
                "seasonal_cash_flow": api_session_state['seasonal_cash_flow'],
                "analysis": {
                    "total_monthly_home_budget": total_home_budget,
                    "total_monthly_seasonal": total_seasonal,
                    "total_monthly_combined": total_home_budget + total_seasonal,
                    "annual_estimate": (total_home_budget + total_seasonal) * 12,
                    "category_breakdown": category_totals,
                    "property_count": len(api_session_state['home_budgets'])
                },
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        data_logger.error(f"Error fetching budgets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch budgets: {str(e)}")

@app.post("/logs")
async def add_log_entry(log_entry: LogEntry, background_tasks: BackgroundTasks):
    """
    POST /logs - Accepts JSON to add a residency log entry
    
    Expected JSON format:
    {
        "state": "Arizona",
        "date": "2024-01-15",
        "notes": "Optional notes"
    }
    
    Automatically updates state day counts and saves data.
    """
    try:
        # Validate state name
        if log_entry.state not in api_session_state['states']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid state '{log_entry.state}'. Must be one of: {list(api_session_state['states'].keys())}"
            )
        
        # Validate and parse date
        try:
            log_date = datetime.fromisoformat(log_entry.date).date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD format."
            )
        
        # Check if log entry for this date already exists
        existing_log = next(
            (log for log in api_session_state['day_log'] 
             if log['date'] == log_entry.date and log['state'] == log_entry.state), 
            None
        )
        
        if existing_log:
            return LogResponse(
                success=False,
                message=f"Log entry already exists for {log_entry.state} on {log_entry.date}",
                data={"existing_entry": existing_log}
            )
        
        # Create new log entry
        new_log = {
            "state": log_entry.state,
            "date": log_entry.date,
            "notes": log_entry.notes or "",
            "created_at": datetime.now().isoformat()
        }
        
        # Update session state
        api_session_state['day_log'].append(new_log)
        api_session_state['states'][log_entry.state] += 1
        
        # Save data in background
        background_tasks.add_task(save_api_data)
        
        # Check for tax residency warning
        days_in_state = api_session_state['states'][log_entry.state]
        tax_warning = None
        if days_in_state >= api_session_state['tax_threshold']:
            tax_warning = f"Warning: You may now be considered a tax resident of {log_entry.state} ({days_in_state} days >= {api_session_state['tax_threshold']} day threshold)"
        
        data_logger.info(f"Added log entry: {log_entry.state} on {log_entry.date}")
        
        return LogResponse(
            success=True,
            message=f"Successfully logged day in {log_entry.state}",
            data={
                "log_entry": new_log,
                "current_state_total": days_in_state,
                "tax_warning": tax_warning
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        data_logger.error(f"Error adding log entry: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add log entry: {str(e)}")

@app.get("/stats")
async def get_statistics():
    """
    GET /stats - Returns comprehensive statistics and analytics
    """
    try:
        load_api_data()
        
        total_days = sum(api_session_state['states'].values())
        total_budget = sum(sum(budget.values()) for budget in api_session_state['home_budgets'].values())
        
        return {
            "success": True,
            "data": {
                "residency_stats": {
                    "total_logged_days": total_days,
                    "days_by_state": api_session_state['states'],
                    "tax_threshold": api_session_state['tax_threshold']
                },
                "budget_stats": {
                    "total_monthly_budget": total_budget,
                    "annual_estimate": total_budget * 12,
                    "property_count": len(api_session_state['home_budgets'])
                },
                "generated_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        data_logger.error(f"Error generating statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate statistics: {str(e)}")

def run_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server"""
    try:
        data_logger.info(f"Starting Snowbird API server on {host}:{port}")
        uvicorn.run(
            "api:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info"
        )
    except Exception as e:
        data_logger.error(f"Failed to start API server: {e}")

if __name__ == "__main__":
    # Run API server directly
    run_api_server()
