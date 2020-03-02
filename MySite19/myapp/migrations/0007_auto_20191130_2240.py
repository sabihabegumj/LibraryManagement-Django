# Generated by Django 2.2.5 on 2019-12-01 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/book/'),
        ),
        migrations.AddField(
            model_name='member',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/member/'),
        ),
    ]
