# AI-Assisted Expense Analyzer

## Overview
Upload CSV, categorize transactions, view expense charts, and optionally get AI-powered insights.

## Run Instructions
1. Create virtual environment and install requirements:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Run the server:
```bash
python manage.py runserver
```

3. Open `http://127.0.0.1:8000/` in your browser.

CSV Format:
- Date
- Description
- Amount
