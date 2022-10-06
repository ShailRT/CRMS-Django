from turtle import heading
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign, OpsUser, Heap, LeadFile, ClientUser, UploadFile
from itertools import chain
import csv 
from django.http import HttpResponse
import os 
from django.conf import settings
from datetime import datetime

# Create your views here.
@login_required(login_url='signin')
def index(request):
    ops_user = OpsUser.objects.filter(user=request.user).first()
    campaign_list = Campaign.objects.filter(user=ops_user)

    context = {
        'campaign_list': campaign_list,
        'lencamp': len(campaign_list)
    }
    return render(request, 'html/index.html', context)

@login_required(login_url='signin')
def push(request, pk):
    ops_user = OpsUser.objects.filter(user=request.user).first()
    camp_object = Campaign.objects.filter(user=ops_user, camp_name=pk).first()
    qty = request.GET.get('quantity')
    leads = Heap.objects.filter(city=camp_object.city, course=camp_object.course)[:(int(qty))]
    headings = ['Name','Phone', 'Course', 'City']
    uuids = ""
    for lead in leads:
        uuids+=f"{lead.lead_id} "
    return render(request, 'push.html', {'leads': leads, 'headings': headings, 'camp_object': camp_object, 'uuids': uuids})


@login_required(login_url='signin')
def campaign(request,pk):
    camp = Campaign.objects.filter(camp_name=pk).first()
    lead_list = LeadFile.objects.filter(campaign = camp)
    context={
        'campaign': camp,
        'lead_list': lead_list
    }

    return render(request, 'campaign.html', context)

@login_required(login_url='signin')
def push_history(request):
    uuid = request.GET.get('uuid')
    lead_object = LeadFile.objects.filter(lead_id=uuid).first()
    headings = []
    row = []
    with open(lead_object.leads.path, 'r') as f:
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
    }
    return render(request, 'push-history.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Creds Invalid')
            return redirect('signin')
    else:
        return render(request, 'html/auth-login-basic.html')
        
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def table(request):
    # leads = []
    # headings = []
    # user = OpsUser.objects.get(user=request.user)
    # if user.campaign.first():
    #     camp_name = user.campaign.first().camp_name
    #     lead = Campaign.objects.get(camp_name=camp_name)
    #     counter = 0
    #     with open(f'{lead.file.path}', 'r') as file:
    #         csvreader = csv.reader(file)
    #         for row in csvreader:
    #             if counter == 0:
    #                 headings += row
    #             else:
    #                 leads.append(row)
    #             counter+=1
    headings = ['Name','Phone', 'Course', 'City']
    ops_object = OpsUser.objects.filter(user=request.user).first()
    campaign = Campaign.objects.filter(user=ops_object, camp_name='camp1').first()
    filter_leads = Heap.objects.filter(course=campaign.course, city=campaign.city)
    leads = filter_leads

    return render(request, 'html/tables-basic.html',{'headings': headings, 'leads': leads})

@login_required(login_url='signin')
def create_lead(request, pk):
    if request.method=="POST":
        user_object = OpsUser.objects.filter(user=request.user).first()
        camp_object = Campaign.objects.filter(user=user_object, camp_name=pk).first()
        uuids = request.POST['uuids']
        uuids = uuids.split()
        lead_object = []
        for id in uuids:
            lead = Heap.objects.filter(lead_id=id).first()
            lead_object.append([lead.name, lead.phone, lead.course, lead.city])
         
        headings = ['Name','Phone', 'Course', 'City']
        now = datetime.now()

        current_time = now.strftime("%H-%M")
        path = os.path.join(settings.MEDIA_ROOT, f'{request.user.username}-{camp_object.camp_name}-{current_time}.csv')
        with open(path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows(lead_object)
        
        new_lead = LeadFile.objects.create(campaign=camp_object, leads=path, quantity=len(lead_object))
        new_lead.save()
        for uuid in uuids:
            delete_lead = Heap.objects.filter(lead_id=uuid).first()
            delete_lead.delete()
        
        
        return redirect('home')
        
@login_required(login_url='signin')
def camp_create(request):
    if request.method == "POST":
        ops_user = OpsUser.objects.filter(user=request.user).first()
        client_user = ClientUser.objects.filter(user=request.user).first()
        camp_name = request.POST['name']
        course = request.POST['course']
        city = request.POST['city']
        quantity = request.POST['quantity']

        new_camp = Campaign.objects.create(user=ops_user, client=client_user, camp_name=camp_name, course=course, city=city, quantity=quantity)
        new_camp.save()
        return redirect('home')
        
    else:
        return redirect('home')

def heap_upload(request):
    headings = ['Name','Phone', 'Course', 'City']

    if request.method == "POST":
        csv_file = request.FILES.get('csv-upload')
        file_object = UploadFile.objects.create(upload=csv_file)
        save_uuid = file_object.upload_id
        file_object.save()
        file_object = UploadFile.objects.filter(upload_id=save_uuid).first()
        exist_count = 0
        create_count = 0
        exist_uuid = []
        with open(file_object.upload.path, 'r') as f:
            csv_reader = csv.reader(f)
            counter=0
            for row in csv_reader:
                if counter==0:
                    headings=row
                else:
                    if Heap.objects.filter(name=row[0], phone=row[1], course=row[2], city=row[3]).exists():
                        exist_count+=1
                        temp = Heap.objects.filter(name=row[0], phone=row[1], course=row[2], city=row[3]).first()
                        exist_uuid.append(temp.lead_id)
                    else:
                        heap_obj = Heap.objects.create(name=row[0], phone=row[1], course=row[2], city=row[3])
                        heap_obj.save()
                        create_count+=1
                counter+=1

        lead_list = Heap.objects.all()
        leads = []
        for lead in lead_list:
            leads.append([lead.name, lead.phone, lead.course, lead.city])
    

        context = {
            'headings': headings,
            'leads': leads,
            'exist': exist_count,
            'created': create_count,
            'exist_uuid': exist_uuid
        }
        return render(request, 'heap-push.html', context)



    lead_list = Heap.objects.all()
    leads = []
    for lead in lead_list:
        leads.append([lead.name, lead.phone, lead.course, lead.city])
    
    context = {
        'headings': headings,
        'leads' : leads,
    }


    return render(request, 'heap-push.html', context)