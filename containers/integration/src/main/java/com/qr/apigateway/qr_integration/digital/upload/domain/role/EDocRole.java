package com.qr.apigateway.qr_integration.digital.upload.domain.role;


import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;

import java.io.IOException;
import java.sql.SQLException;

public interface EDocRole {
    EdocResponseSO uploadAwbSupportiveFileTypes(EdocRequestSO eDocRequestSO) throws SQLException, IOException;
    EdocResponseSO uploadAWB(EdocRequestSO eDocRequestSO) throws SQLException, IOException;
    //AwbDataListSO getAwbByDocType(AwbDataSearchSO awbDataSearchSO) throws Exception;
    //AwbSupportiveDocSOList getAwbSupportiveDocTypes(AwbSupportiveDocSO awbSupportiveDocSO);
    UploadAwbRespSOList uploadAwb(UploadAWBSO uploadAWBSO) throws SQLException;
    UploadAwbRespSOList uploadSuppAwb(UploadSuppDocSO uploadSuppDocSO) throws SQLException;
}
