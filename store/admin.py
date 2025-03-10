from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.contact import Contact
from .models.material import Material
from .models.size import Size
from .models.customization import Customization
from .models.type import Type
from .models.color import Color
from .models.fabric import Fabric
from .models.gsm import GSM
from .models.chosequantity import Chosequantity

from ckeditor.widgets import CKEditorWidget
from django import forms

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = '__all__'
        
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # list_display = ('name', 'price', 'category', 'description', 'image')
    list_display = ('name', 'category', 'image')
    search_fields = ('name', 'description', 'chosequantity',)
    filter_horizontal = ('materials', 'sizes', 'customizations', 'types', 'colors', 'fabrics', 'gsms', 'chosequantitys',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    list_filter = ('parent',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')
    search_fields = ('email', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_customer_name', 'quantity', 'price', 'date', 'address', 'phone', 'detail', 'status')
    search_fields = ('id', 'product__name', 'customer__first_name', 'customer__last_name', 'address', 'phone', 'status')

    def get_customer_name(self, obj):
        return f'{obj.customer.first_name} {obj.customer.last_name}'
    get_customer_name.short_description = 'Customer Name'

admin.site.register(Contact)
admin.site.register(Material)
admin.site.register(Size)
admin.site.register(Customization)
admin.site.register(Type)
admin.site.register(Color)
admin.site.register(Fabric)
admin.site.register(GSM)
admin.site.register(Chosequantity)