from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from webapp.models import Post


def index(request):
    latest_posts_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('webapp/index.html')
    context = { 'latest_posts_list': latest_posts_list }
    return render(request, 'webapp/index.html', context)

def detail(request, post_id):
    return HttpResponse("You're looking at post %s." % post_id)