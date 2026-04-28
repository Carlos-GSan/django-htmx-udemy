from django.http import HttpResponse, QueryDict
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from core.forms import BookForm
from core.models import Book

# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        form =  BookForm(request.POST, user=request.user)
        if form.is_valid():
            name = form.cleaned_data['name']
            genre = form.cleaned_data['genre']
            book, _ = Book.objects.get_or_create(name=name, genre=genre)
            if not request.user.books.filter(id=book.id).exists():
                request.user.books.add(book)
                response =  render(request, 'partials/book-row.html', {'book': book})
                return response
        else:
            context = {'form': form}
            response =  render(request, 'partials/book-form.html',context)
            response['HX-Retarget'] = '#book-form'
            response['HX-Reswap'] = 'outerHTML'
            return response
    books = request.user.books.all()
    context = {'books': books, 'form': BookForm()}
    return render(request, 'index.html', context)

@login_required
@require_http_methods(['DELETE'])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    request.user.books.remove(book)
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'book-deleted'
    return response

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'PUT':
        put_data = QueryDict(request.body)
        form = BookForm(
            put_data,
            user=request.user,
            initial={'name': book.name, 'genre': book.genre}
        )
        if form.is_valid():
            book.name = form.cleaned_data['name']
            book.genre = form.cleaned_data['genre']
            book.save()
        else:
            context = {'form': form, 'book': book}
            response =  render(request, 'partials/book-update-form.html',context)
            response['HX-Retarget'] = '#book-form'
            response['HX-Reswap'] = 'outerHTML'
            return response
            # return the update form and reswap as before (on "index" view)
            
            
    context = {'book': book,
               'form': BookForm(initial={'name': book.name, 'genre': book.genre})
    }
    
    template = 'partials/book-detail-partial.html' if request.headers.get('HX-Request') else 'book-detail.html'
    
    return render(request, template, context)

@login_required
def search_books(request):
    query = request.GET.get('search','')
    books = request.user.books.filter(
        Q(name__icontains=query) | Q(genre__icontains=query))
    return render(request, 'partials/book-table.html', {'books': books})