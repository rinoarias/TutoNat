
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def chatbot_view(request):
    
    return render(
        request = request,
        template_name = "chatbot/chatbot.html",
        context= {
            "title": "Chatbot IA"
        }
    )