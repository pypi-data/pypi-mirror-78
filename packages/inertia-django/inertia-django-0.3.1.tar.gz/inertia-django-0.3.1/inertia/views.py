import json
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.middleware import csrf
from .share import share
from .version import asset_version

from django.views.generic import View
from django.conf import settings
from django.core import serializers
from django.forms.models import model_to_dict
import logging

log = logging.getLogger(__name__)


def _build_context(component_name, props, version, url):
    context = {
        "page": {
            "version": version,
            'url': url,
            "component": component_name,
            "props": props
        },
    }
    return context


def render_inertia(request, component_name, props=None, template_name=None):
    """
    Renders either an HttpRespone or JsonResponse of a component for
    the use in an InertiaJS frontend integration.
    """
    inertia_template = None
    inertia_template = getattr(settings, "INERTIA_TEMPLATE", "base.html")

    if template_name is not None:
        inertia_template = template_name

    if inertia_template is None:
        raise ImproperlyConfigured(
            "No Inertia template found. Either set INERTIA_TEMPLATE"
            "in settings.py or pass template parameter."
        )

    if props is None:
        props = {}
    shared = {}
    if hasattr(request, "session"):
        for k, v in request.session.get("share", {}).items():
            log.debug((k,v))
            shared[k]=v
        props.update(shared)

    for key in ("success", "error", "errors"):
        if hasattr(request, "session") and request.session.get(key):
            del request.session[key]

    # subsequent renders
    inertia_version = asset_version.get_version()
    is_version_correct = 'X-Inertia-Version' in request.headers and \
                         request.headers["X-Inertia-Version"] == str(inertia_version)
    if 'X-Inertia' in request.headers:
        response = JsonResponse({
            "component": component_name,
            "props": props,
            "version": asset_version.get_version(),
            "url": request.get_full_path()
        })
        response['X-Inertia'] = True
        response['Vary'] = 'Accept'
        return response
    context = _build_context(component_name, props,
                             asset_version.get_version(),
                             url=request.get_full_path())

    return render(request, inertia_template, context)

class InertiaMixin:
    component_name = ""
    props = None

    def get_data(self, context):

        return context


    def render_to_response(self, context, **kwargs):
        if self.props is None:
            self.props = {}
        self.props.update(self.get_data(context))
        return render_inertia(self.request, self.component_name, self.props, self.template_name)

