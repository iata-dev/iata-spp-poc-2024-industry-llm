package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class UploadSuppDocSO {
    private String filename;
    private String filedata;
    private String fileType;
    private long digiAwbId;

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getFiledata() {
        return filedata;
    }

    public void setFiledata(String filedata) {
        this.filedata = filedata;
    }

    public long getDigiAwbId() {
        return digiAwbId;
    }

    public void setDigiAwbId(long digiAwbId) {
        this.digiAwbId = digiAwbId;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }
}
