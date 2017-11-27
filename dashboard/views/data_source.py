from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.views.generic import *

from dashboard.views import *
from dashboard.models import DataSource, DataGroup
from dashboard.forms import DataSourceForm, DataGroupForm


class DS_List_View(ListView):
	template_name = 'data_source/datasource_list.html'
	model = DataSource

class DS_View(DetailView):
	template_name='data_source/datasource_detail.html'
	model = DataSource

class DS_Create_View(FormView):
	template_name = 'data_source/datasource_form.html'
	form_class = DataSourceForm
	success_url = reverse_lazy('data_source_list')
	def form_valid(self, form):
		form.save()
		return super(DS_Create, self).form_valid(form)

class DS_Update_View(UpdateView):
	model = DataSource
	template_name = 'data_source/datasource_form.html'
	form_class = DataSourceForm
	success_url = reverse_lazy('data_source_list')
	def form_valid(self, form):
		form.save()
		return super(DS_Update_View, self).form_valid(form)

@login_required()
def data_source_delete(request, pk, template_name='data_source/datasource_confirm_delete.html'):
	datasource = get_object_or_404(DataSource, pk=pk)
	if request.method == 'POST':
		datasource.delete()
		return redirect('data_source_list')
	return render(request, template_name, {'object': datasource})




@login_required()
def data_group_create(request, template_name='data_group/datagroup_form.html'):
	datasource_title = request.session['datasource_title']
	datasource_pk = request.session['datasource_pk']
	new_group_key = DataGroup.objects.all().aggregate(Max('id'))['id__max'] + 1
	default_name = '{} {}'.format(datasource_title, new_group_key)
	#print(request.user)
	initial_values = {'download_by': request.user, 'name': default_name, 'datasource':datasource_pk}
	form = DataGroupForm(request.POST or None, initial=initial_values)
	#print(request.session.keys())
	if form.is_valid():
		form.save()
		#return redirect('data_group_detail', args=[new_group_key])
		return HttpResponseRedirect(reverse('data_group_detail', kwargs={'pk': new_group_key}))
	exists = DataGroup.objects.filter(id=new_group_key).exists()
	if not exists:
		new_group_key = datasource_pk
	obj={'exists': str(exists),
		'id': new_group_key}
	print(DataGroup.objects.all().aggregate(Max('id'))['id__max'])

	return render(request, template_name, {'form': form, 'object': obj})

@login_required()
def data_group_detail(request, pk, template_name='data_group/datagroup_detail.html'):

	data_group = get_object_or_404(DataGroup, pk=pk)
	#print(request.path)
	return render(request, template_name, {'datagroup': data_group})

@login_required()
def data_group_update(request, pk, template_name='data_group/datagroup_form.html'):
	data_group = get_object_or_404(DataGroup, pk=pk)
	print(data_group.datasource)
	form = DataGroupForm(request.POST or None, instance=data_group)
	print(form)
	if form.is_valid():
		data_group.updated_at = datetime.now()
		form.save()
		return HttpResponseRedirect(reverse('data_group_detail', kwargs={'pk': pk}))
	context = {'form': form,
			   'object': {'exists': 'True',
			   			  'id': data_group.id}}
	return render(request, template_name, context)

@login_required()
def data_group_delete(request, pk, template_name='data_source/datasource_confirm_delete.html'):
	data_group = get_object_or_404(DataGroup, pk=pk)
	pk = data_group.datasource.id
	if request.method == 'POST':
		data_group.delete()
		return HttpResponseRedirect(reverse('data_source_detail', kwargs={'pk': pk}))
	return render(request, template_name, {'object': data_group})
