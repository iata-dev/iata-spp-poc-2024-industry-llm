import React, { useRef, useEffect } from "react";
import { Message } from "../types";
import ChatMessage from "./ChatMessage";

interface ChatAreaProps {
  messages: Message[];
  isMobileOrTablet: boolean;
  isProcessing?: boolean;
  isInitialUpload?: boolean;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isMobileOrTablet, isProcessing = false, isInitialUpload = true }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  return (
    <main
      className={`
      flex-1 
      overflow-y-auto 
      chat-area
      ${isMobileOrTablet ? "" : "ml-64"}
      ${isMobileOrTablet ? "mt-44" : "mt-20"}
      -webkit-overflow-scrolling: touch
    `}
    >
      <div
        className={`
          mx-auto 
          ${isMobileOrTablet ? "w-[95%]" : "w-[90%] md:max-w-[70%]"}
          pb-[120px]
        `}
      >
        {/* Add padding to first message only */}
        {messages.map((message, index) => (
          <div key={message.id} className={index === 0 ? "pt-6" : "pt-4"}>
            <ChatMessage message={message} />
          </div>
        ))}

        {isProcessing && (
          <div className='pt-4'>
            <ChatMessage
              message={{ id: Date.now(), text: "", sender: "assistant" }}
              isProcessing={true}
              isInitialUpload={isInitialUpload}
            />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </main>
  );
};

export default ChatArea;
