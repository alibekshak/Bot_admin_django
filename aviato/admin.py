from django.contrib import admin
from .models import *
from .forms import *
from loguru import logger as l

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



class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_time', 'product', 'address', 'bool_status', 'status', 'note', "direction", 'driver', 'location', "delivery_information", 'user')
    search_fields = ['id', 'note', 'address', 'price','time_update_location', 'product', "direction",'user__first_name', 'status', 'location']
    list_editable = ('note', 'address', 'product', 'user', 'status', 'driver', "location")
    list_filter = ('time_update_location', 'status', 'driver', "direction")

    
    def get_fields(self, request, obj):
        return ["note", "address", "product", "price", 
            "phone", "status", "bool_status"]

    
    def save_model(self, request, obj, form, change):
        def get_number_product_1(string):
            try:
                number = ""
                if len(string) == 0: return "❌ Уберите лишний пробел в строке <b>'Товар'</b> "
                else:
                    string = string.lower()
                    i = string.split("шт")[0]
                    for j in range(1, len(i)):
                        if i[-j].isdigit():
                            number += str(i[-j])
                        if i[-j].isalpha():

                            replace_text = f"{number[::-1]}шт"
                            orig_product = string.replace(replace_text, "").lower()
                            pr = Products.objects.get(product=orig_product)
                            l.critical(pr)
                            if number:
                                pr.count -= int(number[::-1])
                            else: pr.count -= 1
                            pr.save()
                            return pr

                    replace_text = f"{number[::-1]}шт"
                    orig_product = string.replace(replace_text, "").lower()
                    pr = Products.objects.get(product=orig_product)
                    l.critical(pr)

                    if number:
                        pr.count -= int(number[::-1])
                    else: pr.count -= 1
                    pr.save()
                    return pr
            except Exception as ex:
                return f"Такой товар не найден ({string}) ({str(ex)})"



class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'count', 'opt_price', "product_sum", "product_percent")
    search_fields = ['id', 'product', 'count', 'opt_price']
    list_filter = ('avalability',)
    list_editable = ('product', 'opt_price', 'count', 'product_sum')

    
    def get_fields(self, request, obj):
        return ['product', 'count', 'opt_price', 'photo']

    
    def save_model(self, request, obj, form, change):

        _ = obj.count 
        try:
            old_obj = self.model.objects.get(id=obj.id)
        except: pass


        try:
            if request.POST.get("count") is None:
                obj.count = old_obj.count + obj.count
            else:
                obj.count = int(request.POST.get("count"))
                obj.fake_count = obj.co
        except Exception as ex:
            obj.count = int(request.POST.get("count"))


        if obj.fake_count != 0:
            if obj.count <= 0:
                pass
            else:
                obj.fake_count += obj.count

        if obj.fake_count == 0:
            obj.fake_count = obj.count
        
        obj.product_suum = obj.opt_price * obj.fake_count
        obj.product_percent = ((obj.opt_price * obj.fake_count) // 100) * 2.5
        obj.product = obj.product.lower()



        if obj.count <= 0:
            obj.availability = False

        if obj.count > 0:
            obj.availability = True


        if obj.count == 123456789:
            l.critical(True)
            obj.count = 2

        obj.save()

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Applications, ApplicationsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(RoleCode, RoleAdmin)