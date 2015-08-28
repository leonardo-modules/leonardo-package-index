from rest_framework.routers import DefaultRouter

from .views import PackageViewSet, CategoryViewSet

router = DefaultRouter()

router.register(r'', PackageViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls
