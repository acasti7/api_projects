from rest_framework import serializers
from .models import ChatMessage,Conversation

'''
serializers are essential for converting model instances into JSON format for API responses,
 and vice versa, parsing JSON data to create or update model instances based on the API input.

Serialization: Converts ChatMessage objects into JSON format that can be sent to clients.
Deserialization: Parses JSON data to create or update ChatMessage objects, ensuring that data types and constraints (like those enforced by the model's field definitions) are adhered to.


Class Meta Note:
The Meta class in Django models and serializers is a special configuration class that 
holds metadata for the model or serializer it is associated with. It's not an instance 
of the Python meta class concept (used to create classes), but rather a simple convention 
used in Django to configure model or serializer behavior in a contained, organized manner.
'''
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        # every field in the ChatMessage model will be included in the serialization/deserialization processes.
    
class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'
        # every field in the Conversation model will be included in the serialization/deserialization processes.