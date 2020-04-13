from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User 
from django.shortcuts import render, get_object_or_404 
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Postdt

#from django.http import HttpResponse
# Create your views here.


def home(request):
    context = {
        'posts' : Postdt.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})    

class PostListView(ListView):
    model = Postdt
    template_name= 'blog/home.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 5


class UserPostListView(ListView):
    model = Postdt
    template_name= 'blog/user_posts.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 3 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Postdt.objects.filter(author=user).order_by('-date')    




class PostDetailView(DetailView):
    model = Postdt
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Postdt
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user        #to set the current author the one who signed in.as author is required for any post otherwise its an integrity error
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Postdt
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user        #to set the current author the one who signed in.as author is required for any post otherwise its an integrity error
        return super().form_valid(form)        

    def test_func(self):                            #to check that only the wrtier of that blog can update that blog
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Postdt
    success_url = '/' 


    def test_func(self):                            #to check that only the wrtier of that blog can update that blog
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False