package com.qr.apigateway.qr_integration.digital.upload.domain.util;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.StringWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

public class JsonUtil<T> {

    public T convertJsonToObject(String jsonText, Class<T> claz) {
        ObjectMapper mapper = new ObjectMapper();
        try{
            DateFormat df = new SimpleDateFormat("dd-MMM-yyyy");
            mapper.setDateFormat(df);
            mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
            return mapper.readValue(jsonText, claz);
        }
        catch(Exception e) {
            System.out.println("JsonUtil -> "+e.getMessage());
        }
        return null;
    }

    public String converObjectToJson(T instance) {
        StringWriter stringWriter = new StringWriter();
        ObjectMapper objectMapper = new ObjectMapper();
        try{
            objectMapper.writeValue(stringWriter, instance);
        }
        catch(Exception e) {
            System.out.println("convertObjectToJson -> "+e.getMessage());
        }
        return stringWriter.toString();
    }
}
