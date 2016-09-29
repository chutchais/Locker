from django.db import models


class Group(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name


class Locker(models.Model):
	USED = 'USED'
	PENDING = 'PENDING'
	STATUS_CHOICES = (
        (USED, 'On using'),
        (PENDING, 'Pending for confirm'),
    )
	lockerid = models.CharField(primary_key=True,max_length=50)
	group = models.ForeignKey('Group' ,related_name='locker_list',blank=True,null=True)
	port_total =  models.IntegerField(default=12)
	description = models.CharField(max_length=255,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	actived = models.BooleanField(default=False) #Used/Not used
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=PENDING)


	def __str__(self):
		return self.lockerid

	def port_count(self):
		return self.lockerport_list.count()
	port_count.short_description="Total Port"

	def on_used(self):
		return self.lockerport_list.filter(status='USED').count()
	on_used.short_description="On used"


class LockerPort(models.Model):
	USED = 'USED'
	AVAILABLE = 'AVAILABLE'
	RESERVED = 'RESERVED'
	STATUS_CHOICES = (
		(USED, 'On using'),
		(AVAILABLE,'Avialable'),
		(RESERVED, 'Reserved for tag'),
		)
	portid = models.IntegerField(default=1)
	lockerid = models.ForeignKey('Locker' ,related_name='lockerport_list')
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	actived = models.BooleanField(default=False) #Used/Not used
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=AVAILABLE)

	def __str__(self):
		return ("Port %s on %s" % (self.portid,self.lockerid))

	def reserved(self):
		return self.reserved_lockerport_list.count()



class Tag(models.Model):
	USR = 'USER'
	ADMIN = 'ADMIN'
	TAGTYPE_CHOICES = (
        (USR, 'Normal user'),
        (ADMIN, 'Administrator'),
    )
	USED = 'USED'
	PENDING = 'PENDING'
	RESERVED = 'RESERVED'
	AVAILABLE = 'AVAILABLE'
	STATUS_CHOICES = (
        (USED, 'On using'),
        (PENDING, 'Pending for confirm'),
        (RESERVED, 'Reserved for tag'),
        (AVAILABLE, 'Available'),
    )

	tagid = models.CharField(primary_key=True,max_length=100)
	tag_label =  models.CharField(max_length=50,blank=True, null=True)
	tagtype = models.CharField(max_length=50,choices=TAGTYPE_CHOICES,default=USR)
	group = models.CharField(max_length=50,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	lockerport = models.OneToOneField('LockerPort' ,related_name='tag_used',blank=True,null=True)#,on_delete=models.CASCADE
	#lockerport = models.ForeignKey('LockerPort' ,related_name='tag_used',blank=True, null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	actived = models.BooleanField(default=False) #Used/Not used
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=PENDING)

	def __str__(self):
		return self.tagid

	def reserved(self):
		return self.reserved_tag_list.count()


	#custom save model
	def save(self, *args, **kwargs):
		#print (self._state.adding)
		if not self._state.adding:
			old = self.__class__.objects.get(pk=self._get_pk_val())
			previouslockerport= old.lockerport
			#print (previouslockerport)
			if previouslockerport :
				previouslockerport.status='AVAILABLE'
				previouslockerport.save()

			if self.lockerport :
				self.status='USED'
				self.lockerport.status='USED'
				self.lockerport.save()
			else:
				self.status='AVAILABLE'

		super(Tag, self).save(*args, **kwargs)


class ReserveLocker(models.Model):
	tagid = models.ForeignKey('Tag' ,related_name='reserved_tag_list')
	lockerport = models.ForeignKey('LockerPort' ,related_name='reserved_lockerport_list')
	description = models.CharField(max_length=255,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return ("Tag %s on %s" % (self.tagid,self.lockerport))

	#custom save model
	def save(self, *args, **kwargs):
		print ('Reserved')
		if self._state.adding:
			self.lockerport.status='RESERVED'
			#import LockerPort
			#lp = LockerPort.objects.get(lockerportid__id='')
			self.lockerport.save()
			print (self.lockerport.status)

		super(ReserveLocker, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		print ('record %s' % self.tagid.reserved_tag_list.count())
		if self.tagid.reserved_tag_list.count()==1:
			self.lockerport.status='AVAILABLE'
			self.lockerport.save()
		super(ReserveLocker, self).delete()


class Tracking(models.Model):
	USED = 'USED'
	CLOSED = 'CLOSED'
	STATUS_CHOICES =((USED, 'On using'),(CLOSED, 'Closed'))
	lockerport= models.ForeignKey('LockerPort',related_name='tracking_list',blank=True,null=True)
	tag_start = models.ForeignKey('Tag',related_name='tracking_start_list',blank=True,null=True)
	tag_stop = models.ForeignKey('Tag',related_name='tracking_stop_list',blank=True,null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=USED)
	
	def __str__(self):
		return ("Tracking %s on %s" % (self.tag_start,self.lockerport))


