# Generated by Django 4.2.2 on 2023-06-22 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StarkApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='tags',
            field=models.ManyToManyField(related_name='quotes', to='StarkApp.tag'),
        ),
    ]