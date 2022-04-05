from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment
from .forms import AuctionListingForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all().order_by('-created_at')
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


# ======================================================================================================================
@login_required(login_url='auctions/login.html')
def create(request):
    return render(request, "auctions/create.html", {
        'form': AuctionListingForm()
    })


@login_required(login_url='auctions/login.html')
def insert(request):
    form = AuctionListingForm(request.POST)
    if form.is_valid():
        auction = AuctionListing(user=request.user, **form.cleaned_data)
        if not auction.image_url:
            auction.image_url = 'https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png'
        auction.save()
        starting_bid = auction.starting_bid
        bid = Bid(amount=starting_bid, user=request.user, auction=auction)
        bid.save()
        print("auction:" + auction.image_url)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create.html', {
            'form': form,
            'error': form.errors
        })


def listing(request, id):
    current = AuctionListing.objects.get(pk=id)
    bid = get_object_or_404(Bid, auction=current)
    comments = Comment.objects.filter(auction=current)
    print("here:" + AuctionListing.objects.get(pk=id).image_url)
    return render(request, 'auctions/listing.html', {
        'auction': current,
        'user': request.user,
        'bid': bid,
        'comments': comments,
        'comment_form': CommentForm()
    })


@login_required(login_url='auctions/login.html')
def update_bid(request, id):
    amount = request.POST['bid']
    if amount:
        amount = float(amount)
        auction = get_object_or_404(AuctionListing, id=id)
        if amount > get_object_or_404(Bid, id=id).amount:
            bid = get_object_or_404(Bid, id=id)
            bid.user, bid.amount = request.user, amount
            bid.save()
            auction.bid_counter += 1
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            raise ValidationError('Bid must be greater than current Bid value')
    else:
        raise ValidationError('Bid must be greater than current Bid value')


@login_required(login_url='auctions/login.html')
def close_bid(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    auction.active, auction.winner = False, request.user.username
    auction.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='auctions/login.html')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


@login_required(login_url='auctions/login.html')
def watch(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    request.user.watchlist.add(auction)
    request.user.watchlist_counter += 1
    request.user.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='auctions/login.html')
def unwatch(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    request.user.watchlist.remove(auction)
    request.user.watchlist_counter -= 1
    request.user.save()
    if '/unwatch/' in request.path:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('wishlist'))


def categories(request):
    return render(request, "auctions/categories.html")


def filter(request):
    q = request.GET['category'].lower()
    return render(request, 'auctions/category.html', {
        'listings': AuctionListing.objects.filter(category=q)
    })


def add_comment(request, id):
    anonymous = User.first_name
    if request.user is not anonymous:
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            comment = Comment(
                user=request.user,
                auction=get_object_or_404(AuctionListing, id=id),
                **f
            )
            comment.save()
            return HttpResponseRedirect(reverse('listing', kwargs={
                'id': id
            }))
    else:
        return render(request, 'auctions/login.html', {
            'message': 'Must be logged in to be able to comment!'
        })
