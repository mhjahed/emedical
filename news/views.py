# news/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q

from .models import Article, Category, Tag, Comment, ArticleImage
from .forms import ArticleForm, CommentForm, ArticleImageForm
from accounts.decorators import medical_staff_required


def article_list(request):
    """Public: List all published articles"""
    articles = Article.objects.filter(status='published').select_related('author', 'category')
    categories = Category.objects.filter(is_active=True)
    
    # Search & Filter
    search = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    tag_filter = request.GET.get('tag', '')
    
    if search:
        articles = articles.filter(
            Q(title__icontains=search) |
            Q(excerpt__icontains=search) |
            Q(content__icontains=search)
        )
    
    if category_filter:
        articles = articles.filter(category__slug=category_filter)
    
    if tag_filter:
        articles = articles.filter(tags__slug=tag_filter)
    
    # Pagination
    paginator = Paginator(articles, 9)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'articles': articles,
        'categories': categories,
        'search': search,
        'category_filter': category_filter,
        'tag_filter': tag_filter,
        'featured_articles': Article.objects.filter(status='published', is_featured=True)[:3],
    }
    return render(request, 'news/article_list.html', context)


def article_detail(request, slug):
    """Public: Article detail with loader"""
    article = get_object_or_404(Article, slug=slug, status='published')
    article.increment_views()
    
    # Get related articles
    related_articles = Article.objects.filter(
        status='published',
        category=article.category
    ).exclude(id=article.id)[:3]
    
    # Comments
    comments = article.comments.filter(is_approved=True)
    comment_form = CommentForm()
    
    # Gallery images for carousel
    gallery_images = article.gallery_images.all()
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'comments': comments,
        'comment_form': comment_form,
        'gallery_images': gallery_images,
    }
    return render(request, 'news/article_detail.html', context)


@login_required
def add_comment(request, slug):
    """Add comment to article"""
    article = get_object_or_404(Article, slug=slug, status='published')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('news:article_detail', slug=slug)


def category_articles(request, slug):
    """Articles by category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    articles = Article.objects.filter(status='published', category=category)
    
    paginator = Paginator(articles, 9)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    return render(request, 'news/category_articles.html', {
        'category': category,
        'articles': articles
    })


def tag_articles(request, slug):
    """Articles by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(status='published', tags=tag)
    
    paginator = Paginator(articles, 9)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    return render(request, 'news/tag_articles.html', {
        'tag': tag,
        'articles': articles
    })


# ============ Doctor/Staff Article Management ============

@medical_staff_required
def my_articles(request):
    """Doctor/Staff: View own articles"""
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    return render(request, 'news/my_articles.html', {'articles': articles})


@medical_staff_required
def create_article(request):
    """Doctor/Staff: Create new article"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            # Doctors can publish directly, others need approval
            if not request.user.is_superadmin and article.status == 'published':
                article.status = 'pending'
            article.save()
            form.save_m2m()
            messages.success(request, 'Article created successfully!')
            return redirect('news:edit_article', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'news/create_article.html', {'form': form})


@medical_staff_required
def edit_article(request, slug):
    """Doctor/Staff: Edit own article"""
    article = get_object_or_404(Article, slug=slug)
    
    # Check permission
    if article.author != request.user and not request.user.is_superadmin:
        messages.error(request, 'You do not have permission to edit this article.')
        return redirect('news:my_articles')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('news:edit_article', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
        # Pre-populate tags
        form.initial['tags_input'] = ', '.join([tag.name for tag in article.tags.all()])
    
    # Gallery images
    gallery_images = article.gallery_images.all()
    image_form = ArticleImageForm()
    
    return render(request, 'news/edit_article.html', {
        'form': form,
        'article': article,
        'gallery_images': gallery_images,
        'image_form': image_form
    })


@medical_staff_required
def add_gallery_image(request, slug):
    """Add image to article gallery"""
    article = get_object_or_404(Article, slug=slug)
    
    if article.author != request.user and not request.user.is_superadmin:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    if request.method == 'POST':
        form = ArticleImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.article = article
            image.save()
            return JsonResponse({
                'success': True,
                'image_url': image.image.url,
                'image_id': image.id
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid form data'})


@medical_staff_required
def delete_gallery_image(request, image_id):
    """Delete image from article gallery"""
    image = get_object_or_404(ArticleImage, id=image_id)
    
    if image.article.author != request.user and not request.user.is_superadmin:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    image.delete()
    return JsonResponse({'success': True})


@medical_staff_required
def delete_article(request, slug):
    """Doctor/Staff: Delete own article"""
    article = get_object_or_404(Article, slug=slug)
    
    if article.author != request.user and not request.user.is_superadmin:
        messages.error(request, 'You do not have permission to delete this article.')
        return redirect('news:my_articles')
    
    article.delete()
    messages.success(request, 'Article deleted successfully!')
    return redirect('news:my_articles')