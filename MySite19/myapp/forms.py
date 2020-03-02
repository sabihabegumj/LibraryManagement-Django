from django import forms
from myapp.models import Order, Review, Book, Member
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    keywords = forms.CharField(max_length=100, required=False)
    title = forms.CharField(max_length=100, required=False)
    category = forms.ChoiceField(choices = CATEGORY_CHOICES, required=False, widget=forms.Select())
    publisher = forms.CharField(max_length=100, required=False)
    max_price = forms.IntegerField(min_value=0, required=False)
    min_reviews =forms.IntegerField(min_value=0, required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'order_type': u'Order Type'}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer','book','rating','comments']
        widgets ={'comments': forms.Textarea()}
        labels = {'reviewer':u'Your Email ID', 'rating':u'Rating:An Integer between 1 (worst) and 5 (best)'}
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False


class RegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'status', 'address', 'city',
                  'province', 'photo', 'auto_renew']