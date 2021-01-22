from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_permission_codename
from django.urls import reverse
from django.utils.html import format_html

from typeidea.custom_site import custom_site

from typeidea.base_admin import BaseOwnerAdmin
from .adminforms import PostAdminForm
from .models import Post, Category, Tag


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

# SSO
# PERMISSION_API = "http://permission.sso.com/has_perm?user={}&perm_code={}"

@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # SSO
    # def has_add_permission(self, request):
    #     opts = self.opts
    #     codename = get_permission_codename('add', opts)
    #     perm_code = "%s.%s" % (opts.app_label, codename)
    #     resp = request.get(PERMISSION_API.format(request.user.username, perm_code))
    #     if resp.status_code == 200:
    #         return True
    #     else:
    #         return False

    form = PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator', 'owner'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    exclude = ('owner', )

    fieldsets = (
        ('基础配置',{
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
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
            'fields': ('tag', ),
        })
    )
    filter_horizontal = ('tag', )  #filter_vertical = ('tags', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    class Media:
        """ 自定义静态资源 """
        css = {
            'all': ("https://github.com/bootcdn/BootCDN/tree/1.0.1/ajax/libs/bootstrap/4.1.3/css/"
                    "bootstrap.min.css", )
        }
        js = ("https://github.com/bootcdn/BootCDN/blob/1.0.1/ajax/libs/bootstrap/4.1.3/js/bootstrap.bundle.js", )


class PostInline(admin.StackedInline):  # StackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1   # 控制额外多几个
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')


# 查看操作日志
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']


