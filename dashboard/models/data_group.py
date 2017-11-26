from datetime import date

from django.db import models
from django.core.urlresolvers import reverse

from.data_source import DataSource

class DataGroup(models.Model):
	datasource = models.ForeignKey('DataSource', on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	download_by = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	download_date = models.DateField(default=date.today)
	scrape_script = models.CharField(max_length=150)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('data_group_detail', kwargs={'pk': self.pk})
