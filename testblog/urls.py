from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Testblog Documentation",
        default_version='v1',
        description="Testblog REST API documentation",
        terms_of_service="https://www.testblog.ru",
        contact=openapi.Contact(email="test@blog.ru"),
        license=openapi.License(name="Test License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls', 'users_api')),
    path('api/posts/', include('blogposts.urls', 'blogpost_api')),
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='docs-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs-swagger-ui'),
]
