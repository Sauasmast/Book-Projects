from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import RegistrationForm, Editprofile, Sell_form
from django.contrib.auth.forms import User, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Sell_book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.

''' This is a simple html content with the about  
us view no logic are implemented on this view '''
def home(request):
   return render(request, 'bookapp/index.html',{})

''' After logged in the contents are handled by this 
views. '''
@login_required
def loggedin(request):
    return render(request, 'bookapp/loggedin.html',{})

''' This is a view for the signup form where people could 
register for an application '''
def signup (request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.email = form.cleaned_data['email']
            post.save()
            return redirect('login')
        else:
            form = RegistrationForm(request.POST)
            return render(request, 'bookapp/signup.html', {'form':form})
            
    else:
        form = RegistrationForm()

        args= {'form':form}
        return render(request, 'bookapp/signup.html', args)


''' Individual Buying and Selling platform after
the user have logged in.'''

class Book_details(LoginRequiredMixin, generic.DetailView):
    model = Sell_book
    context_object_name = 'object_list'
    template_name = 'bookapp/detail.html'

class Sell_book_view(LoginRequiredMixin, generic.TemplateView):
    template_name = "bookapp/sell.html"

    def get(self, request):
        form = Sell_form()
        args = {'form':form}
        return render(request, self.template_name, args)
    
    def post(self, request):
        form = Sell_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            messages.success(request, "Your book has been listed on our record for sale.")
            form = Sell_form() # Responsible for giving out the empty form for duplication purpose
            return redirect('/sell')
        
@login_required
def share(request):
    return render(request, 'bookapp/share.html', {})


''' The profile of the user with the form to edit the profile '''
@login_required
def profile(request):
    book_obj = Sell_book.objects.filter(owner=request.user)
    args = {'user':request.user,'book_obj':book_obj}

    return render(request, 'bookapp/profile.html', args)

@login_required
def edit_profile(request):
    if (request.method == "POST"):
        form = Editprofile(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = Editprofile(instance=request.user)
        return render(request,"bookapp/edit_profile.html",{'forms':form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
        else:
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'bookapp/change_password.html', {'forms': form})

class Book_to_buy(LoginRequiredMixin, generic.ListView):
    template_name='bookapp/buy.html'

    def get_queryset(self):
        return Sell_book.objects.exclude(owner=self.request.user)



''' For deleting the book from the list of the displayed book '''
def delete(request, pk):
    post = get_object_or_404(Sell_book, pk=pk)
    if post.delete():
         messages.success(request, "Because its sold your book has been deleted form our record.")
    else:
         messages.warning(request, "Something Weird happened. Try again!") 

    return redirect('profile')
   

def edit_book(request, pk):
    post = get_object_or_404(Sell_book, pk=pk)
    if request.method == "POST":
        form = Sell_form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('details', pk=post.pk)
    else:
        form = Sell_form(instance=post)
        return render(request, 'bookapp/sell.html', {'form':form})

def sendmail(request, pk):
    messages.success(request, "Please check your mail for the contact information about the owner.")
    email_obj = Sell_book.objects.get(pk=pk)
    email = email_obj.owner.email
    email_send = request.user.email
    body = ("Dear " + request.user.first_name + ",\nThank you for choosing our platform for buying and selling the book. We are really happy you are here. This email is regarding your request to buy "
            + email_obj.book_title + " by the user "+ email_obj.owner.username + "\nPlease contact the owner of the book. The email address is " + email + ".")
    send_mail('Book Share Company', body , 'saugatd6@gmail.com', [email_send,])
    return redirect('details', pk=pk)