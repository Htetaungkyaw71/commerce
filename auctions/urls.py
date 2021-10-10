from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.create,name="create"),
    path('categories',views.categories,name="categories"),
    path('watchlist',views.watchlist,name="watchlist"),
    path('<int:detail_id>',views.detail,name="detail"),
    path('<int:detail_id>/add',views.add,name="add"),
    path('<int:detail_id>/remove',views.remove,name="remove"),
    path('<int:detail_id>/category',views.category,name="category"),
    path('<int:detail_id>/comment',views.comment,name="comment"),
    path('<int:detail_id>/bid',views.bid,name="bid"),
    path('<int:detail_id>/close',views.close,name="close"),
    path('<int:detail_id>/remove_comment/<int:post_id>/',views.remove_comment,name="remove_comment"),


    

]
