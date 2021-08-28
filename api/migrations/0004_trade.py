# Generated by Django 3.0 on 2021-08-28 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_copy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')], default='pending', max_length=255)),
                ('copy_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copy_from+', to='api.Copy')),
                ('copy_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copy_to_receiver', to='api.Copy')),
            ],
        ),
    ]
