from personae.characters.models import Character, Universe, Revision, Attribute
from django.contrib import admin

class AttributeInline(admin.TabularInline):
	model = Attribute
	extra = 3

class UniverseAdmin(admin.ModelAdmin):
	inlines = [AttributeInline]

admin.site.register(Universe, UniverseAdmin)
admin.site.register(Character)
admin.site.register(Revision)
