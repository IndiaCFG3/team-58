from django.shortcuts import render
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from users.models import Profile
from .models import Students
import csv

# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    is_hr = False
    is_operations = False
    is_accounts = False
    is_audit = False
    is_hod = False
    is_enc = False
    is_imapact = False

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        print(self.request.user.id)
        profile = Profile.objects.get(user=self.request.user)
        print(profile.is_accounts)
        context["is_hr"] = profile.is_hr
        context["is_operations"] = profile.is_operations
        context["is_accounts"] = profile.is_accounts
        context["is_audit"] = profile.is_audit
        context["is_hod"] = profile.is_hod
        context["is_enc"] = profile.is_enc
        context["is_imapact"] = profile.is_imapact
        return context

    dataReader = csv.reader(open(
        r'D:\\CFG\\team-58\\Sameeksha\\django_project\\blog\\students.csv'), delimiter=',', quotechar='"')

    for row in dataReader:
        student = Students()
        student.Name = row[0]
        student.BatchId = row[1]
        student.date = row[2]
        student.save()

    dataReader = csv.reader(open(
        r'D:\\CFG\\team-58\\Sameeksha\\django_project\\blog\\passout.csv'), delimiter=',', quotechar='"')

    for row in dataReader:
        passout=Passouts()
        passout.Region = row[0]
        passout.LCDM_Name = models.CharField(max_length=100)
        passout.LDC_Name = models.CharField(max_length=100)
        passout.Batch_Code = models.IntegerField()
        passout.Status = models.CharField(max_length=1)
        passout.Start_Date = models.IntegerField()
        passout.End_Date = models.IntegerField()
        passout.Course_Name = models.CharField(max_length=100)
        passout.Full_Name = models.CharField(max_length=100)
        passout.DOB = models.IntegerField()


    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})
