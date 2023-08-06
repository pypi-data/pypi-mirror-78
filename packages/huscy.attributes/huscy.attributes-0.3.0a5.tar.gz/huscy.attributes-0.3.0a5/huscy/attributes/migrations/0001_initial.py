import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import huscy.attributes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudonym', models.CharField(max_length=128, unique=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('attribute_schema', models.ForeignKey(default=huscy.attributes.models.get_latest_attribute_schema_version, on_delete=django.db.models.deletion.PROTECT, to='attributes.attributeschema')),
            ],
        ),
    ]
