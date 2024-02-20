from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from configparser import ConfigParser
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect

from django.urls import reverse
from django.conf import settings
import google.generativeai as genai

from .models import ChatBot
from django.views.decorators.http import require_POST
from django.core.cache import cache

# Create your views here.

# config = ConfigParser()
# api_key =  settings.GOOGLE_GEMINI_API_KEY

# # first_message = 'Primer mensaje'
# # second_message = 'Segundo mensaje'
# # third_message = 'Tercer mensaje'
# # fourth_message = 'Cuarto mensaje'

# # @csrf_protect
# # def chatbot_view(request):
# #     """
# #     Renderiza la interfaz del chatbot y gestiona las interacciones del usuario.
# #     """

# #     api_key = settings.GOOGLE_GEMINI_API_KEY

# #     if request.method == 'POST':
# #         message = request.POST.get('message')
# #         if message:
# #             # Verificar el token CSRF (ya se realiza automáticamente por la decoración `@csrf_protect`)
# #             try:
# #                 chatbot = ChatBot(api_key=api_key)
# #                 response = chatbot.send_prompt(message)
# #                 return JsonResponse({'response': response})
# #             except genai.errors.GenaiException as e:
# #                 return HttpResponseBadRequest(f"Error: {e}")
# #             except Exception as e:
# #                 return HttpResponseBadRequest(f"Unexpected error: {e}")

# #     context = {
# #         'title': 'ChatBot AI',
# #         'chatbot_name': ChatBot.CHATBOT_NAME,
# #         'first_message': first_message,
# #         'second_message': second_message,
# #         'third_message': third_message,
# #         'fourth_message': fourth_message,
# #     }
# #     return render(request, 'chatbot/chatbot.html', context)


# # def get_conversation_history(request):
# #     """
# #     Recupera el historial de conversaciones de chat si está autenticado.
# #     """

# #     if request.user.is_authenticated:
# #         # Implement logic to retrieve conversation history from database or other source
# #         # Use appropriate authentication and authorization checks
# #         conversation_history = []  # Placeholder
# #         return JsonResponse({'conversation_history': conversation_history})
# #     else:
# #         return HttpResponseBadRequest("Unauthorized access")
        

# # # ========
# # def main():
# #     config = ConfigParser()
# #     api_key =  settings.GOOGLE_GEMINI_API_KEY
    
# #     chatbot = ChatBot(api_key = api_key)
# #     chatbot.start_conversation()
    
# #     # chatbot.clear_conversation()
    
# #     while True:
# #         user_input = input("You: ")
# #         if user_input.lower == 'quit':
# #             print("Existing Chatbot")

# #         try:
# #             response = chatbot.send_prompt(user_input)
# #             print(f"{chatbot.CHATBOT_NAME}: {response}")
# #         except Exception as e:
# #             print(f"Error: {e}")
    

# def chatbot_view(request):
#     """Maneja las interacciones del chatbot y renderiza la plantilla."""
#     error_message = None
#     chatbot_response = None
#     history = []  # Lista para el historial de chat

#     # Obtener el chatbot de la caché o crearlo
#     chatbot = cache.get("chatbot_instance")
#     if chatbot is None:
#         try:
#             chatbot = ChatBot(settings.GOOGLE_GEMINI_API_KEY)
#             chatbot.start_conversation()
#             cache.set("chatbot_instance", chatbot, timeout=900)  # Almacenar en caché por 15 minutos
#         except Exception as e:
#             error_message = f"Error al crear chatbot: {e}"
#             return render(request, 'chatbot/chatbot.html', {'error_message': error_message})

#     # Procesar solicitudes POST (mensajes de usuario)
#     if request.method == 'POST':
#         try:
#             user_message = request.POST.get('message')
#             chatbot_response = chatbot.send_prompt(user_message)

#             # Agregar mensaje de usuario y respuesta del bot al historial
#             history.append({'role': 'user', 'text': user_message})
#             history.append({'role': 'chatbot', 'text': chatbot_response})
#         except GeniAIException as e:
#             error_message = f"Error al enviar prompt: {e}"
#         except AttributeError as e:
#             # Manejar el error de atributo de forma específica
#             if hasattr(e, 'message'):
#                 error_message = f"Error inesperado: {e.message}"
#             else:
#                 error_message = "Error inesperado: 'AttributeError' sin mensaje"
#         except Exception as e:
#             error_message = f"Error desconocido: {e.__class__.__name__}"

#     else:
#         # Mensaje inicial de bienvenida
#         chatbot_response = "Hola! ¿En qué puedo ayudarte hoy?"

#     # Renderizar la plantilla con contexto
#     context = {
#         'chatbot_name': ChatBot.CHATBOT_NAME,
#         'chatbot_response': chatbot_response,
#         'chat_history': history,
#         'error_message': error_message,
#     }

#     return render(request, 'chatbot/chatbot.html', context)

# # @require_POST
# def get_chat_history(request):
#   """Recupera y devuelve el historial de conversaciones en formato JSON."""
#   try:
#     chatbot = ChatBot(settings.GOOGLE_GEMINI_API_KEY)
#     history = chatbot.history
#   except Exception as e:
#     return JsonResponse({'error': f"Error al recuperar el historial: {e}"})
#   return JsonResponse({'history': history})

# def start_new_conversation(request):
#   """Inicia una nueva conversación y redirige a la página del chatbot."""
#   try:
#     chatbot = ChatBot(settings.GOOGLE_GEMINI_API_KEY)
#     chatbot.start_conversation()
#   except Exception as e:
#     error_message = f"Error al iniciar la conversación: {e}"
#     return render(request, 'chatbot.html', {'error_message': error_message})
#   return HttpResponseRedirect(reverse('chatbot'))

# def clear_chat_history(request):
#   """Borra el historial de conversaciones y redirige a la página del chatbot."""
#   try:
#     chatbot = ChatBot(settings.GOOGLE_GEMINI_API_KEY)
#     chatbot.clear_conversation()
#   except Exception as e:
#     error_message = f"Historial de eliminación de errores: {e}"
#     return render(request, 'chatbot/chatbot.html', {'error_message': error_message})
#   return HttpResponseRedirect(reverse('chatbot'))

# add here to your generated API key
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

# @login_required
def ask_question(request):
    if request.method == "POST":
        text = request.POST.get("text")
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        response = chat.send_message(text)
        user = request.user
        ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)
        # Extract necessary data from response
        response_data = {
            "text": response.text,  # Assuming response.text contains the relevant response data
            # Add other relevant data from response if needed
        }
        return JsonResponse({"data": response_data})
    else:
        return HttpResponseRedirect(
            reverse("chat")
        )  # Redirect to chat page for GET requests


@login_required
def chatbot_view(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chatbot/chatbot.html", {"chats": chats})