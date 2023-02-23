from django import template
from django.db import models
from django.db.models.deletion import DO_NOTHING

from Users import models as UserModels
from Server.Utils import EnumChoices


class ACTIVITIES(EnumChoices):
	ASSET = "Asset"
	VULN = "Vulnerability"
	PENTEST = "Pentest"
	SCANNER = "Scanner"
	SCAN = "Scan"
	PLUGIN = "Plugin"
	RULE = "Rule"


class ACTION(EnumChoices):
	ADD = "Add"
	UPDATE = "Update"
	DELETE = "Delete"
	EXECUTE = "Execute"
	TERMINATE = "Terminate"	


class TEMPLATE_TYPE(EnumChoices): 
	HTML = "HTML"
	TEXT = "Text"


class AUTHENTICATION_TYPE(EnumChoices): 
	REST_API = "Rest API"
	WEBSOCKET = "Websocket"


class EmailTemplate(models.Model):
	"""
	Email templates get stored in database so that admins can
	change emails on the fly.
	"""
	TemplateID = models.BigAutoField(primary_key=True)
	TemplateKey = models.CharField(max_length=255, unique=True, db_index=True) # unique identifier of the email template
	TemplateType = models.CharField(blank=False, unique=False, choices=TEMPLATE_TYPE.choices(), max_length=100)
	Subject = models.CharField(max_length=255, blank=False)
	Template = models.TextField(blank=False)


	def __str__(self):
		return f"<{self.TemplateKey}> {self.Subject}"


	class Meta:
		db_table = 'EmailTemplate'
		managed = True
		

	def get_rendered_template(self, templateObj, context):
		return self.get_template(templateObj).render(context)


	def get_template(self, templateObj):
		return template.Template(templateObj)


	def get_subject(self, Subject, context):
		return Subject or self.get_rendered_template(self.Subject, context)


	def get_body(self, body, context):
		return body or self.get_rendered_template(self._get_body(), context)


	def _get_body(self):
		return self.Template


class ErrorLogs(models.Model):
	LogID = models.BigAutoField(primary_key=True)
	Application = models.CharField(blank=False,max_length=100)
	FunctionName = models.CharField(blank=False,max_length=100)
	Logs = models.TextField(blank=False)
	RequestData = models.TextField(blank=True)
	CreatedDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "ErrorLogs"
		managed = True

	def __str__(self) -> str:
		return f"{self.Application} | {self.FunctionName}"


class AuditLogs(models.Model):
	"""
	Audit logs contain user activities and only admins can see this data
	"""
	LogID = models.BigAutoField(primary_key=True)
	User = models.ForeignKey(UserModels.User, db_column="email", on_delete=DO_NOTHING)
	Activity = models.CharField(blank=False, unique=False, choices=ACTIVITIES.choices(), max_length=100)
	Action = models.CharField(blank=False, unique=False, choices=ACTION.choices(), max_length=100)
	Message = models.TextField(blank=False, unique=False)
	CreatedDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "AuditLogs"
		managed = True

	def __str__(self) -> str:
		return f"{self.Action} | {self.Activity} | {self.Organization.OrganizationName}"


class IPBlacklist(models.Model):
	"""
	Audit logs contain user activities and only admins can see this data
	"""
	ID = models.BigAutoField(primary_key=True)
	User = models.ForeignKey(UserModels.User, db_column="UserID", on_delete=models.CASCADE)
	IPAddress = models.CharField(blank=False, null=False, unique=False, max_length=200)
	AuthType = models.CharField(blank=False, choices=AUTHENTICATION_TYPE.choices(), max_length=200)
	Attempt = models.PositiveIntegerField(default=1)
	Blocked = models.BooleanField(default=False)
	BlockTime = models.DateTimeField(blank=True, null=True)
	CreatedDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "IPBlacklist"
		verbose_name_plural = "IP Blacklist DB" # NOTE: To changing name in admin panel
		managed = True

	def __str__(self) -> str:
		return f"{self.User.email} | {self.IPAddress} | {self.Organization.OrganizationName}"