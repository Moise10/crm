# Generated by Django 3.1.4 on 2021-05-11 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0021_auto_20210511_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='lead.category'),
        ),
    ]
