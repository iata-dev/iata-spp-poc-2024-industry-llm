import React from "react";
import { Message } from "../types";
import LoadingMessage from "./LoadingMessage";
import chatAvatar from "../assets/chat-avatar.svg";

interface ChatMessageProps {
  message: Message;
  isProcessing?: boolean;
  isInitialUpload?: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isProcessing, isInitialUpload }) => {
  if (isProcessing) {
    return <LoadingMessage isInitialUpload={isInitialUpload} />;
  }

  const isUploading = message.status === "uploading";
  const isUser = message.sender === "user";

  return (
    <div
      className={`
        flex items-start gap-2 
        ${!isUser ? "bg-gray-50" : ""} 
        py-2 sm:py-4 px-4 sm:px-6 rounded-lg
        ${isUploading ? "opacity-60" : ""}
        transition-opacity duration-200
        ${isUser ? "flex-row-reverse" : ""}
      `}
    >
      {!isUser && (
        <div className='w-8 h-8 flex-shrink-0'>
          <img src={chatAvatar} alt='Assistant' className='w-full h-full' />
        </div>
      )}

      <div className={`flex-1 overflow-hidden ${isUser ? "text-right" : ""}`}>
        {message.files && message.files.length > 0 ? (
          <div className={`flex flex-wrap gap-1.5 sm:gap-2 ${isUser ? "justify-end" : ""}`}>
            {message.files.map((file, index) => (
              <div
                key={index}
                className={`
                  inline-flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1.5 sm:py-2 
                  ${isUser ? "bg-green-100 text-green-800" : "bg-blue-100 text-blue-800"} 
                  rounded-lg
                  ${isUploading ? "animate-pulse" : ""}
                `}
              >
                <span className='text-base font-medium'>{file.name}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className={`prose max-w-none ${isUser ? "ml-auto" : ""}`}>
            <p className='whitespace-pre-wrap text-base'>{message.text}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
