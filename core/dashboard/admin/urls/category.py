from django.urls import path
from .. import views

urlpatterns = [
    path("category/list/", views.AdminCategoryListView.as_view(), name="category-list"),
    path("category/create/", views.AdminCategoryFormView.as_view(), name="category-form"),
    path("category/<int:pk>/edit/", views.AdminCategoryEditView.as_view(), name="category-edit"),
]
