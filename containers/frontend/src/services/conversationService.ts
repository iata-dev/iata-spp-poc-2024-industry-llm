import { Conversation, Message } from "../types";

const CONVERSATIONS_KEY = "chat_conversations";
const ACTIVE_CONVERSATION_KEY = "active_conversation";

export const conversationService = {
  saveConversations(conversations: Conversation[]) {
    localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(conversations));
  },

  loadConversations(): Conversation[] {
    const saved = localStorage.getItem(CONVERSATIONS_KEY);
    return saved ? JSON.parse(saved) : [];
  },

  saveActiveConversation(id: string | null) {
    if (id) {
      localStorage.setItem(ACTIVE_CONVERSATION_KEY, id);
    } else {
      localStorage.removeItem(ACTIVE_CONVERSATION_KEY);
    }
  },

  loadActiveConversation(): string | null {
    return localStorage.getItem(ACTIVE_CONVERSATION_KEY);
  },

  createConversation(firstMessage: Message): Conversation {
    return {
      id: Date.now().toString(),
      title: firstMessage.text.slice(0, 50) + "...",
      timestamp: new Date(),
      preview: firstMessage.text,
      messages: [firstMessage],
      sessionId: crypto.randomUUID(),
    };
  },

  updateConversation(conversation: Conversation, message: Message): Conversation {
    return {
      ...conversation,
      preview: message.text,
      messages: [...conversation.messages, message],
      timestamp: new Date(),
    };
  },
};
