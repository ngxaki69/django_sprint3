from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category
from .constants import TOTAL_POSTS


def index(request):
    template = 'blog/index.html'
    post_list = filter_search(Post.objects)[:TOTAL_POSTS]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(filter_search(Post.objects), id=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = filter_search(category.posts)
    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)


def filter_search(entity):
    time = timezone.now()
    return entity.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=time
    )
