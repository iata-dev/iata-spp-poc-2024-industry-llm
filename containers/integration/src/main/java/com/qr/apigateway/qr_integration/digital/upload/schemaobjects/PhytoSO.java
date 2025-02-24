package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class PhytoSO {
    private String date;
    private String destintaion;
    private String goodbeingtransported;
    private boolean isValid;
    private String origin;
    private String weight;

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getDestintaion() {
        return destintaion;
    }

    public void setDestintaion(String destintaion) {
        this.destintaion = destintaion;
    }

    public String getGoodbeingtransported() {
        return goodbeingtransported;
    }

    public void setGoodbeingtransported(String goodbeingtransported) {
        this.goodbeingtransported = goodbeingtransported;
    }

    public boolean isValid() {
        return isValid;
    }

    public void setValid(boolean valid) {
        isValid = valid;
    }

    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }
}
