from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib import messages,auth
from .models import Book, Review, Member, Order
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import randint
from django.template import RequestContext
from django.core.paginator import Paginator
from django.views import View

# Create your views here.

#def index(request):
#    booklist = Book.objects.all().order_by('id')[:10]
#    paginator = Paginator(booklist, 3)
#    page = request.GET.get('page')
#    booklist = paginator.get_page(page)
#    if 'last_login' in request.session:
#        userlogin = request.session['last_login']
#    else:
#        userlogin='Your last login was more than one hour ago'
#    return render(request, 'myapp/index.html', {'booklist': booklist,'userlogin': userlogin})

class IndexView(View):
    template_name = 'myapp/index.html'
    last_login_cookie = 'last_login'
    def get(self, request):
        last_login = ''
        if self.last_login_cookie in request.session.keys():
            userlogin = request.session.get(self.last_login_cookie)
        else:
            userlogin = 'Your last login was more than one hour ago'
        booklist = Book.objects.all().order_by('id')[:10]
        paginator = Paginator(booklist, 3)
        page = request.GET.get('page')
        booklist = paginator.get_page(page)
        return render(request, self.template_name, {'booklist': booklist, 'userlogin': userlogin})

def about(request):
    cookie= request.COOKIES.get('lucky_num')
    response = HttpResponse()
    flag=0
    if cookie is None:
        mynum= randint(1,100)
        flag=1
    else:
        mynum = request.COOKIES['lucky_num']
    response = render(request,'myapp/about.html', {'mynum':mynum})
    if flag==1:
        response.set_cookie('lucky_num', mynum, expires=300)
    return response


#def detail(request, book_id):
#    book = get_object_or_404(Book, pk=book_id)
#    return render(request, 'myapp/detail.html', {'book': book})

class DetailView(View):
    template_name = 'myapp/detail.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        return render(request, self.template_name, {'book': book})

def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            title = form.cleaned_data['title']
            publisher = form.cleaned_data['publisher']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            min_reviews = form.cleaned_data['min_reviews']
            booklist = Book.objects.all()
            # Keywords:
            if keywords:
                booklist = booklist.filter(description__icontains=keywords)
            # title:
            if title:
                booklist = booklist.filter(title__iexact=title)
            # category:
            if category:
                booklist = booklist.filter(category=category)
            # publisher:
            if publisher:
                    booklist = booklist.filter(publisher__name__iexact=publisher)
            # max_price:
            if max_price:
                booklist = booklist.filter(price__lte=max_price)
            # min_reviews:
            if min_reviews:
                booklist = booklist.filter(num_reviews__gte=min_reviews)
            return render(request, 'myapp/results.html', {'booklist':booklist,'values': request.POST})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form':form})

@login_required(login_url='/myapp/login')
def place_order(request):
    member = Member.objects.filter(username=request.user)
    if member:
          if request.method == 'POST':
              form = OrderForm(request.POST)
              if form.is_valid():
                  books = form.cleaned_data['books']
                  order = form.save(commit=False)
                  type = order.order_type
                  member = Member.objects.get(id=request.user.id)
                  order.member = member
                  order.save()
                  form.save_m2m()
                  total = 0
                  if type == 0:
                      for book in books:
                          total += book.price
                          return render(request, 'myapp/order_response.html',{'books': books, 'total': total})
                  else:
                      for b in order.books.all():
                          member.borrowed_books.add(b)
                          member.save()
                      return render(request, 'myapp/order_response.html',{'books': books, 'total': total})
              else:
                  return render(request, 'myapp/placeorder.html', {'form': form})
          else:
             form = OrderForm()
             return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        error = 'You are not a registered member to place order'
        return render(request, 'myapp/notregistered.html', {'error': error})

@login_required(login_url='/myapp/login')
def review(request):
    member = Member.objects.filter(username=request.user, status__in=(1,2))
    if member:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                book = form.cleaned_data['book']
                review = form.save(commit=False)
                rating = review.rating
                if rating <= 5 and rating >= 1:
                    booklist = Book.objects.all().order_by('id')[:10]
                    book.num_reviews = book.num_reviews + 1
                    book.save()
                    review.save()
                    return render(request, 'myapp/index.html', {'booklist': booklist})
                else:
                    return render(request, 'myapp/review.html',
                                  {'error': 'You must enter a rating between 1 and 5!', 'form': form})
            else:
                form = ReviewForm()
                return render(request, 'myapp/review.html', {'form': form, 'error': 'You must enter a valid data'})
        else:
            form = ReviewForm()
            return render(request, 'myapp/review.html', {'form': form})
    else:
        error = 'You should either be a registered regular or a premium member to review a book!'
        return render(request,'myapp/notregistered.html', {'error':error})

def user_login(request):
    if request.method == 'POST':
        next = request.POST.get('next')
        username = request.POST['username']
        request.session['username'] = username
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        current_login_time = datetime.now()
        timestamp = current_login_time.strftime("%d-%m -%Y (%H:%M:%S)")
        request.session['last_login'] = 'Last Login: ' + timestamp
        request.session.set_expiry(3600)
        if user:
            if user.is_active:
                login(request, user)
                if next == None:
                    return HttpResponseRedirect(reverse('myapp:index'))
                else:
                    return HttpResponseRedirect(next)
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            member = Member(photo=request.FILES['photo'])
            form.save()
            return HttpResponseRedirect(reverse('myapp:user_login'))
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


def check_list(request):
    booklist = Book.objects.all().order_by('id')[:10]
    paginator = Paginator(booklist, 3)
    page = request.GET.get('page')
    booklist = paginator.get_page(page)
    return render(request, 'myapp/check_list.html', {'booklist': booklist})


@login_required(login_url='/myapp/login')
def chk_reviews(request, book_id):
    member = Member.objects.filter(username=request.user)
    avg = 0
    if member:
        review = Review.objects.filter(book__id=book_id).values_list('rating', flat=True)
        book=get_object_or_404(Book,id=book_id)
        total = sum(review)
        number = len(review)
        if len(review) > 0:
            avg = total / number
        return render(request, 'myapp/chk_reviews.html', {'avg': avg, 'book':book, 'total':total, 'number':number})
    else:
        error ='You are not a registered member to check reviews!'
        return render(request,'myapp/notregistered.html',{'error': error})


@login_required(login_url='/myapp/login')
def myorders(request):
    member = Member.objects.filter(username=request.user)
    if member:
        member = Member.objects.get(id=request.user.id)
        orders = Order.objects.filter(member__username=request.user).order_by('order_date')
        return render(request, 'myapp/myorders.html', {'orders': orders, 'member': member})
    else:
        error = "You are not a registered user to have a dashboard to view your orders!"
        return render(request, 'myapp/notregistered.html', {'error': error})
