from __future__ import division
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Thing
from .forms import ThingForm

def top(request):
    number_of_things = Thing.objects.count()
    """
    Display an item IFF it has been compared a number of times equivalent to display_wall.
    This prevents things like:  once-compared items from showing up with a current_score 
    of 1.0 or 0.
    Thought:  The smaller the set of data, the more important it could be to keep track
        of how many *unique* comparisons have been done; i.e. how many *different*
        items something has been compared to.
    """
    display_wall = number_of_things * 0.2

    things = Thing.objects.order_by('-current_score').filter(
        Q(times_defeated__gt = display_wall) |
        Q(times_won__gt = display_wall)
    )
    return render(request, 'top.html', {
        'things': things,
        'number_of_things': number_of_things,
    })
    
def home(request):
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            thing1 = Thing.objects.get(pk=form.cleaned_data['thing1'])
            thing2 = Thing.objects.get(pk=form.cleaned_data['thing2'])
            
            if '_thing1chosen' in request.POST:
                thing1.times_won = thing1.times_won + 1
                # Impl detail:  Save on peformance by having a field for the current score and not a model property
                # Assumes you have quite a bit more traffic to the list page than the actual voting page
                # Maybe in the real world it's the other way around; I'd have to measure it.
                
                # What % of times does this thing win?
                thing1.current_score = thing1.times_won / (thing1.times_won + thing1.times_defeated)
                
                thing2.times_defeated = thing2.times_defeated + 1
                thing2.current_score = thing2.times_won / (thing2.times_won + thing2.times_defeated)
                
                thing1.save()
                thing2.save()
                
            elif '_thing2chosen' in request.POST:
                thing2.times_won = thing2.times_won + 1
                thing2.current_score = thing2.times_won / (thing2.times_won + thing2.times_defeated)

                thing1.times_defeated = thing1.times_defeated + 1
                thing1.current_score = thing1.times_won / (thing1.times_won + thing1.times_defeated)
                
                thing2.save()
                thing1.save()
                
    try:
        collision = True
        max_tries = 5
        i = 0
        while collision == True and i < max_tries:
            thing1, thing2 = Thing.randoms.random(), Thing.randoms.random()
            if thing1.pk != thing2.pk:
                collision = False
            i = i + 1
        if i == max_tries:
            return HttpResponse("Timeout")
    except ValueError:
        return HttpResponse("There must be at least 2 things in the database.")
    
    form = ThingForm(initial={'thing1': thing1.pk, 'thing2': thing2.pk})
    return render(request, 'home.html', {
        'thing1': thing1,
        'thing2': thing2,
        'form': form
        })
    
class ThingCreate(CreateView):
    model = Thing
    success_url = reverse_lazy('home')
    template_name = 'thing_form.html'