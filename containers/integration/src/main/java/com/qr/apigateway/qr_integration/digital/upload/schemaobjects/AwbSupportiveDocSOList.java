package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.List;

public class AwbSupportiveDocSOList {
    private List<AwbSupportiveDocSO> awbSupportiveDocSOList;
    private List<ErrorSO> errorDetails;

    public List<AwbSupportiveDocSO> getAwbSupportiveDocSOList() {
        return awbSupportiveDocSOList;
    }

    public void setAwbSupportiveDocSOList(List<AwbSupportiveDocSO> awbSupportiveDocSOList) {
        this.awbSupportiveDocSOList = awbSupportiveDocSOList;
    }

    public List<ErrorSO> getErrorDetails() {
        return errorDetails;
    }

    public void setErrorDetails(List<ErrorSO> errorDetails) {
        this.errorDetails = errorDetails;
    }
}
