from django.shortcuts import render,redirect,get_object_or_404
from .models import Article,Author,Tag
from .forms import ArticleForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models.aggregates import Count,Sum,Avg,Max,Min

def blog(request):
    author_username = request.GET.get('author')
    authors = Author.objects.all().annotate(article_count = Count('article'),view_count=Avg('article__view_count'))
    articles = Article.objects.all()
    tags = Tag.objects.all().annotate(article_count = Count('article'),view_count=Sum('article__view_count')).order_by('-view_count')


    total_article_count = articles.count()
    view_count_statistic = articles.aggregate(
        total_view_count=Sum('view_count'),
        avg_view_count = Avg('view_count'),
        max_view_count = Max('view_count'),
        min_view_count = Min('view_count'),
    )
    author_username = request.GET.get('author')
    tag_title = request.GET.get('tag')
    page_number = int(request.GET.get('page',1))
    if author_username:
        articles = articles.filter(author__user__username=author_username)
    if tag_title:
        articles = articles.filter(tags__title=tag_title)


    paginator = Paginator(articles,2)
    page = paginator.page(page_number)
    articles = page.object_list

    return render(request,'blog.html',
        context = {'articles': articles,'authors': authors,
                   'tags':tags,'paginator':paginator,
                   'page':page,'total_article_count' : total_article_count,
                   'view_count_statistic': view_count_statistic,
                   'max_viewed_articles': Article.objects.filter(view_count = view_count_statistic.get('max_view_count')),
                   'min_viewed_articles': Article.objects.filter(view_count = view_count_statistic.get('min_view_count')),
                   
    })

def blog_detail(request,pk):
    article = Article.objects.get(pk=pk)
    article.view_count = F('view_count') + 1
    article.refresh_from_db()
    article.save()
    return render(request,'blog-detail.html',context = {'article':article })

def add_article(request):
    if request.method == 'POST':
       form = ArticleForm(data=request.POST,files=request.FILES)
       if form.is_valid():
           form.save(request.user.author)
           return redirect('blog:article-list')
       return render(request,'article-form.html',{'form':form})
    else:
        form = ArticleForm()
        return render(request,'article-form.html',{'form':form})

def edit_article(request,pk):
    article = get_object_or_404(Article,pk=pk)
    if article.author.user != request.user:
        raise PermissionDenied() 
    if request.method == 'POST':
       form = ArticleForm(instance=article,data=request.POST,files=request.FILES)
       if form.is_valid():
           form.save(request.user.author) # type: ignore
           return redirect('blog:article-list')
       return render(request,'article-form.html',{'form':form})
    else:
        form = ArticleForm(instance=article)
        return render(request,'article-form.html',{'form':form})
    
def delete_article(request,pk):
    article = get_object_or_404(Article,pk=pk)
    if article.author.user != request.user:
        raise PermissionDenied()
    article.delete()
    return redirect('blog:article-list')