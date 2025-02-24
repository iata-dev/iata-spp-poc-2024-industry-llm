package com.qr.apigateway.qr_integration.digital.upload.domain.role.impl;


import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
@Component
public class EDocValidation {

    public EdocResponseSO validateSupportiveFileTypeRequest(EdocRequestSO eDocRequestSO, EdocResponseSO eDocResponseSO) {
        List<ErrorSO> errorSOList = new ArrayList<ErrorSO>();
        if(eDocRequestSO.getCommodity()==null) {
            ErrorSO errorSO = new ErrorSO();
            errorSO.setErrorId("Please provide Commodity details");
            errorSO.setErrorMessage("Commodity cannot be null...");
            errorSOList.add(errorSO);
        }
        if(eDocRequestSO.getDest()==null) {
            ErrorSO errorSO = new ErrorSO();
            errorSO.setErrorId("Please provide Destination details");
            errorSO.setErrorMessage("Destination cannot be null...");
            errorSOList.add(errorSO);
        }
        if(eDocRequestSO.getOrigin()==null) {
            ErrorSO errorSO = new ErrorSO();
            errorSO.setErrorId("Please provide Origin details");
            errorSO.setErrorMessage("Origin cannot be null...");
            errorSOList.add(errorSO);
        }
        if(eDocRequestSO.getNatureOfGood()==null) {
            ErrorSO errorSO = new ErrorSO();
            errorSO.setErrorId("Please provide NatureOfGood details");
            errorSO.setErrorMessage("NatureOfGood cannot be null...");
            errorSOList.add(errorSO);
        }
        eDocResponseSO.setErrorDetails(errorSOList);
        return eDocResponseSO;
    }
}
