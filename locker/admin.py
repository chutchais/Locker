#locker12345
from django.contrib import admin

from .models import Group
from .models import Tag
from .models import Locker
from .models import LockerPort
from .models import ReserveLocker
from .models import Tracking


class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name','description')
    fieldsets = [
        (None,               {'fields': ['name','description']}),
    ]

admin.site.register(Group,GroupAdmin)


def create_locker_port(self, request, queryset):
    for obj in queryset:
        obj.status='USED'
        obj.actived=True
        obj.save()
        for i in range(1,13) :
            lp,created = LockerPort.objects.get_or_create(lockerid = obj, portid = i)
    self.message_user(request, "%s successfully create Locker ports." % obj.lockerid)
create_locker_port.short_description = "Create new locker ports"


def clear_locker_port(self, request, queryset):
    #queryset.update(status='USED')
    for obj in queryset:
    	for lp in obj.lockerport_list.all() :
    		tag = Tag.objects.filter(lockerport=lp)
    		lp.status='AVAILABLE'
    		lp.save()
    		tag.update(lockerport=None,status='AVAILABLE')
    self.message_user(request, "%s successfully clear all Locker ports." % obj.lockerid)
clear_locker_port.short_description = "Clear all locker ports"


class LockerPortInline(admin.TabularInline):
    model = LockerPort
    fields = ['portid','lockerid','actived','status']
    extra = 1

    

class LockerAdmin(admin.ModelAdmin):
    search_fields = ['lockerid']
    list_filter = ['group','actived','status']
    list_display = ('lockerid','group','description','port_count','on_used','actived','status')
    fieldsets = [
        (None,               {'fields': ['lockerid','group','description','actived','status']}),
    ]
    inlines = [LockerPortInline]
    actions = [create_locker_port,clear_locker_port]

admin.site.register(Locker,LockerAdmin)


class TagReserveInline(admin.TabularInline):
    model = ReserveLocker
    extra = 1



def clear_reserve(self, request, queryset):
    #queryset.update(status='USED')
    for obj in queryset:
        #Clear tracking
        close_ticket (obj.lockerport)
        obj.lockerport = None
        obj.save()

    self.message_user(request, "%s successfully clear reserver for all Tag." % obj.tagid)
clear_reserve.short_description = "Clear Locker reservation"

class TagAdmin(admin.ModelAdmin):
    search_fields = ['tagid']
    list_filter = ['lockerport__lockerid__lockerid','tagtype','group']
    list_display = ('tagid','tagtype','lockerport','group','description','actived','status')
    fieldsets = [
        (None,               {'fields': ['tagid','tagtype','lockerport','group','description','actived','status']}),
    ]
    order_fields ='tagid'
    inlines = [TagReserveInline]
    actions =[clear_reserve]

admin.site.register(Tag,TagAdmin)


def clear_port(self, request, queryset):
    #queryset.update(status='USED')
    for obj in queryset:
        print (obj)
        #Clear tracking
        close_ticket (obj)
        obj.tag_used.lockerport = None
    	#TODO--Need to find the way to update Tag
    	#obj.save()

    self.message_user(request, "%s successfully create Locker ports." % obj.portid)
clear_port.short_description = "Clear locker ports"

def close_ticket(lockerport):
    try:
        print (lockerport)
        t=Tracking.objects.get(lockerport=lockerport,status='USED')
        if t:
            t.status ='CLOSED'
            t.save()
    except t.DoesNotExist:
        pass

class LockerPortAdmin(admin.ModelAdmin):
	search_fields = ['portid']
	list_filter =['lockerid','status']
	list_display = ('portid','lockerid','get_tag','actived','status')
	fieldsets =[
	(None,					{'fields': ['portid','actived','status']}),
	]
	actions=[clear_port]

	def get_tag(self, obj):
		return obj.tag_used #self.tag_used if hasattr(self,'tag_used') else None
	get_tag.short_description = 'Tag Number'
	get_tag.admin_order_field = 'tag_used__tagid'
    #get_tag.admin_order_field=''

    #def get_tag(self, obj=None, **kwargs):
    #	return obj.tag_used.tagid
    #get_tag.short_description = 'Tag Number'
    #get_sn.admin_order_field = 'sn_wo__sn'

admin.site.register(LockerPort,LockerPortAdmin)



class TrackingAdmin(admin.ModelAdmin):
    search_fields = ['tag_start__tagid','tag_stop__tagid']
    list_filter = ['lockerport__lockerid','status']
    list_display = ('tag_start','lockerport','created_date','tag_stop','modified_date','closed_mode','status')
    fieldsets = [
        (None,               {'fields': ['tag_start','lockerport']}),
    ]

    def closed_mode(self,obj):
        if obj.tag_stop == None:
            return "Normal"
        else :
            return "Normal" if obj.tag_start == obj.tag_stop else "Admin"

admin.site.register(Tracking,TrackingAdmin)


# class ReserveLockerAdmin(admin.ModelAdmin):
#     search_fields = ['tagid']
#     list_filter = ['tagid']
#     list_display = ('tagid','lockerport','description')
#     fieldsets = [
#         (None,               {'fields': ['tagid','lockerport','description','user']}),
#     ]

# admin.site.register(ReserveLocker)

