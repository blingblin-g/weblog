from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import Category

class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = 'Categories'
    menu_icon = 'tag'
    list_display = ('name', 'slug')
    search_fields = ('name',)

modeladmin_register(CategoryAdmin) 