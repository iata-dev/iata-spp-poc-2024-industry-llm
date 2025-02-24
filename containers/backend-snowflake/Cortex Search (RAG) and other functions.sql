USE ROLE accountadmin;

CREATE OR REPLACE WAREHOUSE COMPUTE_WH WITH WAREHOUSE_SIZE='X-SMALL';
CREATE OR REPLACE DATABASE IATA_DB;
CREATE OR REPLACE SCHEMA AWB;

USE WAREHOUSE COMPUTE_WH;
USE DATABASE IATA;
USE SCHEMA AWB;

-- Location to upload documents from front end application
CREATE OR REPLACE STAGE IATA_DB.AWB.DOCS
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Location to store PCR document
CREATE OR REPLACE STAGE IATA_DB.AWB.PCR
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');


-- Upload PCR document to stage IATA_DB.AWB.PCR --

----------------------------------
-------Parse PCR Document---------
----------------------------------
CREATE OR REPLACE TABLE PCR_TEXT AS
SELECT RELATIVE_PATH as file_name, SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
   @IATA_DB.AWB.PCR, -- stage
   RELATIVE_PATH, -- relative path
   {'mode': 'layout'} -- OCR or Layout modes
):content as contents FROM DIRECTORY(@IATA_DB.AWB.PCR) where RELATIVE_PATH LIKE '%.pdf';

select * from pcr_text limit 10;


----------------------------------------------------------------------
-- Chunk the file contents into 3000 character chunks, overlap each
-- chunk by 1000 characters.
----------------------------------------------------------------------
CREATE or REPLACE TABLE PCR_CHUNKED AS
SELECT
   file_name,
   c.value::VARCHAR chunk_text
FROM
   PCR_TEXT,
   LATERAL FLATTEN( input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER (
      contents,
      'markdown',
      3000,
      1000
   )) c;


select * from PCR_CHUNKED limit 10;


----------------------------------------------------------
---Create RAG Search Service for searching PCR Document---
----------------------------------------------------------
CREATE OR REPLACE CORTEX SEARCH SERVICE PCR_SEARCH
    ON CHUNK_TEXT
    ATTRIBUTES FILE_NAME
    WAREHOUSE = compute_wh
    TARGET_LAG = '30 day'
    AS ( SELECT CHUNK_TEXT, FILE_NAME 
    FROM PCR_CHUNKED );


-- Create function to detect document types
CREATE OR REPLACE PROCEDURE "CHECK_DOC_TYPE"("DOC_NAME" VARCHAR(16777216))
RETURNS VARCHAR(16777216)
LANGUAGE SQL
EXECUTE AS OWNER
AS 'declare doc_type varchar;
begin 
  create or replace temp table document_putput as
(select SUBSTR(replace(SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    @IATA_DB.AWB.DOCS,
    :doc_name,
    {''mode'': ''OCR''}
  )[''content''],'''''''',''''),0,200) as content);
  select (snowflake.cortex.classify_text(content,[''Airway Bill'',''Pythosanitary Document'',''Packing List'', ''Invoice'']))[''label'']::varchar into :doc_type from document_putput;
return doc_type;
end';


-- Create search function to search AWB information and match list of documents against PCR document using RAG capabilities.
CREATE OR REPLACE PROCEDURE "SEARCH_PCR"("SEARCH_STRING" VARCHAR(16777216), "DOC_LIST" VARCHAR(16777216))
RETURNS TABLE ("LLM_RES" VARCHAR(16777216))
LANGUAGE SQL
EXECUTE AS OWNER
AS 'DECLARE
 res RESULTSET;
 search_string_conv varchar;
BEGIN

select snowflake.cortex.complete(''llama3.1-8b'', ''convert destination and origin airport codes to country names in the following text. Do not add any explanation or do not start with Here is the text.: ''||:search_string) as conv into :search_string_conv ;

create or replace temp table cortex_search_result as
  (SELECT (
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      ''PCR_SEARCH'', --Search service name
       concat(''{
         "query": "'','' Supplementary Documents required for: '', :search_string_conv ,''",
          "columns":["CHUNK_TEXT"],"limit":5}'')
          )
    ) as chunk);
 res :=(SELECT snowflake.cortex.complete(
    ''llama3.1-8b'', 
     CONCAT(''You are a helpful AI chat assistant for Airway Cargo document inspection with RAG capabilities. Ensure the answer is coherent, concise,and directly relevant to the question of user.Dont say things like "according to the provided context", here is the list of documents required for AWB. Do no add any explanation, Only return the list: '',
        (select chunk from cortex_search_result),
        ''Combine this list with doc_list, deduplicate the results and return a JSON as list of documents with only document name as attribute: '',
        ''doc_list: '',:doc_list,
        '' Question: '', concat(''Combine the Chunk_Texts and find What are the required documents for following AWB content and deduplicate similar documents: '', :search_string),
        '' Answer: ''
    )
) llm_response);
    
    return table(res);
END';

