package com.qr.apigateway.qr_integration.digital.upload.services;



import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;
import org.springframework.web.bind.annotation.RequestBody;

import java.io.IOException;
import java.sql.SQLException;

public interface EDocService {

    EdocResponseSO awbUpload(EdocRequestSO eDocRequestSO) throws SQLException, IOException;
    EdocResponseSO uploadAwbSupportiveFileTypes(EdocRequestSO eDocRequestSO) throws SQLException, IOException;
    //AwbDataListSO getAwbByDocType(AwbDataSearchSO awbDataSearchSO) throws Exception;
    //AwbSupportiveDocSOList getAwbSupportiveDocTypes(AwbSupportiveDocSO awbSupportiveDocSO);
    UploadAwbRespSOList uploadAwb(UploadAWBSO uploadAWBSO) throws SQLException;
    UploadAwbRespSOList uploadSuppAwb(UploadSuppDocSO uploadSuppDocSO) throws SQLException;
}
