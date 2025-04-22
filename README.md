
# AI Expense Analyzer

A Django-based web application that analyzes your expenses from a CSV file, categorizes them, visualizes the data, and generates AI-powered insights using the Cohere API.

---

## 🚀 Features

- Upload and parse CSV files containing expenses.
- Categorize transactions automatically using keyword matching.
- Visualize spending by category using pie charts.
- Generate AI-powered summaries based on your expenses using Cohere.
- Handle edge cases like empty or invalid CSV files.

---

## 📁 Project Structure

```
expense_analyzer/
├── analyzer/               # Main Django app
├── expense_analyzer/       # Project settings
├── test_files/             # Sample test CSV files (valid, invalid, empty)
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, etc.)
├── htmlcov/                # Coverage report
├── .env                    # Environment variables (OpenAI/Cohere API keys)
├── .coverage               # Coverage data
├── manage.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/geerthikumar2100/ai-expense-analyzer.git
cd ai-expense-analyzer
```

2. **Create and activate virtual environment**

```bash
python -m venv env
env\Scripts\activate  # On Windows
# source env/bin/activate  # On Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory and add your Cohere API key:

```
COHERE_API_KEY=your-api-key-here
```

5. **Run the development server**

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🧪 Running Tests

Run unit tests with:

```bash
python manage.py test
```

Generate test coverage:

```bash
coverage run manage.py test
coverage html
```

Open the `htmlcov/index.html` file in your browser to view the report.

---

## 🧼 Resetting Uploaded CSV File

To delete the previously uploaded CSV file, click the red "Delete Uploaded CSV" button after uploading and viewing the analysis.

---


## 📂 Test CSV Files

Inside the `test_files/` folder:

- `valid.csv`: A sample with correct expense data.
- `invalid.csv`: Contains incorrect or corrupt entries for testing error handling.
- `empty.csv`: Used to test how the app handles empty file uploads.

You can use these files to try different upload scenarios.

---

## 🖥️ Dashboard

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to:

- Upload your expense CSV.
- View parsed transactions.
- Analyze category-wise spending.
- Generate AI-powered insights.

---

## 📦 Dependencies

- Django
- matplotlib
- pandas
- python-dotenv
- cohere 
---


## 🧠 AI Integration (Cohere)

This app uses [Cohere](https://cohere.com/) to summarize your expenses using natural language. You can get your API key from their website and paste it in the `.env` file.

---

## 💡 Example Insight

> Based on your transactions, it seems you're spending the most on Food and Shopping. Consider reducing dine-outs or online purchases to improve savings.

---

## 💡 Future Improvements

- Add user authentication
- Track monthly budgets
- Export insights as PDF

---


## 🙌 Contributions

Feel free to fork and raise a PR! For major changes, open an issue first to discuss.

---

## 📃 License

This project is licensed under the MIT License.
