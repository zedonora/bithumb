from django.urls import path
from . import views

app_name = "trade"
urlpatterns = [
    path("", view=views.GetTrade.as_view(), name="search_trade"),
    path("search/", view=views.GetXcoin.as_view(), name="search_api"),
    path("compare/", view=views.GetTicker.as_view(), name="get_ticker"),
    path("ajax/getticker/", view=views.GetAjaxTicker.as_view(), name="get_ajax_ticker"),
]