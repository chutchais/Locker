from django.contrib import admin

from .models import Group
from .models import Tag
from .models import Locker
from .models import LockerPort
from .models import ReserveLocker


class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name','description')
    fieldsets = [
        (None,               {'fields': ['name','description']}),
    ]

admin.site.register(Group,GroupAdmin)


class LockerPortInline(admin.TabularInline):
    model = LockerPort
    extra = 1

class LockerAdmin(admin.ModelAdmin):
    search_fields = ['lockerid']
    list_filter = ['group','actived','status']
    list_display = ('lockerid','group','description','actived','status')
    fieldsets = [
        (None,               {'fields': ['lockerid','group','description','actived','status']}),
    ]
    inlines = [LockerPortInline]

admin.site.register(Locker,LockerAdmin)



class TagAdmin(admin.ModelAdmin):
    search_fields = ['tagid']
    list_filter = ['tagid','tagtype','group']
    list_display = ('tagid','tagtype','group','description','actived','status')
    fieldsets = [
        (None,               {'fields': ['tagid','tagtype','group','description','actived','status']}),
    ]

admin.site.register(Tag,TagAdmin)



class ReserveLockerAdmin(admin.ModelAdmin):
    search_fields = ['tagid']
    list_filter = ['tagid']
    list_display = ('tagid','lockerport','description')
    fieldsets = [
        (None,               {'fields': ['tagid','lockerport','description','user']}),
    ]

admin.site.register(ReserveLocker)

