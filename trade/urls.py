from django.urls import path
from . import views

app_name = "trade"
urlpatterns = [
    path("", view=views.GetTrade.as_view(), name="search_trade"),
    path("search/", view=views.GetXcoin.as_view(), name="search_api"),
]