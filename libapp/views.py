from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, Transaction
from .forms import BookForm, MemberForm, TransactionForm, IssueBookForm
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.

def index(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Book has been successfully created.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = BookForm()  # Handle the GET request to display the form
        return render(request, 'book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Book has been successfully updated.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = BookForm(instance=book)  # Handle the GET request to display the form
        return render(request, 'book_form.html', {'form': form})
    
    
@require_POST
def book_delete(request):
    book_id = request.POST.get('book_id')
    book = get_object_or_404(Book, pk=book_id)
    try:
        book.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def member_list(request):
        members = Member.objects.all()
        return render(request, 'member_list.html', {'members': members})

def member_detail(request, pk):
        member = get_object_or_404(Member, pk=pk)
        return render(request, 'member_detail.html', {'member': member})

def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Member has been successfully created.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MemberForm()  # Handle GET request to display the form
        return render(request, 'member_form.html', {'form': form})

def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Member has been successfully updated.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MemberForm(instance=member)  # Handle GET request to display the form
        return render(request, 'member_form.html', {'form': form})

@require_POST
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)

    try:
        member.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def issue_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    members = Member.objects.all()

    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            outstanding_debt = Transaction.objects.filter(member=member, return_date__isnull=True).aggregate(total_fine=Sum('late_fee'))['total_fine'] or 0

            if outstanding_debt > 500:
                form.add_error(None, "Member has an outstanding debt of more than KES 500.")
            elif book.available_stock < 1:
                form.add_error(None, "No available copies of the book.")
            else:
                transaction = form.save(commit=False)
                transaction.due_date = timezone.now() + timedelta(days=14)
                transaction.rent_fee = 50.00
                transaction.save()
                book.available_stock -= 1
                book.save()
                messages.success(request, f'Book "{book.title}" has been successfully issued to {member.first_name} {member.last_name}.')
                return redirect('book_list')
    else:
        form = IssueBookForm(initial={'book': book})

    return render(request, 'issue_book.html', {'form': form, 'book': book, 'members': members})

def return_book_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    # Calculate fees based on the current date
    current_date = timezone.now().date()
    days_rented = (current_date - transaction.issue_date).days
    transaction.rent_fee = days_rented * 15.00  # KES 15 per day for the rent fee
    
    # Calculate late fee based on due date
    if current_date > transaction.due_date:
        days_late = (current_date - transaction.due_date).days
        transaction.late_fee = days_late * 10.00
    else:
        transaction.late_fee = 0.00  

    if request.method == 'POST':
        # Set the return date and update the transaction status
        transaction.return_date = current_date
        transaction.status = 'returned'
        transaction.save()

        transaction.book.available_stock += 1
        transaction.book.save()

        return redirect('transaction_list')

    # Passing days_rented to the template context
    return render(request, 'return_book.html', {
        'transaction': transaction,
        'current_date': current_date,
        'days_rented': days_rented,
    })


def transaction_list_view(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})


def get_members(request):
    members = Member.objects.all()
    member_list = [{'id': member.id, 'first_name': member.first_name, 'last_name': member.last_name} for member in members]
    return JsonResponse({'members': member_list})

def success_page(request):
    return render(request, 'success_page.html')
