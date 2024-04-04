from django.shortcuts import render, get_object_or_404
from django.http import Http404
from blog.models import Post, Category
from django.utils import timezone


def index(request):
    template = 'blog/index.html'
    time = timezone.now()
    post_list = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=time
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=id)
    if post.pub_date > timezone.now() or not post.is_published \
            or not post.category.is_published:
        raise Http404('Post does not exist')
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    time = timezone.now()
    category_slug = get_object_or_404(Category, slug=category_slug)
    if not category_slug.is_published:
        raise Http404('Category does not exist')
    post_list = Post.objects.filter(
        category_id=category_slug.id,
        is_published=True,
        pub_date__lte=time
    )
    context = {'category': category_slug,
               'post_list': post_list}
    return render(request, template, context)
