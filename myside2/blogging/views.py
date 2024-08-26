# from django.shortcuts import render
from .models import Blog
from django.views import View
# from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from .forms import UserCreationForm, BlogForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


class HomePageView(TemplateView):
    template_name = 'index.html'


class BlogListView(TemplateView, LoginRequiredMixin):
    template_name = 'blogging/list.html'

    def get(self, request):
        blogs = Blog.objects.all()
        context = {
            'blogs': blogs
        }
        return render(request, self.template_name, context)


class CustomLoginView(View):
    template_name = 'blogging/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST
        email = data['email']
        password = data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog_list')
        else:
            messages.error(request, 'Invalid email or password.')
        return render(request, self.template_name)


class RegisterPageView(FormView):
    template_name = 'blogging/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        password_confirm = form.cleaned_data.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(self.request, "Username already exists")
            return self.form_invalid(form)
        elif User.objects.filter(email=email).exists():
            messages.info(self.request, "Email already exists")
            return self.form_invalid(form)
        elif password != password_confirm:
            messages.warning(self.request, "Passwords do not match")
            return self.form_invalid(form)
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            login(self.request, user)
            messages.success(self.request, "Registration successful")
            return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy("login_page"))


# class BlogCreateView(CreateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = 'blogging/newblog.html'
#     success_url = reverse_lazy('blog_list')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


class BlogCreateView(TemplateView):
    template_name = 'blogging/newblog.html'

    def get(self, request):
        form = BlogForm()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BlogForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/blogs/')

        context = {
            "form": form
        }

        return render(request, self.template_name, context)


class BlogUpdateView(TemplateView):
    template_name = 'blogging/update.html'

    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id, author=request.user)
        form = BlogForm(instance=blog)
        context = {
            "form": form,
            "blog": blog
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        blog = get_object_or_404(Blog, id=id, author=request.user)
        form = BlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            form.save()
            return redirect('/blogs/')

        context = {
            "form": form,
            "blog": blog
        }

        return render(request, self.template_name, context)


class BlogDeleteView(TemplateView):
    template_name = "blogging/list.html"

    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id, author=request.user)
        blog.delete()
        return redirect("blog_list")
