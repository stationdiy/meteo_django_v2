from django.template.loader import get_template
from django.template import Context, Template,loader,RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from models import Usuario
from models import Station
from django.contrib.auth.models import User, check_password
from forms import StationForm, UserForm

from django.template import Context, Template,loader
from django.db import connection, models
import pywapi,pprint,pygeoip
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from pygeocoder import Geocoder
from django.core.mail import send_mail
import os, sys





# -*- encoding: utf-8 -*-
def get_ip(request):
     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
     if x_forwarded_for:
         ip = x_forwarded_for.split(',')[0]
     else:
         ip = request.META.get('REMOTE_ADDR')
     return ip
 
     
     
def get_info_ip():

     ip='80.59.169.236' #simulo otra ip
     #inicio geoip con el diccionario para ciudades
     geoip=pygeoip.GeoIP('/home/baurin/Escritorio/programacion/python/GeoIPDB/GeoLiteCity.dat',pygeoip.MEMORY_CACHE) 
     #extraigo informacion para la ip
     info_ip=geoip.record_by_addr(ip)
     return info_ip
     
def location_id_weather(request,busqueda):

     #Sin permisos
     ip='80.59.169.236' #simulo otra ip
     #ip = get_ip(request)
     info_ip=get_info_ip()
     #obtengo la zona horaria y separo en dos con la barra para quedarme con la ciudad
     time_zone=info_ip['time_zone'].split("/")
     #junto ciudad con country_name para buscar el id en la bbdd de weather.com
     city_time=','.join([list(time_zone[1])[0],info_ip['country_name']])
     city_time1=','.join([time_zone[1],info_ip['country_name']])
     #busco id de la ciudad+pais en weather.com
     #pywapi.get_loc_id_from_weather_com('M,Spain')
     loc_id_weather_com1=pywapi.get_loc_id_from_weather_com(city_time)
     loc_id_weather_com2=pywapi.get_loc_id_from_weather_com(city_time1)
     loc_id_weather_com = dict(loc_id_weather_com1.items() + loc_id_weather_com2.items()) 
     n_stat_yahoo=len(loc_id_weather_com)
     for i in range(0,len(loc_id_weather_com1)-1):
           loc_id_weather_com[i]=loc_id_weather_com1[i]  
           loc_id_weather_com[i+10]=loc_id_weather_com2[i] 
             
     return loc_id_weather_com

def meteo_index(request):
     busqueda=''
     loc_id_weather_com=location_id_weather(request,busqueda)
     #Uno los dict de loc_id
     #declaro una lista para meter los resultados de cada estacion
     city_weather=[None]*2*len(loc_id_weather_com)
    
     
     for i in range(0,len(loc_id_weather_com)-1):
         city_weather[i]=pywapi.get_weather_from_weather_com(loc_id_weather_com[i][0],'metric')
                   
     city_yahoo=pywapi.get_weather_from_yahoo(loc_id_weather_com[0][0],'metric')
     #desgloso el contenido de la escripcion html
     enlace_icono_weather=city_yahoo['html_description'].split('"')[1]
     text_yahoo=city_yahoo['html_description'].replace('<br />','').replace('<BR />','').replace('<b>','').replace('<BR/>','').replace('</b>','').split('\n')#.split('<br />')
     stations = Station.objects.all()
     variables_html_vis={'enlace_icono_weather':enlace_icono_weather}
     #paso la geo del centro del mapa que obtengo a partir de la ip del cliente
     variables_html_vis['lat']=city_yahoo['geo']['lat']
     variables_html_vis['long']=city_yahoo['geo']['long']
     variables_html_vis['city_weather']=city_weather
     variables_html_vis['city_yahoo']=city_yahoo
     variables_html_vis['html_des']=text_yahoo
     
     #
     if request.user.is_authenticated():
         usuario_stats=User.objects.get(username=request.user.username)
         num_stats_mias=Station.objects.filter(username=usuario_stats)
         if num_stats_mias==0:
             variables_html_vis['no_tienes_stats']='Aun no tienes ninguna estacion'
         
         act_stat=[[0 for x in xrange(4)] for x in xrange(len(num_stats_mias))]
         stat=[0 for x in xrange(len(num_stats_mias))]
         for i in range(0, len(num_stats_mias)):
             stat[i]=Station.objects.get(MAC=num_stats_mias[i].MAC)
             
         #act_stat[0][i]=Objects Stations
         #act_stat[1][i]=Actioner 1 de la estacion i. Y asi...
         for i in range(0, len(stat)):
             act_stat[i][0]=stat[i]
             if stat[i].actioner1==0:
                 act_stat[i][1]='/media/OFF.jpg'
             else:
                 act_stat[i][1]='/media/ON.jpg'
             if stat[i].actioner2==0:
                 act_stat[i][2]='/media/OFF1.jpg'
             else:
                 act_stat[i][2]='/media/ON1.jpg'
             if stat[i].actioner3==0:
                 act_stat[i][3]='/media/OFF2.jpg'
             else:
                 act_stat[i][3]='/media/ON2.jpg'
             #act_stat[i][4]=stat[i].MAC
             
         variables_html_vis['stations_mines_act']=act_stat
         #variables_html_vis['actuadores']=act_stat[1:]
         #variables_html_vis['form_actioners']=act_form_stat[1]
         #actioners_char = request.POST["actioner_char"]
         variables_html_vis['usuario']=request.user.username
         stations=stations.exclude(username=usuario_stats)
         variables_html_vis['stations']= stations
     else:
         stations=Station.objects.all()
         variables_html_vis['stations']= stations   
    
             
     if request.method=='GET':
     
         if 'option' in request.GET and request.GET['option']:
         
             if request.GET['option']=='0':
                 variables_html_vis['stations']=stations
                 variables_html_vis['stations_mines_act']=act_stat
             elif request.GET['option']=='1':
                 variables_html_vis['city_yahoo']=city_yahoo
                 variables_html_vis['html_des']=text_yahoo
             
             elif request.GET['option']=='2':
                 variables_html_vis['city_weather']=city_weather
             else :
                 variables_html_vis['city_weather']=city_weather
                 variables_html_vis['city_yahoo']=city_yahoo
                 variables_html_vis['html_des']=text_yahoo
                 variables_html_vis['stations']=stations
                 variables_html_vis['stations_mines_act']=act_stat
         
        
         
     
         #address = stations.objects.all
         if 'q' in request.GET and request.GET['q']:
             q = request.GET['q']
             #Estacion DiY
             stations = Station.objects.filter(address__icontains=q)
             variables_html_vis['query']=q
             stations=Station.objects.filter(address__icontains=q)
             variables_html_vis['stations']=stations
             n_stat=len(Station.objects.filter(address__icontains=q))
             variables_html_vis['n_stat']=n_stat
             #Estaciones normales Yahoo y Weather
             loc_id_query=pywapi.get_location_ids(q)
             query_weather=[None]*len(loc_id_query)
             n_stat_yahoo=len(loc_id_query)
             
             for i in range(0,len(loc_id_query)-1):
                 query_weather[i]=pywapi.get_weather_from_weather_com(loc_id_query.keys()[i],'metric')
             query_yahoo=pywapi.get_weather_from_yahoo(loc_id_query.keys()[0],'metric')
             #desgloso el contenido de la escripcion html
             try:
                 enlace_icono_weather=query_yahoo['html_description'].split('"')[1]
                 text_yahoo=query_yahoo['html_description'].replace('<br />','').replace('<BR />','').replace('<b>','').replace('<BR/>','').replace('</b>','').split('\n')#.split('<br />')
                 variables_html_vis={'enlace_icono_weather':enlace_icono_weather}
                 #paso la geo del centro del mapa que obtengo a partir de la ip del cliente
                 variables_html_vis['lat']=query_yahoo['geo']['lat']
                 variables_html_vis['long']=query_yahoo['geo']['long']
                 variables_html_vis['city_weather']=query_weather
                 variables_html_vis['city_yahoo']=query_yahoo
                 variables_html_vis['html_des']=text_yahoo
                 
             except:
                 variables_html_vis['lat']=get_info_ip()['latitude']
                 variables_html_vis['long']=get_info_ip()['longitude']
                 
             variables_html_vis['stations']=stations
                 
         if 'inses' in request.GET and request.GET['inses']:
             inses = request.GET['inses']  
             variables_html_vis['loging']=inses
             user_log_form = UserForm()
             variables_html_vis['user_log_form']=user_log_form
          
         if 'out' in request.GET and request.GET['out']:
             logout(request)
             return redirect('/meteostation/')
         
         if 'newuser' in request.GET and request.GET['newuser']:
             newusuario = request.GET['newuser']  
             variables_html_vis['newusuario']=newusuario
             # formulario inicial
             user_form = UserForm()
             variables_html_vis['user_form']=user_form
         if 'tutorial' in request.GET and request.GET['tutorial']:
             tut=request.GET['tutorial']
             variables_html_vis['tut']=tut 
         if 'newstat' in request.GET and request.GET['newstat']: 
             if request.user.is_authenticated():  
                 newstat = request.GET['newstat']  
                 variables_html_vis['newestacion']=newstat
                 # formulario inicial
                 station_log_form = StationForm()                 
                 variables_html_vis['station_log_form']=station_log_form
                 
             else:
                 variables_html_vis['loging']=1
                 station_log_form = StationForm()
                 variables_html_vis['station_log_form']=station_log_form                 
         if 'mystats' in request.GET and request.GET['mystats']: 
             if request.user.is_authenticated(): 
                 mystats=request.GET['mystats']
                 variables_html_vis['myestaciones']=mystats
                 variables_html_vis['stations_mines_act']=act_stat
                 variables_html_vis['stations']=stat
                 try:
                     variables_html_vis['lat']=act_stat[0][0].position.latitude
                     variables_html_vis['long']=act_stat[0][0].position.longitude 
                 except:
                     variables_html_vis['no_tienes_stats']='Aun no tienes ninguna estacion'          
             else:
                 variables_html_vis['loging']=1
                                  
                 
         if 'id' in request.GET and request.GET['id']: 
              if 'act' in request.GET and request.GET['act']:
                  num_act=request.GET['act']
                  actioner1=Station.objects.get(MAC=request.GET['id']).actioner1
                  actioner2=Station.objects.get(MAC=request.GET['id']).actioner2
                  actioner3=Station.objects.get(MAC=request.GET['id']).actioner3
                  if num_act=='actioner1':
                      Station.objects.filter(MAC=request.GET['id']).update(actioner1=not actioner1, actioner2=actioner2, actioner3=actioner3)
                  if num_act=='actioner2':
                      Station.objects.filter(MAC=request.GET['id']).update(actioner1=actioner1, actioner2=not actioner2, actioner3=actioner3)
                  if num_act=='actioner3':
                      Station.objects.filter(MAC=request.GET['id']).update(actioner1=actioner1, actioner2=actioner2, actioner3=not actioner3)
                  else: 
                      variables_html_vis['loging']=1
                  stat=[0 for x in xrange(len(num_stats_mias))]
                  for i in range(0, len(num_stats_mias)):
                      stat[i]=Station.objects.get(MAC=num_stats_mias[i].MAC)   
                  for i in range(0, len(stat)):
                      act_stat[i][0]=stat[i]
                      if stat[i].actioner1==0:
                          act_stat[i][1]='/media/OFF.jpg'
                      else:
                          act_stat[i][1]='/media/ON.jpg'
                      if stat[i].actioner2==0:
                          act_stat[i][2]='/media/OFF1.jpg'
                      else:
                          act_stat[i][2]='/media/ON1.jpg'
                      if stat[i].actioner3==0:
                          act_stat[i][3]='/media/OFF2.jpg'
                      else:
                          act_stat[i][3]='/media/ON2.jpg'
                  variables_html_vis['stations_mines_act']=act_stat
                                                              
     if request.method=='POST':  
         #if 'upd_act' in request.POST and request.POST['upd_act']:
         if 'crear' in request.POST and request.POST['crear']:
             user_form = UserForm(request.POST)
             
             # formulario enviado
             #user_form = UserForm(request.POST)
             #perfil_form = PerfilForm(request.POST, instance=request.user.perfil)

             if user_form.is_valid() :
                 if request.POST['rep_pass']==user_form.cleaned_data["password"]:
                     username = user_form.cleaned_data["username"]
                     password = user_form.cleaned_data["password"]
                     email = user_form.cleaned_data["email"]
                     if  User.objects.filter(email=email):
                         variables_html_vis['user_form']=user_form
                         variables_html_vis['mens_rep_pass_mal']='El email ya esta siendo utilizado'
                         variables_html_vis['newusuario']=1  
                     else:    
                         # At this point, user is a User object that has already been saved
                         # to the database. You can continue to change its attributes
                         # if you want to change other fields.
                         user = User.objects.create_user(username, email, password)
                         email_tupla=[email]
                         send_mail('Bienvenido a DiY Station ;)', 'Te damos la bienvenida a este portal dirigido a los apasionados de los proyectos DiY. Estate atento al tutorial de nuestra página para aprender a construir tu estación y ver las novedades.\nUn saludo.', settings.EMAIL_HOST_USER,email_tupla, fail_silently=False)

                         # Save new user attributes
                         user.save()
                         variables_html_vis['usuario']=username
                         #request.session['usuario']=username
                         user = authenticate(username=email, password=password)
                         login(request, user)
                         #return HttpResponseRedirect('/meteostation/') 
                     
                 else:
                                         
                     #user_form = UserForm()
                     variables_html_vis['user_form']=user_form
                     variables_html_vis['mens_rep_pass_mal']='La contrasena no coincide'
                     variables_html_vis['newusuario']=1  
                     #return HttpResponseRedirect('/meteostation/?newuser=1')
             else:
                 
                 variables_html_vis['newusuario']=1
                 variables_html_vis['error_mail_or_user']='El nombre de usuario ya esta siendo utilzado.'
                 #user_form = UserForm()
                 variables_html_vis['user_form']=user_form
                 #return HttpResponseRedirect('/meteostation/?newuser=1')        
         #request.user.is_authenticated() 
         if 'asociar' in request.POST and request.POST['asociar']:
             station_log_form = StationForm(request.POST)
             mac = request.POST["MAC"]
             address = request.POST["address"]
             city = request.POST["city"]
             country = request.POST["country"]
             user_stat=User.objects.get(username=request.user.username) 
             try:
                 stat=Station.objects.filter(username=user_stat).filter(MAC= mac) 
             except:
                 stat='None'
                 variables_html_vis['newestacion']=1
                 variables_html_vis['mensaje_error']='Tu usuario o la MAC no coinciden con la del dispositivo conectado.Comprueba que este bien conectado y que los datos coincidan.'              
             if stat!='None' :
                 geoadd=",".join([address,city,country])
                 results = Geocoder.geocode(geoadd)
                 #el resultado es una tupla, por lo que la separo y le doy formato 
                 #al string
                 lat=results[0].coordinates[0]
                 longitud=results[0].coordinates[1]
                 lat_long=','.join([str(lat),str(longitud)])
                 #latitud=results[0].coordinates[0]
                 #longitud=results[0].coordinates[1]                 
                 Station.objects.filter(MAC=mac).update(address=address,city=city,country=country,position=lat_long)
                 variables_html_vis['mensaje']='La estacion se asocio a su cuenta correctamente. Actualice la pagina en unos segundos y ya podra verla.'
                 geoadd=",".join([address,city,country])
                 results = Geocoder.geocode(geoadd)
                 latitud=results[0].coordinates[0]
                 longitud=results[0].coordinates[1]
             else:
                 station_log_form = StationForm()                 
                 variables_html_vis['station_log_form']=station_log_form
                 variables_html_vis['newestacion']=1
                 variables_html_vis['mensaje_error']='No has rellenado bien todos los campos o el usuario no coincide con el del dispositivo'       
         
                     
                        
         if 'log' in request.POST and request.POST['log']:
             user_log_form = UserForm(request.POST)
             email = request.POST['email']
             password = request.POST['password']
             #usuario=User.objects.get(email=email)
             username=User.objects.get(email=email)
             user = authenticate(username=email, password=password)
             
             if user is not None:
                 if user.is_active:
                     login(request, user)
                     variables_html_vis['usuario']=username
                     # Redirect to a success page.
                 else:
                     variables_html_vis['error_loging']='Tu cuenta esta desabilitada.'
                     variables_html_vis['loging']=1
                     user_log_form = UserForm()
                     variables_html_vis['user_log_form']=user_log_form
                                
             else:
                 variables_html_vis['error_loging']='Email o contrasena equivocada.'
                 variables_html_vis['loging']=1
                 user_log_form = UserForm()
                 variables_html_vis['user_log_form']=user_log_form
      
     
     return render_to_response('meteoapp/meteo-index.html',variables_html_vis,context_instance=RequestContext(request))         
     
     
     


     
         

     
     
