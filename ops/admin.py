from django.contrib import admin
from .models import Campaign, OpsUser, Heap, LeadFile, UploadFile

admin.site.register(OpsUser)
admin.site.register(Campaign)
admin.site.register(LeadFile)
admin.site.register(Heap)
admin.site.register(UploadFile)