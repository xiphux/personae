from django.db import models

class Universe(models.Model):
	name = models.CharField(max_length=200)
	descriptor = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Attribute(models.Model):
	universe = models.ForeignKey(Universe)
	name = models.CharField(max_length=200)
	descriptor = models.CharField(max_length=200)
	type = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return self.name

class Character(models.Model):
	universe = models.ForeignKey(Universe)
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Revision(models.Model):
	character = models.ForeignKey(Character)
	rev_date = models.DateTimeField('revision date')

	def __unicode__(self):
		return self.rev_date.ctime()

class AttributeIntegerValue(models.Model):
	revision = models.ForeignKey(Revision)
	attribute = models.ForeignKey(Attribute)
	value = models.IntegerField()

	def __unicode__(self):
		return self.value

class AttributeStringValue(models.Model):
	revision = models.ForeignKey(Revision)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=200)

	def __unicode__(self):
		return self.value

class AttributeTextValue(models.Model):
	revision = models.ForeignKey(Revision)
	attribute = models.ForeignKey(Attribute)
	value = models.TextField()

	def __unicode__(self):
		return self.value
