export type ServiceSource = "azure" | "snowflake";

export type SenderType = "user" | "assistant";

export type MessageStatus = "uploading" | "uploaded" | "error";

export interface Message {
  id: number;
  text: string;
  files?: {
    data: string;
    type: string;
    name: string;
  }[];
  sender: SenderType;
  status?: MessageStatus;
}

export interface SelectedFile {
  id: string;
  name: string;
  data: string;
  type: string;
}

export interface Conversation {
  id: string;
  title: string;
  timestamp: Date;
  preview: string;
  messages: Message[];
  sessionId?: string;
}

export interface EdocRequestSO {
  sessionId?: string;
  fileSOs: FileSO[];
  source: ServiceSource;
}

export interface FileSO {
  fileData: string;
  fileType: string;
  fileName: string;
}

export interface UploadRequestSO {
  source: ServiceSource;
  sessionId?: string;
  fileSOs: {
    fileName: string;
    fileType: string;
    fileData: string;
  }[];
}

export interface EdocResponseSO {
  sessionId: string;
  eDocFileTypeSOS: EDocFileTypeSO[];
  errorDetails?: ErrorSO[];
  responseMsg: string;
  source: ServiceSource;
}

export interface EDocFileTypeSO {
  origin: string;
  destination: string;
  commodity: string;
  natureOfGood: string;
  fileType: string;
  mandateFlag: string;
  name: string;
  description: string;
}

export interface ErrorSO {
  errorId: string;
  errorMessage: string;
}
