package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AwbDocListSO {
    private long id;
    private String docType;
    private String uploadInd;
    private String validInd;
    private String reason;
    private long awbdata_id;

    public AwbDocListSO(long id, String docType, String uploadInd, String validInd, String reason, long awbdata_id) {
        this.id = id;
        this.docType = docType;
        this.uploadInd = uploadInd;
        this.validInd = validInd;
        this.reason = reason;
        this.awbdata_id = awbdata_id;
    }

    public AwbDocListSO() {
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getDocType() {
        return docType;
    }

    public void setDocType(String docType) {
        this.docType = docType;
    }

    public String getUploadInd() {
        return uploadInd;
    }

    public void setUploadInd(String uploadInd) {
        this.uploadInd = uploadInd;
    }

    public String getValidInd() {
        return validInd;
    }

    public void setValidInd(String validInd) {
        this.validInd = validInd;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    public long getAwbdata_id() {
        return awbdata_id;
    }

    public void setAwbdata_id(long awbdata_id) {
        this.awbdata_id = awbdata_id;
    }
}