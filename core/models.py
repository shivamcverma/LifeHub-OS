from django.db import models
from django.contrib.auth.models import User

# Step 2: Database Models
# These models store all the personal life data for each user.

DOCUMENT_CATEGORIES = [
    ('ID', 'Identity (Aadhaar, PAN, etc.)'),
    ('FIN', 'Financial (Bank, Tax)'),
    ('EDU', 'Educational'),
    ('MED', 'Medical'),
    ('OTH', 'Other'),
]

EXPENSE_CATEGORIES = [
    ('FOOD', 'Food & Dining'),
    ('TRAVEL', 'Travel & Transport'),
    ('BILLS', 'Bills & Utilities'),
    ('SHOP', 'Shopping'),
    ('HEALTH', 'Health & Fitness'),
    ('ENT', 'Entertainment'),
    ('OTH', 'Other'),
]

class Document(models.Model):
    """Stores uploaded files like IDs, medical reports, etc."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=10, choices=DOCUMENT_CATEGORIES, default='OTH')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class Expense(models.Model):
    """Tracks daily expenses and categories."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=EXPENSE_CATEGORIES, default='OTH')
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.category} expense: {self.amount}"

class Reminder(models.Model):
    """Life event reminders with priority and due dates."""
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    """Tracks recurring service costs like Netflix, Gym, etc."""
    CYCLE_CHOICES = [
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    service_name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=1, choices=CYCLE_CHOICES, default='M')
    next_renewal = models.DateField()

    def __str__(self):
        return self.service_name
