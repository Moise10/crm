# Generated by Django 3.1.4 on 2021-05-09 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0011_auto_20210509_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lead.userprofile'),
        ),
    ]