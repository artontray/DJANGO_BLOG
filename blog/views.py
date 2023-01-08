from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .models import Comment
from .forms import CommentForm
from django.template import loader
from django.views.generic.base import TemplateView

class PostList(generic.ListView):
    model = Post



    context_object_name = 'all_post'
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    # queryset = Post.objects.filter(status=1,comments__body__contains="fvsgfdgffd").order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['comment_count'] = Comment.objects.all()
        context['display_all_post'] = Post.objects.all()
        # import pdb;pdb.set_trace()
        
        # context['post_count'] = Post.objects.all().count()
        return context



class Ex2View(TemplateView):

    template_name = "index.html"


    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
       
        #. context = Comment.objects.filter(approved=True).order_by("-created_on")
        context['posts'] = Comment.objects.all().count()
        context['data'] = "context data from Ex2"
        return context



class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
		        "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )    


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))