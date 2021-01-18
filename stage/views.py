from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from threading import Thread

from .models import Status
from .services import Stager, Generator, LogFinder

def index(request):
  template = loader.get_template('stage/index.html')
  status_list = Status.objects.order_by('-date')
  context = {'data': status_list}
  return HttpResponse(template.render(context, request))

def workflow(request):
  template = loader.get_template('stage/workflow.html')
  status = Status.objects.create(date=timezone.now())
  status.save()
  context = {'data': [status]}
  return HttpResponse(template.render(context, request))

def detail(request, status_id):
  return HttpResponse("You're looking at question %s." % status_id)

def stage_csv(request, status_id):
  template = loader.get_template('stage/stage_csv.html')
  result = Stager.stage_csv()
  return HttpResponse("You're staging csv %i - %s" % (status_id, result))

def stage_images(request, status_id):
    return HttpResponse("You're staging images: %s." % status_id)

def generate_derivatives(request, status_id):
  template = loader.get_template('stage/generate_derivatives.html')
  output = f"logs/stage/derivatives-{status_id}.txt"
  t = Thread(target=Generator.generate_derivatives, args=(output,))
  t.start()
  
  status = Status.objects.get(pk=status_id)
  context = {'msg' : f"You're generating derivatives: {status_id}",
             'out' : f"stage/derivatives-{status_id}.txt", 
             'data': [status]}
  return HttpResponse(template.render(context, request))

def derivative_logs(request, status_id):
  data = LogFinder.find(f"logs/stage/derivatives-{status_id}.txt")  
  return HttpResponse(data) 

def rebuild_local_site(request, status_id):
    return HttpResponse("You're rebuilding local site: %s." % status_id)

def run_local_site(request, status_id):
    return HttpResponse("You're running local site: %s." % status_id)

def deploy(request, status_id):
    return HttpResponse("You're deploying site to AWS: %s." % status_id)
