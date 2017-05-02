from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import connection


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
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dinosaur", [])
        columns = [col[0] for col in cursor.description]
        dinosaurs =[
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.execute("SELECT * FROM visitor", [])
        columns = [col[0] for col in cursor.description]
        visitors = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.execute("SELECT * FROM employee", [])
        columns = [col[0] for col in cursor.description]
        employees = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.execute("SELECT * FROM exhibit", [])
        columns = [col[0] for col in cursor.description]
        exhibits = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]        

        cursor.execute("SELECT * FROM zone", [])
        columns = [col[0] for col in cursor.description]
        zones = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.execute("SELECT * FROM computerSystem", [])
        columns = [col[0] for col in cursor.description]
        computerSystems = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]        
    print(visitors)
    print(dinosaurs);
    template = loader.get_template('djapp1/index.html')
    context = {'dinosaur_list': dinosaurs, 'visitor_list': visitors, 'employee_list': employees,
    'exhibit_list': exhibits, 'zone_list': zones, 'computerSystem_list': computerSystems

    }

    return HttpResponse(template.render(context, request))
