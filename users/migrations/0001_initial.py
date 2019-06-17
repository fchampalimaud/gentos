# Generated by Django 2.1.8 on 2019-06-17 15:30

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
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('short_name', models.CharField(blank=True, max_length=20)),
                ('logo', models.ImageField(blank=True, help_text='recommended size 220x40 px', upload_to='institution')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_responsible', models.BooleanField(default=False, verbose_name='responsible')),
                ('is_manager', models.BooleanField(default=False, verbose_name='manager')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='users.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Institution'),
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(through='users.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
