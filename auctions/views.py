from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required



from .models import User,Category,Listing,Watchlist,Comment,Bid,Close


def index(request):
    if request.user.is_authenticated:
        lists = Watchlist.objects.filter(user=request.user).all()
        d = 0
        b = []
        for i in lists:
            for a in i.watchlist.all():
                b.append(a)
                d = len(b)
        return render(request, "auctions/index.html",{
        'listings':Listing.objects.all(),
        'c':d
    })        
    close_posts = []
    for c in Close.objects.all():
        close_posts.append(c.post) 
    return render(request, "auctions/index.html",{
        'listings':Listing.objects.all(),
        'close_posts' : close_posts,
    })

def detail(request,detail_id):  
    ok = False
    post = Listing.objects.get(pk=detail_id)
    for i in post.list.all():
        if post in i.watchlist.all():
            ok=True 
    result = post.price
    winner = None
    for b in post.pp.all():
        result = b.bid_price
        winner = b.user
    owner = False
    if request.user == post.owner:
        owner = True
    close_posts = []
    for c in Close.objects.all():
        close_posts.append(c.post)
    return render(request,"auctions/detail.html",{
        'post':post,
        'ok':ok,
        'comments':post.p.all(),
        'current_bid_price':result,
        'winner':winner,
        'owner':owner,
        'close_posts' : close_posts,
        
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create(request):
    lists = Watchlist.objects.filter(user=request.user).all()
    d = 0
    b = []
    for i in lists:
        for a in i.watchlist.all():
            b.append(a)
            d = len(b)
    c  = Category.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        create_listing = Listing.objects.create(owner=request.user,title=title,description=description,image=image,price=price,category=category)
        create_listing.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request,"auctions/create.html",{
        'categories':c, 
        'c':d,
    })

@login_required(login_url='login')
def add(request,detail_id):
    post = Listing.objects.get(pk=detail_id)
    w = Watchlist.objects.create(user=request.user)
    w.save()  
    w.watchlist.add(post)
    return HttpResponseRedirect(reverse('watchlist'))


@login_required(login_url='login')
def watchlist(request):
    lists = Watchlist.objects.filter(user=request.user).all()
    c = 0
    b = []
    for i in lists:
        for a in i.watchlist.all():
            b.append(a)
            c = len(b)
    return render(request,"auctions/watchlist.html",{
        'lists':lists,
        'c':c,
    })

@login_required(login_url='login')
def remove(request,detail_id):
    post = Listing.objects.get(pk=detail_id)
    Watchlist.objects.filter(watchlist=post).delete()
    return HttpResponseRedirect(reverse('detail',args=(post.id,)))



def categories(request):
    if request.user.is_authenticated:
        lists = Watchlist.objects.filter(user=request.user).all()
        c = 0
        b = []
        for i in lists:
            for a in i.watchlist.all():
                b.append(a)
                c = len(b)
        return render(request,"auctions/categories.html",{
        'categories':Category.objects.all(),   
        'c':c   
    })
    return render(request,"auctions/categories.html",{
        'categories':Category.objects.all(),      
    })

def category(request,detail_id):
    if request.user.is_authenticated:
        lists = Watchlist.objects.filter(user=request.user).all()
        c = 0
        b = []
        for i in lists:
            for a in i.watchlist.all():
                b.append(a)
                c = len(b)
        return render(request,"auctions/category.html",{
        'categories':Listing.objects.filter(category=detail_id).all(),
        'aa':Listing.objects.filter(category=detail_id).first(),
        'c':c,
       
    })
    return render(request,"auctions/category.html",{
        'categories':Listing.objects.filter(category=detail_id).all(),
        'aa':Listing.objects.filter(category=detail_id).first(),
    })

@login_required(login_url='login')
def comment(request,detail_id):
    post = Listing.objects.get(id=detail_id)
    if request.method == "POST":
        message = request.POST['message']
        create_comment = Comment.objects.create(user=request.user,message=message,post=post)
        create_comment.save()
        return HttpResponseRedirect(reverse('detail',args=(post.id,)))


@login_required(login_url='login')
def remove_comment(request,detail_id,post_id):
    post = Listing.objects.get(id = post_id)
    comment = Comment.objects.get(id=detail_id).delete()
    return HttpResponseRedirect(reverse('detail',args=(post.id,)))
         

@login_required(login_url='login')
def bid(request,detail_id):
    post = Listing.objects.get(id=detail_id)
    if request.method == "POST":
        bid_price = int(request.POST["bid_price"])
        if bid_price < post.price:
            messages.error(request,"you need to bid higher than current price ")
            return HttpResponseRedirect(reverse('detail',args=(post.id,)))  
        else:
            create_bid = Bid.objects.create(user=request.user,bid_price=bid_price,post=post)
            create_bid.save()
            return HttpResponseRedirect(reverse('detail',args=(post.id,)))  


def close(request,detail_id):
    post = Listing.objects.get(id=detail_id)
    create_close = Close.objects.create(post=post)
    create_close.save()
    return HttpResponseRedirect(reverse('detail',args=(post.id,)))  
    
     
