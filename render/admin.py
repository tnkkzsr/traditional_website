from django.contrib import admin

# Register your models here.
from .models import User, AsahiyakiEvaluation,Asahiyaki

class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'username')
    search_fields = ('username', 'uuid')


admin.site.register(User, UserAdmin)
admin.site.register(AsahiyakiEvaluation)
admin.site.register(Asahiyaki)


