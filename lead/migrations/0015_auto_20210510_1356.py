# Generated by Django 3.1.4 on 2021-05-10 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0014_auto_20210510_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lead.userprofile'),
        ),
    ]