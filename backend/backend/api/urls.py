from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ImageViewset, SearchView

router = DefaultRouter()
router.register("image", ImageViewset, basename="image")

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
]

urlpatterns += router.urls
