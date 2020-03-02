# Import necessary classes
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)
    publisherlist = Publisher.objects.all().order_by('city')[:10]
    heading2 = '<p>' + 'List of Publishers: ' + '</p>'
    response.write(heading2)
    for publisher in publisherlist:
        para2 = '<p>' + str(publisher.name) + ': ' + str(publisher.city) + '</p>'
        response.write(para2)
    return response

def about(request):
    response = HttpResponse()
    response.write("This is an eBook APP")
    return response


def detail(request, book_id):
    response = HttpResponse()
    try:
        book = Book.objects.get(id = book_id)
        heading1 = '<p><b>' + 'BOOK DETAILS:' + '</b></p> <ul align="center"><li>' + '<b>Title: </b>' + str.upper(book.title) + '</li> <li> <b>Price:</b> $' + str(book.price) + '</li> <li> <b> Publisher: </b>' + str(book.publisher) + '</li></ul>'
        response.write(heading1)
    except Book.DoesNotExist:
        response.write("Book Details Does Not Exists")
    return response