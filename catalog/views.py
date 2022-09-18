from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.models import User
#from django.shortcuts import redirect
#from django.core.mail import send_mail, BadHeaderError
#from django.http import HttpResponse
#from django.contrib.auth.forms import PasswordResetForm
#from django.template.loader import render_to_string
#from django.db.models.query_utils import Q
#from django.utils.http import urlsafe_base64_encode
#from django.contrib.auth.tokens import default_token_generator
#from django.utils.encoding import force_bytes

from .models import Book, Author, BookInstance, Genre
# Create your views here.

#def password_reset_request(request):
    #if request.method == "POST":
    #password_reset_form = PasswordResetForm(request.POST)
        #if password_reset_form.is_valid():
            #data = password_reset_form.cleaned_data['email']
            #associated_users = User.objects.filter(Q(email=data))
            #if associated_users.exists():
                #for user in associated_users:
                    #subject = "Password Reset Requested"
                    #email_template_name = "registration/password_reset_email.txt"
                    #c = {
                    #"email":user.email,
                    #'domain':'127.0.0.1:8000',
                    #'site_name': 'Website',
					#"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					#"user": user,
					#'token': default_token_generator.make_token(user),
					#'protocol': 'http',
					#}
                    #email = render_to_string(email_template_name, c)
                    #try:
                        #send_mail(subject, email, 'pythonemailtester123@gmail.com' , [user.email], fail_silently=False)
                    #except BadHeaderError:
                        #return HttpResponse('Invalid header found.')
                    #return redirect ("/password_reset_done/")
    #password_reset_form = PasswordResetForm()
    #return render(request=request, template_name="registration/password_reset_done.html", context={"password_reset_form":password_reset_form})


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

