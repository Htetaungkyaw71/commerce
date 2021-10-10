from django.contrib import admin
from .models import Category,Listing,User,Watchlist,Comment,Bid,Close


admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Close)
