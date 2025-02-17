from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from agent.models import Service
from demande.models import Acte, DemandeActe
from notification.models import Notification
from people.models import People


# Create your views here.
def guest_home(request):
    """Render the home page."""
    if request.user.is_authenticated:
        # If the user is authenticated, you might want to render a different template
        user = request.user
        if hasattr(user, 'people'):
            return render(request, 'index.html', {'user': request.user})
        elif user.agents:
            return redirect('dashboard')
        else:
            return redirect('admin')

    return render(request, 'index.html')

def guest_about(request):
    """Render the about page."""
    if request.user.is_authenticated:
        # If the user is authenticated, you might want to render a different template
        return render(request, 'html/about.html', {'user': request.user})
    return render(request, 'html/about.html')

def guest_contact(request):
    """Render the contact page."""
    if request.user.is_authenticated:
        # If the user is authenticated, you might want to render a different template
        return render(request, 'html/contact.html', {'user': request.user})
    return render(request, 'html/contact.html')

@login_required
def demand_list(request):
    """Render the demand list page."""
    demandes = DemandeActe.objects.filter(people=request.user.people)  # Assuming 'people' is a related model to User
    return render(request, 'html/people/demandelistpeople.html', {'user': request.user, 'demandes': demandes})

@login_required
def add_demand(request):
    """Render the add demand page."""
    if request.user.is_authenticated:
        action = 'add'
        actes = Acte.objects.all()

        error_fields=[]
        if request.method == 'POST':
            acte_id = request.POST.get('acte')
            numActe = request.POST.get('numActe')
            numRegis = request.POST.get('numRegis')
            numCopie = request.POST.get('copie')
            fullName = request.POST.get('fullName')
            birthday = request.POST.get('birthday')

            acte = Acte.objects.get(id=acte_id)
            service = Service.objects.get(id=1)

            if not numCopie or not numRegis or not numActe:
                statedem = 'draft'
                suividem = 'none'
                if not numCopie:
                    numCopie = 0
            else:
                statedem = 'waiting'
                suividem = 'in progress'

                Notification.objects.create(
                    user=request.user,
                    title=f'Demande d\'{acte.libelleActe} envoyée',
                    message=f'Votre demande d\'{acte.libelleActe} pour {fullName} a été envoyée avec succès. Veuillez suivre vos notifications pour être à jour',
                )

            if numCopie and int(numCopie) <= 0:
                error_fields.append('numCopie')
                return render(request, 'html/people/demandedetailpeople.html',{'user': request.user,'action':action,'actes':actes,'error_fields':error_fields})

            DemandeActe.objects.create(
                people=request.user.people,
                acte=acte,
                numActeDem=numActe,
                numRegisDem=numRegis,
                nomConcerneDem=fullName,
                dateNaissDem=birthday,
                numberCopieDem=numCopie,
                dateEnvDem=datetime.now(),
                stateDem=statedem,
                suiviDem=suividem,
                service=service
            )

            messages.success(request, "demande envoyé avec succès !.")
            return redirect('demandelist')
        return render(request, 'html/people/demandedetailpeople.html',{'user': request.user,'action':action,'actes':actes,'error_fields':error_fields})  # Update with your actual template path

@login_required
def edit_demand(request, idDem):
    """Handle editing an existing demand."""
    demande = get_object_or_404(DemandeActe, idDem=idDem)  # Retrieve the demand by ID
    action = 'edit'
    actes = Acte.objects.all()  # Fetch all available actes for the dropdown

    if request.method == 'POST':
        acte_id = request.POST.get('acte')
        numActe = request.POST.get('numActe')
        numRegis = request.POST.get('numRegis')
        numCopie = request.POST.get('copie')
        fullname = request.POST.get('fullname')
        birthday = request.POST.get('birthday')

        acte = Acte.objects.get(id=acte_id)

        if demande.stateDem == 'draft':
            if numCopie and numActe and numRegis:
                demande.stateDem = 'waiting'
                demande.suiviDem = 'in progress'

                Notification.objects.create(
                    user=request.user,
                    title=f'Demande d\'{acte.libelleActe} envoyée',
                    message=f'Votre demande d\'{acte.libelleActe} pour {fullname} a été envoyée avec succès. Veuillez suivre vos notifications pour être à jour',
                )

        # Update the existing demand
        demande.acte = acte
        demande.numActeDem = numActe
        demande.numRegisDem = numRegis
        demande.numberCopieDem = numCopie
        demande.nomConcerneDem = fullname
        demande.dateNaissDem = birthday
        demande.save()  # Save the updated demand

        messages.success(request, "Demande modifiée avec succès.")
        return redirect('demandelist')  # Redirect to the demand list

    return render(request, 'html/people/demandedetailpeople.html', {
        'user': request.user,
        'action': action,
        'actes': actes,
        'demande': demande  # Pass the existing demand to the template
    })

@login_required
def show_demand(request, idDem):
    """Display the details of a specific demand."""
    demande = get_object_or_404(DemandeActe, idDem=idDem)  # Retrieve the demand by ID
    action = 'show'  # Indicate that this is a show action
    actes = Acte.objects.all()  # Fetch all available actes for the dropdown (if needed)

    return render(request, 'html/people/demandedetailpeople.html', {
        'user': request.user,
        'action': action,
        'actes': actes,
        'demande': demande  # Pass the existing demand to the template
    })

@login_required
def profile_user(request):
    """Display the profile"""

    person = People.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=request.user)

    return render(request, 'html/people/profilpeople.html', {
        'person': person,
        'count_notify': notifications.count(),
    })

@login_required
def edit_profile(request):
    """Edit the user profile"""
    person = People.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        address = request.POST.get('address')

        user.first_name = prenom
        user.last_name = nom
        user.email = email
        user.save()

        person.addressPeople = address
        person.telPeople = tel
        person.save()

        return redirect('profile_view')


@login_required
def notif_user(request):
    """Display the notifications of the user"""

    notifications = Notification.objects.filter(user=request.user)

    return render(request, 'html/people/notifpeople.html', {
        'user': request.user,
        'notifications':notifications,
        'count_notify':notifications.count(),
    })
