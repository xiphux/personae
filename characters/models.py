from django.db import models

class Character(models.Model):
	name = models.CharField(max_length=200)

class Revision(models.Model):
	character = models.ForeignKey(Character)
	rev_date = models.DateTimeField('revision date')

class Attribute(models.Model):
	revision = models.ForeignKey(Revision)
	name = models.CharField(max_length=200)
	value = models.TextField()
