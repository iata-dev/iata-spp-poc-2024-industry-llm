package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.Objects;


@JsonIgnoreProperties(ignoreUnknown = true)
public class EDocFileTypeSO {

    private String origin;

    private String destination;

    private String commodity;

    private String natureOfGood;

    private String fileType;
    private String mandateFlag;
    private String name;
    private String description;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public EDocFileTypeSO() {
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

    public String getCommodity() {
        return commodity;
    }

    public void setCommodity(String commodity) {
        this.commodity = commodity;
    }

    public String getNatureOfGood() {
        return natureOfGood;
    }

    public void setNatureOfGood(String natureOfGood) {
        this.natureOfGood = natureOfGood;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public String getMandateFlag() {
        return mandateFlag;
    }

    public void setMandateFlag(String mandateFlag) {
        this.mandateFlag = mandateFlag;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof EDocFileTypeSO that)) return false;
        return Objects.equals(getOrigin(), that.getOrigin()) && Objects.equals(getDestination(), that.getDestination()) && Objects.equals(getCommodity(), that.getCommodity()) && Objects.equals(getNatureOfGood(), that.getNatureOfGood()) && Objects.equals(getFileType(), that.getFileType()) && Objects.equals(getMandateFlag(), that.getMandateFlag());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getOrigin(), getDestination(), getCommodity(), getNatureOfGood(), getFileType(), getMandateFlag());
    }

    @Override
    public String toString() {
        return "EDocFileTypeSO{" +
                "origin='" + origin + '\'' +
                ", destination='" + destination + '\'' +
                ", commodity='" + commodity + '\'' +
                ", natureOfGood='" + natureOfGood + '\'' +
                ", fileType='" + fileType + '\'' +
                ", mandateFlag='" + mandateFlag + '\'' +
                '}';
    }
}
