from django.http import JsonResponse
from django.db.models import QuerySet, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils.text import slugify

from account.models import Account

from .models import Blog, Category, Tag, Comment

from .forms import TextForm, AddBlogForm

def home_view(request):
    return render(request, "pages/index.html")

def blogs_view(request):
    recent_news = Blog.objects.order_by("-created_date")[:3]
    queryset  = Blog.objects.order_by("-created_date")
    categories = Category.objects.all()
    page = request.GET.get("page", 1)
    paginator = Paginator(queryset, 2)
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        redirect("blogs")
    
    context = {
        "blogs": blogs,
        "recent_news": recent_news,
        "categories": categories,
        "paginator": paginator
    }

    return render(request, "pages/blog.html", context)
    
def blog_detail_view(request, slug):
    
    recent_news = Blog.objects.order_by("-created_date")[:3]
    suggest_posts = Blog.objects.order_by("-created_date")[:3]
    blog = get_object_or_404(Blog, slug=slug)
    all_categories = Category.objects.all()
    blog_category = Category.objects.get(id=blog.category.id)
    blog_tags = blog.tags.all()
    all_tags = Tag.objects.all()
    context = {
        "blog": blog,
        "suggest_posts": suggest_posts,
        "all_categories": all_categories,
        "recent_news": recent_news,
        "blog_category": blog_category,
        "blog_tags": blog_tags,
        "all_tags": all_tags
    }
    return render(request, "pages/blog_detail.html", context)

def search_blogs_view(request):

    search_key = request.GET.get("search", None)
    blogs = Blog.objects.order_by("-created_date")

    if search_key:
        search_blogs = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key) 
        )

        context = {
            "blogs": blogs,
        }

def checkout_view(request):
    return render(request, "pages/contact")

def shopping_detail_view(request):
    return render(request, "pages/shopping_detail.html")

def shopping_grid_view(request):
    return render(request, "pages/shopping_grid.html")

def shopping_cart_view(request):
    return render(request, "pages/shopping_cart.html")