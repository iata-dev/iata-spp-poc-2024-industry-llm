package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class AwbDataSearchSO {
    private String sessionId;
    private long id;
    private String docType;

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getDocType() {
        return docType;
    }

    public void setDocType(String docType) {
        this.docType = docType;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }
}
