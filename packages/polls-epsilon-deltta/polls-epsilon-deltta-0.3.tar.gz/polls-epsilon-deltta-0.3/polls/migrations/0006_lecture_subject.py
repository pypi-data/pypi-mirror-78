# Generated by Django 3.1 on 2020-08-26 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_delete_post_test01'),
    ]

    operations = [
        migrations.CreateModel(
            name='lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=20)),
                ('chapter', models.CharField(max_length=5)),
                ('screen', models.BooleanField()),
                ('time', models.BooleanField()),
                ('quiz', models.BooleanField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('last_num', models.IntegerField()),
                ('done_num', models.IntegerField()),
            ],
        ),
    ]
