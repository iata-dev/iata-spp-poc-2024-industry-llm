package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.Objects;

public class FileSO {
    private String fileData;
    private String fileType;
    private String sessionId;
    private String fileName;

    public FileSO() {
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

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof FileSO fileSO)) return false;
        return Objects.equals(getFileData(), fileSO.getFileData()) && Objects.equals(getFileType(), fileSO.getFileType()) && Objects.equals(getSessionId(), fileSO.getSessionId()) && Objects.equals(getFileName(), fileSO.getFileName());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getFileData(), getFileType(), getSessionId(), getFileName());
    }

    @Override
    public String toString() {
        return "FileSO{" +
                "fileData='" + fileData + '\'' +
                ", fileType='" + fileType + '\'' +
                ", sessionId='" + sessionId + '\'' +
                ", fileName='" + fileName + '\'' +
                '}';
    }
}
