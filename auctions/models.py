from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist_counter = models.IntegerField(default=0, blank=True)
    watchlist = models.ManyToManyField('AuctionListing', related_name='watchlist', blank=True)
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(default='https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    bid_counter = models.IntegerField(default=1, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.title}: by {self.user.username}'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, related_name='bids')

    def __str__(self):
        return f'{self.amount} on {self.auction} by {self.user.username}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self):
        return f'{self.user}: {self.text}'