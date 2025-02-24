package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class UploadAwbRespSO {
    @JsonProperty("Agent City")
    private String agentCity;
    @JsonProperty("Agent IATA Code")
    private String agentIataCode;
    @JsonProperty("Agent Name")
    private String agentName;
    @JsonProperty("Consignee Address")
    private String consigneeAddress;
    @JsonProperty("Consignee Country Code")
    private String consigneeCountryCode;

    @JsonProperty("Consignee Name")
    private String consigneeName;

    @JsonProperty("Document Number")
    private String documentNumber;

    @JsonProperty("Document Prefix")
    private String documentPrefix;

    @JsonProperty("Executed On Date")
    private String executedOnDate;

    @JsonProperty("Number Of Pieces")
    private String numberOfPieces;

    @JsonProperty("Shipper Address")
    private String shipperAddress;

    @JsonProperty("Shipper Country Code")
    private String shipperCountryCode;

    @JsonProperty("Shipper Name")
    private String shipperName;
    private String destination;
    private String goodbeingtransported;
    private String origin;
    private String transit;
    private String weight;
    private List<String> requiredDocuments;
    private long digiAwbId;

    public String getAgentCity() {
        return agentCity;
    }

    public void setAgentCity(String agentCity) {
        this.agentCity = agentCity;
    }

    public String getAgentIataCode() {
        return agentIataCode;
    }

    public void setAgentIataCode(String agentIataCode) {
        this.agentIataCode = agentIataCode;
    }

    public String getAgentName() {
        return agentName;
    }

    public void setAgentName(String agentName) {
        this.agentName = agentName;
    }

    public String getConsigneeAddress() {
        return consigneeAddress;
    }

    public void setConsigneeAddress(String consigneeAddress) {
        this.consigneeAddress = consigneeAddress;
    }

    public String getConsigneeCountryCode() {
        return consigneeCountryCode;
    }

    public void setConsigneeCountryCode(String consigneeCountryCode) {
        this.consigneeCountryCode = consigneeCountryCode;
    }

    public String getConsigneeName() {
        return consigneeName;
    }

    public void setConsigneeName(String consigneeName) {
        this.consigneeName = consigneeName;
    }

    public String getDocumentNumber() {
        return documentNumber;
    }

    public void setDocumentNumber(String documentNumber) {
        this.documentNumber = documentNumber;
    }

    public String getDocumentPrefix() {
        return documentPrefix;
    }

    public void setDocumentPrefix(String documentPrefix) {
        this.documentPrefix = documentPrefix;
    }

    public String getExecutedOnDate() {
        return executedOnDate;
    }

    public void setExecutedOnDate(String executedOnDate) {
        this.executedOnDate = executedOnDate;
    }

    public String getNumberOfPieces() {
        return numberOfPieces;
    }

    public void setNumberOfPieces(String numberOfPieces) {
        this.numberOfPieces = numberOfPieces;
    }

    public String getShipperAddress() {
        return shipperAddress;
    }

    public void setShipperAddress(String shipperAddress) {
        this.shipperAddress = shipperAddress;
    }

    public String getShipperCountryCode() {
        return shipperCountryCode;
    }

    public void setShipperCountryCode(String shipperCountryCode) {
        this.shipperCountryCode = shipperCountryCode;
    }

    public String getShipperName() {
        return shipperName;
    }

    public void setShipperName(String shipperName) {
        this.shipperName = shipperName;
    }

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

    public String getTransit() {
        return transit;
    }

    public void setTransit(String transit) {
        this.transit = transit;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }

    public List<String> getRequiredDocuments() {
        return requiredDocuments;
    }

    public void setRequiredDocuments(List<String> requiredDocuments) {
        this.requiredDocuments = requiredDocuments;
    }

    public long getDigiAwbId() {
        return digiAwbId;
    }

    public void setDigiAwbId(long digiAwbId) {
        this.digiAwbId = digiAwbId;
    }
}
