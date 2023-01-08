from . import views
from django.urls import path
from django.views.generic import TemplateView
from blog.views import Ex2View

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    # path("", Ex2View.as_view(), name="home"),
    # path("ex2", TemplateView.as_view(template_name="ex2.html", extra_context={'title': 'Custom Title'})),
]