package com.qr.apigateway.qr_integration.digital.upload.services.impl;



import com.qr.apigateway.qr_integration.digital.upload.domain.role.EDocRole;
import com.qr.apigateway.qr_integration.digital.upload.domain.role.impl.EDocValidation;
import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;
import com.qr.apigateway.qr_integration.digital.upload.services.EDocService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.sql.SQLException;

@Service
public class EDocServiceImpl implements EDocService {


    @Autowired
    EDocRole eDocRole;
    private static final Logger log = LoggerFactory.getLogger(EDocServiceImpl.class);
    private EDocValidation eDocValidation;
    @Override
    public EdocResponseSO awbUpload(EdocRequestSO eDocRequestSO) throws SQLException, IOException {
        return eDocRole.uploadAWB(eDocRequestSO);
    }

    @Override
    public EdocResponseSO uploadAwbSupportiveFileTypes(EdocRequestSO eDocRequestSO) throws SQLException, IOException {

        return eDocRole.uploadAwbSupportiveFileTypes(eDocRequestSO);
    }

    @Override
    public UploadAwbRespSOList uploadAwb(UploadAWBSO uploadAWBSO) throws SQLException{
        return eDocRole.uploadAwb(uploadAWBSO);
    }

    @Override
    public UploadAwbRespSOList uploadSuppAwb(UploadSuppDocSO uploadSuppDocSO) throws SQLException {
        return eDocRole.uploadSuppAwb(uploadSuppDocSO);
    }

    /*@Override
    public AwbDataListSO getAwbByDocType(AwbDataSearchSO awbDataSearchSO) throws Exception {
        return eDocRole.getAwbByDocType(awbDataSearchSO);
    }*/

    /*@Override
    public AwbSupportiveDocSOList getAwbSupportiveDocTypes(AwbSupportiveDocSO awbSupportiveDocSO) {
        return eDocRole.getAwbSupportiveDocTypes(awbSupportiveDocSO);
    }*/
}
