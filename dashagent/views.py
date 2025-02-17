from django.db.models import Count, Q
from django.shortcuts import redirect, render

from demande.models import Acte, DemandeActe
from notification.models import Notification


# Create your views here.
def dashboard(request):
    """Render the dashboard page."""
    if request.user.is_authenticated:
        # If the user is authenticated, you might want to render a different template
        if request.user.agents:
            demande_list_count = DemandeActe.objects.filter(status=True).count()
            demande_list_rejected_count = DemandeActe.objects.filter(Q(status=True) & Q(stateDem='rejected')).count()
            demande_list_completed_count = DemandeActe.objects.filter(Q(status=True) & Q(stateDem='completed')).count()

             # Get the most requested acte
            most_requested_acte = (
                DemandeActe.objects
                .filter(status=True)
                .values('acte__libelleActe')  # Replace 'name' with the actual field name in the Acte model
                .annotate(count=Count('idDem'))  # Count occurrences
                .order_by('-count')  # Order by count descending
                .first()  # Get the first result
            )

            return render(request, 'html/agent/dashboard.html', {'user': request.user, 'total_demande':demande_list_count, 'rejected_demande':demande_list_rejected_count, 'completed_demande':demande_list_completed_count, 'most_requested_acte': most_requested_acte['acte__libelleActe'] if most_requested_acte else 'Aucun acte'})
        else:
            return redirect('admin')

def analyse_list(request):
    """Render the analysis list page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande_list = DemandeActe.objects.filter(Q(status=True) & Q(stateDem='waiting'))
            return render(request, 'html/agent/treatmentlist.html', {'demande_list': demande_list, 'user': request.user, 'action':'analyse'})

def analyse_detail(request, idDem):
    """Render the analysis detail page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande = DemandeActe.objects.get(idDem=idDem)
            actes = Acte.objects.all()

            return render(request, 'html/agent/treatmentdetail.html', {'demande': demande, 'user': request.user, 'action':'analyse', 'actes':actes})

def analyse_validation(request, idDem):
    """Render the analysis validation page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande = DemandeActe.objects.get(idDem=idDem)

            demande.stateDem = 'running'
            demande.suiviDem = 'in progress'
            demande.save()

            Notification.objects.create(
                    user=demande.people.user,
                    title=f'Demande d\'{demande.acte.libelleActe} Validée et en cours de traitement',
                    message=f'Votre demande d\'{demande.acte.libelleActe} pour {demande.nomConcerneDem} a été validé avec succès et est en cours de traitement. Veuillez suivre vos notifications pour être à jour',
                )

            return redirect('analyse_list')

def analyse_rejection(request, idDem):
    """Render the analysis rejection page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande = DemandeActe.objects.get(idDem=idDem)

            demande.stateDem = 'rejected'
            demande.suiviDem = 'stopped'
            demande.save()

            Notification.objects.create(
                    user=demande.people.user,
                    title=f'Demande d\'{demande.acte.libelleActe} rejetée',
                    message=f'Votre demande d\'{demande.acte.libelleActe} pour {demande.nomConcerneDem} a été rejeté faute d\'informations incorrectes. Veuillez reprendre le processus avec les informations adequates',
                )

            return redirect('analyse_list')

def confirmation_list(request):
    """Render the confirmation list page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande_list = DemandeActe.objects.filter(Q(status=True) & Q(stateDem='running'))
            return render(request, 'html/agent/treatmentlist.html', {'demande_list': demande_list, 'user': request.user, 'action':'confirm'})

def confirmation_detail(request, idDem):
    """Render the confirmation detail page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande = DemandeActe.objects.get(idDem=idDem)
            actes = Acte.objects.all()

            return render(request, 'html/agent/treatmentdetail.html', {'demande': demande, 'user': request.user, 'action':'confirm', 'actes':actes})

def historic_list(request):
    """Render the historic list page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande_list =DemandeActe.objects.filter(Q(status=True) & Q(stateDem='completed') | Q(stateDem='rejected'))
            return render(request, 'html/agent/treatmentlist.html', {'demande_list': demande_list, 'user': request.user, 'action':'historic'})

def historic_detail(request, idDem):
    """Render the historic detail page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande = DemandeActe.objects.get(idDem=idDem)
            actes = Acte.objects.all()

            return render(request, 'html/agent/treatmentdetail.html', {'demande': demande, 'user': request.user, 'action':'historic', 'actes':actes})

def confirmation_validation(request, idDem):
    """Render the confirmation validation page."""
    if request.user.is_authenticated:
        if request.user.agents:
            demande = DemandeActe.objects.get(idDem=idDem)

            demande.stateDem = 'completed'
            demande.suiviDem = 'ready'
            demande.save()

            Notification.objects.create(
                    user=demande.people.user,
                    title=f'Demande d\'{demande.acte.libelleActe} prête à être récupérée',
                    message=f'Votre demande d\'{demande.acte.libelleActe} pour {demande.nomConcerneDem} a été finalisé. Veuillez vous rendre au bureau pour la/les récupérer.',
                )

            return redirect('confirmation_list')
