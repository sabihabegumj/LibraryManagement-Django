from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review


# Register your models here.
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name','website','city','country')
    list_display_links = ('name','website')
    list_filter = ('website',)
    search_fields = ('name','website','city','country')
    list_per_page = 5

def add_price(modeladmin, request, queryset):
    for book in queryset:
        book.price = book.price + 10
        book.save()
add_price.short_description = 'Add $10 to Current Price'

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ('title', 'category','num_pages','price','publisher')
    list_display_links = ('title','publisher')
    list_filter = ('title','price')
    search_fields = ('title','category','num_pages','price','publisher')
    list_per_page = 5
    actions = [add_price, ]
class OrderAdmin(admin.ModelAdmin):
    fields = [('books'),( 'member', 'order_type', 'order_date')]
    list_display = ('id', 'member', 'order_type', 'order_date','total_items')
    list_per_page = 5

class MemberAdmin(admin.ModelAdmin):
    fields = [('first_name', 'last_name', 'status', 'borrowed_books', 'photo')]
    list_display = ('first_name', 'last_name', 'status', 'books_borrowed')
    list_per_page = 5


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'book', 'rating', 'comments', 'date')

admin.site.register(Member,MemberAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Review, ReviewAdmin)