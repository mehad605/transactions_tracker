# transactions_tracker/transactions_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="tracker/auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("edit-balance/", views.edit_balance_view, name="edit_balance"),
    path("add-transaction/", views.add_transaction_view, name="add_transaction"),
    path(
        "edit-transaction/<int:pk>/",
        views.edit_transaction_view,
        name="edit_transaction",
    ),
    path("categories/", views.manage_categories_view, name="manage_categories"),
    path("categories/add/", views.add_category_view, name="add_category"),
    path(
        "categories/delete/<int:pk>/",
        views.delete_category_view,
        name="delete_category",
    ),
    path(
        "delete-transaction/<int:pk>/",
        views.delete_transaction_view,
        name="delete_transaction",
    ),
]
