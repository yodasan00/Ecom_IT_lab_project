from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.utils import timezone

def book_list(request):
    books = Book.objects.all().order_by('book_name')
    return render(request, 'books/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Add Book'})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})


#For books and cart display
def book_display(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', [])

    if book_id not in cart:
        cart.append(book_id)
        request.session['cart'] = cart

    return redirect('book_display')


def view_cart(request):
   
    cart = request.session.get('cart', [])
    books_in_cart = Book.objects.filter(id__in=cart)

    # Calculate total
    total_price = sum(book.price for book in books_in_cart)

    return render(request, 'cart.html', {
        'books': books_in_cart,
        'total_price': total_price
    })


def buy_now(request, book_id):
    """Skip cart and go directly to payment page for one book."""
    book = get_object_or_404(Book, id=book_id)
    request.session['buy_now'] = {
        'id': book.id,
        'book_name': book.book_name,
        'author_name': book.author_name,
        'price': float(book.price),
    }
    return redirect('payment_page')


def remove(request, book_id):
    cart = request.session.get('cart', [])

    if book_id in cart:
        cart.remove(book_id)
        request.session['cart'] = cart

    return redirect('view_cart')

def payment_page(request):
    buy_now_item = request.session.get('buy_now')   
    cart = request.session.get('cart', [])

    if buy_now_item:
        books_in_cart = [buy_now_item]
        total_price = buy_now_item['price']

    #Normal cart checkout
    elif cart:
        books = Book.objects.filter(id__in=cart)
        books_in_cart = [
            {'book_name': b.book_name, 'author_name': b.author_name, 'price': float(b.price)}
            for b in books
        ]
        total_price = sum(b['price'] for b in books_in_cart)

    # CASE 3 — Nothing to pay for
    else:
        return redirect('book_display')

    # Handle payment confirmation
    if request.method == 'POST':
        request.session['last_order'] = {
            'books': [b['book_name'] for b in books_in_cart],
            'total': total_price,
            'time': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Clear session data
        request.session.pop('cart', None)
        request.session.pop('buy_now', None)

        return redirect('order_confirmed')

    return render(request, 'payment.html', {
        'books': books_in_cart,
        'total_price': total_price,
    })



def order_confirmed(request):
    order = request.session.get('last_order')
    if not order:
        return redirect('book_display')

    return render(request, 'order_confirmed.html', {'order': order})
