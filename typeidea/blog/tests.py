from django.test import TestCase

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.admin.options import get_content_type_for_model

from typeidea.blog.models import Post

post = Post.objects.get(id=1)
log_entries = LogEntry.objects.filter(
    content_type_id = get_content_type_for_model(post).pk,
    object_id = post.id
)
print(log_entries)

