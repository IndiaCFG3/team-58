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
        passout = Passouts()
        passout.Region = row[0]
        passout.LCDM_Name = row[1]
        passout.LDC_Name = row[2]
        passout.Batch_Code = row[3]
        passout.Status = row[4]
        passout.Start_Date = row[5]
        passout.End_Date = row[5]
        passout.Course_Name = row[6]
        passout.Full_Name = row[7]
        passout.DOB = row[8]
        passout.save()

    dataReader = csv.reader(open(
        r'D:\\CFG\\team-58\\Sameeksha\\django_project\\blog\\placement.csv'), delimiter=',', quotechar='"')

    for row in dataReader:
        placement = Placement()
        placement.Region = row[0]
        placement.ReporteeLDCM = row[1]
        placement.LDC_Name = row[2]
        placement.Batch_Code = row[3]
        placement.Course_Name = row[4]
        placement.Start_Date = row[5]
        placement.End_Date = row[6]
        placement.Student_Id = row[7]
        placement.Student_Name = row[8]
        placement.save()

    dataReader = csv.reader(open(
        r'D:\\CFG\\team-58\\Sameeksha\\django_project\\blog\\batches.csv'), delimiter=',', quotechar='"')

    for row in dataReader:
        batches = Batches()
        batches.Region = row[0]
        batches.Center_Name = row[1]
        batches.LDCM_Name = row[2]
        batches.Reportee = row[3]
        batches.Batch_Type = row[4]
        batches.Batch_Code = row[5]
        batches.Course_Name = row[6]
        batches.Course_Name2 = row[7]
        batches.Status = row[8]
        batches.Start_Date = row[9]
        batches.save()

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
