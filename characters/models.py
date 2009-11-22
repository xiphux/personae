from django.db import models

class Universe(models.Model):
	name = models.CharField(max_length=200)
	descriptor = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.name

class Attribute(models.Model):
	universe = models.ForeignKey(Universe)
	name = models.CharField(max_length=200)
	descriptor = models.CharField(max_length=200)
	multiple = models.BooleanField()
	max = models.PositiveIntegerField(default=0)
	type = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = (('universe','descriptor'),)

	def __unicode__(self):
		return self.name

class Character(models.Model):
	universe = models.ForeignKey(Universe)
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Revision(models.Model):
	character = models.ForeignKey(Character)
	revision = models.PositiveIntegerField()
	rev_date = models.DateTimeField('revision date')

	class Meta:
		unique_together = (('character','revision'),)

	def __unicode__(self):
		return self.rev_date.ctime()

class AttributeIntegerValue(models.Model):
	revisions = models.ManyToManyField(Revision)
	attribute = models.ForeignKey(Attribute)
	value = models.IntegerField()

	def __unicode__(self):
		return str(self.value)

class AttributeStringValue(models.Model):
	revisions = models.ManyToManyField(Revision)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=200)

	def __unicode__(self):
		return self.value

class AttributeTextValue(models.Model):
	revisions = models.ManyToManyField(Revision)
	attribute = models.ForeignKey(Attribute)
	value = models.TextField()

	def __unicode__(self):
		return self.value
