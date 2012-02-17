# Create your views here.

# django stuff
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

# app stuff
from tcc3.core.models import Post, Post_Access

# 3rd party stuff
from datetime import datetime
from time import mktime
import feedparser

def home_page(request):

    max_posts = 7
    posts_data = {}
    
    for site in settings.SITES:
        posts = Post.objects.filter(site=site).order_by("published")[0:max_posts]
        posts_data[site] = posts
    
    return render_to_response('tcc2/index.html', {'posts_data': posts_data, 'sites': settings.SITES})

def post(request, post_num):
    try:
        post_id = int(post_num)
    except ValueError:
        raise Http404()
    return HttpResponse("you are trying to view post number %d" % post_id)

def smoke_test(request):
    now = datetime.now()
    return render_to_response('smoke_test.html', {'current_date': now})
    
def fetch_posts(request):
    """
        all_fetched_posts is a bit of a beast. for clarity:
        
        '<site>' : {
            'meta': {
                'recent_epoch' : <value>
            }
            'posts': {
                0 : {
                    'title': <title>
                    'link' : <link>
                    'date' : <date>
                }
                1 : {
                    'title': <title>
                    'link' : <link>
                    'date' : <date>
                }
                ...
            }
        }
        
    """
    
    all_fetched_posts = {} # initialize this motherfucker!
    
    for site in settings.SITES:
    
        all_fetched_posts[site] = {}
        all_fetched_posts[site]['meta'] = {}
        all_fetched_posts[site]['posts'] = {}
        
        feed_url = settings.SITES_DATA[site]['feed']
        feed = feedparser.parse(feed_url)
        
        # did we catch anything good?
        if not feed.get('status') or not feed.status == 200:
            # log error grabbing site's feed
            return HttpResponse("error grabbing feed for %s" % site)
        
        if feed.bozo == 1:
            # log site's malformed feed
            return HttpResponse("malformed feed for %s" % site)
            
        # try to get the most recent item and find when it was published
        last_updated = feed.entries[0].updated
        all_fetched_posts[site]['meta']['last_updated_string'] = feed.entries[0].updated
        
        # different date formats on different sites, oh boy!
        if site == 'hf':
            all_fetched_posts[site]['meta']['last_updated_datetime'] = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S.%f-05:00')
        elif site == 'fnt':
            all_fetched_posts[site]['meta']['last_updated_datetime'] = datetime.strptime(last_updated, '%a, %d %b %Y %H:%M:%S PST')
        else:
            all_fetched_posts[site]['meta']['last_updated_datetime'] = datetime.strptime(last_updated, '%a, %d %b %Y %H:%M:%S +0000')
            
        all_fetched_posts[site]['meta']['last_updated_epoch'] = mktime( all_fetched_posts[site]['meta']['last_updated_dt'].timetuple() )
        
        for item in range( min(10, len(feed.entries) ) ):
            try:
                title   = feed.entries[item].title 
                link    = feed.entries[item].link
                date    = feed.entries[item].updated
            except:
                # log value not found
                return HttpResponse("error getting value for %s" % site)
                
            post_data = dict(title=title, link=link, date=date)
            
            all_fetched_posts[site]['posts'][item] = post_data
            #Post.objects.create(site=site, url=link, title=title, published=date)
    assert False
    return render_to_response('tcc3/fetched.html', {'all_data': all_fetched_posts})
