from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from dashboard.views import *
from dashboard.models import DataSource, DataGroup
from datetime import datetime


class DataSourceForm(ModelForm):
	class Meta:
		model = DataSource
		fields = ['title', 'url', 'estimated_records', 'type', 'description']

class DataGroupForm(ModelForm):
	class Meta:
		model = DataGroup
		fields = ['name', 'description', 'download_by', 'download_date', 'scrape_script']


@login_required()
def data_source_list(request, template_name='data_source/datasource_list.html'):
	datasource = DataSource.objects.all()
	data = {}
	data['object_list'] = datasource
	return render(request, template_name, data)


@login_required()
def data_source_detail(request, pk, template_name='data_source/datasource_detail.html'):
	datasource = get_object_or_404(DataSource, pk=pk, )
	return render(request, template_name, {'object': datasource})


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
def data_group_create(request, pk, template_name='data_group/datagroup_form.html'):
	form = DataGroupForm(request.POST or None)
	datasource = get_object_or_404(DataSource, pk=pk)
	print(datasource.id)
	if form.is_valid():
		form.save()
		return redirect('data_source_list')
	return render(request, template_name, {'form': form})
