package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class ErrorSO {
    private String errorId;
    private String errorMessage;

    public ErrorSO(String errorId,String errorMessage) {
        this.errorId=errorId;
        this.errorMessage=errorMessage;
    }
    public ErrorSO() {
    }
    public String getErrorId() {
        return errorId;
    }

    public void setErrorId(String errorId) {
        this.errorId = errorId;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
