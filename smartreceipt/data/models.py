#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django.db import models
from django.db.models import Q
from itertools import chain, groupby
from operator import attrgetter
from datetime import date
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from sets import Set
from django.forms import Textarea
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

"""
	class of a integrient type
"""
class IntegrientType(models.Model):
	name = models.CharField(max_length=50)
	
	def __unicode__(self):			  
		return u'%s' % (self.name)

"""
	class of a integrient
"""
class Integrient(models.Model):
	name = models.CharField(max_length=50)
	plural = models.CharField(max_length=50, blank=True, null=True)
	type = models.ForeignKey(IntegrientType, blank=True, null=True, related_name="integrient_type") 
	image = models.ImageField(upload_to='media/integrients', blank=True, null=True)
	important = models.NullBooleanField(default=False, blank=True, null=True)

	def thumbnail(self):
		return '<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="20" style="height: 20px;" /></a>' % ((self.image.name, self.image.name))
	thumbnail.allow_tags = True

	def receipts(self):
		return ReceiptIntegrientRelation.objects.filter(integrient = self)

	def number_of_receipts(self):
		return len(self.receipts())

	def __unicode__(self):			  
		return u'%s' % (self.name)

"""
	class of a receipt
"""
class Receipt(models.Model):
	name = models.CharField(max_length=50)
	teaser = models.CharField(max_length=250, blank=True, null=True)
	description = models.CharField(max_length=20000, blank=True, null=True)
	image = models.ImageField(upload_to='media/receipts', blank=True, null=True)
	time = models.IntegerField(default=0)
	calories = models.IntegerField(default=0)
	portions = models.IntegerField(default=0)
	
	step0 = models.CharField(max_length=1000, blank=True, null=True)
	step1 = models.CharField(max_length=1000, blank=True, null=True)
	step2 = models.CharField(max_length=1000, blank=True, null=True)
	step3 = models.CharField(max_length=1000, blank=True, null=True)
	step4 = models.CharField(max_length=1000, blank=True, null=True)
	step5 = models.CharField(max_length=1000, blank=True, null=True)
	step6 = models.CharField(max_length=1000, blank=True, null=True)
	step7 = models.CharField(max_length=1000, blank=True, null=True)
	step8 = models.CharField(max_length=1000, blank=True, null=True)
	step9 = models.CharField(max_length=1000, blank=True, null=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def url(self):
		return '/data/receipt/%d/%s.html' % (self.id, self.name.replace(' ', '_').lower())
		
	def image_url(self):
		return '/media/%s' % self.image.name
		
	def time_str(self):
		return u'%d min' % self.time
				
	def categories(self):
		return ReceiptCategoryRelation.objects.filter(receipt = self)
		
	def integrients(self):
		return ReceiptIntegrientRelation.objects.filter(receipt = self)
	
	def steps(self):
		steps = []
		
		if self.step0 is not None and self.step0 <> '':
			steps.append(self.step0)
			
		if self.step1 is not None and self.step1 <> '':
			steps.append(self.step1)
	
		if self.step2 is not None and self.step2 <> '':
			steps.append(self.step2)
			
		if self.step3 is not None and self.step3 <> '':
			steps.append(self.step3)
	
		if self.step4 is not None and self.step4 <> '':
			steps.append(self.step4)
			
		if self.step5 is not None and self.step5 <> '':
			steps.append(self.step5)
			
		if self.step6 is not None and self.step6 <> '':
			steps.append(self.step6)
			
		if self.step7 is not None and self.step7 <> '':
			steps.append(self.step7)
			
		if self.step8 is not None and self.step8 <> '':
			steps.append(self.step8)
			
		if self.step9 is not None and self.step9 <> '':
			steps.append(self.step9)
	
		return steps
		
	def countries(self):
		country_list = []
	
		for category in self.categories():
			if category.receiptCategory.is_country:
				country_list.append(category.receiptCategory)
	
		return country_list
		
	def thumbnail(self):
		return '<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="20" style="height: 20px;" /></a>' % ((self.image.name, self.image.name))
	thumbnail.allow_tags = True
	
	def __unicode__(self):			  
		return u'%s' % (self.name)
		
	class Meta:
		ordering = ['name']
	
"""
	class of a ReceiptIntegrientRelation
"""	
class ReceiptIntegrientRelation(models.Model):
	receipt = models.ForeignKey(Receipt)
	integrient = models.ForeignKey(Integrient)
	order = models.IntegerField(default=0)
	amount = models.FloatField(default=0)
	amount_type = models.CharField(max_length=1, choices=(('K', 'Kilogramm'), ('G', 'Gramm'), ('L', 'Liter'), ('M', 'Milliliter'), ('T', 'TL'), ('E', 'EL'), ('S', 'Stück'), ('B', 'Becher'), ('P', 'Prise(n)'), ('C', 'Päckchen'), ('F', 'Flasche(n)'), ('N', 'Scheibe(n)'), ('W', 'Etwas'), ('D', 'Dose'), ('X', 'Glas')))
	
	def quantity(self):
		if self.amount_type == 'K':
			return '%1.1f Kg' % self.amount
			
		if self.amount_type == 'G':
			return '%d g' % self.amount
			
		if self.amount_type == 'L':
			return '%1.1f l' % self.amount
			
		if self.amount_type == 'M':
			return '%d ml' % self.amount
			
		if self.amount_type == 'T':
			return '%d TL' % self.amount
			
		if self.amount_type == 'E':
			return '%d EL' % self.amount
			
		if self.amount_type == 'S':
			return '%d' % self.amount
			
		if self.amount_type == 'B':
			return '%d Becher' % self.amount
			
		if self.amount_type == 'P':
			return '%d Prise(n)' % self.amount
			
		if self.amount_type == 'C':
			return '%d Päckchen' % self.amount
			
		if self.amount_type == 'F':
			if int(self.amount) == self.amount:
				return '%d Flasche(n)' % self.amount
			else:
				return '%1.1f Flasche(n)' % self.amount
			
		if self.amount_type == 'N':
			return '%d Scheibe(n)' % self.amount
			
		if self.amount_type == 'W':
			return ''
			
		if self.amount_type == 'D':
			return '%d Dose(n)' % self.amount
			
		if self.amount_type == 'X':
			return '%d Glas' % self.amount
			
		return '%1.1f %s' % (self.amount, self.get_amount_type_display())
		
	def is_plural(self):
		if self.amount_type == 'S':
			if self.amount > 1:
				return True
		
		return False
	
	def __unicode__(self):			  
		return u'%s - %s' % (self.receipt.name, self.integrient.name)
	
"""
	class of a ReceiptCategory
"""	
class ReceiptCategory(models.Model):
	name = models.CharField(max_length=50)
	parentReceiptCategory = models.ForeignKey("self", blank=True, null=True)
	image = models.ImageField(upload_to='media/category', blank=True, null=True)
	is_country = models.NullBooleanField(default=False, blank=True, null=True)
	
	def thumbnail(self):
		return '<img border="0" alt="" src="/media/%s" height="20" style="height:20px" />' % (self.image.name)
	thumbnail.allow_tags = True
	
	def path(self):
		if self.parentReceiptCategory is None:
			return self.name
		else:
			return u'%s - %s' % (self.parentReceiptCategory.path(), self.name)
	
	def url(self):
		return '/data/category/%d/%s.html' % (self.id, self.name.replace(' ', '_').lower())
	
	def children(self):
		return ReceiptCategory.objects.filter(parentReceiptCategory = self)
		
	def receipts(self):
		return ReceiptCategoryRelation.objects.filter(receiptCategory = self)
		
	def number_of_receipts(self):
		num = len(self.receipts())
		
		for child in ReceiptCategory.objects.filter(parentReceiptCategory = self):
			num = num + child.number_of_receipts()
		
		return num
		
	def admin_url(self):
		return mark_safe('<a href="%s">%s</a>' % (self.id, self.name))
	admin_url.allow_tags = True
	
	def __unicode__(self):			  
		return u'%s' % (self.path())
		
"""
	class of a ReceiptIntegrientRelation
"""	
class ReceiptCategoryRelation(models.Model):
	receipt = models.ForeignKey(Receipt)
	receiptCategory = models.ForeignKey(ReceiptCategory)
	
	def __unicode__(self):			  
		return u'%s -> %s' % (self.receipt, self.receiptCategory)
		
"""
	class of a ReceiptTopic
"""	
class ReceiptTopic(models.Model):
	name = models.CharField(max_length=50)
	parentReceiptTopic = models.ForeignKey("self", blank=True, null=True)
	
	def path(self):
		if self.parentReceiptTopic is None:
			return self.name
		else:
			return u'%s - %s' % (self.parentReceiptTopic.path(), self.name)
	
	def url(self):
		return '/data/topic/%d/%s.html' % (self.id, self.name.replace(' ', '_').lower())
	
	def children(self):
		return ReceiptTopic.objects.filter(parentReceiptTopic = self)
		
	def receipts(self):
		return ReceiptTopicRelation.objects.filter(receiptTopic = self)
	
	def __unicode__(self):			  
		return u'%s' % (self.path())
		
"""
	class of a ReceiptTopicRelation
"""	
class ReceiptTopicRelation(models.Model):
	receipt = models.ForeignKey(Receipt)
	receiptTopic = models.ForeignKey(ReceiptTopic)
	
	def __unicode__(self):			  
		return u'%s -> %s' % (self.receipt, self.receiptTopic)
