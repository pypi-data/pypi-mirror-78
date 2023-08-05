# Django libraries
from django.conf.urls import include, url
# 3rd party libraries
from rest_framework.renderers import (
    CoreJSONRenderer, DocumentationRenderer, SchemaJSRenderer
)
from rest_framework.schemas import SchemaGenerator, get_schema_view
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny
# Standard/core python libraries
# Our custom libraries


def get_docs_view(
        title=None, description=None, schema_url=None, urlconf=None,
        public=True, patterns=None, generator_class=SchemaGenerator,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
        permission_classes=[AllowAny],
        renderer_classes=None):

    if renderer_classes is None:
        renderer_classes = [DocumentationRenderer, CoreJSONRenderer]
    return get_schema_view(
        title=title,
        url=schema_url,
        urlconf=urlconf,
        description=description,
        renderer_classes=renderer_classes,
        public=public,
        patterns=patterns,
        generator_class=generator_class,
        authentication_classes=authentication_classes,
        permission_classes=permission_classes,
    )


def get_schemajs_view(
        title=None, description=None, schema_url=None, urlconf=None,
        public=True, patterns=None, generator_class=SchemaGenerator,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
        permission_classes=[AllowAny]):
    renderer_classes = [SchemaJSRenderer]

    return get_schema_view(
        title=title,
        url=schema_url,
        urlconf=urlconf,
        description=description,
        renderer_classes=renderer_classes,
        public=public,
        patterns=patterns,
        generator_class=generator_class,
        authentication_classes=authentication_classes,
        permission_classes=permission_classes,
    )


def include_docs_urls(
        title=None, description=None, schema_url=None, urlconf=None,
        public=True, patterns=None, generator_class=SchemaGenerator,
        authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,
        permission_classes=[AllowAny],
        renderer_classes=None, namespace='api-docs'):

    docs_view = get_docs_view(
        title=title,
        description=description,
        schema_url=schema_url,
        urlconf=urlconf,
        public=public,
        patterns=patterns,
        generator_class=generator_class,
        authentication_classes=authentication_classes,
        renderer_classes=renderer_classes,
        permission_classes=permission_classes,
    )

    schema_js_view = get_schemajs_view(
        title=title,
        description=description,
        schema_url=schema_url,
        urlconf=urlconf,
        public=public,
        patterns=patterns,
        generator_class=generator_class,
        authentication_classes=authentication_classes,
        permission_classes=permission_classes,
    )
    urls = [
        url(r'^$', docs_view, name='docs-index'),
        url(r'^schema.js$', schema_js_view, name='schema-js')
    ]
    return include((urls, 'api-docs'), namespace=namespace)
