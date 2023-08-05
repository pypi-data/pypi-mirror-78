# Django libraries
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# 3rd party libraries
# Standard/core python libraries
# Our custom libraries

# VARSIONS URLS (ALL VERSIONS)
urlpatterns = [
    # VERSIONS URLS (Managed by SPRINGLABS_DJANGO)  

    url(r'^v19/', include('api.v19.urls', namespace='v19')), 
 

    url(r'^v18/', include('api.v18.urls', namespace='v18')), 
 

    url(r'^v9/', include('api.v9.urls', namespace='v9')), 
 

    url(r'^v8/', include('api.v8.urls', namespace='v8')), 
 

    url(r'^v7/', include('api.v7.urls', namespace='v7')), 
 

    url(r'^v7/', include('api.v7.urls', namespace='v7')), 
 

    url(r'^v6/', include('api.v6.urls', namespace='v6')), 
 

    url(r'^v6/', include('api.v6.urls', namespace='v6')), 
 

    url(r'^v5/', include('api.v5.urls', namespace='v5')), 
 

    url(r'^v4/', include('api.v4.urls', namespace='v4')), 
    url(r'^v3/', include('api.v3.urls', namespace='v3')),
    url(r'^v2/', include('api.v2.urls', namespace='v2')), 
    url(r'^v1/', include('api.v1.urls', namespace='v1')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
