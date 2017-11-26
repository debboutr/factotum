from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from dashboard.views import *
from dashboard.models import DataSource, DataGroup
from datetime import datetime
from django.http import HttpResponseRedirect

class DataSourceForm(ModelForm):
	class Meta:
		model = DataSource
		fields = ['title', 'url', 'estimated_records', 'type', 'description']

class DataGroupForm(ModelForm):
	class Meta:
		model = DataGroup
		fields = ['name', 'description', 'datasource', 'download_by', 'download_date', 'scrape_script']
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(DataGroupForm, self).__init__(*args, **kwargs)


@login_required()
def data_source_list(request, template_name='data_source/datasource_list.html'):
	datasource = DataSource.objects.all()
	data = {}
	data['object_list'] = datasource
	return render(request, template_name, data)


@login_required()
def data_source_detail(request, pk, template_name='data_source/datasource_detail.html'):
	datasource = get_object_or_404(DataSource, pk=pk, )
	datagroup_list = DataGroup.objects.filter(datasource=pk)
	request.session['datasource_title'] = datasource.title
	request.session['datasource_pk'] = datasource.pk
	#print(datasource.title,'|',datasource.pk)
	context = {
		'object': datasource,
		'datagroup_list': datagroup_list,
	}
	return render(request, template_name, context)


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
	new_group_key = DataGroup.objects.filter(datasource=datasource_pk).count() + 1
	default_name = '{} {}'.format(datasource_title, new_group_key)
	print(request.user)
	initial_values = {'download_by': request.user, 'name': default_name, 'datasource':datasource_pk}
	form = DataGroupForm(request.POST or None, initial=initial_values)
	print(request.session.keys())
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('data_group_detail', kwargs={'pk': new_group_key}))
	return render(request, template_name, {'form': form})

# @login_required()
# def data_group_list(request, template_name='data_group/datagroup_form.html'):
# 	pass

@login_required()
def data_group_dets(request, pk, template_name='data_group/datagroup_detail.html'):

	data_group = get_object_or_404(DataGroup, pk=pk)
	print(request.path)
	return render(request, template_name, {'datagroup': data_group})

@login_required()
def data_group_update(request, pk, template_name='data_group/datagroup_form.html'):
	data_group = get_object_or_404(DataGroup, pk=pk)
	form = DataGroupForm(request.POST or None, instance=data_group)
	print(form)
	if form.is_valid():
		data_group.updated_at = datetime.now()
		form.save()
		return HttpResponseRedirect(reverse('data_group_detail', kwargs={'pk': pk}))
	context = {'form': form,
			   'object': data_group}
	return render(request, template_name, context)

@login_required()
def data_group_delete(request, pk, template_name='data_source/datasource_confirm_delete.html'):
	data_group = get_object_or_404(DataGroup, pk=pk)
	if request.method == 'POST':
		data_group.delete()
		return redirect('data_source_list')
	return render(request, template_name, {'object': data_group})
