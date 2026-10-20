from django.urls import path
from . import views
from .views import aboutus_view
from .views import privacy_view

app_name = "listings"

urlpatterns = [
      path(
            "",
            views.listing_list,
            name="list"
      ),
      path(
            "create/",
            views.listing_create,
            name="create"
      ),

      path(
            "<int:pk>/", 
            views.listing_detail, 
            name="detail"),
      
      path(
            "about/", 
            aboutus_view, 
            name="aboutus"),
      
      path(
            "places/", 
            views.places_view, 
            name="places"),

      path(
            "privacy/", 
            privacy_view, 
            name="privacy"),

      path(
            "terms/", 
            views.terms_view, 
            name="terms"),

      path(
            "<int:pk>/",
            views.listing_detail,
            name="detail"),

      path(
            "favorite/<int:place_id>/toggle/",
            views.toggle_favorite,
            name="toggle_favorite",
            ),
      path(
            "favorites/",
            views.favorites,
            name="favorites",
            ),
      ]
