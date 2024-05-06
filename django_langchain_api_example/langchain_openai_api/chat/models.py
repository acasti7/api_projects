from django.db import models
from django.contrib.auth.models import User

##
##Django’s Object-Relational Mapping (ORM) layer, which provides a high-level API for database interaction.


# Create your data models here.
###-User (pk->id)
#####Built In Data Model with multiple fields e.g., id, username, password, groups, email, is_active,
###-Conversation (pk->id, fk->User.id) --> note "id" is an autogenerated field
###-ChatMessage (pk->id, fk->Conversation.id)  --> since no primary key is explicitly defined in the "Conversation" model, Django automatically creates an id field which acts as the primary key. So, the conversation ForeignKey in ChatMessage essentially points to this id field of the Conversation model.

class Conversation(models.Model):
    ## Data Model for convsersation, links User to Chat Message
    # --Implicit `id = models.AutoField(primary_key=True)` added by Django--
    
    # store the title of the conversation
    # Indexes: Since the title field is marked as unique, Django automatically creates an index for this field, which can improve lookup performance.
    title = models.CharField(max_length=100, unique=True)

    # create user id field which crossreferences the conversation model to the build in user model currently being used in authentication step
    # 'on_delete', enforces constraint when the associated user is deleted, then related conversations should also be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # '__str__' is a django method to define the default human-readable representation
        return f"{self.user}:{self.title}"
    
    ''' USAGE 
    # Creating a new user
    user = User.objects.create_user('john_doe', 'john@example.com', 'johndoepassword')

    # Creating a new conversation associated with the user
    conversation = Conversation.objects.create(title='Project Discussion', user=user)

    # Printing the conversation
    print(conversation)  # Output: john_doe:Project Discussion
    '''

class ChatMessage(models.Model):
    ## Data Model for Chat Message, connects to Conversation
    ## Explicitly generate id field (note this may be good )
    id = models.AutoField(primary_key=True)

    ## Establish many-to-one relationship with Conversation
    conversation = models.ForeignKey(Conversation, default=None, on_delete=models.CASCADE)

    ## store responses from user
    user_response = models.TextField(null=True, default ='')

    ## store responses from ai
    ai_response = models.TextField(null=True, default='')

    ## store date and time when each message was created
    ### Leverages django function which Automatically sets the field to the date and time when the message is first created.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation}: {self.id}"

    ''' Usage
    # Assuming 'conversation' is an instance of Conversation model
    new_message = ChatMessage.objects.create(
        conversation=conversation,
        user_response="Hello, how are you?",
        ai_response="I'm good! How can I assist you today?",
    )
    print(new_message)  # Output might be "ConversationTitle: 1" assuming the message ID is 1
    '''