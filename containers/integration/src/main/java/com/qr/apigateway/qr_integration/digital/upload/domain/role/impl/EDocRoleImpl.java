package com.qr.apigateway.qr_integration.digital.upload.domain.role.impl;


import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.qr.apigateway.qr_integration.digital.upload.domain.helper.AzureInteg;
import com.qr.apigateway.qr_integration.digital.upload.domain.role.EDocRole;
import com.qr.apigateway.qr_integration.digital.upload.domain.util.JsonUtil;
import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;
import com.qr.apigateway.qr_integration.snowflake.SnowFlakeInteg;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ResourceLoader;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.sql.*;
import java.util.*;
import java.util.Date;

@Component
public class EDocRoleImpl implements EDocRole {

    private static final Logger log = LoggerFactory.getLogger(EDocRoleImpl.class);


    @Autowired
    private ResourceLoader resourceLoader;

    @Autowired
    private AzureInteg azureInteg;

    @Autowired
    private RestTemplate restTemplate;

    @Value("${amazon.service.url}")
    private String url;

    private static final Map<String, String> cityCountryMap = new HashMap<String, String>();
    private static final Map<String, String> carCodeMap = new HashMap<String, String>();
    private static final Map<String, String> countryMap = new HashMap<String, String>();

    static {
        //for localhost testing only
        javax.net.ssl.HttpsURLConnection.setDefaultHostnameVerifier(
                new javax.net.ssl.HostnameVerifier() {

                    @Override
                    public boolean verify(String hostname,
                                          javax.net.ssl.SSLSession sslSession) {
                        if (hostname.equals("ec2-13-41-229-168.eu-west-2.compute.amazonaws.com")) {
                            return true;
                        }
                        return false;
                    }
                });
    }

    public EDocRoleImpl() {
        cityCountryMap.put("US", "ATL");
        cityCountryMap.put("ATL", "US");
        cityCountryMap.put("LHR","GB");
        cityCountryMap.put("FRA", "DE");
        cityCountryMap.put("CDG", "FR");
        cityCountryMap.put("FCO", "IT");
        cityCountryMap.put("HND", "JP");
        cityCountryMap.put("SYD", "AU");
        cityCountryMap.put("PEK", "CN");
        cityCountryMap.put("DEL", "IN");
        cityCountryMap.put("GRU", "BR");
        cityCountryMap.put("ICN", "KR");
        cityCountryMap.put("SVO", "RU");
        cityCountryMap.put("CAN", "CA");
        cityCountryMap.put("JNB", "ZA");
        cityCountryMap.put("CUN", "MX");
        cityCountryMap.put("BOM", "IN");
        cityCountryMap.put("DOH", "QA");
        cityCountryMap.put("ELDORADO AIRPORT BOGOTA, COLOMBIA", "CO");
        cityCountryMap.put("MADRID", "ES");
        cityCountryMap.put("SUVARNABHUMI AIRPORT THAILAND","TH");
        cityCountryMap.put("NARITA AIRPORT","JP");
        cityCountryMap.put("EL DORADO, BOGOTA D.C., COLOMBIA","CO");
        cityCountryMap.put("SANTIAGO","CL");
        cityCountryMap.put("SANTIAGO DE CHILE","CL");
        cityCountryMap.put("MARISCAL SUCRE - UIO","EC");
        cityCountryMap.put("AMSTERDAM HOLLAND","NL");


        carCodeMap.put("157","QR");
        carCodeMap.put("125","BA");
        carCodeMap.put("001","AA");
        carCodeMap.put("045","LA");


            countryMap.put("AF", "Afghanistan");
            countryMap.put("AL", "Albania");
            countryMap.put("DZ", "Algeria");
            countryMap.put("AS", "American Samoa");
            countryMap.put("AD", "Andorra");
            countryMap.put("AO", "Angola");
            countryMap.put("AI", "Anguilla");
            countryMap.put("AQ", "Antarctica");
            countryMap.put("AG", "Antigua and Barbuda");
            countryMap.put("AR", "Argentina");
            countryMap.put("AM", "Armenia");
            countryMap.put("AW", "Aruba");
            countryMap.put("AU", "Australia");
            countryMap.put("AT", "Austria");
            countryMap.put("AZ", "Azerbaijan");
            countryMap.put("BS", "Bahamas");
            countryMap.put("BH", "Bahrain");
            countryMap.put("BD", "Bangladesh");
            countryMap.put("BB", "Barbados");
            countryMap.put("BY", "Belarus");
            countryMap.put("BE", "Belgium");
            countryMap.put("BZ", "Belize");
            countryMap.put("BJ", "Benin");
            countryMap.put("BM", "Bermuda");
            countryMap.put("BT", "Bhutan");
            countryMap.put("BO", "Bolivia");
            countryMap.put("BA", "Bosnia and Herzegovina");
            countryMap.put("BW", "Botswana");
            countryMap.put("BV", "Bouvet Island");
            countryMap.put("BR", "Brazil");
            countryMap.put("IO", "British Indian Ocean Territory");
            countryMap.put("BN", "Brunei Darussalam");
            countryMap.put("BG", "Bulgaria");
            countryMap.put("BF", "Burkina Faso");
            countryMap.put("BI", "Burundi");
            countryMap.put("CV", "Cabo Verde");
            countryMap.put("KH", "Cambodia");
            countryMap.put("CM", "Cameroon");
            countryMap.put("CA", "Canada");
            countryMap.put("KY", "Cayman Islands");
            countryMap.put("CF", "Central African Republic");
            countryMap.put("TD", "Chad");
            countryMap.put("CL", "Chile");
            countryMap.put("CN", "China");
            countryMap.put("CX", "Christmas Island");
            countryMap.put("CC", "Cocos (Keeling) Islands");
            countryMap.put("CO", "Colombia");
            countryMap.put("KM", "Comoros");
            countryMap.put("CG", "Congo (Brazzaville)");
            countryMap.put("CD", "Congo (Kinshasa)");
            countryMap.put("CK", "Cook Islands");
            countryMap.put("CR", "Costa Rica");
            countryMap.put("CI", "Côte d'Ivoire");
            countryMap.put("HR", "Croatia");
            countryMap.put("CU", "Cuba");
            countryMap.put("CY", "Cyprus");
            countryMap.put("CZ", "Czech Republic");
            countryMap.put("DK", "Denmark");
            countryMap.put("DJ", "Djibouti");
            countryMap.put("DM", "Dominica");
            countryMap.put("DO", "Dominican Republic");
            countryMap.put("EC", "Ecuador");
            countryMap.put("EG", "Egypt");
            countryMap.put("SV", "El Salvador");
            countryMap.put("GQ", "Equatorial Guinea");
            countryMap.put("ER", "Eritrea");
            countryMap.put("EE", "Estonia");
            countryMap.put("SZ", "Eswatini");
            countryMap.put("ET", "Ethiopia");
            countryMap.put("FK", "Falkland Islands");
            countryMap.put("FO", "Faroe Islands");
            countryMap.put("FJ", "Fiji");
            countryMap.put("FI", "Finland");
            countryMap.put("FR", "France");
            countryMap.put("GF", "French Guiana");
            countryMap.put("PF", "French Polynesia");
            countryMap.put("TF", "French Southern Territories");
            countryMap.put("GA", "Gabon");
            countryMap.put("GM", "Gambia");
            countryMap.put("GE", "Georgia");
            countryMap.put("DE", "Germany");
            countryMap.put("GH", "Ghana");
            countryMap.put("GI", "Gibraltar");
            countryMap.put("GR", "Greece");
            countryMap.put("GL", "Greenland");
            countryMap.put("GD", "Grenada");
            countryMap.put("GP", "Guadeloupe");
            countryMap.put("GU", "Guam");
            countryMap.put("GT", "Guatemala");
            countryMap.put("GG", "Guernsey");
            countryMap.put("GN", "Guinea");
            countryMap.put("GW", "Guinea-Bissau");
            countryMap.put("GY", "Guyana");
            countryMap.put("HT", "Haiti");
            countryMap.put("HM", "Heard Island and McDonald Islands");
            countryMap.put("VA", "Holy See");
            countryMap.put("HN", "Honduras");
            countryMap.put("HK", "Hong Kong");
            countryMap.put("HU", "Hungary");
            countryMap.put("IS", "Iceland");
            countryMap.put("IN", "India");
            countryMap.put("ID", "Indonesia");
            countryMap.put("IR", "Iran");
            countryMap.put("IQ", "Iraq");
            countryMap.put("IE", "Ireland");
            countryMap.put("IM", "Isle of Man");
            countryMap.put("IL", "Israel");
            countryMap.put("IT", "Italy");
            countryMap.put("JM", "Jamaica");
            countryMap.put("JP", "Japan");
            countryMap.put("JE", "Jersey");
            countryMap.put("JO", "Jordan");
            countryMap.put("KZ", "Kazakhstan");
            countryMap.put("KE", "Kenya");
            countryMap.put("KI", "Kiribati");
            countryMap.put("KP", "North Korea");
            countryMap.put("KR", "South Korea");
            countryMap.put("KW", "Kuwait");
            countryMap.put("KG", "Kyrgyzstan");
            countryMap.put("LA", "Laos");
            countryMap.put("LV", "Latvia");
            countryMap.put("LB", "Lebanon");
            countryMap.put("LS", "Lesotho");
            countryMap.put("LR", "Liberia");
            countryMap.put("LY", "Libya");
            countryMap.put("LI", "Liechtenstein");
            countryMap.put("LT", "Lithuania");
            countryMap.put("LU", "Luxembourg");
            countryMap.put("MO", "Macau");
            countryMap.put("MG", "Madagascar");
            countryMap.put("MW", "Malawi");
            countryMap.put("MY", "Malaysia");
            countryMap.put("MV", "Maldives");
            countryMap.put("ML", "Mali");
            countryMap.put("MT", "Malta");
            countryMap.put("MH", "Marshall Islands");
            countryMap.put("MQ", "Martinique");
            countryMap.put("MR", "Mauritania");
            countryMap.put("MU", "Mauritius");
            countryMap.put("YT", "Mayotte");
            countryMap.put("MX", "Mexico");
            countryMap.put("FM", "Micronesia");
            countryMap.put("MD", "Moldova");
            countryMap.put("MC", "Monaco");
            countryMap.put("MN", "Mongolia");
            countryMap.put("ME", "Montenegro");
            countryMap.put("MS", "Montserrat");
            countryMap.put("MA", "Morocco");
            countryMap.put("MZ", "Mozambique");
            countryMap.put("MM", "Myanmar");
            countryMap.put("NA", "Namibia");
            countryMap.put("NR", "Nauru");
            countryMap.put("NP", "Nepal");
            countryMap.put("NL", "Netherlands");
            countryMap.put("NC", "New Caledonia");
            countryMap.put("NZ", "New Zealand");
            countryMap.put("NI", "Nicaragua");
            countryMap.put("NE", "Niger");
            countryMap.put("NG", "Nigeria");
            countryMap.put("NU", "Niue");
            countryMap.put("NF", "Norfolk Island");
            countryMap.put("MP", "Northern Mariana Islands");
            countryMap.put("NO", "Norway");
            countryMap.put("OM", "Oman");
            countryMap.put("PK", "Pakistan");
            countryMap.put("PW", "Palau");
            countryMap.put("PS", "Palestinian Territory");
            countryMap.put("PA", "Panama");
            countryMap.put("PG", "Papua New Guinea");
            countryMap.put("PY", "Paraguay");
            countryMap.put("PE", "Peru");
            countryMap.put("PH", "Philippines");
            countryMap.put("PN", "Pitcairn");
            countryMap.put("PL", "Poland");
            countryMap.put("PT", "Portugal");
            countryMap.put("PR", "Puerto Rico");
            countryMap.put("QA", "Qatar");
            countryMap.put("RE", "Réunion");
            countryMap.put("RO", "Romania");
            countryMap.put("RU", "Russia");
            countryMap.put("RW", "Rwanda");
            countryMap.put("BL", "Saint Barthélemy");
            countryMap.put("SH", "Saint Helena, Ascension and Tristan da Cunha");
            countryMap.put("KN", "Saint Kitts and Nevis");
            countryMap.put("LC", "Saint Lucia");
            countryMap.put("MF", "Saint Martin (French part)");
            countryMap.put("PM", "Saint Pierre and Miquelon");
            countryMap.put("VC", "Saint Vincent and the Grenadines");
            countryMap.put("WS", "Samoa");
            countryMap.put("SM", "San Marino");
            countryMap.put("ST", "São Tomé and Príncipe");
            countryMap.put("SA", "Saudi Arabia");
            countryMap.put("SN", "Senegal");
            countryMap.put("RS", "Serbia");
            countryMap.put("SC", "Seychelles");
            countryMap.put("SL", "Sierra Leone");
            countryMap.put("SG", "Singapore");
            countryMap.put("SX", "Sint Maarten (Dutch part)");
            countryMap.put("SK", "Slovakia");
            countryMap.put("SI", "Slovenia");
            countryMap.put("SB", "Solomon Islands");
            countryMap.put("SO", "Somalia");
            countryMap.put("ZA", "South Africa");
            countryMap.put("GS", "South Georgia and the South Sandwich Islands");
            countryMap.put("SS", "South Sudan");
            countryMap.put("ES", "Spain");
            countryMap.put("LK", "Sri Lanka");
            countryMap.put("SD", "Sudan");
            countryMap.put("SR", "Suriname");
            countryMap.put("SJ", "Svalbard and Jan Mayen");
            countryMap.put("SE", "Sweden");
            countryMap.put("CH", "Switzerland");
            countryMap.put("SY", "Syria");
            countryMap.put("TW", "Taiwan");
            countryMap.put("TJ", "Tajikistan");
            countryMap.put("TZ", "Tanzania");
            countryMap.put("TH", "Thailand");
            countryMap.put("TL", "Timor-Leste");
            countryMap.put("TG", "Togo");
            countryMap.put("TK", "Tokelau");
            countryMap.put("TO", "Tonga");
            countryMap.put("TT", "Trinidad and Tobago");
            countryMap.put("TN", "Tunisia");
            countryMap.put("TR", "Turkey");
            countryMap.put("TM", "Turkmenistan");
            countryMap.put("TC", "Turks and Caicos Islands");
            countryMap.put("TV", "Tuvalu");
            countryMap.put("UG", "Uganda");
            countryMap.put("UA", "Ukraine");
            countryMap.put("AE", "United Arab Emirates");
            countryMap.put("GB", "United Kingdom");
            countryMap.put("US", "United States");
            countryMap.put("UM", "United States Minor Outlying Islands");
            countryMap.put("UY", "Uruguay");
            countryMap.put("UZ", "Uzbekistan");
            countryMap.put("VU", "Vanuatu");
            countryMap.put("VE", "Venezuela");
            countryMap.put("VN", "Vietnam");
            countryMap.put("VG", "Virgin Islands, British");
            countryMap.put("VI", "Virgin Islands, U.S.");
            countryMap.put("WF", "Wallis and Futuna");
            countryMap.put("EH", "Western Sahara");
            countryMap.put("YE", "Yemen");
            countryMap.put("ZM", "Zambia");
            countryMap.put("ZW", "Zimbabwe");


    }

    @Override
    public EdocResponseSO uploadAwbSupportiveFileTypes(EdocRequestSO eDocRequestSO) throws SQLException, IOException {
        EdocResponseSO edocResponseSO=new EdocResponseSO();
        List<ErrorSO> errorSOList = new ArrayList<ErrorSO>();
        if(eDocRequestSO.getFileSOs()!=null && !eDocRequestSO.getFileSOs().isEmpty()) {
            FileSO fileSO = eDocRequestSO.getFileSOs().get(0);
            if(null!=fileSO && (fileSO.getFileData()==null || fileSO.getFileData().isBlank()) ) {
                ErrorSO errorSO = new ErrorSO();
                errorSO.setErrorId("Invalid Data");
                errorSO.setErrorMessage("FileData shared is empty..");
                errorSOList.add(errorSO);
            }
            else if ( eDocRequestSO.getSessionId()==null){
                ErrorSO errorSO = new ErrorSO();
                errorSO.setErrorId("Invalid session");
                errorSO.setErrorMessage("Invalid session");
                errorSOList.add(errorSO);
            }
            else {

                ClassLoader classLoader = getClass().getClassLoader();
                AwbDataListSO awbDataListSO=null;
                String fileName=Calendar.getInstance().getTimeInMillis()+"_"+eDocRequestSO.getFileSOs().get(0).getFileName();
                try {
                    awbDataListSO = azureInteg.getAwbDataByDocType(eDocRequestSO.getSessionId(),"AWB");
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
                if(awbDataListSO==null || awbDataListSO.getAwbDataSOList()==null || awbDataListSO.getAwbDataSOList().size()==0){
                    ErrorSO errorSO = new ErrorSO();
                    errorSO.setErrorId("Invalid session");
                    errorSO.setErrorMessage("Invalid session");
                    errorSOList.add(errorSO);

                    edocResponseSO.setErrorDetails(errorSOList);
                    return edocResponseSO;
                }
                byte[] decodedFile = Base64.getDecoder().decode(eDocRequestSO.getFileSOs().get(0).getFileData().getBytes(StandardCharsets.UTF_8));
               // File file = new File(resourceLoader.getResource(".").getFile()+"/" + fileName);
                log.info(("classLoader.getResourcegetFile() "+classLoader.getResource(".").getFile()) );

                try (OutputStream stream = new FileOutputStream(classLoader.getResource(".").getFile() +fileName)) {
                    stream.write(decodedFile);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                String filePath=classLoader.getResource(".").getFile() +fileName;
                SnowFlakeInteg snowFlakeInteg=new SnowFlakeInteg();
                Connection connection = snowFlakeInteg.getConnection();
                Statement statement = connection.createStatement();
             //   ResultSet pcrJSON =  statement.executeQuery("CALL CHECK_DOC_TYPE(\'"+fileName+"\')");

                PhytoCertDetailsSO phytoData =null;
                try {

                    statement = connection.createStatement();
                    ResultSet resultSet =  statement.executeQuery("PUT file://"+filePath+" @DOCS AUTO_COMPRESS=FALSE;");

                    Statement query = connection.createStatement();
                    ResultSet phytoJsonJSON =  statement.executeQuery("SELECT parse_json(PCR!PREDICT(GET_PRESIGNED_URL(@DOCS,\'"+fileName+"\'))) as output");
                    ResultSetMetaData resultSetMetaData = phytoJsonJSON.getMetaData();
                    System.out.println("Number of columns=" + resultSetMetaData.getColumnCount());

                    int rowIdx = 0;
                    int docId=0;
                    while (phytoJsonJSON.next()) {
                        System.out.println("row " + rowIdx + ", column 0: " + phytoJsonJSON.getString(1));
                        ObjectMapper mapper = new ObjectMapper();
                        //while (phytoJsonJSON.next()) {
                            System.out.println("row " + rowIdx + ", column 0: " + phytoJsonJSON.getString(1));

                            phytoData = mapper.readValue(phytoJsonJSON.getString(1), PhytoCertDetailsSO.class);
                            System.out.println("row " + rowIdx + ", column 0: " + phytoJsonJSON.getString(1));
                            List<ErrorSO> errorSOS =new ArrayList<ErrorSO>();
                            String insertString = convertPhytoSOToEntity(phytoData, eDocRequestSO.getSessionId(), errorSOS);
                            if(errorSOS.isEmpty()) {
                                try {
                                    docId = azureInteg.insertSupportingData(insertString);
                                    if(docId==0) {
                                        errorSOS.add(setErrorSOObj("Insert","Failed"));
                                        edocResponseSO.setErrorDetails(errorSOS);
                                    }
                                } catch (Exception e) {
                                    throw new RuntimeException(e);
                                }
                            }
                            else{
                                edocResponseSO.setErrorDetails(errorSOS);
                            }
                        //}
                    }
                   List<ErrorSO> errLst= compareAWBAndPhyto(eDocRequestSO.getSessionId(),docId);
                    if(errLst.size()>0){
                        errorSOList.addAll(errLst);
                        updateAwbDocList(awbDataListSO.getAwbDataSOList().get(0).getId(), "Y","N",errLst.get(0).getErrorMessage());
                    }
                    else {
                        updateAwbDocList(awbDataListSO.getAwbDataSOList().get(0).getId(), "Y","Y","Validated & verified all supporting documents against AWB");
                    }
                    //                    log.info("awbJSON.getString(0)"+awbJSON.getString(0));
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }


            }

        }


        edocResponseSO.setErrorDetails(errorSOList);
        edocResponseSO.setResponseMsg("Validated & verified all supporting documents against AWB");
        edocResponseSO.setSessionId(eDocRequestSO.getSessionId());
        if(errorSOList.size()>0){
            edocResponseSO.setResponseMsg("Supporting document validation failed");


        }
        return edocResponseSO;
    }

    public String convertPhytoSOToEntity(PhytoCertDetailsSO phytoCertDetailsSO, String sessionId, List<ErrorSO> errorSOList) {
        StringBuilder insQuery = new StringBuilder("INSERT INTO dbo.AWB_DATA (id, consigneeName, execDate, shipperName, natureOfGoods, pieces, origin, destination, qrCode, weight, stamp, sessionId, docType)\n" +
                "VALUES (NEXT VALUE FOR awbDataSeq , '");

        if(null!=phytoCertDetailsSO.getConsignee() &&
                !phytoCertDetailsSO.getConsignee().isEmpty()) {
            String cosineName = phytoCertDetailsSO.getConsignee().get(0).getValue().replaceAll("[^a-zA-Z]+","");
            insQuery.append(cosineName);
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Consignee Name","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getDate() &&
                !phytoCertDetailsSO.getDate().isEmpty()) {
            insQuery.append(phytoCertDetailsSO.getDate().get(0).getValue());
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Execution Date","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getExporter() &&
                !phytoCertDetailsSO.getExporter().isEmpty()) {

            String shipperName = phytoCertDetailsSO.getExporter().get(0).getValue().replaceAll("[^a-zA-Z]+","");
            insQuery.append(shipperName);
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Shipper Name","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getName_of_Produce() &&
                !phytoCertDetailsSO.getName_of_Produce().isEmpty()) {
            String natureOfGood = phytoCertDetailsSO.getName_of_Produce().get(0).getValue().replaceAll("[^a-zA-Z]+","");
            insQuery.append(natureOfGood);
            insQuery.append("',");
        }
        else {
            errorSOList.add(setErrorSOObj("Name of Produce","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getPackaging() &&
                !phytoCertDetailsSO.getPackaging().isEmpty()) {
            if(phytoCertDetailsSO.getPackaging().get(0).getValue().contains(" ")){
               ;
            }
            insQuery.append( phytoCertDetailsSO.getPackaging().get(0).getValue().split(" ")[0]);
            insQuery.append(",'");
        }
        else {
            errorSOList.add(setErrorSOObj("Packaging","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getPlace_of_Origin() &&
                !phytoCertDetailsSO.getPlace_of_Origin().isEmpty()) {
            String origin = phytoCertDetailsSO.getPlace_of_Origin().get(0).getValue().replaceAll("[^a-zA-Z]+","");
            insQuery.append(origin);
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Place of Origin","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getPoint_of_Entry() &&
                !phytoCertDetailsSO.getPoint_of_Entry().isEmpty()) {
            String destination = phytoCertDetailsSO.getPoint_of_Entry().get(0).getValue().replaceAll("[^a-zA-Z]+","");
            insQuery.append(destination);
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Point Of Entry","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getQR_Code() &&
                !phytoCertDetailsSO.getQR_Code().isEmpty()) {
            String qrCode = phytoCertDetailsSO.getQR_Code().get(0).getValue().replaceAll("[^a-zA-Z]+","");
            insQuery.append(qrCode);
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("QR Code","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getQuantity_Declared() &&
                !phytoCertDetailsSO.getQuantity_Declared().isEmpty()) {
            String qrCode = phytoCertDetailsSO.getQuantity_Declared().get(0).getValue().replace(",","");
            qrCode = qrCode.replace(" ","");
            insQuery.append(qrCode);
         //   insQuery.append(phytoCertDetailsSO.getQuantity_Declared().getFirst().getValue());
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Quantity Declared","Data Missing"));
        }
        if(null!=phytoCertDetailsSO.getStamp() &&
                !phytoCertDetailsSO.getStamp().isEmpty()) {
            insQuery.append(phytoCertDetailsSO.getStamp().get(0).getValue().replaceAll(" ",""));
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("Stamp","Data Missing"));
        }

        insQuery.append(sessionId).append("','");
        if(errorSOList.isEmpty()){
            insQuery.append("PHYTO'");
            insQuery.append(")");
        }
        return insQuery.toString();
    }
    @Override
    public EdocResponseSO uploadAWB(EdocRequestSO eDocRequestSO) throws SQLException, IOException {
        EdocResponseSO eDocResponseSO = new EdocResponseSO();

        List<ErrorSO> errorSOList = new ArrayList<ErrorSO>();
        if(eDocRequestSO.getFileSOs()!=null && !eDocRequestSO.getFileSOs().isEmpty()) {
            FileSO fileSO = eDocRequestSO.getFileSOs().get(0);
            if(null!=fileSO && (fileSO.getFileData()==null || fileSO.getFileData().isBlank())) {
                ErrorSO errorSO = new ErrorSO();
                errorSO.setErrorId("Invalid Data");
                errorSO.setErrorMessage("FileData shared is empty..");
                errorSOList.add(errorSO);
            }
            else{


                ClassLoader classLoader = getClass().getClassLoader();
                ObjectMapper mapper = new ObjectMapper();
                String fileName=Calendar.getInstance().getTimeInMillis()+"_"+eDocRequestSO.getFileSOs().get(0).getFileName();
                byte[] decodedFile = Base64.getDecoder().decode(eDocRequestSO.getFileSOs().get(0).getFileData().getBytes(StandardCharsets.UTF_8));
                // File file = new File(classLoader.getResource(".").getFile() + eDocRequestSO.getFileSOs().get(0).getFileName());
                log.info(("classLoader.getResourcegetFile() "+classLoader.getResource(".").getFile()) );
                try (OutputStream stream = new FileOutputStream(classLoader.getResource(".").getFile() +fileName)) {
                    stream.write(decodedFile);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                String sessionId = UUID.randomUUID().toString();
                log.info("Generated Session Id: "+sessionId);
                eDocResponseSO.setSessionId(sessionId);
                LLMRequestSO llmRequestSO = new LLMRequestSO();
                llmRequestSO.setSessionId(sessionId);
                llmRequestSO.setFileSOs(new ArrayList<FileSO>());
                eDocResponseSO.seteDocFileTypeSOS(new ArrayList<EDocFileTypeSO>());

                String filePath=classLoader.getResource(".").getFile() +fileName;
                SnowFlakeInteg snowFlakeInteg=new SnowFlakeInteg();
                Connection connection = snowFlakeInteg.getConnection();
                AWBDetailsSO awbData =null;
                try {

                    Statement statement = connection.createStatement();
                    ResultSet resultSet =  statement.executeQuery("PUT file://"+filePath+" @DOCS AUTO_COMPRESS=FALSE;");

                    Statement query = connection.createStatement();
                    ResultSet awbJSON =  statement.executeQuery("SELECT parse_json(AWB_DOCAI!PREDICT(GET_PRESIGNED_URL(@DOCS,\'"+fileName+"\'))) as output");
                    ResultSetMetaData resultSetMetaData = awbJSON.getMetaData();
                    System.out.println("Number of columns=" + resultSetMetaData.getColumnCount());
                    for (int colIdx = 0; colIdx < resultSetMetaData.getColumnCount(); colIdx++) {
                        System.out.println(
                                "Column " + colIdx + ": type=" + resultSetMetaData.getColumnTypeName(colIdx + 1));
                    }
                    int rowIdx = 0;
                    while (awbJSON.next()) {
                        System.out.println("row " + rowIdx + ", column 0: " + awbJSON.getString(1));
                        byte[] jsonData = awbJSON.getString(1).toString().getBytes();

                         awbData = mapper.readValue(awbJSON.getString(1), AWBDetailsSO.class);
                        System.out.println("row " + rowIdx + ", column 0: " + awbJSON.getString(1));
                        List<ErrorSO> errorSOS =new ArrayList<ErrorSO>();
                        String insertString = convertSOToEntity(awbData, sessionId, errorSOS);
                        if(errorSOS.isEmpty()) {
                            try {
                                boolean insertFlag = azureInteg.insertData(insertString);
                                if(insertFlag) {
                                    AwbDataSearchSO awbDataSearchSO = new AwbDataSearchSO();
                                    awbDataSearchSO.setSessionId(sessionId);
                                    awbDataSearchSO.setDocType("AWB");
                                    AwbDataListSO awbDataListSO = getAwbByDocType(awbDataSearchSO);
                                    long awbDataId = 0;
                                    if(awbDataListSO!=null && !awbDataListSO.getAwbDataSOList().isEmpty()) {
                                        awbDataId = awbDataListSO.getAwbDataSOList().get(0).getId();
                                    }
                                    AwbSupportiveDocSO awbSupportiveDocSO = new AwbSupportiveDocSO("157", cityCountryMap.get(awbData.getDeparture_Airport_Cd().get(0).getValue()),
                                            cityCountryMap.get(awbData.getDestination_Airport_Cd().get(0).getValue()), awbData.getNature_of_Goods().get(0).getValue(),"");
                                    AwbSupportiveDocSOList awbSupportiveDocSOList= getAwbSupportiveDocTypes(awbSupportiveDocSO);
                                    if(null!=awbSupportiveDocSOList && !awbSupportiveDocSOList.getAwbSupportiveDocSOList().isEmpty()) {
                                        for(AwbSupportiveDocSO awbSupportiveDocSOObj: awbSupportiveDocSOList.getAwbSupportiveDocSOList()) {
                                            List<String> doctypes = Arrays.stream(awbSupportiveDocSOObj.getDocCheckList().split(",")).toList();
                                            if(!doctypes.isEmpty()) {
                                                eDocResponseSO.setResponseMsg("Below are the list of supporting documents requried");
                                                for(String docType:  doctypes) {
                                                    EDocFileTypeSO fileSO1=new EDocFileTypeSO();
                                                    fileSO1.setFileType(docType);
                                                    fileSO1.setName(docType);
                                                    fileSO1.setMandateFlag("Y");
                                                    eDocResponseSO.geteDocFileTypeSOS().add(fileSO1);

                                                    String awbDocListInsQuery = prepareAwbDocList(awbDataId, docType);
                                                    azureInteg.insertData(awbDocListInsQuery);
                                                }
                                            }
                                        }
                                    }
                                }
                                else{
                                    errorSOList.add(setErrorSOObj("Invalid AWB","Could not extract the data from submitted AWB"));
                                   // eDocResponseSO.setErrorDetails(errorSOS);
                                }
                            } catch (Exception e) {
                                System.out.println( e);
                                throw new RuntimeException(e);
                            }
                        }
                        else{
                            eDocResponseSO.setErrorDetails(errorSOS);
                        }

                    }
                    //                    log.info("awbJSON.getString(0)"+awbJSON.getString(0));
                } catch (SQLException e) {
                    throw new RuntimeException(e);
                } catch (StreamReadException e) {
                    throw new RuntimeException(e);
                } catch (DatabindException e) {
                    throw new RuntimeException(e);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

             /*   try {
                    Statement statement = connection.createStatement();
                    //Pass the carrier code, origin country code, destination country code, nature of goods

                    ResultSet pcrJSON =  statement.executeQuery("CALL SEARCH_PCR(\'goods:"+awbData.getNature_of_Goods().get(0).getValue()+",Destination:"+awbData.getDestination_Airport_Cd().get(0).getValue()+",Origin:"+awbData.getDeparture_Airport_Cd().get(0).getValue()+"\',\'Phytosanitary Certificate,Invoice,Pckinglist\')");
                    ResultSetMetaData resultSetMetaData = pcrJSON.getMetaData();
                    while (pcrJSON.next()) {
                        System.out.println("PCR data " + pcrJSON.getString(1));
                        System.out.println("PCR data " + "{ \"documentList\":"+pcrJSON.getString(1)+"}");
                       SupportingDocumentList supportingDocList = mapper.readValue("{ \"documentList\":"+pcrJSON.getString(1)+"}", SupportingDocumentList.class);
                        String[] docList=pcrJSON.getString(1).split(",");
                        if(supportingDocList!=null && supportingDocList.getDocumentList()!=null){
                            for(int i=0;i<supportingDocList.getDocumentList().size();i++){
                                EDocFileTypeSO fileSO1=new EDocFileTypeSO();
                                fileSO1.setName(supportingDocList.getDocumentList().get(i).getName());
                                eDocResponseSO.geteDocFileTypeSOS().add(supportingDocList.getDocumentList().get(i));

                            }
                        }
                        for(int i=0;i<docList.length-1;i++){
                            EDocFileTypeSO fileSO1=new EDocFileTypeSO();

                            String docName=docList[i];
                            docName= docName.replace("[","");
                            docName= docName.replace("]","");
                            docName= docName.replace("\n","");
                            docName= docName.replace("\"","");
                            docName= docName.replace(" ","");
                            //fileSO1.setFileType(docName);
                            //eDocResponseSO.geteDocFileTypeSOS().add(fileSO1);
                        }

                    }
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }*/





                //establishing LLM connection
                //call LLM API service
                //capturing LLM API service response
                //storing request & LLM API response in SnowFlake DB
            }
            eDocResponseSO.setErrorDetails(errorSOList);
            if(errorSOList.size()>0){
                eDocResponseSO.setSessionId("");
            }
        }
        if(eDocResponseSO.getErrorDetails().size()==0 && eDocResponseSO.geteDocFileTypeSOS().size()==0){
            eDocResponseSO.setResponseMsg("Invalid AWB");
            errorSOList.add(setErrorSOObj("Invalid AWB","Could not extract the data from submitted AWB"));
            eDocResponseSO.setErrorDetails(errorSOList);

        }
        return eDocResponseSO;

    }
	 private boolean validateUploadSuppAwb(UploadSuppDocSO uploadSuppDocSO) {
        if(uploadSuppDocSO.getFiledata()==null || uploadSuppDocSO.getFiledata().isBlank()) {
            return Boolean.FALSE;
        }
        if(uploadSuppDocSO.getFilename()==null || uploadSuppDocSO.getFilename().isBlank()) {
            return Boolean.FALSE;
        }
        if(uploadSuppDocSO.getDigiAwbId()<=0) {
            return Boolean.FALSE;
        }
        return Boolean.TRUE;
    }
    @Override
    public UploadAwbRespSOList uploadSuppAwb(UploadSuppDocSO uploadSuppDocSO) throws SQLException {
        UploadAwbRespSOList uploadAwbRespSOList = new UploadAwbRespSOList();
        if(validateUploadSuppAwb(uploadSuppDocSO)) {
            uploadSuppDocSO.setFileType("Phytosanitary Certificate");
            ValidateDocSO validateDocSO = new ValidateDocSO();
            List<String> docTypes = azureInteg.getDigAwbSupTypes(uploadSuppDocSO.getDigiAwbId());
            validateDocSO.setList_of_mandatory_documents(docTypes);
            List<UploadAWBSO> uploadAWBSOList = azureInteg.getDigAwbById(uploadSuppDocSO.getDigiAwbId());
            UploadAWBSO uploadAWBSO = new UploadAWBSO();
            uploadAWBSO.setFilename(uploadSuppDocSO.getFilename());
            uploadAWBSO.setFiledata(uploadSuppDocSO.getFiledata());
            uploadAWBSO.setFiletype(uploadSuppDocSO.getFileType());
            uploadAWBSOList.add(uploadAWBSO);
            validateDocSO.setFiles(uploadAWBSOList);
            ValidateDocRespSO validateDocRespSO = saveUploadAwbSuppSO(validateDocSO);
            if(validateDocRespSO!=null) {
                if(validateDocRespSO.getPhyto()==null ||
                        (validateDocRespSO.getPhyto()!=null && validateDocRespSO.getPhyto().getDate()==null)) {
                    ErrorSO errorSO = new ErrorSO();
                    errorSO.setErrorId(validateDocRespSO.getStatus());
                    errorSO.setErrorMessage(validateDocRespSO.getMessage());
                    uploadAwbRespSOList.setUploadAwbRespSO(null);
                    uploadAwbRespSOList.setErrorSO(errorSO);
                }
                else{
                    UploadAWBSO uploadAwhSOObj = new UploadAWBSO();
                    uploadAwhSOObj.setFilename(uploadSuppDocSO.getFilename());
                    uploadAwhSOObj.setFiledata(uploadSuppDocSO.getFiledata());
                    uploadAwhSOObj.setFiletype(uploadSuppDocSO.getFileType());
                    long digiAwbId = azureInteg.saveDigiAwbSuppDoc(uploadAwhSOObj, uploadSuppDocSO.getDigiAwbId());
                    if(digiAwbId>0) {
                        System.out.println("Saved Successfully");
                        long rowsUpdatted = 0;
                        if(validateDocRespSO.getPhyto().isValid()) {
                            rowsUpdatted = azureInteg.updateAwbSupDocType(uploadSuppDocSO.getFileType(),
                                    "Y", "Y", validateDocRespSO.getMindocsrequirementmet(), digiAwbId);
                        }
                        else{
                            rowsUpdatted = azureInteg.updateAwbSupDocType(uploadSuppDocSO.getFileType(),
                                    "Y", "N", validateDocRespSO.getMindocsrequirementmet(), uploadSuppDocSO.getDigiAwbId());
                        }
                        if(rowsUpdatted>0) {
                            System.out.println("Updated Successfully");
                        }
                    }
                }
            }
        }
        else {
            ErrorSO errorSO = new ErrorSO();
            errorSO.setErrorId("Invalid Input");
            errorSO.setErrorMessage("Invalid Input");
            uploadAwbRespSOList.setErrorSO(errorSO);
        }
        return uploadAwbRespSOList;
    }
    private ValidateDocRespSO  saveUploadAwbSuppSO(ValidateDocSO validateDocSO){
        StringBuilder serviceurl = new StringBuilder("");
        serviceurl.append(url);
        serviceurl.append("validatedocs");
        ValidateDocRespSO validateDocRespSO = null;
        String requestJson = new JsonUtil<ValidateDocSO>().converObjectToJson(validateDocSO);
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> httpEntity = new HttpEntity<String>(requestJson, httpHeaders);
        ResponseEntity<String> response = restTemplate.exchange(serviceurl.toString(), HttpMethod.POST, httpEntity, String.class);
        if(response.getBody()!=null) {
            validateDocRespSO = new JsonUtil<ValidateDocRespSO>().convertJsonToObject(response.getBody(), ValidateDocRespSO.class);
        }
        return validateDocRespSO;
    }
    private boolean validateUploadAwb(UploadAWBSO uploadAWBSO) {
        if(uploadAWBSO.getFiledata()==null || uploadAWBSO.getFiledata().isBlank()) {
            return Boolean.FALSE;
        }
        if(uploadAWBSO.getFilename()==null || uploadAWBSO.getFilename().isBlank()) {
            return Boolean.FALSE;
        }
        return Boolean.TRUE;
    }
    @Override
    public UploadAwbRespSOList uploadAwb(UploadAWBSO uploadAWBSO) throws SQLException {
        UploadAwbRespSOList uploadAwbRespSOList = new UploadAwbRespSOList();
        if(validateUploadAwb(uploadAWBSO)) {
            UploadAwbRespSO uploadAwbRespSO = method(uploadAWBSO);
            if(uploadAwbRespSO!=null) {
                if(uploadAwbRespSO.getDocumentNumber()==null) {
                    ErrorSO errorSO = new ErrorSO();
                    errorSO.setErrorId("filedata");
                    errorSO.setErrorMessage("Invalid Input");
                    uploadAwbRespSOList.setUploadAwbRespSO(null);
                    uploadAwbRespSOList.setErrorSO(errorSO);
                }
                else{
                    String sessionId = UUID.randomUUID().toString();
                    log.info("Generated Session Id: "+sessionId);
                    uploadAwbRespSOList.setUploadAwbRespSO(uploadAwbRespSO);
                    uploadAWBSO.setFiletype("Air WayBill");
                    long digiAwbId = azureInteg.saveDigiAwb(uploadAWBSO, sessionId);
                    if(digiAwbId>0) {
                        System.out.println("Saved Successfully");
                        /**
                         * get list of required documents based on carrierCode, Origin, Destination, Nature Of Goods
                         * from awb_supportive_doc table
                          */

                        AwbSupportiveDocSO awbSupportiveDocSO = new AwbSupportiveDocSO();
                        awbSupportiveDocSO.setCarCode(carCodeMap.get(uploadAwbRespSO.getDocumentPrefix()));
                        awbSupportiveDocSO.setOrigin(uploadAwbRespSO.getShipperCountryCode());
                        awbSupportiveDocSO.setDestination(uploadAwbRespSO.getConsigneeCountryCode());
                        if(uploadAwbRespSO.getGoodbeingtransported()!=null && uploadAwbRespSO.getGoodbeingtransported().contains("SALMON")) {
                            awbSupportiveDocSO.setNatureOfGoods("PERISHABLE");
                        }
                        else if(uploadAwbRespSO.getGoodbeingtransported()!=null && uploadAwbRespSO.getGoodbeingtransported().contains("FRUITS")) {
                            awbSupportiveDocSO.setNatureOfGoods("FRUITS");
                        }
                        AwbSupportiveDocSOList awbSupportiveDocSOList = azureInteg.fetchAwbSupportiveDocs(awbSupportiveDocSO);
                        List<String> requiredDocs = new ArrayList<String>();
                        if(null!=awbSupportiveDocSOList && !awbSupportiveDocSOList.getAwbSupportiveDocSOList().isEmpty()) {
                            requiredDocs = Arrays.stream(awbSupportiveDocSOList.getAwbSupportiveDocSOList().get(0).getDocCheckList().split(",")).toList();

                            /**
                             *  based on required document types, insert record into digital_awb_sup_doc_types for each document Type.
                             */
                            for(String requiredDoc:  requiredDocs) {
                                if(requiredDoc.equalsIgnoreCase("Air WayBill")) {
                                    azureInteg.insertAwbSupDocType(requiredDoc, "Y", "Y", "", digiAwbId);
                                }
                                else{
                                    azureInteg.insertAwbSupDocType(requiredDoc, "", "", "", digiAwbId);
                                }
                            }
                            uploadAwbRespSO.setRequiredDocuments(requiredDocs);
                            uploadAwbRespSO.setDigiAwbId(digiAwbId);
                            uploadAwbRespSOList.setUploadAwbRespSO(uploadAwbRespSO);
                        }
                    }
                }
            }
        }
        else {
            ErrorSO errorSO = new ErrorSO();
            errorSO.setErrorId("Invalid Input");
            errorSO.setErrorMessage("Invalid Input");
            uploadAwbRespSOList.setErrorSO(errorSO);
        }
        return uploadAwbRespSOList;
    }
    private UploadAwbRespSO method(UploadAWBSO uploadAWBSO) {
        StringBuilder serviceurl = new StringBuilder("");
        serviceurl.append(url);
        serviceurl.append("uploadawb64");
        UploadAwbRespSO uploadAwbRespSO = null;
        String requestJson = new JsonUtil<UploadAWBSO>().converObjectToJson(uploadAWBSO);
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> httpEntity = new HttpEntity<String>(requestJson, httpHeaders);
        try{
            ResponseEntity<String> response = restTemplate.exchange(serviceurl.toString(), HttpMethod.POST, httpEntity, String.class);
            if(response.getBody()!=null) {
                uploadAwbRespSO = new JsonUtil<UploadAwbRespSO>().convertJsonToObject(response.getBody(), UploadAwbRespSO.class);
            }
        }catch(Exception e){
            throw e;
        }

        return uploadAwbRespSO;
    }
    public void updateAwbDocList (long id, String uploadInd, String validInd, String reason) throws Exception {
        StringBuilder updQuery = new StringBuilder("UPDATE  dbo.AWB_DOCLIST set uploadInd=?, validInd=?, reason=? \n" +
                "where awbdata_id=?");
        boolean updateFlag = azureInteg.updateData(updQuery.toString(), id, uploadInd, validInd, reason);
        if(updateFlag) {
            System.out.println(" AWB_DOCLIST TABLE UPDATED SUCCESSFULLY FOR THE DOC_ID"+id);
        }
    }
    private String prepareAwbDocList(long awbDataId, String docType) throws Exception {

        StringBuilder insQuery = new StringBuilder("INSERT INTO dbo.AWB_DOCLIST (id, docType, awbdata_id)\n" +
                "VALUES (NEXT VALUE FOR awb_doclist_seq , '"+docType+"', "+awbDataId+")");


        return insQuery.toString();
    }

    private AwbDataListSO getAwbByDocType(AwbDataSearchSO awbDataSearchSO) throws Exception {
        AwbDataListSO awbDataListSO= new AwbDataListSO();
        if((awbDataSearchSO.getSessionId()!=null || !awbDataSearchSO.getSessionId().isBlank())
        && (awbDataSearchSO.getDocType()!=null || !awbDataSearchSO.getDocType().isBlank())) {
            awbDataListSO= azureInteg.getAwbDataByDocType(awbDataSearchSO.getSessionId(), awbDataSearchSO.getDocType());
        }
        else{
            List<ErrorSO> errorSOList = new ArrayList<ErrorSO>();
            ErrorSO errorSO=setErrorSOObj("Invalid Input","Please valid Input Data");
            errorSOList.add(errorSO);
            awbDataListSO.setErrorDetails(errorSOList);
        }
        return awbDataListSO;
    }

    private AwbSupportiveDocSOList getAwbSupportiveDocTypes(AwbSupportiveDocSO awbSupportiveDocSO) {
        AwbSupportiveDocSOList awbSupportiveDocSOList = null;
        List<ErrorSO> errorDetails = new ArrayList<ErrorSO>();
        if(!validateAwbSupportiveDocTypes(awbSupportiveDocSO, errorDetails)) {
            return azureInteg.fetchAwbSupportiveDocs(awbSupportiveDocSO);
        }
        return null;
    }

    public boolean validateAwbSupportiveDocTypes(AwbSupportiveDocSO awbSupportiveDocSO, List<ErrorSO> errorDetails) {
        if(awbSupportiveDocSO.getOrigin()==null || awbSupportiveDocSO.getOrigin().isBlank()) {
            ErrorSO errorSO=setErrorSOObj("Origin","Please valid Input Data");
            errorDetails.add(errorSO);
        }
        if(awbSupportiveDocSO.getCarCode()==null || awbSupportiveDocSO.getCarCode().isBlank()) {
            ErrorSO errorSO=setErrorSOObj("carCode","Please valid Input Data");
            errorDetails.add(errorSO);
        }
        if(awbSupportiveDocSO.getDestination()==null || awbSupportiveDocSO.getDestination().isBlank()) {
            ErrorSO errorSO=setErrorSOObj("destination","Please valid Input Data");
            errorDetails.add(errorSO);
        }
        if(awbSupportiveDocSO.getNatureOfGoods()==null || awbSupportiveDocSO.getNatureOfGoods().isBlank()) {
            ErrorSO errorSO=setErrorSOObj("natureOfGoods","Please valid Input Data");
            errorDetails.add(errorSO);
        }
        if(!errorDetails.isEmpty()) {
            return Boolean.TRUE;
        }
        return Boolean.FALSE;
    }
    List<ErrorSO>  compareAWBAndPhyto(String sessionId, int docId)  {

        List<ErrorSO> errorList=new ArrayList<ErrorSO>();
        AwbDataListSO awbDataListSO= null;
        AwbDataListSO phytoListSO=null;
        try {
            awbDataListSO = azureInteg.getAwbDataByDocType(sessionId,"AWB");
            phytoListSO= azureInteg.getAwbDataByDocTypeById(docId,"PHYTO");

        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        if(awbDataListSO.getAwbDataSOList().size()==0){
            ErrorSO err=new ErrorSO("","Corresponding AWB not found");
            errorList.add(err);
        }
        AwbDataSO awbSo=  awbDataListSO.getAwbDataSOList().get(0);
        AwbDataSO phytoSo=phytoListSO.getAwbDataSOList().get(0);
        SnowFlakeInteg snowFlakeInteg=new SnowFlakeInteg();
        Connection connection = null;
        Statement statement =null;
        try {
            connection = snowFlakeInteg.getConnection();
            statement=  connection.createStatement();

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }



        if(awbSo.getShpName()!=null && phytoSo.getShpName()!=null){
            try{
                ResultSet awbJSON =  statement.executeQuery("SELECT JAROWINKLER_SIMILARITY(\'"+awbSo.getShpName()+"\',\'"+ phytoSo.getShpName()+"\')");
                ResultSetMetaData resultSetMetaData = awbJSON.getMetaData();
                System.out.println("Number of columns=" + resultSetMetaData.getColumnCount());
                while (awbJSON.next()) {
                            if(Integer.valueOf(awbJSON.getString(1))<90){
                                ErrorSO err=new ErrorSO("Mismatch in Shipper name","Mismatch in Shipper name");
                                errorList.add(err);
                            }
                    }
            }catch (Exception e){

            }

        }

        if(awbSo.getConsName()!=null && phytoSo.getConsName()!=null){
            try{
                ResultSet awbJSON =  statement.executeQuery("SELECT JAROWINKLER_SIMILARITY(\'"+awbSo.getConsName()+"\',\'"+ phytoSo.getConsName()+"\')");
                ResultSetMetaData resultSetMetaData = awbJSON.getMetaData();
                System.out.println("Number of columns=" + resultSetMetaData.getColumnCount());
                while (awbJSON.next()) {
                    if(Integer.valueOf(awbJSON.getString(1))<90){
                        ErrorSO err=new ErrorSO("Mismatch in Consignee name","Mismatch in Consignee name");
                        errorList.add(err);
                    }
                }
            }catch (Exception e){

            }

        }
        if(awbSo.getWeight()!=null && phytoSo.getWeight()!=null){
            try{
                String  awbWt=awbSo.getWeight().replace("KG","");
                awbWt=awbSo.getWeight().replace("Kg","");
                awbWt=awbSo.getWeight().replace("kg","");

                String  phytoWt=awbSo.getWeight().replace("KG","");
                phytoWt=awbSo.getWeight().replace("Kg","");
                phytoWt=awbSo.getWeight().replace("kg","");
                if(!awbWt.equalsIgnoreCase(phytoWt)){
                    ErrorSO err=new ErrorSO("Mismatch in Weight","Mismatch in Weight");
                    errorList.add(err);
                }

            }catch (Exception e){

            }

        }
        if(awbSo.getOrigCntry()!=null && phytoSo.getOrigCntry()!=null){
            try{

                ResultSet awbJSON =  statement.executeQuery("SELECT JAROWINKLER_SIMILARITY(\'"+awbSo.getOrigCntry()+"\',\'"+ phytoSo.getOrigCntry()+"\')");
                ResultSetMetaData resultSetMetaData = awbJSON.getMetaData();
                System.out.println("Number of columns=" + resultSetMetaData.getColumnCount());
                while (awbJSON.next()) {
                    if(Integer.valueOf(awbJSON.getString(1))<90){
                        ErrorSO err=new ErrorSO("Mismatch in Origin country","Mismatch in Origin country");
                        errorList.add(err);
                    }
                }
            }catch (Exception e){

            }

        }
            return errorList;
    }
private ErrorSO setErrorSOObj(String errorId, String errorMessage) {
    ErrorSO errorSO = new ErrorSO();
    errorSO.setErrorId(errorId);
    errorSO.setErrorMessage(errorMessage);
    return errorSO;
}
private String convertSOToEntity(AWBDetailsSO awbDetailsSO, String sessionId, List<ErrorSO> errorSOList) {
        StringBuilder insQuery = new StringBuilder("INSERT INTO dbo.AWB_DATA (id, origin, destination, sessionId, shipperName, consigneeName, weight, natureOfGoods, orgin_cntry, dest_cntry, docType)\n" +
                "VALUES (NEXT VALUE FOR awbDataSeq , '");
        String originCntry="";
        String destCntry="";
        if(null!=awbDetailsSO.getDeparture_Airport_Cd() &&
                !awbDetailsSO.getDeparture_Airport_Cd().isEmpty()) {
            insQuery.append(awbDetailsSO.getDeparture_Airport_Cd().get(0).getValue());
            originCntry = cityCountryMap.get(awbDetailsSO.getDeparture_Airport_Cd().get(0).getValue());
            insQuery.append("','");
        }
        else {
            errorSOList.add(setErrorSOObj("origin","Data Missing"));
        }
    if(null!=awbDetailsSO.getDestination_Airport_Cd() &&
            !awbDetailsSO.getDestination_Airport_Cd().isEmpty()) {
        insQuery.append(awbDetailsSO.getDestination_Airport_Cd().get(0).getValue());
        destCntry = cityCountryMap.get(awbDetailsSO.getDestination_Airport_Cd().get(0).getValue());
        insQuery.append("','");
    }
    else {
        errorSOList.add(setErrorSOObj("destination","Data Missing"));
    }
    insQuery.append(sessionId);
    insQuery.append("','");
    if(null!=awbDetailsSO.getShipper_Name() &&
            !awbDetailsSO.getShipper_Name().isEmpty()) {
        insQuery.append(awbDetailsSO.getShipper_Name().get(0).getValue());
        insQuery.append("','");
    }
    else {
        errorSOList.add(setErrorSOObj("Shipper Name","Data Missing"));
    }
    if(null!=awbDetailsSO.getConsignee_Name() &&
            !awbDetailsSO.getConsignee_Name().isEmpty()) {
        insQuery.append(awbDetailsSO.getConsignee_Name().get(0).getValue());
        insQuery.append("','");
    }
    else {
        errorSOList.add(setErrorSOObj("Consignee Name","Data Missing"));
    }
    if(null!=awbDetailsSO.getChargeable_Weight() &&
            !awbDetailsSO.getChargeable_Weight().isEmpty()) {
        insQuery.append(awbDetailsSO.getChargeable_Weight().get(0).getValue());
        insQuery.append("','");
    }
    else {
        errorSOList.add(setErrorSOObj("Chargeable Weight","Data Missing"));
    }
    if(null!=awbDetailsSO.getNature_of_Goods() &&
            !awbDetailsSO.getNature_of_Goods().isEmpty()) {
        insQuery.append(awbDetailsSO.getNature_of_Goods().get(0).getValue());
        insQuery.append("','");
    }
    else {
        errorSOList.add(setErrorSOObj("Nature Of Goods","Data Missing"));
    }
    insQuery.append(originCntry);
    insQuery.append("','");
    insQuery.append(destCntry);
    insQuery.append("','");
    insQuery.append("AWB'");
    insQuery.append(")");
    return insQuery.toString();
}
}