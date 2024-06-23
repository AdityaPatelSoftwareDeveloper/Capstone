from django.shortcuts import render,redirect
from django.contrib import messages
from portfolio.models import Contact,Form,Internship
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def home(request):
    return render(request,'home.html')

def skills(request):
    posts=Form.objects.all()
    context={"posts":posts}
    return render(request,'skills.html',context)


def about(request):
    return render(request,'about.html')


def form(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to access this page")
        return redirect("/auth/login/")

    if request.method == "POST":
        fname = request.POST.get('name')
        femail = request.POST.get('email')
        fusn = request.POST.get('usn')
        fcollege = request.POST.get('cname')
        foffer = request.POST.get('offer')
        fstartdate = request.POST.get('startdate')

        # Save the form data to the database
        query = Internship(fullname=fname, usn=fusn, email=femail, college_name=fcollege, offer_status=foffer, start_date=fstartdate)
        query.save()

        # Render the form data to the email template
        template = render_to_string('send_form_email.html', {
            'name': fname,
            'email': femail,
            'usn': fusn,
            'college': fcollege,
            'offer': foffer,
            'startdate': fstartdate,
        })

        # Send the email
        email_message = EmailMessage(
            "New Form Submission",
            template,
            settings.EMAIL_HOST_USER,
            ['jbpatel5244@gmail.com'],
        )
        email_message.content_subtype = 'html'  # Set the content subtype to HTML
        email_message.fail_silently = False
        email_message.send()

        messages.success(request, "Form is Submitted Successfully!")
        return redirect('/form')

    return render(request, 'intern.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'No Subject')  # Adding a default subject in case it's missing
        message = request.POST.get('desc')  # Update this line to match the form field name

        template = render_to_string('send_email.html', {
            'name': name,
            'email': email,
            'message': message,  # Update this line to match the form field name
        })

        email_message = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['jbpatel5244@gmail.com'],
        )
        email_message.content_subtype = 'html'  # Set the content subtype to HTML
        email_message.fail_silently = False
        email_message.send()
        messages.success(request, "Thanks for contacting me. I will get back to you Soon!")

    return render(request, 'contact.html')




