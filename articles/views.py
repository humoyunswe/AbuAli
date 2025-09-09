from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Article
from .forms import ArticleForm, CommentForm
from comments.models import Comment
from likes.models import Like
from django.core.cache import cache

def article_list(request):
    articles = Article.objects.filter(is_published=True).select_related('author').prefetch_related('tags', 'likes', 'comments').annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Фильтр по тегам
    tag = request.GET.get('tag')
    if tag:
        articles = articles.filter(tags__name=tag)
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        articles = articles.order_by('-likes_count', '-created_at')
    elif sort_by == 'most_commented':
        articles = articles.order_by('-comments_count', '-created_at')
    else:
        articles = articles.order_by('-created_at')
    
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Популярные теги
    popular_tags = cache.get_or_set('popular_tags', lambda: Article.tags.most_common()[:10], 60 * 60) # Cache for 1 hour
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'popular_tags': popular_tags,
        'current_tag': tag,
        'sort_by': sort_by,
    }
    return render(request, 'articles/article_list.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    # Увеличиваем счетчик просмотров
    article.views += 1
    article.save(update_fields=['views'])
    
    # Комментарии
    comments = article.comments.filter(parent=None, is_approved=True).order_by('-created_at')
    
    # Проверяем, лайкнул ли пользователь статью
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, article=article).exists()
    
    # Форма комментария
    comment_form = CommentForm()
    
    # Похожие статьи
    related_articles = Article.objects.filter(
        tags__in=article.tags.all(),
        is_published=True
    ).exclude(id=article.id).distinct()[:3]
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'related_articles': related_articles,
    }
    return render(request, 'articles/article_detail.html', context)

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.is_published = form.cleaned_data.get('is_published', True)
            article.save()
            form.save_m2m()
            messages.success(request, 'Статья успешно создана!')
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Создать статью'})

@login_required
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена!')
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Редактировать статью', 'article': article})

@login_required
@require_POST
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        
        # Проверяем, это ответ на комментарий
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent = get_object_or_404(Comment, id=parent_id)
        
        comment.save()
        messages.success(request, 'Комментарий добавлен!')
    
    return redirect('article_detail', slug=slug)

@login_required
@require_POST
def toggle_like(request, slug):
    article = get_object_or_404(Article, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, article=article)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': article.get_likes_count()
    })


