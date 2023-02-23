from django.contrib import admin
from .models import EmailTemplate, ErrorLogs, AuditLogs, IPBlacklist


class EmailAdmin(admin.ModelAdmin):
	list_display = ('TemplateKey', 'Subject', 'TemplateID', 'TemplateType')
	search_fields = ('TemplateKey', 'Subject')


class Logs(admin.ModelAdmin):
	list_display = ('Application', 'FunctionName', 'Logs', 'RequestData', 'CreatedDate')
	readonly_fields = ('Application', 'FunctionName', 'Logs', 'RequestData', 'CreatedDate')
	search_fields = ('Application', 'FunctionName', 'CreatedDate')


class Audit(admin.ModelAdmin):
	model = AuditLogs
	list_display = ("Activity", "User", "Action", "CreatedDate", "Message")
	list_display_links = ("Activity",)
	search_fields = ("User__email", "Message")
	readonly_fields = ("User", "Action", "Activity", "Message", "CreatedDate")
	list_filter = ("User__email", "Action", "Activity", "CreatedDate")
	exclude = ("LogID",)

	fieldsets = (
		("AdministrativeDetails", {"fields": ("User", "CreatedDate")}),
		("ActivityDetails", {"fields": ("Action", "Activity", "Message")})        
	)


class IPBlacklistPanel(admin.ModelAdmin):
	model = IPBlacklist
	list_display = ("User", "ID", "IPAddress", "AuthType", "Attempt", "Blocked", "BlockTime")
	list_display_links = ("User",)
	search_fields = ("User__email", "IPAddress")
	readonly_fields = ("ID", "CreatedDate")
	list_filter = ("AuthType", "Blocked")
	
	fieldsets = (
		("AdministrativeDetails", {"fields": ("User", "CreatedDate")}),
		("AuthenticationDetails", {"fields": ("IPAddress", "AuthType", "Attempt", "Blocked", "BlockTime")})
	)


admin.site.register(EmailTemplate, EmailAdmin)
admin.site.register(ErrorLogs, Logs)
admin.site.register(AuditLogs, Audit)
admin.site.register(IPBlacklist, IPBlacklistPanel)