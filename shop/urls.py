"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import (test_view, products_list, ProductsListView, ProductDetailsView, CreateProductView,
                           UpdateProductView, DeleteProductView, )
from product.views import (ProductViewSet, ReviewViewSet)

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('reviews', ReviewViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # path('', test_view),
    # path('api/v1/products/', ProductsListView.as_view()),
    # path('api/v1/products/details/<int:pk>/', ProductDetailsView.as_view()),
    # path('api/v1/products/create/', CreateProductView.as_view()),
    # path('api/v1/products/update/<int:pk>/', UpdateProductView.as_view()),
    # path('api/v1/products/delete/<int:pk>/', DeleteProductView.as_view()),
    # path('api/v1/products/', ProductViewSet.as_view(
    #     {'post': 'create', 'get': 'list'}
    # )),
    #
    # path('api/v1/products/<int:pk>/', ProductViewSet.as_view(
    #     {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
    # )),
    path('api/v1/', include('account.urls')),
    path('api/v1/', include('order.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
