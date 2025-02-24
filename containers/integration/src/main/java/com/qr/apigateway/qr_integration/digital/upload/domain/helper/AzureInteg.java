package com.qr.apigateway.qr_integration.digital.upload.domain.helper;

import com.qr.apigateway.qr_integration.digital.upload.domain.entity.UploadAwb;
import com.qr.apigateway.qr_integration.digital.upload.schemaobjects.*;
import net.snowflake.client.jdbc.internal.apache.arrow.flatbuf.Bool;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;


@Component
public class AzureInteg {
    @Value("azure.db.username")
    private String azureDBUsername;
    @Value("azure.db.password")
    private String azureDBPassword;

    // Connection details
    public void getAwbs() throws Exception{
        Connection conn = null;
        Statement stmt = null;
        try {
            conn = getConnection();
            stmt = conn.createStatement();
        String sql = "SELECT id, awb_num FROM dbo.AWB_DATA";
        ResultSet rs = stmt.executeQuery(sql);

        while (rs.next()) {
            // Retrieve by column name
            int id = rs.getInt("id");
            String awbNum = rs.getString("awb_num");

            // Display values
            System.out.print("ID: " + id);
            System.out.print(", AWB Number: " + awbNum);
        }
        // Step 5: Clean-up environment
        rs.close();
        stmt.close();
        conn.close();
    } catch (SQLException se) {
        // Handle errors for JDBC
        se.printStackTrace();
    } catch (Exception e) {
        // Handle errors for Class.forName
        e.printStackTrace();
    } finally {
        // Finally block to close resources
        try {
            if (stmt != null) stmt.close();
        } catch (SQLException se2) {
        } // Nothing we can do
        try {
            if (conn != null) conn.close();
        } catch (SQLException se) {
            se.printStackTrace();
        }
    }
    }
    public AwbSupportiveDocSOList fetchAwbSupportiveDocs(AwbSupportiveDocSO awbSupportiveDocSO) {
        AwbSupportiveDocSOList awbSupportiveDocSOList = new AwbSupportiveDocSOList();
        List<AwbSupportiveDocSO> awbSupportiveDocSOs = new ArrayList<AwbSupportiveDocSO>();

        Connection conn = null;
        PreparedStatement pstmt = null;
        String natureOfGoods="";
        if(awbSupportiveDocSO.getNatureOfGoods().toLowerCase().contains("fruits")){
            natureOfGoods="FRUITS";
        }
        if(awbSupportiveDocSO.getNatureOfGoods().toLowerCase().contains("vegetables")){
            natureOfGoods="FRUITS";
        }
        if(awbSupportiveDocSO.getNatureOfGoods().toLowerCase().contains("perishable")){
            natureOfGoods="PERISHABLE";
        }
        StringBuilder selectStr = new StringBuilder("SELECT carCode, origin, destination, natureOfGoods, docCheckList FROM dbo.AWB_SUPPORTIVE_DOC ");
        selectStr.append("WHERE carCode= ? and origin=? and destination=? and natureOfGoods like ?");
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(selectStr.toString());
            pstmt.setString(1, awbSupportiveDocSO.getCarCode());
            pstmt.setString(2, awbSupportiveDocSO.getOrigin());
            pstmt.setString(3, awbSupportiveDocSO.getDestination());
            pstmt.setString(4, '%'+natureOfGoods+'%');

            ResultSet rset = pstmt.executeQuery();
            while(rset.next()) {
                awbSupportiveDocSOs.add(convertAwbSupportiveDocEntityToSO(rset));
            }
            if(awbSupportiveDocSOs.isEmpty()) {
                List<ErrorSO> errorDetails = new ArrayList<ErrorSO>();
                ErrorSO errorSO = new ErrorSO();
                errorSO.setErrorId("No Data");
                errorSO.setErrorMessage("No Records available, based on given input Data.");
                errorDetails.add(errorSO);
                awbSupportiveDocSOList.setErrorDetails(errorDetails);
            }
            awbSupportiveDocSOList.setAwbSupportiveDocSOList(awbSupportiveDocSOs);
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }


        awbSupportiveDocSOList.setAwbSupportiveDocSOList(awbSupportiveDocSOs);
        return awbSupportiveDocSOList;
    }
    public AwbSupportiveDocSO convertAwbSupportiveDocEntityToSO(ResultSet rset) throws SQLException {

        String carCode = (String) rset.getString("carCode");
        String origin = (String) rset.getString("origin");
        String destination = (String) rset.getString("destination");
        String natureOfGoods = (String) rset.getString("natureOfGoods");
        String docCheckList = (String) rset.getString("docCheckList");

        return new AwbSupportiveDocSO(carCode, origin, destination, natureOfGoods, docCheckList);
    }
    public Boolean insertData(String insStmt) throws Exception{
        Connection conn = null;
        Statement stmt = null;
        Boolean insertFlag = Boolean.FALSE;
        try {
            conn = getConnection();
            stmt = conn.createStatement();
            int id= stmt.executeUpdate(insStmt);
            if(id>0) {
                System.out.println("Inserted Successfully");
                insertFlag = Boolean.TRUE;
            }
            stmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return insertFlag;
    }
    public Integer insertSupportingData(String insStmt) throws Exception{
        Connection conn = null;
        Statement statement = null;
        PreparedStatement stmt = null;
        Boolean insertFlag = Boolean.FALSE;
        int awbDataId =0;
        try {
            conn = getConnection();
            statement = conn.createStatement();
            ResultSet resultSet = statement.executeQuery("select next value for awbDataSeq");
            if(resultSet!=null && resultSet.next()) {
                awbDataId = resultSet.getInt(1);
                insStmt = insStmt.replace("NEXT VALUE FOR awbDataSeq", Integer.toString(awbDataId));
            }
            stmt = conn.prepareStatement(insStmt);
            //stmt = conn.createStatement();
            int id= stmt.executeUpdate();
            //int id= 0;
            if(id>0) {
                System.out.println("Inserted Successfully");
                stmt.close();
                conn.close();
                return awbDataId;
            }
            stmt.close();
            conn.close();
            return id;
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return 0;
    }
    public Boolean updateData(String updStmt, long id, String uploadInd, String validInd, String reason) throws Exception{
        Connection conn = null;
        PreparedStatement pstmt = null;
        Boolean updateFlag = Boolean.FALSE;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(updStmt);
            pstmt.setString(1, uploadInd);
            pstmt.setString(2, validInd);
            pstmt.setString(3, reason);
            pstmt.setLong(4,id);

            int recordUpdate = pstmt.executeUpdate();
            if(recordUpdate>0) {
                updateFlag= Boolean.TRUE;
            }
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return updateFlag;
    }

    public AwbDataListSO getAwbDataByDocType(String sessionId, String docType) throws Exception{
        AwbDataListSO awbDataListSO = new AwbDataListSO();
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT id, origin, destination, sessionId, shipperName, consigneeName, orgin_cntry, dest_cntry, pieces, weight, natureOfGoods, execDate, docsList, verDocList, errorDocList, errorDesc, docType\n" +
                    "FROM dbo.AWB_DATA \n" +
                    "WHERE  sessionId= ? AND docType = ?");
            pstmt.setString(1, sessionId);
            pstmt.setString(2, docType);

            ResultSet rset = pstmt.executeQuery();
            List<AwbDataSO> awbDataSOS = new ArrayList<AwbDataSO>();
            while(rset.next()) {
                awbDataSOS.add(convertEntityToSO(rset));
            }
            awbDataListSO.setAwbDataSOList(awbDataSOS);
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return awbDataListSO;
    }
    public List<UploadAWBSO> getDigAwbById(long digAwbId) {
        List<UploadAWBSO> uploadAWBSOList = new ArrayList<UploadAWBSO>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT fileName, fileData, fileType \n" +
                    "FROM dbo.DIGITAL_AWB \n" +
                    "WHERE  dig_awb_id= ?");
            pstmt.setLong(1, digAwbId);

            ResultSet rset = pstmt.executeQuery();
            while(rset.next()) {
                UploadAWBSO uploadAWBSO = new UploadAWBSO();
                uploadAWBSO.setFilename(rset.getString(1));
                uploadAWBSO.setFiledata(rset.getString(2));
                uploadAWBSO.setFiletype(rset.getString(3));
                uploadAWBSOList.add(uploadAWBSO);
            }
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return uploadAWBSOList;
    }
    public AwbDataListSO getAwbDataByDocTypeById(Integer docId, String docType) throws Exception{
        AwbDataListSO awbDataListSO = new AwbDataListSO();
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT id, origin, destination, sessionId, shipperName, consigneeName, orgin_cntry, dest_cntry, pieces, weight, natureOfGoods, execDate, docsList, verDocList, errorDocList, errorDesc, docType\n" +
                    "FROM dbo.AWB_DATA \n" +
                    "WHERE  id= ? AND docType = ?");
            pstmt.setLong(1, docId);
            pstmt.setString(2, docType);

            ResultSet rset = pstmt.executeQuery();
            List<AwbDataSO> awbDataSOS = new ArrayList<AwbDataSO>();
            while(rset.next()) {
                awbDataSOS.add(convertEntityToSO(rset));
            }
            awbDataListSO.setAwbDataSOList(awbDataSOS);
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return awbDataListSO;
    }
    public AwbDocListSO getAwbListByAwbDataId(Integer awbDataId, String docType) throws Exception{
        AwbDocListSO awbDataListSO = new AwbDocListSO();
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT id, docType, uploadInd, validInd, reason, awbdata_id \n" +
                    "FROM dbo.AWB_DOCLIST \n" +
                    "WHERE  awbdata_id= ? AND docType = ?");
            pstmt.setLong(1, awbDataId);
            pstmt.setString(2, docType);

            ResultSet rset = pstmt.executeQuery();
            while(rset.next()) {
                return convertAwbDocListEntityToSO(rset);
            }
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return null;
    }
    public List<String> getDigAwbSupTypes(long digAwbId) {
        List<String> docTypes = new ArrayList<String>();
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT docType \n" +
                    "FROM dbo.digital_awb_sup_doc_types \n" +
                    "WHERE  digawbId= ?");
            pstmt.setLong(1, digAwbId);

            ResultSet rset = pstmt.executeQuery();
            while(rset.next()) {
                docTypes.add(rset.getString(1));
            }
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return docTypes;
    }
    public List<AwbDocListSO> getAwbListByAwbDataId(long awbDataId, String docType) throws Exception{
        List<AwbDocListSO> awbDocListSOS = new ArrayList<AwbDocListSO>();
        AwbDocListSO awbDataListSO = new AwbDocListSO();
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT id, docType, uploadInd, validInd, reason, awbdata_id \n" +
                    "FROM dbo.AWB_DOCLIST \n" +
                    "WHERE  awbdata_id= ? AND docType = ?");
            pstmt.setLong(1, awbDataId);
            pstmt.setString(2, docType);

            ResultSet rset = pstmt.executeQuery();
            while(rset.next()) {
                awbDocListSOS.add(convertAwbDocListEntityToSO(rset));
            }
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return awbDocListSOS;
    }
    private AwbDocListSO convertAwbDocListEntityToSO(ResultSet rset) throws SQLException {
        Long id = (Long) rset.getLong("id");
        String docType = (String) rset.getString("docType");
        String uploadInd = (String) rset.getString("uploadInd");
        String validInd = (String) rset.getString("validInd");
        String reason = (String) rset.getString("reason");
        Long awbdataId = (Long) rset.getLong("awbdata_id");

        return new AwbDocListSO(id, docType, uploadInd, validInd, reason, awbdataId);
    }

    private AwbDataSO convertEntityToSO(ResultSet rset) throws SQLException {
        Long id = (Long) rset.getLong("id");
        String origin = (String) rset.getString("origin");
        String destination = (String) rset.getString("destination");
        String sessionId = (String) rset.getString("sessionId");
        String shpName = (String) rset.getString("shipperName");
        String consName = (String) rset.getString("consigneeName");
        String origCntry = (String) rset.getString("orgin_cntry");
        String destCntry = (String) rset.getString("dest_cntry");
        int pieces = (Integer) rset.getInt("pieces");
        String weight = (String) rset.getString("weight");
        String natureOfGoods = (String) rset.getString("natureOfGoods");
        String execDate = rset.getString("execDate");
        String docsList = (String) rset.getString("docsList");
        String verDocsList = (String) rset.getString("verDocList");
        String errorDocsList = (String) rset.getString("errorDocList");
        String errorDesc = (String) rset.getString("errorDesc");
        String docType = (String) rset.getString("docType");

        return new AwbDataSO(id, origin, destination, sessionId, shpName, consName,
                origCntry, destCntry, pieces, weight, natureOfGoods, execDate, docsList, verDocsList,
                errorDocsList, docType);
    }
    public UploadAwb getAwbDataById(long digAwbId) {
        UploadAwb uploadAwb = null;
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            conn = getConnection();
            pstmt = conn.prepareStatement("SELECT fileData, fileType \n" +
                    "FROM dbo.DIGITAL_AWB \n" +
                    "WHERE  dig_awb_id = ?");
            pstmt.setLong(1, digAwbId);

            ResultSet rset = pstmt.executeQuery();
            while(rset.next()) {
                uploadAwb = new UploadAwb();
                uploadAwb.setFileType(rset.getString(1));
                uploadAwb.setFileData(rset.getString(2));;
            }
            pstmt.close();
            conn.close();
        } catch (SQLException se) {
            // Handle errors for JDBC
            se.printStackTrace();
        } catch (Exception e) {
            // Handle errors for Class.forName
            e.printStackTrace();
        } finally {
            // Finally block to close resources
            try {
                if (pstmt != null) pstmt.close();
            } catch (SQLException se2) {
            } // Nothing we can do
            try {
                if (conn != null) conn.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return uploadAwb;
    }
    public long insertAwbSupDocType(String docType, String uploadInd, String validInd, String remarks, long digiAwbId) throws SQLException {
        String insQuery = "INSERT INTO dbo.digital_awb_sup_doc_types ( docType, uploadInd, validInd, remarks, digawbId) VALUES (?,?,?,?,?)";
        try(
                Connection conn  = getConnection();
                PreparedStatement pstmt = conn.prepareStatement(insQuery)) {

            // Set the parameters for the prepared statement
            pstmt.setString(2, uploadInd);
            pstmt.setString(3, validInd);
            pstmt.setString(4, remarks);
            pstmt.setLong(5, digiAwbId);
            pstmt.setString(1, docType);

            // Execute the update statement
            int rowsAffected = pstmt.executeUpdate();

            if(rowsAffected>0) {
                return 1;
            }
        }
        catch(SQLException se) {
            System.err.println("SQL Exception: "+se.getMessage());
        }
        return -1;
    }

    public long updateAwbSupDocType(String docType, String uploadInd, String validInd, String remarks, long digiAwbId) throws SQLException {
        String updQuery = "UPDATE  dbo.digital_awb_sup_doc_types set uploadInd=?, validInd=?, remarks=? WHERE digawbId=? and docType=?";
        try(
                Connection conn  = getConnection();
                PreparedStatement pstmt = conn.prepareStatement(updQuery)) {
            if(docType!=null && docType.equalsIgnoreCase("Phytosanitary Certificate")) {
                docType="Phytosanitary Document";
            }
            // Set the parameters for the prepared statement
            pstmt.setString(1, uploadInd);
            pstmt.setString(2, validInd);
            pstmt.setString(3, remarks);
            pstmt.setLong(4, digiAwbId);
            pstmt.setString(5, docType);

            // Execute the update statement
            int rowsAffected = pstmt.executeUpdate();

            if(rowsAffected>0) {
                return 1;
            }
            }
        catch(SQLException se) {
            System.err.println("SQL Exception: "+se.getMessage());
        }
        return -1;
    }
    public long saveDigiAwbSuppDoc(UploadAWBSO uploadAWBSO, long digiAwbId) throws SQLException {
        String insQuery = "INSERT INTO dbo.DIGITAL_AWB (digAwbId, fileData, fileType, fileName) VALUES(?,?,?,?)";
        try(
                Connection conn  = getConnection();
                PreparedStatement pstmt = conn.prepareStatement(insQuery, PreparedStatement.RETURN_GENERATED_KEYS)) {

            // Set the parameters for the prepared statement
            pstmt.setLong(1, digiAwbId);
            pstmt.setString(2, uploadAWBSO.getFiledata());
            pstmt.setString(3, uploadAWBSO.getFiletype());
            pstmt.setString(4, uploadAWBSO.getFilename());

            // Execute the insert statement
            int rowsAffected = pstmt.executeUpdate();

            // Retrieve the generated key(s)
            try (ResultSet rs = pstmt.getGeneratedKeys()) {
                if (rs.next()) {
                    int generatedId = rs.getInt(1);
                    if(generatedId>0){
                        return generatedId;
                    }
                }
            }        }
        catch(SQLException se) {
            System.err.println("SQL Exception: "+se.getMessage());
        }
        return -1;
    }
    public long saveDigiAwb(UploadAWBSO uploadAWBSO, String sessionId) throws SQLException {
        String insQuery = "INSERT INTO dbo.DIGITAL_AWB (sessionId, fileData, fileType, fileName) VALUES(?,?,?,?)";
        try(
            Connection conn  = getConnection();
            PreparedStatement pstmt = conn.prepareStatement(insQuery, PreparedStatement.RETURN_GENERATED_KEYS)) {

                // Set the parameters for the prepared statement
                pstmt.setString(1, sessionId);
                pstmt.setString(2, uploadAWBSO.getFiledata());
                pstmt.setString(3, uploadAWBSO.getFiletype());
                pstmt.setString(4, uploadAWBSO.getFilename());

                // Execute the insert statement
                int rowsAffected = pstmt.executeUpdate();

                // Retrieve the generated key(s)
                try (ResultSet rs = pstmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        int generatedId = rs.getInt(1);
                        if(generatedId>0){
                            return generatedId;
                        }
                    }
                }        }
        catch(SQLException se) {
            System.err.println("SQL Exception: "+se.getMessage());
        }
        return -1;
    }
    public  Connection getConnection()
            throws SQLException
    {
        try
        {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        }
        catch (ClassNotFoundException ex)
        {
            System.err.println("Driver not found");
        }
        // build connection properties

        // create a new connection
        String connectStr = "jdbc:sqlserver://digiawb.database.windows.net:1433;database=DIGIAWB_DB;user="+azureDBUsername+";password="+azureDBPassword+";encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;";
        return DriverManager.getConnection(connectStr);
    }
}
