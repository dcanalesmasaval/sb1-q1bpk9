from openai import OpenAI
from config import settings
from models import User, Thread, Message, AssistantResponse
from typing import Dict

class AssistantManager:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.users: Dict[str, User] = {}
        self.threads: Dict[str, Thread] = {}

    def get_or_create_thread(self, user_id: str) -> str:
        user = self.users.get(user_id)
        if not user:
            user = User(id=user_id, assistant_id=settings.default_assistant_id)
            self.users[user_id] = user

        if not user.thread_id:
            thread = self.client.beta.threads.create()
            user.thread_id = thread.id
            self.threads[thread.id] = Thread(id=thread.id)

        return user.thread_id

    def send_message(self, user_id: str, message_content: str) -> AssistantResponse:
        thread_id = self.get_or_create_thread(user_id)
        user = self.users[user_id]

        # Add user message to thread
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_content
        )

        # Run the assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=user.assistant_id
        )

        # Wait for the run to complete
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        # Retrieve the assistant's response
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        assistant_message = next(msg for msg in messages if msg.role == "assistant")

        # Update local thread
        self.threads[thread_id].messages.append(Message(role="user", content=message_content))
        self.threads[thread_id].messages.append(Message(role="assistant", content=assistant_message.content[0].text.value))

        return AssistantResponse(message=assistant_message.content[0].text.value, thread_id=thread_id)