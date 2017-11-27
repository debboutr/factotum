from django.forms import ModelForm
from dashboard.models import DataSource, DataGroup

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
