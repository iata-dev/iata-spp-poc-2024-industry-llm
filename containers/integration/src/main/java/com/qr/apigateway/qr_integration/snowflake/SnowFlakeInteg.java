package com.qr.apigateway.qr_integration.snowflake;

import org.springframework.beans.factory.annotation.Value;

import java.sql.*;
import java.util.Properties;


public class SnowFlakeInteg {

    @Value("snowflake.username")
    private String snowFlakeUsername;
    @Value("snowflake.password")
    private String snowFlakePassword;
    @Value("snowflake.account")
    private String snowFlakeAccount;

    // Connection details
    public void putAwb() throws Exception{

      /*  String url = "jdbc:snowflake://<account>.snowflakecomputing.com";
        String user = "<username>";
        String password = "<password>";
        String warehouse = "<warehouse>";
        String database = "<database>";
        String schema = "<schema>";

        // Query to execute
        String query = "SELECT * FROM <table_name> LIMIT 10";

        // Load the Snowflake driver
        try {
            Class.forName("net.snowflake.client.jdbc.SnowflakeDriver");
        } catch (ClassNotFoundException e) {
            System.err.println("Error loading Snowflake Driver: " + e.getMessage());
            return;
        }

        // Establish connection and execute query
        try (
                Connection connection = DriverManager.getConnection(
                        url,
                        user,
                        password)) {

            // Set session parameters (optional)
            connection.createStatement().execute("USE WAREHOUSE " + warehouse);
            connection.createStatement().execute("USE DATABASE " + database);
            connection.createStatement().execute("USE SCHEMA " + schema);

            // Prepare and execute query
            try (PreparedStatement preparedStatement = connection.prepareStatement(query);
                 ResultSet resultSet = preparedStatement.executeQuery()) {

                // Process the result set
                while (resultSet.next()) {
                    System.out.println("Column 1: " + resultSet.getString(1));
                    // Add more columns as needed
                }
            }

        } catch (
                SQLException e) {
            System.err.println("SQL Exception: " + e.getMessage());
        }*/

        System.out.println("Create JDBC connection");
        Connection connection = getConnection();
        System.out.println("Done creating JDBC connectionn");

        System.out.println("Create JDBC statement");
        Statement statement = connection.createStatement();
        System.out.println("Done creating JDBC statementn");


        System.out.println("Create demo table");
        //statement.executeUpdate("create or replace table demo(C1 STRING)");
        //statement.close();
        System.out.println("Done creating demo tablen");


        System.out.println("Insert 'hello world'");
      // statement.executeUpdate(" CREATE STAGE AWB_RAW_2");
        //statement.close();
        System.out.println("Done inserting 'hello world'n");
        // query the data
        System.out.println("Query demo");
       ;
        ClassLoader classLoader = getClass().getClassLoader();
       String fileP=classLoader.getResource(".").getFile()+"test.pdf";
        ResultSet resultSet =  statement.executeQuery("PUT file://"+fileP+" @AWB_RAW AUTO_COMPRESS=FALSE;");
       // ResultSet resultSet = statement.executeQuery("SELECT AWB_DOCAI!PREDICT(GET_PRESIGNED_URL(@AWB_RAW, 'XMLAWB_Report_2024-12-24_16-26-35.pdf'))");
      //  ResultSet resultSet = statement.executeQuery("SHOW STAGES LIKE 'AWB_RAW'");
       // ResultSet resultSet = statement.executeQuery("SHOW GRANTS ON STAGE @AWB_RAW");
        System.out.println("Metadata:");
        System.out.println("================================");
        // fetch metadata
        ResultSetMetaData resultSetMetaData = resultSet.getMetaData();
        System.out.println("Number of columns=" +
                resultSetMetaData.getColumnCount());
        for (int colIdx = 0; colIdx < resultSetMetaData.getColumnCount();
             colIdx++)
        {
            System.out.println("Column " + colIdx + ": type=" +
                    resultSetMetaData.getColumnTypeName(colIdx+1));
        }
        // fetch data
        System.out.println("nData:");
        System.out.println("================================");
        int rowIdx = 0;
        while(resultSet.next())
        {
            System.out.println("row " + rowIdx + ", column 0: " +
                    resultSet.getString(1));
        }
        statement.close();
    }
 public  Connection getConnection()
            throws SQLException
    {
        try
        {
            Class.forName("net.snowflake.client.jdbc.SnowflakeDriver");
        }
        catch (ClassNotFoundException ex)
        {
            System.err.println("Driver not found");
        }
        // build connection properties
        Properties properties = new Properties();
        properties.put("user", snowFlakeUsername);     // replace "" with your username
        properties.put("password", snowFlakePassword); // replace "" with your password
        properties.put("account", snowFlakeAccount);  // replace "" with your account name
        //properties.put("db", "SNOWFLAKE_SAMPLE_DATA");       // replace "" with target database name
        //properties.put("schema", "TPCH_SF1");
        properties.put("db", "IATA_DB");       // replace "" with target database name
        properties.put("schema", "AWB");
        properties.put("role", "ACCOUNTADMIN");// replace "" with target schema name
        //properties.put("tracing", "on");

        // create a new connection
        String connectStr = System.getenv("SF_JDBC_CONNECT_STRING");
        // use the default connection string if it is not set in environment
        if(connectStr == null)
        {
            connectStr = "jdbc:snowflake://"+snowFlakeAccount+".snowflakecomputing.com"; // replace accountName with your account name
        }
        return DriverManager.getConnection(connectStr, properties);
    }
}
