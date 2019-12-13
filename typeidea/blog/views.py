from django.shortcuts import render
from .models import Post, Tag, Category
from config.models import SideBar

# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExit:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all()
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)

from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

from .models import Post, Category, Tag
from config.models import SideBar


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#
# class PostListView(ListView):
#     queryset = Post.latest_posts()
#     paginate_by = 1
#     context_object_name = 'post_list' # 如果不设置此项，在模块中需要使用objec_list变量
#     template_name = 'blog/list.html'

# 处理分类导航，侧边栏，底部导航等基础数据
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

class IndexView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

# 分类列表页
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

# 标签列表页
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset,根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)

class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
