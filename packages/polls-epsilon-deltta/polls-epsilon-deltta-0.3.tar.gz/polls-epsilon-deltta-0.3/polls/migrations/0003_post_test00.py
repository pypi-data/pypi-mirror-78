# Generated by Django 3.1 on 2020-08-25 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200826_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_test00',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField()),
                ('body', models.TextField()),
            ],
            options={
                'db_table': 'music_ablbum',
            },
        ),
    ]
