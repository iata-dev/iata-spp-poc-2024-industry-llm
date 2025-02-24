import { getApiUrl } from "../api";
import { strings } from "../constants/strings";
import { SelectedFile, Message, Conversation, EdocRequestSO, EdocResponseSO, ServiceSource, UploadRequestSO } from "../types";
import { getCleanBase64 } from "../utils/fileUtils";

export const handleRealSubmit = async (
  selectedFiles: SelectedFile[],
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>,
  setConversations: React.Dispatch<React.SetStateAction<Conversation[]>>,
  activeConversationId: string | null,
  source: ServiceSource,
  isInitialUpload: boolean,
  currentSessionId?: string
) => {
  const newMessage: Message = {
    id: Date.now() + Math.floor(Math.random() * 1000),
    text: "",
    files: selectedFiles.map((file) => ({
      data: file.data,
      type: file.type,
      name: file.name,
    })),
    sender: "user",
    status: "uploading",
  };

  setMessages((prev) => [...prev, newMessage]);
  if (activeConversationId) {
    setConversations((prev) =>
      prev.map((conv) =>
        conv.id === activeConversationId
          ? {
              ...conv,
              messages: [...conv.messages, newMessage],
              preview: strings.upload.preview.filesSent(selectedFiles.length),
            }
          : conv
      )
    );
  }

  try {
    const request: UploadRequestSO = {
      source,
      fileSOs: selectedFiles.map((file) => ({
        fileName: file.name,
        fileType: file.type,
        fileData: getCleanBase64(file.data),
      })),
      sessionId: !isInitialUpload ? currentSessionId : undefined,
    };

    const response = await uploadFiles(request, isInitialUpload, !isInitialUpload ? currentSessionId : undefined);

    const hasErrors = response.errorDetails && response.errorDetails.length > 0;
    const newStatus = hasErrors ? "error" : "uploaded";

    setMessages((prev) => prev.map((msg) => (msg.id === newMessage.id ? { ...msg, status: newStatus } : msg)));

    if (activeConversationId) {
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === activeConversationId
            ? {
                ...conv,
                messages: conv.messages.map((msg) => (msg.id === newMessage.id ? { ...msg, status: newStatus } : msg)),
                sessionId: isInitialUpload ? response.sessionId : conv.sessionId,
              }
            : conv
        )
      );
    }

    const assistantMessage: Message = {
      id: Date.now() + Math.floor(Math.random() * 1000),
      text: formatResponseMessage(response),
      sender: "assistant",
    };

    setMessages((prev) => [...prev, assistantMessage]);

    if (activeConversationId) {
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === activeConversationId
            ? {
                ...conv,
                messages: [...conv.messages, assistantMessage],
              }
            : conv
        )
      );
    }

    return true;
  } catch (error) {
    console.error(strings.upload.errors.uploadFailed, error);
    return false;
  }
};

const formatResponseMessage = (response: EdocResponseSO): string => {
  let message = response.responseMsg || "";

  // Add error messages if they exist
  if (response.errorDetails && response.errorDetails.length > 0) {
    message += "\n\nErrors:";
    response.errorDetails.forEach((error) => {
      message += `\n- ${error.errorMessage}`;
    });
  }

  // Add required documents if they exist
  if (response.eDocFileTypeSOS && response.eDocFileTypeSOS.length > 0) {
    message += "\n\nRequired documents:";
    response.eDocFileTypeSOS.forEach((doc) => {
      message += `\n- ${doc.name}`;
    });
  }

  return message;
};

export const uploadFiles = async (request: EdocRequestSO, isAwb: boolean = true, sessionId?: string): Promise<EdocResponseSO> => {
  const endpoint = isAwb ? "awbUpload" : "supportingDocsUpload";

  // Clean the base64 data in the request while maintaining the EdocRequestSO structure
  const cleanedRequest = {
    ...request,
    sessionId,
    fileSOs: request.fileSOs.map((file) => ({
      fileName: file.fileName,
      fileType: file.fileType,
      fileData: getCleanBase64(file.fileData),
    })),
  };

  try {
    const response = await fetch(getApiUrl(endpoint), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(cleanedRequest),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Error response:", errorText);
      throw new Error(strings.upload.errors.httpError(response.status));
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
};
