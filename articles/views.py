from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    FormView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from django.core.paginator import Paginator
from .models import Article, Comment
from .forms import CommentForm

# Create your views here.


class ArticleListView(ListView):
    paginate_by = 5
    model = Article
    template_name = "article_list.html"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    fields = (
        "title",
        "body",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = self.get_comment_form()
        context["comments_page_obj"] = self.get_comments_pagination(context)
        return context

    def get_comment_form(self):
        return CommentForm()

    def get_comments_pagination(self, context):
        """returns pagination for comments section"""
        comments_list = Comment.objects.filter(article=context["article"])
        paginator = Paginator(comments_list, 5)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        return page_obj


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
