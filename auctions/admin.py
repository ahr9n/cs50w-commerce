from django.contrib import admin
from .models import User, AuctionListing, Comment, Bid

# Register your models here.
admin.site.site_header = "Auction's site Administration"


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "price", "starting_bid", "created_at")


class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "auction", "created_at")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "auction", "created_at")


admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
