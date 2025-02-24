package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class ConincidenceSO {

    private String destination;
    private String goodbeingtransported;
    private String origin;
    private String weight;

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public String getGoodbeingtransported() {
        return goodbeingtransported;
    }

    public void setGoodbeingtransported(String goodbeingtransported) {
        this.goodbeingtransported = goodbeingtransported;
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
