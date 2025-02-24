import { EDocResponseSO } from "./types";

export const mockResponses: EDocResponseSO[] = [
  // Response 1: Initial upload success, needs two more documents
  {
    correlationId: "corr-123",
    sessionId: "session-123",
    geteDocReferenceList: [
      { fileName: "File number 1", mandateFlag: "N" }, // First file just uploaded
      { fileName: "File number 2", mandateFlag: "Y" }, // Need this
      { fileName: "File number 3", mandateFlag: "Y" }, // And this
    ],
  },

  // Response 2: Second upload, still needs one document
  {
    correlationId: "corr-124",
    sessionId: "session-123",
    geteDocReferenceList: [
      { fileName: "File number 1", mandateFlag: "N" }, // Already have this
      { fileName: "File number 2", mandateFlag: "N" }, // Just uploaded this
      { fileName: "File number 3", mandateFlag: "Y" }, // Still need this one
    ],
  },

  // Response 3: Final upload, all complete
  {
    correlationId: "corr-125",
    sessionId: "session-123",
    geteDocReferenceList: [
      { fileName: "File number 1", mandateFlag: "N" }, // Have this
      { fileName: "File number 2", mandateFlag: "N" }, // Have this
      { fileName: "File number 3", mandateFlag: "N" }, // Just got this
    ],
  },
];
