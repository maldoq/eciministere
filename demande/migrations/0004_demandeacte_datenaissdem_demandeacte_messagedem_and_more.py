# Generated by Django 5.1.5 on 2025-02-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0003_demandeacte_message_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandeacte',
            name='dateNaissDem',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='demandeacte',
            name='messageDem',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='demandeacte',
            name='nomConcerneDem',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
