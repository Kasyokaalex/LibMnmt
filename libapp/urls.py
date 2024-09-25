from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('issue_book/<int:book_id>/', views.issue_book_view, name='issue_book'),
    path('members/', views.member_list, name='member_list'),
    path('members/', views.member_list, name='member_list'),
    path('members/new/', views.member_create, name='member_create'),
    path('members/<int:pk>/edit/', views.member_update, name='member_update'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    path('get_members/', views.get_members, name='get_members'),
    path('success/', views.success_page, name='success_page'),
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('return_book/<int:transaction_id>/', views.return_book_view, name='return_book'),
    path('books/delete/', views.book_delete, name='book_delete'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/update/<int:pk>/', views.book_update, name='book_update'),

]