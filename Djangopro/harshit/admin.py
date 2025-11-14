from django.contrib import admin
from .models import ChaiVarity, ChaiReview, Store, ChaiCertification

# Register your models here.

class ChaiReviewInline(admin.TabularInline):
    model = ChaiReview
    extra = 2

class ChaiVarityAdmin(admin.ModelAdmin):
    list_display = ('name',type,'date_added')
    inlines = [ChaiReviewInline]

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name','location')
    filter_horizontal = ('chai_varities',  )

class ChaiCertificationAmin(admin.ModelAdmin):
    list_display = ('chai','certification_number')


admin.site.register(ChaiVarity,ChaiVarityAdmin)
admin.site.register(Store,StoreAdmin)
admin.site.register(ChaiCertification,ChaiCertificationAmin)

