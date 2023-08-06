
from django.contrib import admin
from django.shortcuts import render as django_render


def render(request, template_name, context=None):

    ctx = admin.site.each_context(request)
    ctx.update(context or {})

    return django_render(request, template_name, ctx)
