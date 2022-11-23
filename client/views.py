from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from ops.models import Campaign, ClientUser, LeadFile
import csv
from django.contrib.auth.decorators import login_required

def client_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Creds invalid')
            return redirect('client-login')
    else:
        return render(request, 'client-login.html')

@login_required(login_url='client-login')
def dashboard(request):
    client = ClientUser.objects.filter(user=request.user).first()
    campaign = Campaign.objects.filter(client=client)
    context = {
        'campaign_list': campaign,
    }
    
    return render(request, 'dashboard.html', context)

@login_required(login_url='client-login')
def campaign(request, pk):
    camp = Campaign.objects.filter(id=pk).first()
    lead_list = LeadFile.objects.filter(campaign = camp)
    context={
        'campaign': camp,
        'lead_list': lead_list,
        'user': request.user
    }

    return render(request, 'client-campaign.html', context)

@login_required(login_url='client-login')
def lead_pack(request):
    uuid = request.GET.get('uuid')
    lead_pack = LeadFile.objects.filter(lead_id = uuid).first()
    headings = []
    row = []
    with open(lead_pack.leads.path, 'r') as f:
        reader = csv.reader(f)
        counter = 0
        for i in reader:
            counter+=1
            if counter == 1:
                headings+=i
            else:
                row.append(i)

    context = {
        'headings': headings,
        'leads': row,
        'user': request.user,
        'lead_download': lead_pack.leads.url
    }
    return render(request, 'lead-pack.html', context)

@login_required(login_url='client-login')
def client_logout(request):
    auth.logout(request)
    return redirect('client-login')
    

