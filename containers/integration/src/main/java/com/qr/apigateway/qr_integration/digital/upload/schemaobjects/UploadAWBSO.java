package com.qr.apigateway.qr_integration.digital.upload.schemaobjects;

import java.util.List;

public class UploadAWBSO {
    private String filename;
    private String filedata;
    private String filetype;

    public UploadAWBSO() {

    }

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getFiledata() {
        return filedata;
    }

    public void setFiledata(String filedata) {
        this.filedata = filedata;
    }

    public String getFiletype() {
        return filetype;
    }

    public void setFiletype(String filetype) {
        this.filetype = filetype;
    }
}
