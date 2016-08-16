from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect

from datetime import date

from .models import Slot, Position, Party, Time


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user=user)
        return render(request, 'PartyShiftSchedule/landingPage.html', {'username': username})

    return HttpResponseRedirect('/login_landing')


@login_required(login_url='/login/')
def foo(request):
    user = request.user
    return render(request, 'PartyShiftSchedule/landingPage.html', {'username': user})


def shift_schedule(request):
    next_party = get_next_party()
    positions = Position.objects.all()
    rows = list()

    times = Time.objects.filter(party=next_party)
    rows += [get_schedule_row(time, next_party) for time in times]

    context = {
        'positions': positions,
        'rows': rows
    }
    return render(request, 'PartyShiftSchedule/shift_schedule.html', context)


def get_schedule_row(time, party):
    slots = Slot.objects.filter(time=time)
    positions = Position.objects.filter(party=party)
    row = [time]

    for position in positions:
        pos_slots = slots.filter(position=position)
        row += [pos_slot.user for pos_slot in pos_slots]
        # pad to the right
        row += [''] * (position.pref_users - len(pos_slots))

    return [str(e) for e in row]


def get_next_party():
    # TODO: Get the party from somewhere else. Dropdown menu, if the tool is used for more then one upcoming party?
    next_partys = Party.objects.filter(date__gte=date.today()).order_by('date')
    if len(next_partys) == 0:
        return
    return next_partys[0]