# Generated by Django 3.2.9 on 2021-12-10 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('care_always_api', '0003_auto_20211210_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='care_always_api.appointment'),
        ),
    ]
