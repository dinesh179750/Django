from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .birthday import birthday_art, next_birthday
from .forms import ContactForm
from .models import Contact

def contact_list(request):
    query = request.GET.get("q", "").strip()
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(company__icontains=query)
        )
    return render(request, "contacts/contact_list.html", {"contacts": contacts, "query": query})

def home(request):
    return render(request, "contacts/home.html")

def about(request):
    return render(request, "contacts/about.html")

def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f"{contact.full_name} was added successfully.")
            return redirect("contact_detail", pk=contact.pk)
    else:
        form = ContactForm()
    return render(request, "contacts/contact_form.html", {"form": form, "page_title": "Add a contact", "button_text": "Save contact"})

def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    birthday, days = next_birthday(contact.date_of_birth)
    art = birthday_art(days)
    return render(request, "contacts/contact_detail.html", {
        "contact": contact, "birthday": birthday, "days_remaining": days, "birthday_art": art,
    })

def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact details updated.")
            return redirect("contact_detail", pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/contact_form.html", {"form": form, "page_title": "Edit contact", "button_text": "Update contact"})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        name = contact.full_name
        contact.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("contact_list")
    return render(request, "contacts/contact_confirm_delete.html", {"contact": contact})
