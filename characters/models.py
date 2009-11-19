from django.db import models

class Universe(models.Model):
	name = models.CharField(max_length=200)

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

class Attribute(models.Model):
	revision = models.ForeignKey(Revision)
	name = models.CharField(max_length=200)
	value = models.TextField()

	def __unicode__(self):
		return self.name
