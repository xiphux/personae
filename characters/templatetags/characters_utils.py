from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def dots(value, max):
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
def squares(value, max):
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
