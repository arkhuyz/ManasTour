
from django.db import models
from django.conf import settings
from django.db.models import Avg


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     icon = models.ImageField(
#         upload_to="categories/",
#         blank=True,
#         null=True
#     )
#
#     def __str__(self):
#         return self.name


class Factor(models.Model):
      name = models.CharField(max_length=100)
      factor_type = models.CharField(max_length=100)

      def __str__(self):
            return self.name


class Category(models.Model):
      name = models.CharField(
            max_length=100,
            unique=True
      )

      slug = models.SlugField(
            max_length=100,
            unique=True,
            blank=True,
            null=True
      )

      def __str__(self):
            return self.name


class Place(models.Model):
      PRICE_CHOICES = [
            ("free", "Бесплатно"),
            ("paid", "Платно"),
      ]

      title = models.CharField(max_length=200)

      description = models.TextField()

      category = models.ForeignKey(
            Category,
            on_delete=models.CASCADE,
            related_name="places"
      )

      address = models.CharField(max_length=300)

      latitude = models.DecimalField(
            max_digits=9,
            decimal_places=6
      )

      longitude = models.DecimalField(
            max_digits=9,
            decimal_places=6
      )

      price_type = models.CharField(
            max_length=20,
            choices=PRICE_CHOICES,
            default="free"
      )

      price = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True
      )

      working_hours = models.CharField(
            max_length=200,
            blank=True
      )

      factors = models.ManyToManyField(
            Factor,
            blank=True,
            related_name="places"
      )

      created_at = models.DateTimeField(auto_now_add=True)

      updated_at = models.DateTimeField(auto_now=True)

      # @property
      # def average_rating(self):
      #       result = self.reviews.filter(
      #             is_moderated=True
      #       ).aggregate(
      #             average=Avg("rating")
      #       )

      #       return round(result["average"] or 0, 2)

      def __str__(self):
            return self.title


class PlaceImage(models.Model):
      place = models.ForeignKey(
            Place,
            on_delete=models.CASCADE,
            related_name="images"
      )

      image = models.ImageField(
            upload_to="places/",
            default="default.png"
      )

      is_main = models.BooleanField(
            default=False
      )

      def __str__(self):
            return f"Фото места: {self.place.title}"


class Comment(models.Model):
      place = models.ForeignKey(
            "Place",
            on_delete=models.CASCADE,
            related_name="comments"
      )
      author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="place_comments"
      )
      text = models.TextField("Текст комментария", max_length=2000)
      created_at = models.DateTimeField("Дата создания", auto_now_add=True)

      class Meta:
            ordering = ["-created_at"]
            verbose_name = "Комментарий"
            verbose_name_plural = "Комментарии"

      def __str__(self):
            return f"Комментарий от {self.author} к {self.place}"
      

class Favorite(models.Model):
      user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="favorite_places"
      )
      place = models.ForeignKey(
            "Place",
            on_delete=models.CASCADE,
            related_name="favorites"
      )
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
            constraints = [
                  models.UniqueConstraint(
                  fields=["user", "place"],
                  name="unique_user_favorite_place"
                  )
            ]
            verbose_name = "Избранное место"
            verbose_name_plural = "Избранные места"

      def __str__(self):
            return f"{self.user} — {self.place}"