from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,View
from .models import Post,Comment
from taggit.models import Tag
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.db.models import Count

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        if self.kwargs.get('tag',False):
            tag = get_object_or_404(Tag,slug=self.kwargs['tag'])
            return Post.objects.filter(tags__in=[tag])
        return Post.objects.all()
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('tag',False):
            tag = get_object_or_404(Tag,slug=self.kwargs['tag'])
            context['tag'] = tag
        return context

class PostDetailView(View):
    def get(self,*args,**kwargs):
        p = get_object_or_404(Post,slug=kwargs.get('slug'))
        post_tags_ids = p.tags.values_list('id',flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=p.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
        context = {
           'post':p,
           'comments':p.comments.filter(active=True),
           'form': CommentForm(),
           'similar_posts':similar_posts
        }
        print(similar_posts)
        return render(self.request,'blog/post-detail.html',context=context)
    
    def post(self,*args,**kwargs):
        form = CommentForm(self.request.POST or None)
        p = get_object_or_404(Post,slug=kwargs.get('slug'))
        post_tags_ids = p.tags.values_list('id',flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=p.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
        
        context = {
           'post':p,
           'comments':p.comments.filter(active=True),
           'form':CommentForm(),
           'similar_posts':similar_posts
        }
        if form.is_valid():
            n_form = form.save(commit=False)
            n_form.post = p
            n_form.save()

        return render(self.request,'blog/post-detail.html',context=context)

class SharePostView(View):
    def get(self,*args,**kwargs):
        form = EmailPostForm()
        return render(self.request,'blog/share.html',context={'form':form})
    
    def post(self,*args,**kwargs):
        form = EmailPostForm(self.request.POST or None)
        p = get_object_or_404(Post,slug=kwargs.get('slug'))
        post_url = self.request.build_absolute_uri(p.get_absolute_url())
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], p.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(p.title, post_url, cd['name'], cd['comments'])
            send_mail(subject,message,'kingstugi@devs.com',[cd['to']])
        return render(self.request,'blog/share.html')

