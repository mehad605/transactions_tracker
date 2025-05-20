from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .forms import RegisterForm, TransactionForm, BalanceForm
from .models import Transaction, Category, UserProfile
import json
from django.utils import timezone


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = RegisterForm()

    return render(
        request,
        "tracker/auth/register.html",
        {
            "form": form,
            "username": request.POST.get("username", ""),
            "email": request.POST.get("email", ""),
        },
    )


@login_required
def home_view(request):
    today = timezone.now().date()

    # Retrieve query parameters with defaults
    current_type = request.GET.get("type", "expenses")
    active_range = request.GET.get("range", "day")
    selected_date = request.GET.get("date", today.isoformat())
    selected_month = request.GET.get("month", today.strftime("%Y-%m"))
    selected_year = request.GET.get("year", str(today.year))
    category_filter = request.GET.get("category", "")
    search_query = request.GET.get("search", "")

    # Filter transactions based on user, type, and date range
    transactions = Transaction.objects.filter(
        user=request.user, is_expense=(current_type == "expenses")
    ).order_by("-date")

    try:
        if active_range == "month":
            year, month = map(int, selected_month.split("-"))
            transactions = transactions.filter(date__year=year, date__month=month)
        elif active_range == "year":
            transactions = transactions.filter(date__year=int(selected_year))
        else:  # Daily filtering
            date_obj = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
            transactions = transactions.filter(date=date_obj)
    except ValueError:
        messages.error(request, "Invalid date format. Please check your input.")
        transactions = transactions.filter(date=today)

    # Apply additional filters
    if category_filter:
        transactions = transactions.filter(category__name=category_filter)
    if search_query:
        transactions = transactions.filter(comment__icontains=search_query)

    # Fetch categories and prepare chart data
    categories = Category.objects.filter(is_expense=(current_type == "expenses"))
    category_data = {
        "labels": [cat.name for cat in categories],
        "datasets": [
            {
                "label": "Amount",
                "data": [
                    float(
                        transactions.filter(category=cat).aggregate(
                            total=Sum("amount")
                        )["total"]
                        or 0
                    )
                    for cat in categories
                ],
                "backgroundColor": [
                    "#ff5555",
                    "#50fa7b",
                    "#8be9fd",
                    "#ffb86c",
                    "#ff79c6",
                    "#bd93f9",
                ],
            }
        ],
    }

    context = {
        "current_type": current_type,
        "active_range": active_range,
        "selected_date": selected_date,
        "selected_month": selected_month,
        "selected_year": selected_year,
        "transactions": transactions,
        "categories": categories,
        "category_data": json.dumps(category_data),
        "today": today,
    }

    return render(request, "tracker/home.html", context)


# ... (rest of your views)


@login_required
def edit_balance_view(request):
    if request.method == "POST":
        form = BalanceForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Balance updated successfully")
            return redirect("home")
    else:
        form = BalanceForm(instance=request.user.userprofile)
    return render(request, "tracker/edit_balance.html", {"form": form})


@login_required
def add_transaction_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            profile = request.user.userprofile
            if transaction.is_expense:
                profile.balance -= transaction.amount
            else:
                profile.balance += transaction.amount
            profile.save()

            messages.success(request, "Transaction added successfully")
            return redirect("home")
        else:
            messages.error(request, "Error occurred while adding transaction")
    else:
        form = TransactionForm()
    return render(request, "tracker/transaction_form.html", {"form": form})


@login_required
def edit_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    old_amount = transaction.amount

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            updated_transaction = form.save()

            profile = request.user.userprofile
            if updated_transaction.is_expense:
                profile.balance += old_amount - updated_transaction.amount
            else:
                profile.balance += updated_transaction.amount - old_amount
            profile.save()

            messages.success(request, "Transaction updated successfully")
            return redirect("home")
        else:
            messages.error(request, "Error occurred while updating transaction")
    else:
        form = TransactionForm(instance=transaction)
    return render(request, "tracker/transaction_form.html", {"form": form})


@login_required
def manage_categories_view(request):
    categories = Category.objects.all()
    return render(
        request, "tracker/category_management.html", {"categories": categories}
    )


@login_required
def add_category_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        is_expense = request.POST.get("type") == "expense"
        if name:
            Category.objects.create(name=name, is_expense=is_expense)
            messages.success(request, "Category added successfully")
        else:
            messages.error(request, "Error: Category name cannot be empty")
        return redirect("manage_categories")
    return redirect("manage_categories")


@login_required
def delete_category_view(request, pk):
    try:
        Category.objects.filter(pk=pk).delete()
        messages.success(request, "Category deleted successfully")
    except Exception as e:
        messages.error(request, f"Error deleting category: {e}")
    return redirect("manage_categories")


@login_required
def delete_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        # Update balance
        profile = request.user.userprofile
        if transaction.is_expense:
            profile.balance += transaction.amount
        else:
            profile.balance -= transaction.amount
        profile.save()

        transaction.delete()
        messages.success(request, "Transaction deleted successfully")
        return redirect("home")
    return redirect("home")
