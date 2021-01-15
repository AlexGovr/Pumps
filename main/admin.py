from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Main.models import Manufacturer, Eq_type, Eq_model, Eq_mark

class ManufAdmin(admin.ModelAdmin):
    pass
class Eq_type_admin(admin.ModelAdmin):
    pass
class Eq_model_admin(admin.ModelAdmin):
    pass
class Eq_mark_admin(admin.ModelAdmin):
    pass

admin.site.register(Manufacturer, ManufAdmin)
admin.site.register(Eq_type, Eq_type_admin)
admin.site.register(Eq_model, Eq_model_admin)
admin.site.register(Eq_mark, Eq_mark_admin)


# class ManufInline(admin.StackedInline):
#     model = Manufacturer
#     can_delete = False
#     verbose_name_plural = 'manufacturer'

# class EqInline(admin.StackedInline):
#     model = Equipment_type
#     can_delete = False
#     verbose_name_plural = 'manufacturer'

# class UserAdmin(BaseUserAdmin):
#     inlines = (ManufInline, EqInline)

# # Re-register UserAdmin
# admin.site.register(ManufInline, UserAdmin)
# admin.site.register(EqInline, UserAdmin)