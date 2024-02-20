from django.urls import path
from .views import *

urlpatterns = [
    # path("chatbot/", chatbot_view, name="chat"),
    path("ask_question/", ask_question, name="ask_question"),
    # path('get_conversation_history/', get_conversation_history, name='get_conversation_history'),
    path('chatbot/', chatbot_view, name='chatbot'),
    # path('chatbot/history/', get_chat_history, name='chatbot_history'),
    # path('chatbot/start/', start_new_conversation, name='chatbot_start'),
    # path('chatbot/clear/', clear_chat_history, name='chatbot_clear'),
    
]
