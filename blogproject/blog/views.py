from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Tag
from markdown import markdown,Markdown
from comment.forms import CommentForm
from django.views.generic import ListView,DetailView

from  django.db.models import Q
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list':post_list})
    # return HttpResponse('<h1>hellow world</h1>')

class IndexView(ListView):
    #获取模型，获取的模型是Post
    model = Post
    #指定这个试图渲染的模板
    template_name = 'blog/index.html'
    #指定获取的模型列表数据保存的变量名为post_list，这个变量名会传递给模板
    context_object_name = 'post_list'
    #类视图ListView已写好了分页的功能，只需调用这个属性给它赋一个值即可（表示每页显示多少条数据）
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)
        return context
    def pagination_data(self,paginator,page,is_paginated):
        #首先是要先判断一下是否有分页
        if not is_paginated:
            return {}
        #显示首页，值为Ｔure时显示
        first = False
        #左边的仨点
        left_has_more = False
        #当前页左边显示的页码
        left = []
        #当前页右边显示的页码
        right = []
        #当前页右边的仨点
        right_has_more = False
        #最后一页
        last = False
        #当前页
        page_number = page.number
        #获取分页后的页总数
        total_pages = paginator.num_pages
        #获取的是分页后所有页的页码的列表，不过后面的这个获取方法，我还不知道，没找着
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            #取这个当前页左边的两页，因为page_range的里面存的是所有页码的列表，而取它需要用下标来取，所以后面应写【当前页-3】才能取到左边第二个页码值
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
                #为什么这个判断中不用写是否显示首页，因为下面还有一个判断语句，只要这个值大于1就显示，这里的这个大于二判断的，都大于2了，所以肯定会执行下面的那个判断
                #first = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if left[0] > 2:
                left_has_more = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages:
                last = True
        data = {
            'first':first,
            'left_has_more':left_has_more,
            'left':left,
            'right':right,
            'right_has_more':right_has_more,
            'last':last
        }
        return data






# def detail(request,pk):
#     post = get_object_or_404(Post,pk = pk)
#     post.increase_views()
#     post.body = markdown(post.body,
#                          extensions=[
#                              'markdown.extensions.extra',
#                              'markdown.extensions.codehilite',
#                              'markdown.extensions.toc',
#                          ])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post': post,
#         'form': form,
#         'comment_list': comment_list,
#     }
#     return render(request,'blog/detail.html',context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        #因为context已有post，所以不用在添加，
        # 并且context后面用的不是等于号，而是用update用来上传就行
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context


# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request,'blog/index.html',context={'post_list': post_list})

class ArchivesView(IndexView):
    #记住基类中的这个方法就是从模型获取数据列表
    def get_queryset(self):
        return super().get_queryset().filter(
                            #获取URL传递的参数：self.kwargs.get('某某')
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
        )

# def category(request,pk):
    # cate = get_object_or_404(Category,pk = pk)
    # post_list = Post.objects.filter(category=cate)
    # return render(request,'blog/index.html',context={'post_list': post_list})

class CategoryView(IndexView):
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'
        #get_queryset这个方法实际上就是从模型中获取数据，
        # 咱写的这个模型是Post，所以获取的就是Post类的所有对象，
        # 我们在此只是重写一下这个方法，让这个方法添加一个过滤，
        # 只要属于cate这个类别下的所有post
    def get_queryset(self):
        cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk = self.kwargs.get('pk'))
        return super().get_queryset().filter(tags = tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request,'blog/index.html',{'error_msg':error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request,'blog/index.html',{'post_list':post_list})