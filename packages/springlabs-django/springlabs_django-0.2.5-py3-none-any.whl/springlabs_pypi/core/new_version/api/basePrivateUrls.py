# Django libraries
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# 3rd party libraries
# Standard/core python libraries
# Our custom libraries

# PRIVATE URLS name_version
private_urls = [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
