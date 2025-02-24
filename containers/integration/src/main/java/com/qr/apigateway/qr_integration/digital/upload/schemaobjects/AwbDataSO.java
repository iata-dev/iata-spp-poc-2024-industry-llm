package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.Date;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AwbDataSO {
    private long id;
    String origin;
    String destination;
    String sessionId;
    String shpName;
    String consName;
    String origCntry;
    String destCntry;
    int pieces;
    String weight;
    String natureOfGoods;
    String execDate;
    String docsList;
    String verDocsList;
    String errorDocsList;
    String errorDesc;
    String docType;
    public AwbDataSO() {

    }
    public AwbDataSO (long id, String origin, String destination, String sessionId,
                      String shpName, String consName, String origCntry, String destCntry,
                      int pieces, String weight, String natureOfGoods, String execDate,
                      String docsList, String verDocsList, String errorDocsList,
                      String docType) {
        this.id=id;
        this.origin=origin;
        this.destination=destination;
        this.sessionId=sessionId;
        this.shpName=shpName;
        this.consName=consName;
        this.origCntry=origCntry;
        this.destCntry=destCntry;
        this.pieces=pieces;
        this.weight=weight;
        this.natureOfGoods=natureOfGoods;
        this.execDate=execDate;
        this.docsList=docsList;
        this.verDocsList=verDocsList;
        this.errorDocsList=errorDocsList;
        this.docType=docType;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
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

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getShpName() {
        return shpName;
    }

    public void setShpName(String shpName) {
        this.shpName = shpName;
    }

    public String getConsName() {
        return consName;
    }

    public void setConsName(String consName) {
        this.consName = consName;
    }

    public String getOrigCntry() {
        return origCntry;
    }

    public void setOrigCntry(String origCntry) {
        this.origCntry = origCntry;
    }

    public String getDestCntry() {
        return destCntry;
    }

    public void setDestCntry(String destCntry) {
        this.destCntry = destCntry;
    }

    public int getPieces() {
        return pieces;
    }

    public void setPieces(int pieces) {
        this.pieces = pieces;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }

    public String getNatureOfGoods() {
        return natureOfGoods;
    }

    public void setNatureOfGoods(String natureOfGoods) {
        this.natureOfGoods = natureOfGoods;
    }

    public String getExecDate() {
        return execDate;
    }

    public void setExecDate(String execDate) {
        this.execDate = execDate;
    }

    public String getDocsList() {
        return docsList;
    }

    public void setDocsList(String docsList) {
        this.docsList = docsList;
    }

    public String getVerDocsList() {
        return verDocsList;
    }

    public void setVerDocsList(String verDocsList) {
        this.verDocsList = verDocsList;
    }

    public String getErrorDocsList() {
        return errorDocsList;
    }

    public void setErrorDocsList(String errorDocsList) {
        this.errorDocsList = errorDocsList;
    }

    public String getErrorDesc() {
        return errorDesc;
    }

    public void setErrorDesc(String errorDesc) {
        this.errorDesc = errorDesc;
    }

    public String getDocType() {
        return docType;
    }

    public void setDocType(String docType) {
        this.docType = docType;
    }
}
