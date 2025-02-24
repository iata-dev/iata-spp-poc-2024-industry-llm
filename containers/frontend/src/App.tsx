import { useState, useEffect, FormEvent, ChangeEvent, useRef } from "react";
import { Conversation, Message, SelectedFile, ServiceSource } from "./types";
import { PWAPrompt } from "./components/PWAPrompt";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import FileUploadForm from "./components/FileUploadForm";
import { strings } from "./constants/strings";
import { createCameraCaptureFile, createFileObject, fileToBase64 } from "./utils/fileUtils";
import { handleRealSubmit } from "./services/uploadService";
import { conversationService } from "./services/conversationService";
import ServiceSelectionOverlay from "./components/ServiceSelectionOverlay";

function App() {
  const [selectedFiles, setSelectedFiles] = useState<SelectedFile[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [activeService, setActiveService] = useState<ServiceSource | null>(null);
  const [isInitialUpload, setIsInitialUpload] = useState<boolean>(true);
  const [isMobileOrTablet, setIsMobileOrTablet] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: strings.initialMessages.uploadPrompt,
      sender: "assistant",
    },
  ]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check if device is mobile or tablet
    const checkDevice = () => {
      const userAgent = navigator.userAgent.toLowerCase();
      const isMobile = /iphone|ipad|ipod|android|blackberry|windows phone/g.test(userAgent);
      const isTablet = /(ipad|tablet|playbook|silk)|(android(?!.*mobile))/g.test(userAgent);
      setIsMobileOrTablet(isMobile || isTablet);
    };

    checkDevice();
    window.addEventListener("resize", checkDevice);

    return () => {
      window.removeEventListener("resize", checkDevice);
    };
  }, []);

  useEffect(() => {
    const savedConversations = conversationService.loadConversations();
    const activeId = conversationService.loadActiveConversation();

    if (savedConversations.length === 0) {
      const initialMessage: Message = {
        id: Date.now(),
        text: strings.initialMessages.uploadPrompt,
        sender: "assistant",
      };

      const initialConversation: Conversation = {
        id: Date.now().toString(),
        title: "Snowflake Conversation",
        timestamp: new Date(),
        preview: "No files uploaded yet",
        messages: [initialMessage],
      };

      setConversations([initialConversation]);
      setActiveConversationId(initialConversation.id);
      setMessages(initialConversation.messages);
      conversationService.saveConversations([initialConversation]);
      conversationService.saveActiveConversation(initialConversation.id);
    } else {
      setConversations(savedConversations);
      setActiveConversationId(activeId);
      if (activeId) {
        const activeConv = savedConversations.find((conv) => conv.id === activeId);
        if (activeConv) {
          setMessages(activeConv.messages);
        }
      }
    }
  }, []);

  useEffect(() => {
    conversationService.saveConversations(conversations);
  }, [conversations]);

  useEffect(() => {
    conversationService.saveActiveConversation(activeConversationId);
  }, [activeConversationId]);
  const handleImageUpload = async (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      for (const file of Array.from(files)) {
        try {
          const base64Data = await fileToBase64(file);
          const fileObj = createFileObject(file, base64Data, selectedFiles.length === 0 ? `initial_${Date.now().toString()}` : undefined);
          setSelectedFiles((prev) => [...prev, fileObj]);
        } catch (error) {
          console.error("Error processing file:", error);
        }
      }
    }
  };

  const handleServiceSelect = (service: ServiceSource) => {
    setActiveService(service);

    const initialMessage: Message = {
      id: Date.now(),
      text: strings.initialMessages.uploadPrompt,
      sender: "assistant",
    };

    const initialConversation: Conversation = {
      id: Date.now().toString(),
      title: service === "azure" ? "Azure Conversation" : "Snowflake Conversation",
      timestamp: new Date(),
      preview: "No files uploaded yet",
      messages: [initialMessage],
    };

    setConversations([initialConversation]);
    setActiveConversationId(initialConversation.id);
    setMessages(initialConversation.messages);
    conversationService.saveConversations([initialConversation]);
    conversationService.saveActiveConversation(initialConversation.id);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (selectedFiles.length > 0 && activeService) {
      setIsProcessing(true);

      try {
        const currentConversation = conversations.find((conv) => conv.id === activeConversationId);
        const currentSessionId = currentConversation?.sessionId;

        await handleRealSubmit(
          selectedFiles,
          setMessages,
          setConversations,
          activeConversationId,
          activeService,
          isInitialUpload,
          currentSessionId
        );

        setSelectedFiles([]);
        if (isInitialUpload) {
          setIsInitialUpload(false);
        }
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const handleCameraCapture = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        const base64Data = await fileToBase64(file);
        const fileObj = createCameraCaptureFile(base64Data);
        setSelectedFiles((prev) => [...prev, fileObj]);
      } catch (error) {
        console.error("Error processing camera capture:", error);
      }
    }
  };

  const removeFile = (id: string) => {
    setSelectedFiles((prev) => prev.filter((file) => file.id !== id));
  };

  const handleNewConversation = (service: "azure" | "snowflake") => {
    const initialMessage: Message = {
      id: Date.now(),
      text: strings.initialMessages.uploadPrompt,
      sender: "assistant",
    };

    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: service === "azure" ? "Azure Conversation" : "Snowflake Conversation",
      timestamp: new Date(),
      preview: "No files uploaded yet",
      messages: [initialMessage],
      // sessionId will be set after the first file upload from the backend response
    };

    setConversations((prev) => {
      const updatedConversations = [newConversation, ...prev];
      localStorage.setItem("chat_conversations", JSON.stringify(updatedConversations));
      return updatedConversations;
    });

    setActiveConversationId(newConversation.id);
    localStorage.setItem("active_conversation", newConversation.id);

    setMessages([initialMessage]);
    setActiveService(service);
    setIsInitialUpload(true);
  };

  return (
    <div className='min-h-screen bg-white flex flex-col'>
      <Header isMobileOrTablet={isMobileOrTablet} onMenuClick={() => setIsSidebarOpen(true)} />

      <Sidebar
        isMobileOrTablet={isMobileOrTablet}
        isSidebarOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onNewConversation={handleNewConversation}
        conversations={conversations}
        activeConversationId={activeConversationId}
        activeService={activeService}
        onConversationSelect={(id) => {
          const selectedConv = conversations.find((conv) => conv.id === id);
          if (selectedConv) {
            setActiveConversationId(id);
            setMessages(selectedConv.messages);
          }
        }}
      />

      <div className='relative flex-1'>
        {!activeService && <ServiceSelectionOverlay onServiceSelect={handleServiceSelect} isMobileOrTablet={isMobileOrTablet} />}
        <ChatArea messages={messages} isMobileOrTablet={isMobileOrTablet} isProcessing={isProcessing} />
      </div>

      <FileUploadForm
        selectedFiles={selectedFiles}
        onFileSelect={handleImageUpload}
        onCameraCapture={handleCameraCapture}
        onSubmit={handleSubmit}
        onRemoveFile={removeFile}
        isMobileOrTablet={isMobileOrTablet}
        isProcessing={isProcessing}
      />
      <PWAPrompt isMobileOrTablet={isMobileOrTablet} />
    </div>
  );
}

export default App;
