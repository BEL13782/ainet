# Generated by Django 2.0.3 on 2018-03-23 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('ref', models.IntegerField()),
                ('maker', models.CharField(max_length=20)),
                ('resolution', models.CharField(max_length=15)),
                ('IP', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('website', models.URLField()),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=60)),
                ('state_province', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AINET.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('image', models.ImageField(upload_to=None)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AINET.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AINET.Site')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='Snapshot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AINET.Snapshot'),
        ),
        migrations.AddField(
            model_name='camera',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AINET.Zone'),
        ),
    ]
