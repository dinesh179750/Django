
from django.shortcuts import render, redirect
from .models import Agent, Investigate


# ADD AGENT
def add_agent(request):

    if request.method == "POST":

        name = request.POST.get('name')

        Agent.objects.create(name=name)

        return redirect('agent')

    return render(request, 'add_agent.html')


# ADD CASE
def add_case(request):

    agents = Agent.objects.all().order_by('-id')

    if request.method == "POST":

        cid = request.POST.get('id')
        ctype = request.POST.get('type')
        address = request.POST.get('address')
        cname = request.POST.get('cname')
        agent_id = request.POST.get('agent')
        status = request.POST.get('status')
        desc = request.POST.get('desc')

        obj = Agent.objects.get(id=agent_id)

        Investigate.objects.create(
            case_id=cid,
            case_type=ctype,
            loc=address,
            complaint_name=cname,
            assigned_agent=obj,
            case_status=status,
            case_description=desc
        )

        return redirect('list_data')

    context = {
        'agents': agents
    }

    return render(request, 'add_case.html', context)


# LIST ALL CASES
def list_data(request):

    data = Investigate.objects.all()

    context = {
        'data': data
    }

    return render(request, 'case_list.html', context)


# SINGLE CASE DETAILS
def single_data(request, pk):

    data1 = Investigate.objects.get(case_id=pk)

    context = {
        'data1': data1
    }

    return render(request, 'single.html', context)


# EDIT CASE
def edit(request, id):

    data2 = Investigate.objects.get(case_id=id)

    if request.method == "POST":

        data2.case_type = request.POST.get('type')
        data2.loc = request.POST.get('address')
        data2.complaint_name = request.POST.get('cname')
        data2.case_status = request.POST.get('status')
        data2.case_description = request.POST.get('desc')

        data2.save()

        return redirect('list_data')

    context = {
        'data2': data2
    }

    return render(request, 'update.html', context)


# DELETE CASE
def delete_case(request, vk):

    data3 = Investigate.objects.get(case_id=vk)

    data3.delete()

    return redirect('list_data')
