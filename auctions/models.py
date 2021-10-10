from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    owner = models.ForeignKey('User',on_delete=models.CASCADE,related_name="poster")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    image = models.URLField()
    price = models.IntegerField()
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name="categories")

    def __str__(self):
        return f"{self.title} {self.description} {self.image} {self.price}"


class Watchlist(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name="watcher")
    watchlist = models.ManyToManyField('Listing',blank=True,related_name="list")


class Comment(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name="commenter")
    message = models.CharField(max_length=200)
    post = models.ForeignKey('Listing',on_delete=models.CASCADE,related_name="p")

    def __str__(self):
        return f"{self.message}"




class Bid(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name="bidder")
    bid_price = models.IntegerField()
    post = models.ForeignKey('Listing',on_delete=models.CASCADE,related_name="pp")

    def __str__(self):
        return f"{self.bid_price}"

class Close(models.Model):
    post = models.ForeignKey('Listing',on_delete=models.CASCADE,related_name="close_post")
    



