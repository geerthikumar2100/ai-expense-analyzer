# analyzer/models.py
from django.db import models

class ExpenseData(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define the primary key
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.date} - {self.description} - {self.amount}'
