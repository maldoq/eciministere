from django.db import models
from people import models as people_models
from agent import models as agent_models
from django.db.models import Max

from django.utils import timezone


# Define choices for stateDem
STATE_CHOICES = [
    ('draft', 'Brouillon'),
    ('waiting', 'En attente'),
    ('running', 'En cours'),
    ('completed', 'Terminé'),
    ('rejected', 'Rejeté'),
]

# Define choices for suiviDem
SUIVI_CHOICES = [
    ('none', 'Pas de suivi'),
    ('in progress', 'En progression'),
    ('ready', 'Prêt'),
    ('stopped', 'Interrompu'),
]

# Create your models here.
class Acte(models.Model):
    libelleActe = models.CharField(max_length=50)

    def __str__(self):
        return self.libelleActe  # Return a string representation of the Acte

class DemandeActe(models.Model):
    idDem = models.CharField(max_length=40, primary_key=True)
    numRegisDem = models.CharField(max_length=40)  # Corrected CharField
    numActeDem = models.CharField(max_length=40)  # Corrected CharField
    numberCopieDem = models.SmallIntegerField(default=0)
    dateEnvDem = models.DateTimeField()
    stateDem = models.CharField(max_length=30, choices=STATE_CHOICES)  # Added choices
    suiviDem = models.CharField(max_length=30, choices=SUIVI_CHOICES)  # Added choices
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModif = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    acte = models.ForeignKey(Acte, on_delete=models.CASCADE, related_name='demandes')  # Changed to 'demandes'
    people = models.ForeignKey(people_models.People, on_delete=models.CASCADE, related_name='demandes')  # Changed to 'demandes'
    service = models.ForeignKey(agent_models.Service, on_delete=models.CASCADE, related_name='demandes')  # Changed to 'demandes'

    def save(self, *args, **kwargs):
        if not self.idDem:  # Only generate idDem if it hasn't been set
            # Get the current count of demands for the day
            today = timezone.now().date()
            count = DemandeActe.objects.filter(dateAjout__date=today).count() + 1  # Count demands for today
            # Format the idDem
            self.idDem = f"DM-{count:04d}-{today.strftime('%d-%m')}-{timezone.now().strftime('%H-%M')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Demande {self.idDem} - {self.acte.libelleActe}"  # Return a string representation of the DemandeActe