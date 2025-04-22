# analyzer/utils.py

import os
import cohere
from dotenv import load_dotenv
from io import TextIOWrapper
import csv
import cohere
import io

client = cohere.Client("IZmyKWyXUBrgED8Y3YWu3HZ9ROEf8WIp79sPIEOp") 
load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

CATEGORY_KEYWORDS = {
    "Groceries": ["grocery", "supermarket", "store", "mart", "big bazaar"],
    "Transport": ["uber", "ola", "taxi", "bus", "train", "metro", "ride"],
    "Food": ["zomato", "swiggy", "dominos", "cafe", "restaurant", "snack"],
    "Entertainment": ["movie", "netflix", "cinema", "game", "prime", "theater"],
    "Utilities": ["electricity", "water", "gas", "internet", "recharge", "bill", "subscription"],
    "Shopping": ["amazon", "flipkart", "clothes", "shopping"],
    "Medical": ["pharmacy", "hospital", "medical"],
    "Fitness": ["gym", "fitness"],
}

def categorize_transaction(description):
    desc = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in desc for kw in keywords):
            return category
    return "Others"

def custom_parse_csv(file):
    decoded_file = file.read().decode('utf-8') 
    file.seek(0)  
    data = []
    required_fields = {'Date', 'Description', 'Amount'}
    reader = csv.DictReader(io.StringIO(decoded_file))  

    if not required_fields.issubset(reader.fieldnames):
        raise ValueError("CSV missing required columns: Date, Description, Amount")

    for row in reader:
        try:
            amount = float(row['Amount'])
            description = row['Description']
            category = categorize_transaction(description)
            data.append({
                'date': row['Date'],
                'description': description,
                'amount': amount,
                'category': category,
            })
        except (ValueError, KeyError):
            continue

    return data


def generate_ai_insight(summary_dict):
    """
    summary_dict: e.g., {'Dining': 320, 'Groceries': 150}
    Returns: plain language AI-generated insight
    """
    if not summary_dict:
        return "No data available for generating AI insights."

    spending_text = ", ".join([f"{k}: ₹{v:.2f}" for k, v in summary_dict.items()])
    prompt = (
        f"Here is a summary of my monthly spending: {spending_text}. "
        f"Give me 1-2 plain language insights about my spending habits."
    )

    try:
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"⚠️ AI failed: {str(e)}"
