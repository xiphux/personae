from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def dots(value, max):
	if len(value) == 0:
		value = 0
	else:
		value = int(value)
	if max > 0:
		ret = ""
		for num in range(max):
			if num < value:
				ret += '&#9673;'
			else:
				ret += '&#9678;'
		return mark_safe(ret)
	else:
		return mark_safe(''.join(['&#9673;' for num in xrange(value)]))

@register.filter
@stringfilter
def squares(value, max):
	if len(value) == 0:
		value = 0
	else:
		value = int(value)
	if max > 0:
		ret = ""
		for num in range(max):
			if num < value:
				ret += '&#9635;'
			else:
				ret += '&#9634;'
		return mark_safe(ret)
	else:
		return mark_safe(''.join(['&#9635;' for num in xrange(value)]))

@register.filter
def diff(a, b):
	try:
		aint = int(a.value)
	except:
		aint = 0
	try:
		bint = int(b.value)
	except:
		bint = 0
	if aint > bint:
		return "+" + str(aint - bint)
	elif aint < bint:
		return str(aint - bint)
	else:
		return "0"

@register.filter
def get_range(value):
	return range(value + 1)
