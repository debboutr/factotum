import unittest
import csv
import collections
from selenium import webdriver
from selenium.webdriver.support.select import Select
from django.utils import timezone
from django.test import LiveServerTestCase

from dashboard.models import DataGroup, DataSource, DataDocument
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse



# val = len(DataGroup.objects.filter(data_source_id=1))
URL = 'http://127.0.0.1:8000'

def log_karyn_in(object):
	'''
	Log user in for further testing.
	'''
	object.browser.get(URL + '/login/')
	body = object.browser.find_element_by_tag_name('body')
	object.assertIn('Please sign in', body.text)
	username_input = object.browser.find_element_by_name("username")
	username_input.send_keys('Karyn')
	password_input = object.browser.find_element_by_name("password")
	password_input.send_keys('specialP@55word')
	object.browser.find_element_by_class_name('btn').click()


class TestAuthInBrowser(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_login(self):
		self.browser.get(URL + '/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Welcome to Factotum', body.text)

class TestDataSource(LiveServerTestCase):

	fixtures = ['seed_data']

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_data_source_name(self):
		self.browser.get(URL + '/datasource/1')
		h1 = self.browser.find_element_by_name('title')
		self.assertIn('Walmart MSDS', h1.text)

	#When a new data source is entered, the data source is automatically assigned the state 'awaiting triage.'
	def test_state_and_priority(self):
		valid_states = ['Awaiting Triage','In Progress','Complete','Stale']
		valid_priorities = ['High','Medium','Low']
		self.browser.get(URL + '/datasource/1')
		state = self.browser.find_element_by_name('state')
		self.assertIn(state.text, valid_states)
		self.assertIn('Awaiting Triage', state.text)
		select = Select(self.browser.find_element_by_name('priority'))
		self.assertEqual([o.text for o in select.options], valid_priorities)
		selected_option = select.first_selected_option
		self.assertIn(selected_option.text, valid_priorities)
		# is there a better way to loop through datasources???
		# do we need to do all ????
		self.browser.get(URL + '/datasource/2')
		state = self.browser.find_element_by_name('state')
		self.assertIn(state.text, valid_states)
		self.assertIn('Awaiting Triage', state.text)

	def test_datagroup_list_length(self):
		b = len(DataGroup.objects.filter(data_source_id=1))
		self.browser.get(URL + '/datasource/1')
		row_count = len(self.browser.find_elements_by_xpath(
								"//table[@id='data_group_table']/tbody/tr"))
		self.assertEqual(b, row_count)


class TestDataGroup(LiveServerTestCase):

	fixtures = ['seed_data']

	def setUp(self):
		self.browser = webdriver.Chrome()
		log_karyn_in(self)

	def tearDown(self):
		self.browser.quit()

	def test_data_group_name(self):
		self.browser.get(URL + '/datagroup/1')
		h1 = self.browser.find_element_by_name('title')
		self.assertIn('Walmart MSDS', h1.text)
		pdflink = self.browser.find_elements_by_xpath('/html/body/div/table/tbody/tr[1]/td[1]/a')[0]
		self.assertIn('shampoo.pdf',pdflink.get_attribute('href'))
	
	def create_data_group(self, data_source, testusername = 'Karyn', name='Walmart MSDS 3', description='Another data group, added programatically'):
		source_csv = open('./sample_files/walmart_msds_3.csv','rb')
		return DataGroup.objects.create(name=name, 
										description=description, data_source = data_source,
										downloaded_by=User.objects.get(username=testusername) ,
										downloaded_at=timezone.now(),
										csv=SimpleUploadedFile('walmart_msds_3.csv', source_csv.read() )
										)
	
	def upload_pdfs(self):
		store = settings.MEDIA_URL + self.dg.dgurl()
		pdf1_name = '0ffeb4ae-2e36-4400-8cfc-a63611011d44.pdf'
		pdf2_name = '1af3fa0f-edf3-4a41-bcec-7436d0689bd8.pdf'
		local_pdf = open('./sample_files/' + pdf1_name, 'rb')
		fs = FileSystemStorage(store + '/pdf')
		fs.save(pdf1_name, local_pdf)
		local_pdf = open('./sample_files/' + pdf2_name, 'rb')
		fs = FileSystemStorage(store + '/pdf')
		fs.save(pdf2_name, local_pdf)
		return [pdf1_name, pdf2_name]

	def create_data_documents(self, data_group):
		dds = []
		#pdfs = [f for f in os.listdir('/media/' + self.dg.dgurl() + '/pdf') if f.endswith('.pdf')]
		#pdfs
		with open(data_group.csv.path) as dg_csv:
			table = csv.DictReader(dg_csv)
			errors = []
			count = 0
			for line in table: # read every csv line, create docs for each
					count+=1
					if line['filename'] == '':
						errors.append(count)
					if line['title'] == '': # updates title in line object
						line['title'] = line['filename'].split('.')[0]
					dd = DataDocument.objects.create(filename=line['filename'],
						title=line['title'],
						product_category=line['product'],
						url=line['url'],
						matched = line['filename'] in self.pdfs,
						data_group=data_group)
					dds.append(dd)
			return dds

	# creation of another DataGroup from csv and pdf sources
	def test_new_data_group(self):
		# DataGroup
		dg_count_before = DataGroup.objects.count()
		ds = DataSource.objects.get(pk=1)
		self.dg = self.create_data_group(data_source=ds)
		dg_count_after = DataGroup.objects.count()
		self.assertEqual(dg_count_after, dg_count_before + 1) # See if the DataGroup object has been created
		self.pdfs = self.upload_pdfs()
		self.dds = self.create_data_documents(self.dg)

		self.assertEqual(3, self.dg.pk) # Confirm the new object's pk is 3
		# TODO: why can't I open a page for the newly added object?
		self.browser.get(URL + '/datagroup/3')
		# could also use 
		# self.browser.get(URL + reverse('data_group_detail', kwargs={'pk': self.dg.pk}))
		self.assertEqual('factotum', self.browser.title)
		h1 = self.browser.find_element_by_name('title')
		self.assertEqual('Walmart MSDS 3', h1.text)
		
		# deleting the DataGroup will clean up the file system
		self.dg.delete()