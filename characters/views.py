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
		universe_attributes = character.universe.attribute_set.all()
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
		try:
			val = request.POST[attr.descriptor]
		except (KeyError):
			continue

		if len(val) == 0:
			continue

		if attr.type == 1 or attr.type == 4:
			val = int(val)
			if val < 1:
				continue

		if attr.type == 1:
			if revision is not None:
				oldattrset = revision.attributeintegervalue_set
			else:
				oldattrset = None
			newattrset = newrevision.attributeintegervalue_set
		elif attr.type == 2:
			if revision is not None:
				oldattrset = revision.attributestringvalue_set
			else:
				oldattrset = None
			newattrset = newrevision.attributestringvalue_set
		elif attr.type == 3:
			if revision is not None:
				oldattrset = revision.attributetextvalue_set
			else:
				oldattrset = None
			newattrset = newrevision.attributetextvalue_set
		elif attr.type == 4:
			if revision is not None:
				oldattrset = revision.attributechoicevalue_set
			else:
				oldattrset = None
			newattrset = newrevision.attributechoicevalue_set

		createnew = True
		if revision is not None:
			try:
				if attr.type == 4:
					oldval = oldattrset.get(attribute=attr.id)
					if oldval.choice.id == val:
						oldval.revisions.add(newrevision)
						oldval.save()
						createnew = False
				else:
					oldval = oldattrset.get(attribute=attr.id)
					if oldval.value == val:
						oldval.revisions.add(newrevision)
						oldval.save()
						createnew = False
			except (AttributeIntegerValue.DoesNotExist, AttributeStringValue.DoesNotExist, AttributeTextValue.DoesNotExist, AttributeChoiceValue.DoesNotExist):
				pass
		if createnew:
			if attr.type == 4:
				ch = AttributeChoice.objects.get(pk=val)
				newattrset.create(attribute=attr, choice=ch)
			else:
				newattrset.create(attribute=attr, value=val)

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
	revision_integer_attributes = revision.attributeintegervalue_set.all()
	revision_string_attributes = revision.attributestringvalue_set.all()
	revision_text_attributes = revision.attributetextvalue_set.all()
	revision_choice_attributes = revision.attributechoicevalue_set.all()

	attribute_list = {}

	for attr in universe_attributes:
		if attr.type == 1:
			attrvaluelist = revision_integer_attributes
		elif attr.type == 2:
			attrvaluelist = revision_string_attributes
		elif attr.type == 3:
			attrvaluelist = revision_text_attributes
		elif attr.type == 4:
			attrvaluelist = revision_choice_attributes
		else:
			continue
		try:
			val = attrvaluelist.get(attribute=attr.id)
			attribute_list[attr.descriptor] = val
		except (AttributeIntegerValue.DoesNotExist, AttributeStringValue.DoesNotExist, AttributeTextValue.DoesNotExist, AttributeChoiceValue.DoesNotExist):
			pass
	
	return attribute_list
