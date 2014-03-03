from django.contrib import admin
from cleartherack.models import Purchase, Item, ItemStock

class PurchaseAdmin(admin.ModelAdmin):

	list_display = ('purchase_date', 'user', 'amt','rack_cleared','com_trip','free_coffee')
	list_filter = ('user','rack_cleared','com_trip','free_coffee')
	search_fields = ('user',)
	save_on_top = True

class ItemAdmin(admin.ModelAdmin):

	list_display = ('name','active')
	list_filter = ('active',)
	search_fields = ('name',)
	save_on_top = True

class ItemStockAdmin(admin.ModelAdmin):

	list_display = ('user','item','stock_status','entry_date')
	list_filter = ('user','item','stock_status')
	search_fields = ('user','item',)
	save_on_top = True


admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemStock,ItemStockAdmin)