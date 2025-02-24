package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class EdocResponseSO {
    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    // private String correlationId;
    private String sessionId;
    private List<EDocFileTypeSO> eDocFileTypeSOS;
    private List<ErrorSO> errorDetails=new ArrayList<ErrorSO>();
    private String source;

    public String getResponseMsg() {
        return responseMsg;
    }

    public void setResponseMsg(String responseMsg) {
        this.responseMsg = responseMsg;
    }

    private String responseMsg;

    public EdocResponseSO() {
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }


    public List<ErrorSO> getErrorDetails() {
        return errorDetails;
    }

    public void setErrorDetails(List<ErrorSO> errorDetails) {
        this.errorDetails = errorDetails;
    }

    public List<EDocFileTypeSO> geteDocFileTypeSOS() {
        return eDocFileTypeSOS;
    }

    public void seteDocFileTypeSOS(List<EDocFileTypeSO> eDocFileTypeSOS) {
        this.eDocFileTypeSOS = eDocFileTypeSOS;
    }
}
