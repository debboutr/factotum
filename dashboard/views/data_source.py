from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.views.generic import TemplateView

from dashboard.views import *
from dashboard.models import DataSource, DataGroup
from dashboard.forms import DataSourceForm, DataGroupForm

# @login_required()
# def data_source_list(request, template_name='data_source/datasource_list.html'):
# 	datasource = DataSource.objects.all()
# 	data = {}
# 	data['object_list'] = datasource
# 	return render(request, template_name, data)

class DS_List_View(TemplateView):
	template_name = 'data_source/datasource_list.html'
	def get_context_data(self, **kwargs):
		print(self.kwargs)
		context = super(DS_List_View, self).get_context_data(**kwargs)
		context['object_list'] = DataSource.objects.all()
		return context

# @login_required()
# def data_source_detail(request, pk, template_name='data_source/datasource_detail.html'):
# 	datasource = get_object_or_404(DataSource, pk=pk, )
# 	datagroup_list = DataGroup.objects.filter(datasource=pk)
# 	request.session['datasource_title'] = datasource.title
# 	request.session['datasource_pk'] = datasource.pk
# 	#print(datasource.title,'|',datasource.pk)
# 	context = {
# 		'object': datasource,
# 		'datagroup_list': datagroup_list,
# 	}
# 	return render(request, template_name, context)

class DS_View(TemplateView):
	model = DataSource
	template_name='data_source/datasource_detail.html'
	def get_context_data(self, **kwargs):
		context = super(DS_View, self).get_context_data(**kwargs)
		pk = self.kwargs['pk']
		context['object'] = get_object_or_404(DataSource, pk=pk, )
		context['datagroup_list'] = DataGroup.objects.filter(datasource=pk)
		return context


@login_required()
def data_source_create(request, template_name='data_source/datasource_form.html'):
	form = DataSourceForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('data_source_list')
	return render(request, template_name, {'form': form})


@login_required()
def data_source_update(request, pk, template_name='data_source/datasource_form.html'):
	datasource = get_object_or_404(DataSource, pk=pk)
	form = DataSourceForm(request.POST or None, instance=datasource)
	if form.is_valid():
		datasource.updated_at = datetime.now()
		form.save()
		return redirect('data_source_list')
	return render(request, template_name, {'form': form})


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

# @login_required()
# def data_group_list(request, template_name='data_group/datagroup_form.html'):
# 	pass

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
