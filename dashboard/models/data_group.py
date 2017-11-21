from django.db import models
from django.core.urlresolvers import reverse

from.data_source import DataSource

class DataGroup(models.Model):
	datasource = models.ForeignKey(DataSource)
	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	download_by = models.CharField(max_length=150)
	download_date = models.DateTimeField(null=True)
	scrape_script = models.CharField(max_length=150)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('data_group_edit', kwargs={'pk': self.pk})
