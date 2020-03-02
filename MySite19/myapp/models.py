from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True,default="USA")
    def __str__(self):
        return self.name

def validate_price(price):
    if price <= 0 and price >= 1000:
        raise ValidationError(
            _('%(price)s is not valid'),
            params={'price': price},
        )

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    description = models.TextField(blank=True)
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    num_reviews = models.PositiveIntegerField(default=0)
    book_photo = models.ImageField(upload_to='photos/%Y/%m/%d/book/', blank= True)
    def __str__(self):
        return self.title


class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=20,default="Windsor")
    province=models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/member/', blank=True)
    def __str__(self):
        return self.first_name
    def books_borrowed(self):
        return ", ".join([str(p) for p in self.borrowed_books.all()])
    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

class Order(models.Model):
    order_type  = [
        (0, 'Purchase'),
        (1, 'Borrow'),
     ]
    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=order_type, default=1)
    order_date = models.DateField(default=timezone.now)
    def __str__(self):
        return "Order Id "+str(self.id) + " Date " + str(self.order_date)
    def total_items(self):
        return self.books.count()

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.book+' '+str(self.rating)



