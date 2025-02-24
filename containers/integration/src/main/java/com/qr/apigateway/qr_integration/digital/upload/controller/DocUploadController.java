package com.qr.apigateway.qr_integration.digital.upload.controller;


import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;
import com.qr.apigateway.qr_integration.digital.upload.services.EDocService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("/awb")
public class DocUploadController {

    @GetMapping("/testApp")
    public String test() {
        log.info("Inside the awbUpload method...");
        return "Server up and running";
    }

    @Autowired
    private EDocService eDocService;
    private static final Logger log = LoggerFactory.getLogger(DocUploadController.class);
    @PostMapping("/upload")
    public EdocResponseSO awbUpload(@RequestBody EdocRequestSO eDocRequestSO) throws SQLException, IOException {
        if(eDocRequestSO.getSource().equalsIgnoreCase("snowflake")){
            log.info("Inside the awbUpload method Snowflake...");
            return eDocService.awbUpload(eDocRequestSO);
        }else{
            UploadAWBSO uploadAWBSO=new UploadAWBSO();
            uploadAWBSO.setFiledata(eDocRequestSO.getFileSOs().get(0).getFileData());
            uploadAWBSO.setFilename(eDocRequestSO.getFileSOs().get(0).getFileName());
            uploadAWBSO.setFiletype(eDocRequestSO.getFileSOs().get(0).getFileType());
            UploadAwbRespSOList uploadAwbRespSOList=eDocService.uploadAwb(uploadAWBSO);
            EdocResponseSO edocresponseSO=new EdocResponseSO();
            edocresponseSO.getErrorDetails().add(uploadAwbRespSOList.getErrorSO());
            edocresponseSO.seteDocFileTypeSOS(new ArrayList<EDocFileTypeSO>());
            uploadAwbRespSOList.getUploadAwbRespSO().getRequiredDocuments().forEach(e-> {
                EDocFileTypeSO eDocFileTypeSO=new EDocFileTypeSO();
                eDocFileTypeSO.setMandateFlag("Y");
                eDocFileTypeSO.setName(e);
                eDocFileTypeSO.setFileType(e);
                edocresponseSO.geteDocFileTypeSOS().add(eDocFileTypeSO);

            });
            return edocresponseSO;
        }

    }


    @PostMapping("/uploadSupportingDocuments")
    public EdocResponseSO uploadAwbSupportiveFileTypes(@RequestBody EdocRequestSO eDocRequestSO) throws SQLException, IOException {
        log.info("Inside the uploadAwbSupportiveFileTypes method...");
        return eDocService.uploadAwbSupportiveFileTypes(eDocRequestSO);
    }

    @RequestMapping(value="/main", method= RequestMethod.GET)
    public String index() {return "index.html";}

    @PostMapping("/uploadAwb")
    public UploadAwbRespSOList uploadAwb(@RequestBody UploadAWBSO uploadAWBSO)  throws SQLException{
        log.info("Inside the uploadAwb method...");
        return eDocService.uploadAwb(uploadAWBSO);
    }

    @PostMapping("/uploadSupDocs")
    public UploadAwbRespSOList uploadSuppAwb(@RequestBody UploadSuppDocSO uploadSuppDocSO)  throws SQLException{
        log.info("Inside the validateDocs method...");
        return eDocService.uploadSuppAwb(uploadSuppDocSO);
    }
}
