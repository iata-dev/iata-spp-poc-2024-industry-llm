export const strings = {
  // Button labels
  buttons: {
    newAwbSubmission: "New conversation",
    azureService: "Azure service",
    snowflakeService: "Snowflake service",
    uploadFile: "Upload file",
    takePhoto: "Take photo",
    submit: "Submit",
    close: "Close",
    install: "Install App",
    remove: "Remove",
  },

  // Titles and headers
  titles: {
    appName: "IATA Document Assistant",
    newAzureConversation: "New Azure conversation",
    newSnowflakeConversation: "New Snowflake conversation",
  },

  // Messages
  messages: {
    uploadSuccess: "Document uploaded successfully",
    uploadError: "There was an error uploading your files. Please try again.",
    provideMandatoryDocs: (docs: string[]) => `Document uploaded successfully. Please also provide:\n${docs.join("\n")}`,
    allDocsUploaded: "All documents have been uploaded successfully!",
    startedNewConversation: (service: string) => `Started new ${service} conversation`,
  },

  // Alt texts for accessibility
  altTexts: {
    chatAvatar: "Chat Avatar",
    menuIcon: "Menu",
    closeIcon: "Close",
    uploadIcon: "Upload",
    cameraIcon: "Camera",
    removeIcon: "Remove",
  },

  // Prompts and instructions
  prompts: {
    pwaInstall: "Install this app on your device for the best experience",
  },

  // Error messages
  errors: {
    fileUpload: "Error uploading files. Please try again.",
    networkError: (status: number) => `HTTP error! status: ${status}`,
  },

  // Placeholders
  placeholders: {
    origin: "Origin",
    destination: "Destination",
    commodity: "Commodity",
    natureOfGoods: "Nature of Goods",
  },

  // Initial messages
  initialMessages: {
    uploadPrompt: "Please upload your AWB for checking here",
  },

  // File related
  files: {
    cameraCapture: "camera_capture.jpg",
  },

  // Upload service messages
  upload: {
    success: {
      documentsRequired: (docs: string[]) => `Document uploaded successfully. Please also provide:\n${docs.join("\n")}`,
      allComplete: "All documents have been uploaded successfully!",
    },
    errors: {
      uploadFailed: "There was an error uploading your files. Please try again.",
      httpError: (status: number) => `HTTP error! status: ${status}`,
    },
    debug: {
      simulatingApi: "Simulating API request...",
      mockResponse: "Mock response received:",
      uploadError: "Error uploading files:",
    },
    preview: {
      filesSent: (count: number) => `${count} file${count > 1 ? "s" : ""} sent`,
    },
  },
};
