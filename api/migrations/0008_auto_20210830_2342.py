# Generated by Django 3.0 on 2021-08-30 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210830_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copy',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='api.Book'),
        ),
    ]