from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from demande.models import DemandeActe, Acte
from agent.models import Service
from django.contrib import messages

from datetime import datetime

# Create your views here.
def guest_home(request):
    """Render the home page."""
    if request.user.is_authenticated:
        # If the user is authenticated, you might want to render a different template
        return render(request, 'index.html', {'user': request.user})
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
        if request.method == 'POST':
            acte_id = request.POST.get('acte')
            numActe = request.POST.get('numActe')
            numRegis = request.POST.get('numRegis')
            numCopie = request.POST.get('copie')

            acte = Acte.objects.get(id=acte_id)
            service = Service.objects.get(id=1)

            DemandeActe.objects.create(
                people=request.user.people,
                acte=acte,
                numActeDem=numActe,
                numRegisDem=numRegis,
                numberCopieDem=numCopie,
                dateEnvDem=datetime.now(),
                stateDem='waiting',
                suiviDem='in progress',
                service=service
            )

            messages.success(request, "demande envoyé avec succès !.")
            return redirect('demandelist')  
        return render(request, 'html/people/demandedetailpeople.html',{'user': request.user,'action':action,'actes':actes})  # Update with your actual template path

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

        acte = Acte.objects.get(id=acte_id)
        service = demande.service  # Keep the same service as before

        # Update the existing demand
        demande.acte = acte
        demande.numActeDem = numActe
        demande.numRegisDem = numRegis
        demande.numberCopieDem = numCopie
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
