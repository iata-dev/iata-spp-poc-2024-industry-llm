//Config with dev proxy to avoid CORS origin errors

// export const API_CONFIG = {
//   baseUrl: "/api",
//   endpoints: {
//     awbUpload: "/awb/upload",
//     supportingDocsUpload: "/awb/uploadSupportingDocuments",
//   },
// } as const;

// export const getApiUrl = (endpoint: keyof typeof API_CONFIG.endpoints): string => {
//   return `${API_CONFIG.baseUrl}${API_CONFIG.endpoints[endpoint]}`;
// };

//Config with direct Azure url, not using dev proxy

export const API_CONFIG = {
  // Direct Azure URL
  baseUrl: "https://qrorchestrator-d8dwbkdrh6eqapa5.westeurope-01.azurewebsites.net",
  endpoints: {
    awbUpload: "/awb/upload",
    supportingDocsUpload: "/awb/uploadSupportingDocuments",
  },
} as const;

export const getApiUrl = (endpoint: keyof typeof API_CONFIG.endpoints): string => {
  return `${API_CONFIG.baseUrl}${API_CONFIG.endpoints[endpoint]}`;
};
