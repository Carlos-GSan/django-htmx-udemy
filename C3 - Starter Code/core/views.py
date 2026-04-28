from django.http import HttpResponse
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