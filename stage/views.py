from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

from .models import Status
from .services import Stager, Generator

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
  result = Generator.generate_derivatives()
  return HttpResponse("You're generating derivatives: %s - %s" % (status_id, result))

def rebuild_local_site(request, status_id):
    return HttpResponse("You're rebuilding local site: %s." % status_id)

def run_local_site(request, status_id):
    return HttpResponse("You're running local site: %s." % status_id)

def deploy(request, status_id):
    return HttpResponse("You're deploying site to AWS: %s." % status_id)
