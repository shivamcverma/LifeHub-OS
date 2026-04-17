from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date, datetime

from .models import Document, Expense, Reminder, Subscription
from .forms import UserSignupForm, DocumentForm, ExpenseForm, ReminderForm, SubscriptionForm

# Step 3: Backend views (CRUD operations)

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    # Aggregating data for the dashboard
    docs_count = Document.objects.filter(user=request.user).count()
    
    # Smart Insights: Monthly Spending
    current_month = date.today().month
    monthly_spending = Expense.objects.filter(
        user=request.user, 
        date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Upcoming Reminders
    upcoming_reminders = Reminder.objects.filter(
        user=request.user, 
        is_completed=False, 
        date__gte=datetime.now()
    ).order_by('date')[:5]
    
    # Subscriptions Summary
    total_sub_cost = Subscription.objects.filter(user=request.user).aggregate(Sum('cost'))['cost__sum'] or 0
    
    context = {
        'docs_count': docs_count,
        'monthly_spending': monthly_spending,
        'upcoming_reminders': upcoming_reminders,
        'total_sub_cost': total_sub_cost,
    }
    return render(request, 'core/dashboard.html', context)

# --- Document Locker ---

@login_required
def document_list(request):
    documents = Document.objects.filter(user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            messages.success(request, "Document uploaded successfully!")
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'core/documents.html', {'documents': documents, 'form': form})

@login_required
def delete_document(request, pk):
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    doc.delete()
    messages.info(request, "Document deleted.")
    return redirect('document_list')

# --- Expense Tracker ---

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added!")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'core/expenses.html', {'expenses': expenses, 'form': form})

# --- Reminder System ---

@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user).order_by('date')
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            rem = form.save(commit=False)
            rem.user = request.user
            rem.save()
            messages.success(request, "Reminder set!")
            return redirect('reminder_list')
    else:
        form = ReminderForm()
    return render(request, 'core/reminders.html', {'reminders': reminders, 'form': form})

# --- Subscription Tracker ---

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            messages.success(request, "Subscription tracked!")
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, 'core/subscriptions.html', {'subscriptions': subscriptions, 'form': form})

def emergency_mode(request):
    # Future implementation for secure document sharing
    return render(request, 'core/emergency.html')
