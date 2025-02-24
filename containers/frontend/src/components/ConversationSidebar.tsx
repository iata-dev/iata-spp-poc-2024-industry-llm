import React from "react";
import { Conversation } from "../types";

interface ConversationSidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onConversationSelect: (id: string) => void;
}

const ConversationSidebar: React.FC<ConversationSidebarProps> = ({ conversations, activeConversationId, onConversationSelect }) => {
  const formatDateTime = (date: Date) => {
    const conversationDate = new Date(date);
    return conversationDate.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getFileCount = (conversation: Conversation) => {
    const successfulFiles = conversation.messages
      .filter((msg) => msg.sender === "user" && msg.status === "uploaded" && msg.files)
      .reduce((total, msg) => total + (msg.files?.length || 0), 0);

    const errorFiles = conversation.messages
      .filter((msg) => msg.sender === "user" && msg.status === "error" && msg.files)
      .reduce((total, msg) => total + (msg.files?.length || 0), 0);

    const uploadingFiles = conversation.messages
      .filter((msg) => msg.sender === "user" && msg.status === "uploading" && msg.files)
      .reduce((total, msg) => total + (msg.files?.length || 0), 0);

    if (successfulFiles === 0 && errorFiles === 0 && uploadingFiles === 0) {
      return "No files uploaded yet";
    }

    let status = [];
    if (successfulFiles > 0) {
      status.push(`${successfulFiles} ${successfulFiles === 1 ? "file" : "files"} uploaded`);
    }
    if (errorFiles > 0) {
      status.push(`${errorFiles} with errors`);
    }
    if (uploadingFiles > 0) {
      status.push(`${uploadingFiles} uploading`);
    }

    return status.join(", ");
  };

  return (
    <div className='flex-1 overflow-y-auto'>
      {conversations.map((conversation) => (
        <button
          key={conversation.id}
          onClick={() => onConversationSelect(conversation.id)}
          className={`w-full text-left p-4 hover:bg-gray-100 transition-colors border-b border-gray-100 ${
            activeConversationId === conversation.id ? "bg-gray-100" : ""
          }`}
        >
          <div className='font-medium text-gray-900'>{conversation.title}</div>

          <div className='text-sm text-gray-600 mt-1'>{getFileCount(conversation)}</div>

          <div className='text-xs text-gray-400 mt-1'>{formatDateTime(conversation.timestamp)}</div>
        </button>
      ))}
    </div>
  );
};

export default ConversationSidebar;
