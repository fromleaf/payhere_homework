"""
URL configuration for payhere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import accounts.urls as accounts_urls
import products.urls as products_urls
from payhere.core.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="payhere API",
        default_version='v1',
        description="payhere API"
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    )
]

urlpatterns += [
    path('accounts/', include(accounts_urls)),
    path('products/', include(products_urls)),
]
