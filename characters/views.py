from personae.characters.models import Universe
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

def newcharacter(request):
	universe_list = Universe.objects.all().order_by('name')
	return render_to_response('characters/newcharacter.html', {'universe_list': universe_list}, context_instance=RequestContext(request))

def createcharacter(request):
	try:
		char_name = request.POST['name']
		if len(char_name) == 0:
			raise KeyError
	except (KeyError):
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

		

def detail(request, character_id):
	return HttpResponse("You're looking at character %s." % character_id)

def edit(request, character_id):
	return HttpResponse("You're editing character %s." % character_id)

def newrevision(request, character_id):
	return HttpResponse("You're creating a new revision for character %s." % character_id)

def viewrevision(request, character_id, revision_id):
	return HttpResponse("You're looking at revision %s of character %s." % (revision_id, character_id))
