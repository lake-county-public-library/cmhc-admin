from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from threading import Thread

from .models import Status
from .forms import CsvForm
from .services import Stager, Generator, LogFinder

def index(request):
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
  template = loader.get_template('stage/workflow.html')
  status = Status.objects.get(pk=status_id)

  csv_form = CsvForm()

  context = {'status': status,
             'csv_form': csv_form}
  return HttpResponse(template.render(context, request))

def detail(request, status_id):
  return HttpResponse("You're looking at question %s." % status_id)

def stage_csv(request, status_id):
  if request.method == 'POST':
    form = CsvForm(request.POST)
    if form.is_valid():
      filename = form.cleaned_data['csv_filename']
      try:
        Stager.stage_csv(form.cleaned_data['csv_filename'])
        # TODO: Change status on successful staging
      except Exception as e:
        return render(request, 'stage/stage_csv.html', {
          'error_msg': str(e),
          'status_id': status_id
        })

      template = loader.get_template('stage/stage_csv.html')
      context = {'status_id': status_id,
                 'filename' : filename}
      return HttpResponse(template.render(context, request))

  else:
    form = CsvForm()

  return render(request, 'stage/stage_csv.html', {'form': form})

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
