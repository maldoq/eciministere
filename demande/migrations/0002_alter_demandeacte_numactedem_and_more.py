# Generated by Django 5.1.5 on 2025-01-26 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandeacte',
            name='numActeDem',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='demandeacte',
            name='numRegisDem',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='demandeacte',
            name='numberCopieDem',
            field=models.SmallIntegerField(null=True),
        ),
    ]
