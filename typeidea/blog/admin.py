from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前分类 """

    title = "分类过滤器"
    paramter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name', 'status', 'is_nav', 'created_time')
    list_display = [CategoryOwnerFilter] # 让用户在侧边栏的过滤器只看到自己创建的分类
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category_name']

    actions_on_top = True
    actions_on_bottom = True

    # 编写页面
    save_on_top = True

    exclude = ('owner',)

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/jd/bootstrap.bundle.js', )




