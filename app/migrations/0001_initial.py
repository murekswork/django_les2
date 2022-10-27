# Generated by Django 4.1.2 on 2022-10-26 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Product', max_length=100)),
                ('price', models.FloatField(default=99999)),
                ('value', models.IntegerField(default=0)),
                ('rating', models.FloatField(default=5)),
                ('description', models.CharField(default='No description', max_length=1024)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
    ]
