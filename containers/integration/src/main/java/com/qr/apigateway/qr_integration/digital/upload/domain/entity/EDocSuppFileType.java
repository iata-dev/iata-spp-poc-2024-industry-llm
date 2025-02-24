package com.qr.apigateway.qr_integration.digital.upload.domain.entity;

import java.util.Objects;

//@Entity
//@Table(name="DOC_SPRT_FILTYP",schema="api_ownr")
public class EDocSuppFileType {
    //@Id
   // @Column(name="SPT_FILTYP_id",nullable = false)
    private Long sptFilTypeId;
    //@Column(name="orig")
    private String origin;
    //@Column(name="dest")
    private String destination;
    //@Column(name="commodity")
    private String commodity;
    //@Column(name="natureOfGood")
    private String natureOfGoods;
    //@Column(name="spt_File_Type")
    private String supportiveFileType;
    //@Column(name="mandate_ind")
    private boolean mandateFlag;


}
