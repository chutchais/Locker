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
        (USED, 'In using'),
        (PENDING, 'Pending for confirm'),
        (RESERVED, 'Reserved for tag'),
        (AVAILABLE, 'Available'),
    )

	tagid = models.CharField(primary_key=True,max_length=100)
	tagtype = models.CharField(max_length=50,choices=TAGTYPE_CHOICES,default=USR)
	group = models.CharField(max_length=50,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	lockerport = models.ForeignKey('LockerPort' ,related_name='tag_used',blank=True, null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	actived = models.BooleanField(default=False) #Used/Not used
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=PENDING)

	def __str__(self):
		return self.tagid


class ReserveLocker(models.Model):
	tagid = models.ForeignKey('Tag' ,related_name='reserved_tag_list')
	lockerport = models.ForeignKey('LockerPort' ,related_name='reserved_lockerport_list')
	description = models.CharField(max_length=255,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return ("Tag %s on %s" % (self.tagid,self.lockerport))