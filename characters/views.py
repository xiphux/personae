import datetime
from personae.characters.models import Universe, Character, Revision
from personae.characters.datafunctions import buildattributelist, saveattributeset, saveattribute, diffrevisions
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

#
# Front index page
# request: django request object
#
@login_required
def index(request):
	characters = Character.objects.filter(user=request.user).order_by('name')
	return render_to_response('characters/index.html', {'characters': characters}, context_instance=RequestContext(request))

#
# Create new character form
# request: django request object
#
@login_required
def newcharacter(request):
	universe_list = Universe.objects.all().order_by('name')
	return render_to_response('characters/newcharacter.html', {'universe_list': universe_list}, context_instance=RequestContext(request))

#
# Create new character form POST action
# request: django request object
#
@login_required
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

	char = universe.character_set.create(name=char_name, user=request.user)
	return HttpResponseRedirect(reverse('personae.characters.views.detail', args=(char.id,)))
		
#
# Character detail page
# request: django request object
# character_id: character id
#
@login_required
def detail(request, character_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	if character.user != request.user:
		return HttpResponse("You do not have access to view this character.")

	try:
		revision = Revision.objects.filter(character=character_id).order_by('-rev_date')[0]
	except (Revision.DoesNotExist, IndexError):
		return render_to_response('characters/norevisions.html', {'character': character}, context_instance=RequestContext(request))

	return HttpResponseRedirect(reverse('personae.characters.views.viewrevision', args=(character_id, revision.id)))
	
#
# Edit character action
# request: django request object
# character_id: character id
#
@login_required
def edit(request, character_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	if character.user != request.user:
		return HttpResponse("You do not have access to edit this character.")

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
		}, context_instance=RequestContext(request))

	attribute_list = buildattributelist(universe_attributes, revision)

	return render_to_response(template, {
		'attributes': attribute_list,
		'character': character,
		'editmode': True,
		'universe_attributes': universe_attribute_list,
	}, context_instance=RequestContext(request))

#
# Save revision post action
# request: django request object
# character_id: character id
#
@login_required
def saverevision(request, character_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	if character.user != request.user:
		return HttpResponse("You do not have access to edit this character.")

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
# request: django request object
# character_id: character id
#
@login_required
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
# request: django request object
# character_id: character id
# revision_id: revision id
#
@login_required
@cache_page
def viewrevision(request, character_id, revision_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	if character.user != request.user:
		return HttpResponse("You do not have access to view this character.")

	try:
		revision = character.revision_set.get(revision=revision_id)
	except (Revision.DoesNotExist):
		return HttpResponse("No such revision for character %s." % character.name)

	prevrevision = None
	nextrevision = None
	try:
		prevrevision = character.revision_set.get(revision=(int(revision_id)-1))
	except (Revision.DoesNotExist):
		pass

	try:
		nextrevision = character.revision_set.get(revision=(int(revision_id)+1))
	except (Revision.DoesNotExist):
		pass

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
		'prevrevision': prevrevision,
		'nextrevision': nextrevision,
	}, context_instance=RequestContext(request))

@login_required
@cache_page
def diffrevision(request, character_id, revision_id):
	try:
		character = Character.objects.get(pk=character_id)
	except (Character.DoesNotExist):
		return HttpResponse("No such character.")

	if character.user != request.user:
		return HttpResponse("You do not have access to view this character.")

	try:
		revision = character.revision_set.get(revision=revision_id)
	except (Revision.DoesNotExist):
		return HttpResponse("No such revision for character %s." % character.name)

	try:
		prevrevision = character.revision_set.get(revision=(int(revision_id)-1))
	except (Revision.DoesNotExist):
		return HttpResponse("No previous revision.")

	difflist = diffrevisions(prevrevision, revision)

	#raise Exception(difflist)

	return render_to_response('characters/diff.html', {
		'character': character,
		'leftrev': prevrevision,
		'rightrev': revision,
		'difflist': difflist,
	}, context_instance=RequestContext(request))

