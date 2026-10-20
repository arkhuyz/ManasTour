
from django.shortcuts import render
from listings.models import Place

def home(request):
      places = (
            Place.objects
            .prefetch_related("images")
            .order_by("-created_at")[:8]
      )

      print(places)

      context = {
            "places": places
      }

      return render(
            request,
            template_name="home.html",
            context=context
      )
