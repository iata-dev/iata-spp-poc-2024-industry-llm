package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AWBDetailsSO {


    private List<AWBPropertySO> Account_No=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Agent_IATA_Code=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Chargeable_Weight=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Consignee_Account_No=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Consignee_Address=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Consignee_Name=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Currency_Cd=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Departure_Airport_Cd=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Destination_Airport_Cd=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Nature_of_Goods=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Issued_By=new ArrayList<AWBPropertySO>();

    private List<AWBPropertySO> Shipper_Address=new ArrayList<AWBPropertySO>();
    private List<AWBPropertySO> Shipper_Name=new ArrayList<AWBPropertySO>();

    @JsonProperty("Account_No")
    public List<AWBPropertySO> getAccount_No() {
        return Account_No;
    }

    public void setAccount_No(List<AWBPropertySO> account_No) {
        Account_No = account_No;
    }
    @JsonProperty("Agent_IATA_Code")
    public List<AWBPropertySO> getAgent_IATA_Code() {
        return Agent_IATA_Code;
    }

    public void setAgent_IATA_Code(List<AWBPropertySO> agent_IATA_Code) {
        Agent_IATA_Code = agent_IATA_Code;
    }
    @JsonProperty("Chargeable_Weight")
    public List<AWBPropertySO> getChargeable_Weight() {
        return Chargeable_Weight;
    }

    public void setChargeable_Weight(List<AWBPropertySO> chargeable_Weight) {
        Chargeable_Weight = chargeable_Weight;
    }
    @JsonProperty("Consignee_Account_No")
    public List<AWBPropertySO> getConsignee_Account_No() {
        return Consignee_Account_No;
    }

    public void setConsignee_Account_No(List<AWBPropertySO> consignee_Account_No) {
        Consignee_Account_No = consignee_Account_No;
    }
    @JsonProperty("Consignee_Address")
    public List<AWBPropertySO> getConsignee_Address() {
        return Consignee_Address;
    }

    public void setConsignee_Address(List<AWBPropertySO> consignee_Address) {
        Consignee_Address = consignee_Address;
    }
    @JsonProperty("Consignee_Name")
    public List<AWBPropertySO> getConsignee_Name() {
        return Consignee_Name;
    }

    public void setConsignee_Name(List<AWBPropertySO> consignee_Name) {
        Consignee_Name = consignee_Name;
    }
    @JsonProperty("Currency_Cd")
    public List<AWBPropertySO> getCurrency_Cd() {
        return Currency_Cd;
    }

    public void setCurrency_Cd(List<AWBPropertySO> currency_Cd) {
        Currency_Cd = currency_Cd;
    }
    @JsonProperty("Departure_Airport_Cd")
    public List<AWBPropertySO> getDeparture_Airport_Cd() {
        return Departure_Airport_Cd;
    }

    public void setDeparture_Airport_Cd(List<AWBPropertySO> departure_Airport_Cd) {
        Departure_Airport_Cd = departure_Airport_Cd;
    }
    @JsonProperty("Destination_Airport_Cd")
    public List<AWBPropertySO> getDestination_Airport_Cd() {
        return Destination_Airport_Cd;
    }

    public void setDestination_Airport_Cd(List<AWBPropertySO> destination_Airport_Cd) {
        Destination_Airport_Cd = destination_Airport_Cd;
    }
    @JsonProperty("Nature_of_Goods")
    public List<AWBPropertySO> getNature_of_Goods() {
        return Nature_of_Goods;
    }

    public void setNature_of_Goods(List<AWBPropertySO> nature_of_Goods) {
        Nature_of_Goods = nature_of_Goods;
    }
    @JsonProperty("Issued_By")
    public List<AWBPropertySO> getIssued_By() {
        return Issued_By;
    }

    public void setIssued_By(List<AWBPropertySO> issued_By) {
        Issued_By = issued_By;
    }
    @JsonProperty("Shipper_Address")
    public List<AWBPropertySO> getShipper_Address() {
        return Shipper_Address;
    }

    public void setShipper_Address(List<AWBPropertySO> shipper_Address) {
        Shipper_Address = shipper_Address;
    }
    @JsonProperty("Shipper_Name")
    public List<AWBPropertySO> getShipper_Name() {
        return Shipper_Name;
    }

    public void setShipper_Name(List<AWBPropertySO> shipper_Name) {
        Shipper_Name = shipper_Name;
    }
}
