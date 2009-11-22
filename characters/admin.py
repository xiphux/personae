from personae.characters.models import Character, Universe, Revision, Attribute, AttributeChoice
from django.contrib import admin

class AttributeInline(admin.TabularInline):
	model = Attribute
	extra = 3

class AttributeChoiceInline(admin.TabularInline):
	model = AttributeChoice
	extra = 3

class AttributeAdmin(admin.ModelAdmin):
	inlines = [AttributeChoiceInline]

class UniverseAdmin(admin.ModelAdmin):
	inlines = [AttributeInline]

admin.site.register(Universe, UniverseAdmin)
admin.site.register(Character)
admin.site.register(Revision)
admin.site.register(Attribute, AttributeAdmin)
