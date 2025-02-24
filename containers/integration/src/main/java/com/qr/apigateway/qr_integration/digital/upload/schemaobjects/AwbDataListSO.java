package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.List;

public class AwbDataListSO {
    private List<AwbDataSO> awbDataSOList;
    private List<ErrorSO> errorDetails;

    public List<AwbDataSO> getAwbDataSOList() {
        return awbDataSOList;
    }

    public void setAwbDataSOList(List<AwbDataSO> awbDataSOList) {
        this.awbDataSOList = awbDataSOList;
    }

    public List<ErrorSO> getErrorDetails() {
        return errorDetails;
    }

    public void setErrorDetails(List<ErrorSO> errorDetails) {
        this.errorDetails = errorDetails;
    }
}
