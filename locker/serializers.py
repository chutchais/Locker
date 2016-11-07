from rest_framework import serializers
from .models import LockerPort
from .models import Locker




class LockerPortSerializer(serializers.ModelSerializer):

    class Meta:
        model = LockerPort
        fields = ( 'portid','actived','status')


class LockerSerializer(serializers.ModelSerializer):
	lockerport_list = LockerPortSerializer(many=True,read_only=True)
	class Meta:
		model = Locker
		fields = ('lockerid','actived','status','lockerport_list')