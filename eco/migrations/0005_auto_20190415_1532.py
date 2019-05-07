# Generated by Django 2.1.7 on 2019-04-15 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco', '0004_auto_20190414_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=256)),
                ('first_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='diy_files',
            field=models.FileField(default='settings.MEDIA_ROOT/kit.jpg', upload_to='kit/%Y/%m/%D'),
        ),
    ]
