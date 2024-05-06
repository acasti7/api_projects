from django.shortcuts import render
import requests
from .serializers import ChatMessageSerializer, ConversationSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import ChatMessage, Conversation
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
# Create your views here.


llm = OpenAI()

memory = ConversationBufferMemory()

# API for title generator
# API_URL = "http://127.0.0.1:8000/"
# headers = {"Authorization": f"Bearer YOUR_API_TOKEN"}

# def generate_title(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     ## --Added by Andrew
#     # ##handle other instances
#     response_data = response.json()
#     print(response_data)
#     if isinstance(response_data,list) and response_data:
#         return response.json()[0]['generated_text'] #-- orignial code
#     elif isinstance(response_data,dict) and 'generated_text' in response_data:
#         return response_data['generated_text']
    

# retrieving the last 4 conversations from the db for memory efficiency while providing context to model
def retrieve_conversation(title, user):
    # number of conversations
    num_recent_conversations = 4

    # Retrieve the most recent conversation history from the database
    conversation_obj = Conversation.objects.get(title=title,user=user)
    conversation_id = getattr(conversation_obj, 'id')

    # Retrieve recent conversation messages
    conversation_context = ChatMessage.objects.filter(
        conversation_id=conversation_id
    ).order_by('-timestamp')[:num_recent_conversations:-1]

    # Storing the retieved data from db to model memory
    lst =[]
    for msg in conversation_context:
        input_msg = getattr(msg, 'user_response')
        output_msg = getattr(msg, 'ai_response')
        lst.append({"input":input_msg, "output":output_msg})
    
    for x in lst:
        inputs = {"input":x["input"]}
        outputs = {"output":x["output"]}
        memory.save_context(inputs,outputs)
    
    retrieved_chat_history = ChatMessageHistory(
        messages = memory.chat_memory.messages
    )

    return retrieved_chat_history

# function to store new messages to database
def store_message(user_response, ai_response, conversation_id):
    ChatMessage.objects.create(
        user_response=user_response,
        ai_response=ai_response,
        conversation_id=conversation_id,
    )

# function to store conversation to database
def store_title(title,user):
    Conversation.objects.create(
        title=title,
        user=user
    )

# function to get ALL chat history of conversation and create a new chat
@csrf_exempt
@api_view(['POST','GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat(request):
    # get chat history
    if request.method == 'GET':
        request_data = JSONParser().parse(request)
        provided_title = request_data.get('title')
        user = request.user
        if provided_title:
            conversation_title = Conversation.objects.get(
                title=provided_title,
                user=user
            ) # reference model, and get attributes
            conversation_id = getattr(conversation_title,'id')

            #get chat object
            ChatObj = ChatMessage.objects.filter(
                conversation_id=conversation_id
                ).order_by('timestamp')
            Chat = ChatMessageSerializer(ChatObj, many=True)
            return JsonResponse(Chat.data, safe=False)
        else:
            return JsonResponse({'error':'Title not provided'}, status=400)
    
    #create new chat or continue old conversation by providing title
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        prompt = request_data.get('prompt')
        user = request.user
        provided_title = request_data.get('title')
        if provided_title:
            # Create a ChatMessageHistory instance
            retrieved_chat_history = retrieve_conversation(provided_title,user)
            #--andrew added
            title = provided_title
            #--
        else:
            memory.clear()
            retrieved_chat_history = ChatMessageHistory(messages=[])

            # Generate a default title if needed...
            ## may want to use prompts (i.e. the question) to generate the title
            # title = generate_title({
            #     "inputs": prompt
            # })
            title = prompt
            store_title(title,user)

        reloaded_chain = ConversationChain(
            llm=llm,
            memory = ConversationBufferMemory(
                chat_memory=retrieved_chat_history),
                verbose=True
        )

        response = reloaded_chain.predict(input=prompt)

        conversation_title = Conversation.objects.get(title=title, user=user)
        conversation_id = getattr(conversation_title, 'id')
        store_message(prompt, response, conversation_id)

        return JsonResponse({
            'ai_response': response,
            'title':title
        }, status=201)

# Retrieve all conversations of a user (Title only)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_title(request):
    user=request.user
    titles= Conversation.objects.filter(user=user)
    serialized= ConversationSerializer(titles,many=True)
    return JsonResponse(serialized.data, safe=False)

#  Delete a conversation by providing title of conversation
@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_conversation(request):
    user=request.user
    data=JSONParser().parse(request)
    title=data.get('title')
    obj=Conversation.objects.get(user=user, title=title)
    obj.delete()
    return JsonResponse("Deleted successfully", safe=False)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request):
    request_data = JSONParser().parse(request)
    provided_title = request_data.get('title')
    user = request.user
    if provided_title:
        conversation_title = Conversation.objects.get(
            title=provided_title, user=user
        )
        conversation_id = getattr(conversation_title,'id')
        ChatObj = ChatMessage.objects.filter(
            conversation_id=conversation_id
        ).order_by('timestamp')
        return JsonResponse(Chat.data, safe=False)
    else:
        return JsonResponse({'error': 'Title not provided'}, status=400)




