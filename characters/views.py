import datetime
from personae.characters.models import Universe, Character, Revision, Attribute, AttributeChoice, AttributeIntegerValue, AttributeStringValue, AttributeTextValue, AttributeChoiceValue
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

#
# Front index page
#
def index(request):
	characters = Character.objects.all().order_by('name')
	return render_to_response('characters/index.html', {'characters': characters})

#
# Create new character form
#
def newcharacter(request):
	universe_list = Universe.objects.all().order_by('name')
	return render_to_response('characters/newcharacter.html', {'universe_list': universe_list}, context_instance=RequestContext(request))

#
# Create new character form POST action
#
def createcharacter(request):
	try:
		char_name = request.POST['name']
		if len(char_name) == 0:
			raise ValueError
	except (KeyError, ValueError):
		universe_list = Universe.objects.all().order_by('name')
		return render_to_response('characters/newcharacter.html', {
			'universe_list': universe_list,
			'error_message': "You didn't enter a character name.",
		}, context_instance=RequestContext(request))

	try:
		universe = Universe.objects.get(pk=request.POST['universe'])
	except (KeyError, Universe.DoesNotExist):
		universe_list = Universe.objects.all().order_by('name')
		return render_to_response('characters/newcharacter.html', {
			'universe_list': universe_list,
			'error_message': "You didn't choose a universe.",
		}, context_instance=RequestContext(request))

	char = universe.character_set.create(name=char_name)
	return HttpResponseRedirect(reverse('personae.characters.views.detail', args=(char.id,)))
		
#
# Character detail page
#
def detail(request, character_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	try:
		revision = Revision.objects.filter(character=character_id).order_by('-rev_date')[0]
	except (Revision.DoesNotExist, IndexError):
		return render_to_response('characters/norevisions.html', {'character': character})

	return HttpResponseRedirect(reverse('personae.characters.views.viewrevision', args=(character_id, revision.id)))
	
#
# Edit character action
#
def edit(request, character_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	if len(character.universe.descriptor) == 0:
		return HttpResponse("Invalid universe descriptor.")
	
	template = "characters/universes/" + character.universe.descriptor + ".html"

	try:
		universe_attributes = character.universe.attribute_set.all()
	except:
		return HttpResponse("Error: universe has no attributes defined.")

	universe_attribute_list = {}
	for attr in universe_attributes:
		universe_attribute_list[attr.descriptor] = attr

	try:
		revision = Revision.objects.filter(character=character_id).order_by('-rev_date')[0]
	except (Revision.DoesNotExist, IndexError):
		return render_to_response(template, {
			'character': character,
			'editmode': True,
			'universe_attributes': universe_attribute_list,
		})

	attribute_list = buildattributelist(universe_attributes, revision)

	return render_to_response(template, {
		'attributes': attribute_list,
		'character': character,
		'editmode': True,
		'universe_attributes': universe_attribute_list,
	}, context_instance=RequestContext(request))

#
# Save revision post action
#
def saverevision(request, character_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	try:
		universe_attributes = character.universe.attribute_set.filter(parentattribute__isnull=True)
	except:
		return HttpResponse("Error: universe has no attributes defined.")

	revision = None
	try:
		revision = Revision.objects.filter(character=character_id).order_by('-rev_date')[0]
		revisionnum = revision.revision + 1
	except (Revision.DoesNotExist, IndexError):
		revisionnum = 1

	newrevision = character.revision_set.create(revision=revisionnum, rev_date=datetime.datetime.now())

	try:
		revname = request.POST['revisionname']
		if len(revname) > 0:
			newrevision.name = revname
	except (KeyError):
		pass

	try:
		revnotes = request.POST['revisionnotes']
		if len(revnotes) > 0:
			newrevision.notes = revnotes
	except (KeyError):
		pass

	for attr in universe_attributes:
		if attr.type == 5:
			saveattributeset(attr, request.POST, newrevision, revision)
		else:
			saveattribute(attr, request.POST, newrevision, revision)

	newrevision.save()

	return HttpResponseRedirect(reverse('personae.characters.views.viewrevision', args=(character_id, newrevision.id,)))

#
# Jump to revision
#
def gotorevision(request, character_id):
	try:
		revision_id = request.GET['revision']
		if len(revision_id) == 0:
			raise ValueError
	except (KeyError, ValueError):
		return HttpResponse("No revision specified.")
	
	return HttpResponseRedirect(reverse('personae.characters.views.viewrevision', args=(character_id, revision_id,)))

#
# View revision page
#
def viewrevision(request, character_id, revision_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	try:
		revision = character.revision_set.get(revision=revision_id)
	except (Revision.DoesNotExist):
		return HttpResponse("No such revision for character %s." % character.name)

	try:
		universe_attributes = character.universe.attribute_set.all()
	except:
		return HttpResponse("Error: universe has no attributes defined.")

	attribute_list = buildattributelist(universe_attributes, revision)

	#raise Exception(attribute_list)

	universe_attribute_list = {}
	for attr in universe_attributes:
		universe_attribute_list[attr.descriptor] = attr

	template = "characters/universes/" + character.universe.descriptor + ".html"

	try:
		revision_list = character.revision_set.all()
	except:
		revision_list = False

	return render_to_response(template, {
		'attributes': attribute_list,
		'character': character,
		'revision_list': revision_list,
		'revision': revision,
		'universe_attributes': universe_attribute_list,
	})

def buildattributelist(universe_attributes, revision):
	attribute_list = {}

	univ_attributes_readlist = universe_attributes.filter(parentattribute__isnull=True)

	for attr in univ_attributes_readlist:
		val = readattribute(attr, revision)
		if val is not None:
			attribute_list[attr.descriptor] = val
	
	return attribute_list

def readattribute(attr, revision):
	if attr.type == 1:
		attrvaluelist = revision.attributeintegervalue_set.all()
	elif attr.type == 2:
		attrvaluelist = revision.attributestringvalue_set.all()
	elif attr.type == 3:
		attrvaluelist = revision.attributetextvalue_set.all()
	elif attr.type == 4:
		attrvaluelist = revision.attributechoicevalue_set.all()
	elif attr.type == 5:
		attrvaluelist = revision.attributesetvalue_set.all()
	else:
		return

	if attr.type == 5:
		if attr.multiple:
			vallist = attrvaluelist.filter(attribute=attr.id).order_by('line')
			val = {}
			data_lists = {}
			for subattr in attr.attribute_set.all():
				data_lists[subattr.descriptor] = readattribute(subattr, revision)
			for valitem in vallist:
				val[valitem.line] = {}
				for subattr in attr.attribute_set.all():
					try:
						tmp = data_lists[subattr.descriptor][valitem.line]
						val[valitem.line][subattr.descriptor] = tmp
					except (IndexError, KeyError):
						pass
			return val
		else:
			subattr_values = {}
			for subattr in attr.attribute_set.all():
				val = readattribute(subattr, revision)
				if val is not None:
					subattr_values[subattr.descriptor] = val
			if len(subattr_values) > 0:
				return subattr_values
	else:
		try:
			if attr.multiple:
				vallist = attrvaluelist.filter(attribute=attr.id).order_by('line')
				val = {}
				for valitem in vallist:
					val[valitem.line] = valitem
			else:
				val = attrvaluelist.get(attribute=attr.id)
			return val
		except (AttributeIntegerValue.DoesNotExist, AttributeStringValue.DoesNotExist, AttributeTextValue.DoesNotExist, AttributeChoiceValue.DoesNotExist):
			pass

def saveattributeset(attr, postdata, newrevision, oldrevision):
	vallist = {}
	maxlines = 0
	for subattr in attr.attribute_set.all():
		data = postdata.getlist(subattr.descriptor)
		if len(data) > maxlines:
			maxlines = len(data)
		vallist[subattr.descriptor] = data
	
		for i in range(maxlines):
			newvallist = []
			for subattr in attr.attribute_set.all():
				try:
					val = savesingleattribute(subattr, i+1, vallist[subattr.descriptor][i], newrevision, oldrevision)
					if val is not None:
						newvallist.append(val)
				except (IndexError, KeyError):
					pass
			if len(newvallist) > 0:
				needsnew = False
				if oldrevision is None:
					needsnew = True
				else:
					for item in newvallist:
						if item.attributesetvalue.count() == 0:
							needsnew = True
				if needsnew == True:
					setattr = newrevision.attributesetvalue_set.create(attribute=attr, line=i+1)
					for item in newvallist:
						item.attributesetvalue.add(setattr)
						item.save()
				else:
					setattr = oldrevision.attributesetvalue_set.get(attribute=attr, line=i+1)
					setattr.revisions.add(newrevision)
					setattr.save()

def saveattribute(attr, postdata, newrevision, oldrevision):
	if attr.multiple == True:
		try:
			vallist = postdata.getlist(attr.descriptor)
		except (KeyError):
			return

		if len(vallist) == 0:
			return
		
		count = 0
		for ln in vallist:
			val = ln
			if len(val) == 0:
				continue

			if attr.type == 1 or attr.type == 4:
				val = int(val)
				if val < 1:
					continue

			count += 1
			savesingleattribute(attr, count, val, newrevision, oldrevision)

				
	else:
		try:
			val = postdata[attr.descriptor]
		except (KeyError):
			return

		savesingleattribute(attr, 0, val, newrevision, oldrevision)

def savesingleattribute(attr, line, data, newrevision, oldrevision):
	if line < 0:
		return

	val = data

	if len(val) == 0:
		return

	if attr.type == 1 or attr.type == 4:
		val = int(val)
		if val < 1:
			return

	if attr.type == 1:
		if oldrevision is not None:
			oldattrset = oldrevision.attributeintegervalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributeintegervalue_set
	elif attr.type == 2:
		if oldrevision is not None:
			oldattrset = oldrevision.attributestringvalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributestringvalue_set
	elif attr.type == 3:
		if oldrevision is not None:
			oldattrset = oldrevision.attributetextvalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributetextvalue_set
	elif attr.type == 4:
		if oldrevision is not None:
			oldattrset = oldrevision.attributechoicevalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributechoicevalue_set
	else:
		return

	if oldrevision is not None:
		try:
			oldval = oldattrset.get(attribute=attr, line=line)
			if ((attr.type == 4) and (oldval.choice.id == val)) or (oldval.value == val):
				oldval.revisions.add(newrevision)
				oldval.save()
				return oldval
		except (AttributeIntegerValue.DoesNotExist, AttributeStringValue.DoesNotExist, AttributeTextValue.DoesNotExist, AttributeChoiceValue.DoesNotExist):
			pass
	if attr.type == 4:
		ch = AttributeChoice.objects.get(pk=val)
		return newattrset.create(attribute=attr, choice=ch, line=line)
	else:
		return newattrset.create(attribute=attr, value=val, line=line)


