package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.List;
import java.util.Objects;

public class EdocRequestSO {
    private String sessionId;

    private String origin;

    private String dest;

    private String commodity;

    private String natureOfGood;

    private List<FileSO> fileSOs;
    private String source;
    public EdocRequestSO() {
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
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

    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }

    public String getDest() {
        return dest;
    }

    public void setDest(String dest) {
        this.dest = dest;
    }

    public String getCommodity() {
        return commodity;
    }

    public void setCommodity(String commodity) {
        this.commodity = commodity;
    }

    public String getNatureOfGood() {
        return natureOfGood;
    }

    public void setNatureOfGood(String natureOfGood) {
        this.natureOfGood = natureOfGood;
    }
}
