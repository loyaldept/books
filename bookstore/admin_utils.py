from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, User
from .forms import BookForm, UserForm
from django.contrib import messages
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password

class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"

class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"

class ListUserView(ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')

class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'

class ACreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'dashboard/chat_form.html'
    success_url = reverse_lazy('alchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class AListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'dashboard/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')

@login_required
def aabook_form(request):
    return render(request, 'dashboard/add_book.html')

@login_required
def aabook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, 
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('albook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('aabook_form')

class ABookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'dashboard/book_list.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')

class AManageBook(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'dashboard/manage_books.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')

class ADeleteBook(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete2.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Data was dele successfully'

class ADeleteBookk(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Data was dele successfully'

class AViewBook(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'dashboard/book_detail.html'

class AEditView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'dashboard/edit_book.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Data was updated successfully'

class ADeleteRequest(LoginRequiredMixin,ListView):
    model = DeleteRequest
    template_name = 'dashboard/delete_request.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_queryset(self):
        return DeleteRequest.objects.order_by('-id')

class AFeedback(LoginRequiredMixin,ListView):
    model = Feedback
    template_name = 'dashboard/feedback.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_queryset(self):
        return Feedback.objects.order_by('-id')

@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))

    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashborad')
    else:
        a = data

        # Searching for It
        qs5 =models.Book.objects.filter(id__iexact=a).distinct()
        qs6 =models.Book.objects.filter(id__exact=a).distinct()

        qs7 =models.Book.objects.all().filter(id__contains=a)
        qs8 =models.Book.objects.select_related().filter(id__icontains=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word="Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request,'dashboard/result.html',{'files':files,'word':word})
        return render(request,'dashboard/result.html',{'files':files,'word':word})
