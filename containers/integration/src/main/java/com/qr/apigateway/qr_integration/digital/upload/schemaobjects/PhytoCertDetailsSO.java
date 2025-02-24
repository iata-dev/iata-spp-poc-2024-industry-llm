package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class PhytoCertDetailsSO {

    private List<AWBPropertySO> Consignee=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Date=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Exporter=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Name_of_Produce=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Packaging=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Place_of_Origin=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Point_of_Entry=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> QR_Code=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Quantity_Declared=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Stamp=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> __documentMetadata=new ArrayList<AWBPropertySO>();

    @JsonProperty("Consignee")
    public List<AWBPropertySO> getConsignee() {
        return Consignee;
    }

    public void setConsignee(List<AWBPropertySO> consignee) {
        Consignee = consignee;
    }
    @JsonProperty("Date")
    public List<AWBPropertySO> getDate() {
        return Date;
    }

    public void setDate(List<AWBPropertySO> date) {
        Date = date;
    }
    @JsonProperty("Exporter")
    public List<AWBPropertySO> getExporter() {
        return Exporter;
    }

    public void setExporter(List<AWBPropertySO> exporter) {
        Exporter = exporter;
    }
    @JsonProperty("Name_of_Produce")
    public List<AWBPropertySO> getName_of_Produce() {
        return Name_of_Produce;
    }

    public void setName_of_Produce(List<AWBPropertySO> name_of_Produce) {
        Name_of_Produce = name_of_Produce;
    }
    @JsonProperty("Packaging")
    public List<AWBPropertySO> getPackaging() {
        return Packaging;
    }

    public void setPackaging(List<AWBPropertySO> packaging) {
        Packaging = packaging;
    }
    @JsonProperty("Place_of_Origin")
    public List<AWBPropertySO> getPlace_of_Origin() {
        return Place_of_Origin;
    }

    public void setPlace_of_Origin(List<AWBPropertySO> place_of_Origin) {
        Place_of_Origin = place_of_Origin;
    }
    @JsonProperty("Point_of_Entry")
    public List<AWBPropertySO> getPoint_of_Entry() {
        return Point_of_Entry;
    }

    public void setPoint_of_Entry(List<AWBPropertySO> point_of_Entry) {
        Point_of_Entry = point_of_Entry;
    }
    @JsonProperty("QR_Code")
    public List<AWBPropertySO> getQR_Code() {
        return QR_Code;
    }

    public void setQR_Code(List<AWBPropertySO> QR_Code) {
        this.QR_Code = QR_Code;
    }
    @JsonProperty("Quantity_Declared")
    public List<AWBPropertySO> getQuantity_Declared() {
        return Quantity_Declared;
    }

    public void setQuantity_Declared(List<AWBPropertySO> quantity_Declared) {
        Quantity_Declared = quantity_Declared;
    }
    @JsonProperty("Stamp")
    public List<AWBPropertySO> getStamp() {
        return Stamp;
    }

    public void setStamp(List<AWBPropertySO> stamp) {
        Stamp = stamp;
    }
    @JsonProperty("DocumentMetadata")
    public List<AWBPropertySO> get__documentMetadata() {
        return __documentMetadata;
    }

    public void set__documentMetadata(List<AWBPropertySO> __documentMetadata) {
        this.__documentMetadata = __documentMetadata;
    }
}
