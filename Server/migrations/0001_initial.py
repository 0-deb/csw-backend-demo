# Generated by Django 4.1.6 on 2023-02-14 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('TemplateID', models.BigAutoField(primary_key=True, serialize=False)),
                ('TemplateKey', models.CharField(db_index=True, max_length=255, unique=True)),
                ('TemplateType', models.CharField(choices=[('HTML', 'HTML'), ('TEXT', 'Text')], max_length=100)),
                ('Subject', models.CharField(max_length=255)),
                ('Template', models.TextField()),
            ],
            options={
                'db_table': 'EmailTemplate',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ErrorLogs',
            fields=[
                ('LogID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Application', models.CharField(max_length=100)),
                ('FunctionName', models.CharField(max_length=100)),
                ('Logs', models.TextField()),
                ('RequestData', models.TextField(blank=True)),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ErrorLogs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='IPBlacklist',
            fields=[
                ('ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('IPAddress', models.CharField(max_length=200)),
                ('AuthType', models.CharField(choices=[('REST_API', 'Rest API'), ('WEBSOCKET', 'Websocket')], max_length=200)),
                ('Attempt', models.PositiveIntegerField(default=1)),
                ('Blocked', models.BooleanField(default=False)),
                ('BlockTime', models.DateTimeField(blank=True, null=True)),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(db_column='UserID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'IP Blacklist DB',
                'db_table': 'IPBlacklist',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AuditLogs',
            fields=[
                ('LogID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Activity', models.CharField(choices=[('ASSET', 'Asset'), ('VULN', 'Vulnerability'), ('PENTEST', 'Pentest'), ('SCANNER', 'Scanner'), ('SCAN', 'Scan'), ('PLUGIN', 'Plugin'), ('RULE', 'Rule')], max_length=100)),
                ('Action', models.CharField(choices=[('ADD', 'Add'), ('UPDATE', 'Update'), ('DELETE', 'Delete'), ('EXECUTE', 'Execute'), ('TERMINATE', 'Terminate')], max_length=100)),
                ('Message', models.TextField()),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(db_column='email', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'AuditLogs',
                'managed': True,
            },
        ),
    ]
