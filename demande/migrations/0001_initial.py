# Generated by Django 5.1.5 on 2025-01-17 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelleActe', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DemandeActe',
            fields=[
                ('idDem', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('numRegisDem', models.CharField(max_length=40)),
                ('numActeDem', models.CharField(max_length=40)),
                ('numberCopieDem', models.SmallIntegerField(default=0)),
                ('dateEnvDem', models.DateTimeField()),
                ('stateDem', models.CharField(choices=[('draft', 'Brouillon'), ('waiting', 'En attente'), ('running', 'En cours'), ('completed', 'Terminé'), ('rejected', 'Rejeté')], max_length=30)),
                ('suiviDem', models.CharField(choices=[('none', 'Pas de suivi'), ('in progress', 'En progression'), ('ready', 'Prêt'), ('stopped', 'Interrompu')], max_length=30)),
                ('dateAjout', models.DateTimeField(auto_now_add=True)),
                ('dateModif', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('acte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='demande.acte')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='people.people')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes', to='agent.service')),
            ],
        ),
    ]
