# AI Expense Analyzer

## Overview

The **AI Expense Analyzer** is a web application built with Django to help users analyze and optimize their monthly expenses. Users can upload CSV files containing their transaction data, which the app parses, categorizes, and visualizes. Additionally, the app provides AI-powered insights to guide better spending and budgeting habits.

## Features

- **CSV Upload & Parsing**: Upload CSV files with `Date`, `Description`, and `Amount` columns. The app safely parses and validates entries, skipping malformed rows.
- **Expense Categorization**: Transactions are categorized into predefined groups (e.g., Food, Transport) via keyword matching; uncategorized entries fall under "Others."  
- **Visualization**: Generates a pie chart summarizing spending by category, embedded directly in the dashboard.  
- **AI Insights**: Uses the Cohere API to generate plain‑language insights about spending patterns, with graceful handling of API errors.  
- **Error Handling**: Alerts users to invalid file types, missing columns, or no valid transactions.

## Project Structure

```
AI_Expense_Analyzer_Project/
├── analyzer/                # Main Django app
│   ├── templates/           # HTML templates (dashboard.html)
│   ├── utils.py             # CSV parsing, categorization, AI logic
│   ├── views.py             # Dashboard view
│   ├── forms.py             # UploadCSVForm
│   ├── tests.py             # Unit tests
│   └── urls.py              # App URL routes
├── expense_analyzer/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py                # Django CLI script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (excluded by .gitignore)
└── README.md                # Project documentation
```

## Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/ai-expense-analyzer.git
   cd ai-expense-analyzer
   ```

2. **Install dependencies**
   ```bash
   python3 -m venv env
   source env/bin/activate     # macOS/Linux
   env\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create a `.env` in the project root:
   ```env
   COHERE_API_KEY=<your-cohere-api-key>
   DJANGO_SECRET_KEY=<your-django-secret-key>
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   ```

5. **Run server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/dashboard/`.

## Testing & Coverage

- **Run tests**:
  ```bash
  python manage.py test analyzer
  ```

- **Generate coverage report**:
  ```bash
  coverage run manage.py test analyzer
  coverage report
  coverage html   # opens ./htmlcov/index.html
  ```

## Usage

1. **Upload** a valid CSV on the dashboard.  
2. **View** parsed transactions and category breakdown.  
3. **Analyze** spending with both basic and AI‑powered insights.

## Key Design Decisions

- **Keyword-Based Categorization**: Fast, transparent, and easy to extend with new keywords.  
- **AI Integration**: Provides context‑aware insights; fallback to a user‑friendly error message on failure.  
- **Modular Utils**: `utils.py` contains pure functions for parsing and AI logic, making them easy to test.

## Dependencies

- Django
- cohere-python
- python-dotenv
- matplotlib
- coverage

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

