package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class AwbSupportiveDocSO {
    private String carCode;
    private String origin;
    private String destination;
    private String natureOfGoods;
    private String docCheckList;

    public AwbSupportiveDocSO() {
    }

    public AwbSupportiveDocSO(String carCode, String origin, String destination, String natureOfGoods, String docCheckList) {
        this.carCode = carCode;
        this.origin = origin;
        this.destination = destination;
        this.natureOfGoods = natureOfGoods;
        this.docCheckList = docCheckList;
    }

    public String getCarCode() {
        return carCode;
    }

    public void setCarCode(String carCode) {
        this.carCode = carCode;
    }

    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public String getNatureOfGoods() {
        return natureOfGoods;
    }

    public void setNatureOfGoods(String natureOfGoods) {
        this.natureOfGoods = natureOfGoods;
    }

    public String getDocCheckList() {
        return docCheckList;
    }

    public void setDocCheckList(String docCheckList) {
        this.docCheckList = docCheckList;
    }
}
