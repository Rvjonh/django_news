from django.contrib import admin

from .models import Article, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0  # show a number of new Comment froms


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
