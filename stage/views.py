from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone, dateformat
from django.urls import reverse
from threading import Thread
from pathlib import Path

from .models import Status
from .forms import CsvForm
from .services import Stager, WaxHelper, LogFinder

def index(request):
  """
  """
  if request.method == 'POST':
    status = Status.objects.create(date=timezone.now())
    status.save()
    return HttpResponseRedirect(reverse('stage:workflow', args=(status.id,)))
  else:
    template = loader.get_template('stage/index.html')
    status_list = Status.objects.order_by('-date')
    context = {'data': status_list}
    return HttpResponse(template.render(context, request))

def workflow(request, status_id):
  """
  """
  template = loader.get_template('stage/workflow.html')
  status = Status.objects.get(pk=status_id)

  csv_form = CsvForm()

  context = {'status': status,
             'csv_form': csv_form}
  return HttpResponse(template.render(context, request))

def detail(request, status_id):
  """
  """
  return HttpResponse("You're looking at question %s." % status_id)

def output_file_path(status_id, phase):
  """ 
  """ 
  BASE_DIR = Path(__file__).resolve().parent.parent
  return f"%s/logs/stage/{status_id}-{phase}.txt" %str(BASE_DIR)


def stage_csv(request, status_id):
  """
  """
  status = Status.objects.get(pk=status_id)

  if request.method == 'POST':
    form = CsvForm(request.POST)
    if form.is_valid():
      filename = form.cleaned_data['csv_filename']
      try:
        output = output_file_path(status_id, "csv")
        Stager.stage_csv(form.cleaned_data['csv_filename'], output)

      except Exception as e:
        return render(request, 'stage/stage_csv.html', {
          'error_msg': str(e),
          'status': status
        })

      # Update status
      status.csv_staged = True
      status.save()

      template = loader.get_template('stage/stage_csv.html')
      context = {'status': status,
                 'filename' : filename,
                 'csv_staged': status.csv_staged}
      return HttpResponse(template.render(context, request))

  else:
    form = CsvForm()

  return render(request, 'stage/stage_csv.html', {'form': form})

def stage_images(request, status_id):
  """
  """
  status = Status.objects.get(pk=status_id)
 
  output = output_file_path(status_id, "images")
  t = Thread(target=Stager.stage_images, args=(output,))
  t.start()
    
  # Update status
  status.images_staged = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s') 
  context = {'msg' : f"Image staging initiated: %s" %dt,
             'out' : f"stage/images-{status_id}.txt", 
             'status': status}
  template = loader.get_template('stage/stage_images.html')
  return HttpResponse(template.render(context, request))


def generate_derivatives(request, status_id):
  """
  """
  output = output_file_path(status_id, "derivatives")
  t = Thread(target=WaxHelper.generate_derivatives, args=(output,))
  t.start()
  
  status = Status.objects.get(pk=status_id)

  # Update status
  status.derivatives_generated = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s') 
  context = {'msg' : f"Derivative generation initiated: %s" %dt,
             'out' : f"stage/derivatives-{status_id}.txt", 
             'status': status}
  template = loader.get_template('stage/generate_derivatives.html')
  return HttpResponse(template.render(context, request))

def derivative_logs(request, status_id):
  """
  """
  log = output_file_path(status_id, "derivatives")
  data = LogFinder.find(log, "TIFFFetchNormalTag")
  return HttpResponse(data) 

def images_logs(request, status_id):
  """
  """
  log = output_file_path(status_id, "images")
  data = LogFinder.find(log)  
  return HttpResponse(data) 

def pages_logs(request, status_id):
  """
  """
  log = output_file_path(status_id, "pages")
  data = LogFinder.find(log)  
  return HttpResponse(data) 

def index_logs(request, status_id):
  """
  """
  log = output_file_path(status_id, "index")
  data = LogFinder.find(log)  
  return HttpResponse(data) 

def run_local_logs(request, status_id):
  """
  """
  log = output_file_path(status_id, "run")
  data = LogFinder.find(log)  
  return HttpResponse(data) 

def deploy_logs(request, status_id):
  """
  """
  log = output_file_path(status_id, "deploy")
  data = LogFinder.find(log)
  return HttpResponse(data)

def generate_pages(request, status_id):
  """
  """
  output = output_file_path(status_id, "pages")
  t = Thread(target=WaxHelper.generate_pages, args=(output,))
  t.start()
  
  status = Status.objects.get(pk=status_id)

  # Update status
  status.pages_generated = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s') 
  context = {'msg' : f"Page generation initiated: %s" %dt,
             'out' : f"stage/pages-{status_id}.txt", 
             'status': status}
  template = loader.get_template('stage/generate_pages.html')
  return HttpResponse(template.render(context, request))

def generate_index(request, status_id):
  """
  """
  output = output_file_path(status_id, "index")
  t = Thread(target=WaxHelper.generate_index, args=(output,))
  t.start()
  
  status = Status.objects.get(pk=status_id)

  # Update status
  status.indexes_rebuilt = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s') 
  context = {'msg' : f"Index generation initiated: %s" %dt,
             'out' : f"stage/index-{status_id}.txt", 
             'status': status}
  template = loader.get_template('stage/generate_index.html')
  return HttpResponse(template.render(context, request))

def run_local_site(request, status_id):
  """
  """
  output = output_file_path(status_id, "run")
  t = Thread(target=WaxHelper.run_local, args=(output,))
  t.start()

  status = Status.objects.get(pk=status_id)

  # Update status
  status.deploy_local = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
  context = {'msg' : f"Local site initiated: %s" %dt,
             'out' : f"stage/run-{status_id}.txt",
             'status': status}
  template = loader.get_template('stage/run_local.html')
  return HttpResponse(template.render(context, request))

  
def kill_local_site(request, status_id):
  """
  """
  WaxHelper.kill_local()

  status = Status.objects.get(pk=status_id)

  # Update status
  status.kill_local = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
  context = {'msg' : f"Local site stopped: %s" %dt,
             'status': status}
  template = loader.get_template('stage/kill_local.html')
  return HttpResponse(template.render(context, request))


def deploy(request, status_id):
  """
  """
  output = output_file_path(status_id, "deploy")
  t = Thread(target=WaxHelper.deploy, args=(output,))
  t.start()

  status = Status.objects.get(pk=status_id)

  # Update status
  status.deploy_aws = True
  status.save()

  dt = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
  context = {'msg' : f"Deploying to AWS: %s" %dt,
             'out' : f"stage/deploy-{status_id}.txt",
             'status': status}
  template = loader.get_template('stage/deploy.html')
  return HttpResponse(template.render(context, request))
