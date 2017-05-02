from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db import connection
from django.core.urlresolvers import reverse
import datetime
import re

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
    error_messageA = ""
    error_messageB = ""

    with connection.cursor() as cursor:
    
        if request.method == 'POST' and "dinosaur" in request.POST:
            print(request.POST.get("id"))
            print(request.POST.get("species"))
            ba = bool(re.search('[0-9]*', request.POST.get("id")))
            bb = bool(re.search('[a-zA-Z]*', request.POST.get("species")))
            bc = bool(re.search('[a-zA-Z]*', request.POST.get("dietary_order")))
            bd = bool(re.search('[0-9]|10', request.POST.get("threat_level")))
            be = bool(re.search('[0-1]', request.POST.get("contained")))
            cursor.execute("SELECT id FROM dinosaur", [])
            bf = True

            columns = [col[0] for col in cursor.description]
            bg =[
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

            for item in bg:
                print(item)
                if int(request.POST.get("id")) == int(item['id']):
                    bf = False
            print(ba, bb, bc, bd, be, bf)
            if ba and bb and bc and bd and be and bf:
                cursor.execute("INSERT INTO dinosaur(id, species, dietary_order, threat_level, contained) VALUES("+request.POST.get("id")+", \""+request.POST.get("species")+"\",\""+request.POST.get("dietary_order")+"\","+request.POST.get("threat_level")+","+request.POST.get("contained")+")", [])
            else:
                error_messageA = "Your entry was rejected. One or more of your fields was invalid."

        if request.method == 'POST' and "visitor" in request.POST:
            print(request.POST.get("id"))
            print(request.POST.get("species"))
            ba = bool(re.search('[0-9]*', request.POST.get("id")))
            bb = bool(re.search('[a-zA-Z ]*', request.POST.get("name")))
            bc = bool(re.search('[0-3]', request.POST.get("strikes")))

            cursor.execute("SELECT id FROM visitor", [])
            bf = True

            columns = [col[0] for col in cursor.description]
            bg =[
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]

            for item in bg:
                print(item)
                if int(request.POST.get("id")) == int(item['id']):
                    bf = False


            if ba and bb and bc and bf:
                cursor.execute("INSERT INTO visitor(id, name, strikes) VALUES("+request.POST.get("id")+", \""+request.POST.get("name")+"\","+request.POST.get("strikes")+")", [])
            else:
                error_messageB = "Your entry was rejected. One or more of your fields was invalid."

        cursor.execute("SELECT visitor.name, visitorLocation.number, zone.lockdown_status, visitorLocation.x_coord, y_coord FROM visitor, visitorLocation, zone WHERE visitor.id = visitorLocation.id AND zone.number = visitorLocation.number AND zone.lockdown_status != 'ZONE NOT ON LOCKDOWN: NO DANGER';")
        columns = [col[0] for col in cursor.description]        
        query1 =[
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.execute("SELECT dinosaur.species, zone.number as zone, COUNT(dinosaur.species) as count FROM dinosaur, zone, lives, exhibitLocation WHERE dinosaur.id = lives.id AND lives.name = exhibitLocation.name AND exhibitLocation.number = zone.number AND zone.lockdown_status != 'ZONE NOT ON LOCKDOWN: NO DANGER' GROUP BY dinosaur.species, zone.number;")
        columns = [col[0] for col in cursor.description]
        query2 =[
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        cursor.execute("SELECT a.name as aname, b.name as bname FROM visitor as a, visitor as b, visitorLocation as x, visitorLocation as y WHERE a.id = x.id AND b.id = y.id AND a.id != b.id AND x.number = y.number AND power((x.x_coord - y.x_coord), 2) + power((x.y_coord - y.y_coord),2) < power(30,2) AND a.id > b.id;")
        columns = [col[0] for col in cursor.description]
        query3 =[
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

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

        cursor.execute("SELECT * FROM zone", [])
        columns = [col[0] for col in cursor.description]
        zones = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]                
    # print(visitors)
    # print(dinosaurs);
    template = loader.get_template('djapp1/index.html')
    context = {'query3': query3, 'query2': query2, 'query1': query1, 'error_messageB': error_messageB, 'error_messageA': error_messageA, 'dinosaur_list': dinosaurs, 'visitor_list': visitors, 'employee_list': employees,
    'exhibit_list': exhibits, 'zone_list': zones, 'computerSystem_list': computerSystems, 'zone_list': zones

    }

    return HttpResponse(template.render(context, request))

