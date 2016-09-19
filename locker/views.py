from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Locker
from .models import LockerPort
from .models import Tag
from .serializers import LockerPortSerializer
from .serializers import LockerSerializer

from .models import Tracking

# Create your views here.
def index(request):
	context ={
        "data": "data",
        "form": "form"
    }
	return render(request, 'locker/index.html',context)

def admin_page(request):
	context ={
        "data": "data",
        "form": "form"
    }
    
	return render(request, 'locker/admin.html',context)

@api_view(['GET', 'POST'])
def update_locker_status(request,lockerid):
	objLocker,created = Locker.objects.get_or_create(lockerid=lockerid)
	if created :
		message ="New locker created.."
	else:
		message ="Current status %s" % (objLocker.status)

	return Response({'locker': lockerid ,'message':message})


@api_view(['GET', 'POST'])
def get_locker_status(request,lockerid):
	if request.method == 'GET':
		#lockerPort = LockerPort.objects.filter(lockerid__lockerid=lockerid)
		lockerPort = Locker.objects.filter(lockerid = lockerid)
		
		if lockerPort:
			serializer = LockerSerializer(lockerPort,many=True)
			return Response(serializer.data )
		else:
			data ={"lockerid": lockerid,"message": "Not exist in system"}
			return Response(data)


@api_view(['GET', 'POST'])
def get_tag_status(request,tagid):
	if request.method == 'GET':
		#lockerPort = LockerPort.objects.filter(lockerid__lockerid=lockerid)
		try:
			#check Tag
			tag = Tag.objects.get(tagid=tagid)
			if tag.lockerport:
				data ={"accept": False ,"tagid": tagid,"tagtype":tag.tagtype,"lockerid":tag.lockerport.lockerid.lockerid,"portid":tag.lockerport.portid,
				"message": "On using","status":tag.status}
			else :
				data ={"accept": True,"tagid": tagid,"tagtype":tag.tagtype,"lockerid":"","portid":"","message": "Tag is ready for use","status":tag.status}
			return Response(data)
		except Tag.DoesNotExist :
			data ={"accept": False,"tagid": tagid,"message": ("Tag %s doesn't exist in system" % tagid)}
			return Response(data)


@api_view(['GET','POST'])
def register_tag(request,tagid):
			tag,created = Tag.objects.get_or_create(tagid=tagid)
			if created :
				#newtag.save()
				data ={"accept":True,"tagid": tagid,"message": "Tag register successful"}
			else :
				data ={"accept":False,"tagid": tagid,"status": tag.status,"message": "Tag already exist"}
			return Response(data)


@api_view(['GET', 'POST'])
def reserve_locker(request,tagid,lockerid,portid):
	lockerport= LockerPort()
	tag=Tag()
	try :
		tag = Tag.objects.get(tagid=tagid)
		if tag.lockerport:
			data ={"tagid": tagid,"message": "This tag has been using","accept":False,"status":tag.status}
		else:

			lockerport = LockerPort.objects.get(portid=portid,lockerid__lockerid=lockerid)
			objLp = lockerport.tag_used if hasattr(lockerport,'tag_used') else None
			if objLp :
				data ={"tagid": tagid,"message": "Locker Port already reserved","accept":False,"status":lockerport.status}
			else :
				tag.lockerport = lockerport
				tag.status='USED'
				tag.save()
				lockerport.status='USED'
				lockerport.save()
				data ={"tagid": tagid,"message": "Reserve successful","accept":True,"status":tag.status}
				#Add tracking
				t=Tracking(lockerport=lockerport,tag_start=tag)
				t.save()

	except lockerport.DoesNotExist :
		data ={"tagid": tagid,"message": "Locker Port does not exist in system","accept":False}
	except tag.DoesNotExist :
		data ={"tagid": tagid,"message": "Tag does not exist in system","accept":False}

	return Response(data)

@api_view(['GET', 'POST'])
def clear_tag(request,tagid):
	tag = Tag.objects.get(tagid=tagid)
	lockerport = LockerPort.objects.get(tag_used=tag)
	#clear Ticket
	close_ticket (tag,lockerport)

	lockerport.status='AVAILABLE'
	lockerport.save()

	tag.lockerport = None
	tag.status='AVAILABLE'
	tag.save()
	
	
	data ={"tagid": tagid,"message": "Clear successful","accept":True,"status":tag.status}
	return Response(data)

@api_view(['GET', 'POST'])
def clear_locker(request,lockerid,portid):
	lockerport=LockerPort()
	tag=Tag()
	try :
		lockerport = LockerPort.objects.get(portid=portid,lockerid__lockerid=lockerid)
		lockerport.status='AVAILABLE'
		lockerport.save()
		if lockerport :
			tag = Tag.objects.get(lockerport=lockerport)
			#clear Ticket
			close_ticket (tag,lockerport)
			tag.lockerport = None
			tag.status='AVAILABLE'
			tag.save()
		data ={"lockerid": lockerid,"portid":portid,"message": "Clear successful","accept":True,"status":lockerport.status}
	except lockerport.DoesNotExist:
		data ={"lockerid": lockerid,"portid":portid,"message": "Locker Port does not exist in system","accept":False}
	except tag.DoesNotExist:
		data ={"lockerid": lockerid,"portid":portid,"message": "Clear successful","accept":True,"status":lockerport.status}

	return Response(data)


def close_ticket(tag,lockerport):
	try:
		t=Tracking.objects.get(lockerport=lockerport,tag_start=tag,status='USED')
		if t:
			t.status ='CLOSED'
			t.tag_stop =tag
			t.save()
	except t.DoesNotExist:
		pass
