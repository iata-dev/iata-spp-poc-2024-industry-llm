package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.List;

public class ValidateDocSO {
    private List<String> list_of_mandatory_documents;
    private List<UploadAWBSO> files;

    public List<String> getList_of_mandatory_documents() {
        return list_of_mandatory_documents;
    }

    public void setList_of_mandatory_documents(List<String> list_of_mandatory_documents) {
        this.list_of_mandatory_documents = list_of_mandatory_documents;
    }

    public List<UploadAWBSO> getFiles() {
        return files;
    }

    public void setFiles(List<UploadAWBSO> files) {
        this.files = files;
    }
}
