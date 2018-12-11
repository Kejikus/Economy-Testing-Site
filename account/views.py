from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import TestData


def attempts(request):
    raise NotImplementedError()


def result(request):
    raise NotImplementedError()


def register(request):
    context = request.session.pop('context', {})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = TestData.add_record(form)

            request.session['user_data_id'] = new_user.id
            request.session['registered'] = True
            return redirect("testing:testing", permanent=True)
        else:
            context['errors'] = form.errors
    else:
        context.update({
            'form': RegisterForm()
        })

    return render(request, 'register.html', context)
