from personae.characters.models import Character, Revision, Attribute
from django.contrib import admin

class AttributeInline(admin.TabularInline):
	model = Attribute
	extra = 3

class RevisionAdmin(admin.ModelAdmin):
	inlines = [AttributeInline]


admin.site.register(Character)
admin.site.register(Revision, RevisionAdmin)
