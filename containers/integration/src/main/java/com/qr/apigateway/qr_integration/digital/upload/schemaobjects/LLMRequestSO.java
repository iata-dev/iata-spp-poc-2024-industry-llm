package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;


import java.util.List;

public class LLMRequestSO {
    private String sessionId;
    private List<FileSO> fileSOs;

    public LLMRequestSO() {
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public List<FileSO> getFileSOs() {
        return fileSOs;
    }

    public void setFileSOs(List<FileSO> fileSOs) {
        this.fileSOs = fileSOs;
    }
}
