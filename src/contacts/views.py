from django.shortcuts import render
from .forms import EmailPostForm

def contact(request):
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Form fields passed validation
            cd = form.cleaned_data

    else:
        form = EmailPostForm()
    return render(request, 'contacts/contact.html', {'form': form})
