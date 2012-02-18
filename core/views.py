# Create your views here.

# django stuff
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

# app stuff
from tcc3.core.models import Post, Post_Access

# 3rd party stuff
from datetime import datetime
from time import mktime, gmtime
import feedparser

def home_page(request):
    """pull the posts for each of the sites on the homepage from the db"""

    max_posts = 7
    all_fetched_posts = {}
    
    for site in settings.SITES:
        all_fetched_posts[site] = {}
        posts = Post.objects.filter(site=site).order_by("published")[0:max_posts]
        all_fetched_posts[site] = posts
    #assert False
    return render_to_response('tcc2/index.html', {'all_fetched_posts': all_fetched_posts, 'sites': settings.SITES})

def post(request, post_num):
    try:
        post_id = int(post_num)
    except ValueError:
        raise Http404()
    return HttpResponse("you are trying to view post number %d" % post_id)
    
def fetch_posts(request):
    """check all the sites to see if there are new posts and write then into the db if so"""
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
        all_fetched_posts[site]['meta']['last_updated_epoch'] = string_to_epoch(feed.entries[0].updated, site)
        
        for item in range( min(10, len(feed.entries) ) ):   # 10 is a sanity cap so we don't parse entire 100 item feed
            try:
                title   = feed.entries[item].title 
                link    = feed.entries[item].link
                epoch   = string_to_epoch( feed.entries[item].updated, site )
            except:
                # log value not found
                return HttpResponse("error getting value for %s" % site)            
            
            # now that we've gotten the values for this feed item, let's see if we have it in the DB
            try:
                p = Post.objects.get(url=link)
            except Post.DoesNotExist:
                date = epoch_to_django_date( epoch )
                Post.objects.create(site=site, url=link, title=title, published=date)
                
                # get the data to pass to view, in case someone's watching
                post_data = dict(title=title, link=link, date=date)
                all_fetched_posts[site]['posts'][item] = post_data
            else:
                # this post already exists, don't add it
                pass
            

    return render_to_response('tcc3/fetched.html', {'all_data': all_fetched_posts})

# helper functions
def string_to_epoch(datetime_string, site):
    """turn those pesky date strings into an epoch time"""
    
    # different date formats on different sites, oh boy!
    if site == 'hf':
        format_string = '%Y-%m-%dT%H:%M:%S.%f-05:00'
    elif site == 'fnt':
        format_string = '%a, %d %b %Y %H:%M:%S PST'
    else:
        format_string = '%a, %d %b %Y %H:%M:%S +0000'
        
    datetime_object = datetime.strptime(datetime_string, format_string)
    return mktime( datetime_object.timetuple() )
    
def epoch_to_django_date(epoch):
    time = gmtime(epoch)
    return "%s-%s-%s %s:%s" % (time.tm_year, str(time.tm_mon).zfill(2), str(time.tm_mday).zfill(2), time.tm_hour, time.tm_min)
    

# smoke test!
def smoke_test(request):
    """is anything on fire? no? good."""
    now = datetime.now()
    return render_to_response('smoke_test.html', {'current_date': now})
        
        