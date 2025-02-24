package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

public class ValidateDocRespSO {
    private UploadAwbRespSO awb;
    private ConincidenceSO conincidence;
    private String mindocsrequirementmet;
    private PhytoSO phyto;
    private String message;
    private String status;

    public UploadAwbRespSO getAwb() {
        return awb;
    }

    public void setAwb(UploadAwbRespSO awb) {
        this.awb = awb;
    }

    public ConincidenceSO getConincidence() {
        return conincidence;
    }

    public void setConincidence(ConincidenceSO conincidence) {
        this.conincidence = conincidence;
    }

    public String getMindocsrequirementmet() {
        return mindocsrequirementmet;
    }

    public void setMindocsrequirementmet(String mindocsrequirementmet) {
        this.mindocsrequirementmet = mindocsrequirementmet;
    }

    public PhytoSO getPhyto() {
        return phyto;
    }

    public void setPhyto(PhytoSO phyto) {
        this.phyto = phyto;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
