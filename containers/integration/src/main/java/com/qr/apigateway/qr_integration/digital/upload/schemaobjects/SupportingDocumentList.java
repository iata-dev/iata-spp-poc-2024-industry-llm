package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.ArrayList;
import java.util.List;

public class SupportingDocumentList {

    private List<EDocFileTypeSO> documentList=new ArrayList<EDocFileTypeSO>();

    public List<EDocFileTypeSO> getDocumentList() {
        return documentList;
    }

    public void setDocumentList(List<EDocFileTypeSO> documentList) {
        this.documentList = documentList;
    }
}
