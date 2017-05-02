# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.

def homepage(request):
    '''
    Context format:
    {
        'homepage_text_title' : 'Title for the page',
        'homepage_image_url' : 'URL For the homepage image',
        'homepage_text_content' : 'Text on the right',
    }
    '''
    template = loader.get_template('djapp1/homepage.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
