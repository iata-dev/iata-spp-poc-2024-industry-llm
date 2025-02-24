package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class UploadAwbRespSOList {
    private UploadAwbRespSO uploadAwbRespSO;
    private ErrorSO errorSO;

    public UploadAwbRespSO getUploadAwbRespSO() {
        return uploadAwbRespSO;
    }

    public void setUploadAwbRespSO(UploadAwbRespSO uploadAwbRespSO) {
        this.uploadAwbRespSO = uploadAwbRespSO;
    }

    public ErrorSO getErrorSO() {
        return errorSO;
    }

    public void setErrorSO(ErrorSO errorSO) {
        this.errorSO = errorSO;
    }
}
