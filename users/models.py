from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
# Create your models here.

status = [
	(0, 'Fail'),
	(1, 'Pass'),
	(2, 'Bypass'),
]

Final_status = [
	(0, 'Rejected'),
	(1, 'OK'),
]


class Data(models.Model):
	dt = models.DateTimeField(auto_now_add=True, auto_now=False)
	rating = models.CharField(max_length=255)
	hold = models.IntegerField(default=2, choices=status)
	hold_a = models.FloatField(default=0)
	hold_t = models.FloatField(default=0)
	hold_v = models.FloatField()
	trip = models.IntegerField(default=2, choices=status)
	trip_a = models.FloatField(default=0)
	trip_t = models.FloatField(default=0)
	trip_v = models.FloatField()
	arc = models.IntegerField(default=0, choices=status)
	cont = models.IntegerField(default=2, choices=status)
	knr = models.IntegerField(default=2, choices=status)
	hv = models.IntegerField(default=2, choices=status)
	status = models.IntegerField(default=0, choices=Final_status)


	def __str__(self):
		return '{} {}'.format(self.dt.strftime("%d/%m/%y %I:%M:%S %p"), self.status)

class Email(models.Model):
	email_id = models.EmailField()

	def __str__(self):
		return self.email_id


Machine_Choice = [
    (1, 'In'),
    (2, 'Out'),
]

class Machine(models.Model):
	line = models.PositiveIntegerField(verbose_name='Line Number')
	machine = models.PositiveIntegerField(verbose_name='Machne Number', choices=Machine_Choice)

	def __str__(self):
		return 'Line {} & Machine {}'.format(self.line, self.get_machine_display())


class MailStatus(models.Model):
	dt = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.dt.strftime("%d/%m/%Y")


class ShiftTime(models.Model):
	From = models.PositiveIntegerField(validators=[MaxValueValidator(23)])
	to = models.PositiveIntegerField(validators=[MaxValueValidator(23)])

	def __str__(self):
		return 'from {} to {}'.format(self.From, self.to)