from django.contrib import admin
from .models import *
from .forms import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'first_name', 'username', 'role')
    search_fields = ('user_id', 'first_name', 'username', 'role')
    list_editable = ('user_id', 'first_name', 'username', 'role')
    list_filter = ('id', 'user_id', 'first_name', 'username', 'role')

    def get_fields(self, obj, request):
        return ['first_name', 'username', 'role']


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active_user', 'code', 'role')
    search_fields = ('id', 'code', 'role')
    list_editable = ('user', 'active_user', 'code', 'role')
    list_filter = ('id', 'user', 'active_user', 'code', 'role')

    def get_fields(self, request, obj):
        return ["code", "role"]

    def save_model(self, request, obj, form, change):
        obj.user = Profile.objects.all().first()
        obj.save()


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'count', 'opt_price', 'avalability')
    search_fields = ('id', 'product')
    list_editable = ('product', 'count', 'opt_price', 'avalability')
    list_filter = ('id', 'product', 'count', 'opt_price')


    def get_fields(self, request, obj):
        return ['product']
    


class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'adress', 'product', 'delivery_information', 'location')
    search_fields = ('id', 'adress', 'product')
    list_editable = ('adress', 'product', 'location', 'delivery_information')
    list_filter = ('id', 'adress', 'product', 'location')

    def get_fields(self, request, obj):
        return ['adress','product']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(RoleCode, RoleAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Applications, ApplicationsAdmin)