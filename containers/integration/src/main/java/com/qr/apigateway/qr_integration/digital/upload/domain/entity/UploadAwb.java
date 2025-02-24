package com.qr.apigateway.qr_integration.digital.upload.domain.entity;

public class UploadAwb {
    private long digAwbId;
    private String sessionId;
    private String fileData;
    private String fileType;

    public long getDigAwbId() {
        return digAwbId;
    }

    public void setDigAwbId(long digAwbId) {
        this.digAwbId = digAwbId;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getFileData() {
        return fileData;
    }

    public void setFileData(String fileData) {
        this.fileData = fileData;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }
}
