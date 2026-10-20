from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Place, Comment, Favorite
from django.utils.http import url_has_allowed_host_and_scheme


# Create your views here.
def listing_list(requests):
      return render(requests, 'listings/list.html')


def listing_create(requests):
      return render(requests, 'listings/create.html')





def aboutus_view(request):
      return render(request, "sites/aboutus.html")




def places_view(request):
      places = (
            Place.objects
            .prefetch_related("images")
            .order_by("-created_at")
      )

      return render(request, "sites/places.html", {
      "places": places,
      })\

def privacy_view(request):
      return render(request, "sites/privacy.html")

def terms_view(request):
      return render(request, "sites/terms.html")


def listing_detail(request, pk):
      place = get_object_or_404(Place, pk=pk)

      if request.method == "POST":
            if not request.user.is_authenticated:
                  return redirect("registration:login")

            text = request.POST.get("text", "").strip()

            if text:
                  Comment.objects.create(
                  place=place,
                  author=request.user,
                  text=text
                  )

                  return redirect("listings:detail", pk=place.pk)

      recommended_places = (
            Place.objects.exclude(pk=place.pk)
            .order_by("-created_at")[:6]
      )

      comments = place.comments.select_related("author").all()

      is_favorite = False

      if request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(
            user=request.user,
            place=place
      ).exists()

      context = {
            "place": place,
            "recommended_places": recommended_places,
            "comments": comments,
            "is_favorite": is_favorite,
      }

      return render(request, "sites/place_detail.html", context)

@login_required(login_url="registration:login")
def toggle_favorite(request, place_id):
      if request.method != "POST":
            return redirect("listings:detail", pk=place_id)

      place = get_object_or_404(Place, pk=place_id)

      favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            place=place
      )

      if not created:
            favorite.delete()
      next_url = request.POST.get("next", "")

      if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
      ):
            return redirect(next_url)

      return redirect("listings:detail", pk=place_id)


      


@login_required(login_url="registration:login")
def favorites(request):
      favorite_places = (
            Place.objects.filter(favorites__user=request.user)
            .prefetch_related("images")
            .order_by("-favorites__created_at")
      )

      return render(
            request,
            "sites/favorites.html",
            {"places": favorite_places}
      )