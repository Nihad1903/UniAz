from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('unichat.urls')),
    path("ads.txt", TemplateView.as_view(template_name="ads.txt", content_type="text/plain")),
]
