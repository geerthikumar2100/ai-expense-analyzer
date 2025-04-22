# analyzer/views.py

import csv
import io
import base64
import matplotlib.pyplot as plt

from django.shortcuts import render
from .forms import UploadCSVForm
from .utils import categorize_transaction, generate_ai_insight
import os
from django.conf import settings
from django.shortcuts import redirect
from .models import ExpenseData  


def dashboard_view(request):
    form = UploadCSVForm()
    summary = []
    chart = None
    insight = None
    ai_insight = None
    error = None

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES.get('file')
                if not file.name.lower().endswith('.csv'):
                    raise ValueError("Uploaded file is not a CSV file.")

                wrapper = io.TextIOWrapper(file, encoding='utf-8')
                reader = csv.DictReader(wrapper)
                required_fields = ['Date', 'Description', 'Amount']
                if not reader.fieldnames or any(field not in reader.fieldnames for field in required_fields):
                    raise ValueError(
                        f"CSV missing required columns. Make sure it has: {', '.join(required_fields)}."
                    )

                for row in reader:
                    if not all(key in row for key in required_fields):
                        continue  
                    try:
                        amount = float(row['Amount'])
                    except ValueError:
                        continue  

                    category = categorize_transaction(row['Description'])
                    summary.append({
                        'date': row['Date'],
                        'description': row['Description'],
                        'amount': amount,
                        'category': category
                    })

                if not summary:
                    raise ValueError("No valid transactions found in the uploaded CSV.")

                totals = {}
                for item in summary:
                    totals.setdefault(item['category'], 0)
                    totals[item['category']] += item['amount']

                fig, ax = plt.subplots()
                ax.pie(totals.values(), labels=totals.keys(), autopct='%1.1f%%')
                ax.axis('equal')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close(fig)
                buf.seek(0)
                chart = base64.b64encode(buf.read()).decode('utf-8')

                
                overall = sum(totals.values())
                top_category, top_amount = max(totals.items(), key=lambda x: x[1])
                top_pct = (top_amount / overall) * 100 if overall else 0
                insight = (
                    f"You spent the most on {top_category} "
                    f"(₹{top_amount:.2f}, {top_pct:.1f}% of total)."
                )

                
                ai_insight = generate_ai_insight(totals)

            except Exception as e:
                error = f"⚠️ Error: {e}"

    
    if not ai_insight:
        ai_insight = "AI insight unavailable."

    return render(request, 'dashboard.html', {
        'form': form,
        'summary': summary,
        'chart': chart,
        'insight': insight,
        'ai_insight': ai_insight,
        'error': error,
    })


def delete_csv(request):
    if request.method == 'POST':
        file_path = os.path.join('media', 'uploaded_expenses.csv')
        if os.path.exists(file_path):
            os.remove(file_path)
        request.session.flush()  # Clear session-stored data if any
    return redirect('dashboard')
