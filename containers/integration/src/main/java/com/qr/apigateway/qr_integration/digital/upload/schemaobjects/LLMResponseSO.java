package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class LLMResponseSO {
    private String awbPrefix;
    private String awbNumber;
    private String commodity;
    private String product;

    public LLMResponseSO() {
    }

    public String getAwbPrefix() {
        return awbPrefix;
    }

    public void setAwbPrefix(String awbPrefix) {
        this.awbPrefix = awbPrefix;
    }

    public String getAwbNumber() {
        return awbNumber;
    }

    public void setAwbNumber(String awbNumber) {
        this.awbNumber = awbNumber;
    }

    public String getCommodity() {
        return commodity;
    }

    public void setCommodity(String commodity) {
        this.commodity = commodity;
    }

    public String getProduct() {
        return product;
    }

    public void setProduct(String product) {
        this.product = product;
    }
}
