from django.contrib import admin
from .models import *
from .utils.load import load_repository

#def bunk_load_repository(self, request, queryset):
#  rows_updated = load_repository()
#  if rows_updated == 1:
#    message_bit = "1 row was"
#  else:
#    message_bit = "%s rows were" % rows_updated
#  self.message_user(request, "%s successfully inserted." % message_bit)

#bunk_load_repository.short_description = "Load repository data"


# Register your models here.

admin.site.register(Language)
admin.site.register(Family)
admin.site.register(Sentence)
admin.site.register(Word)
admin.site.register(Character)
admin.site.register(Repository_Detail)
admin.site.register(Repository_Source)
admin.site.register(Inverted_Sentence)
admin.site.register(Inverted_Word)
#admin.site.add_action(bunk_load_repository, 'load_repository')