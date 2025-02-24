# Document Validation and Compliance Verification

## Overview
This system ensures a compliant and smooth shipping experience by validating cargo documents, checking for regulatory compliance, embargo restrictions, and required shipping documentation. It leverages **Retrieval-Augmented Generation (RAG)** to extract and apply the latest regulations and country-specific shipping requirements to minimize risks.

## How the System Works

### 1. **Air Waybill (AWB) Validation**
- Extracts key shipping details from AWB images.
- Validates mandatory fields such as shipper, consignee, and routing details.
- Flags missing or inconsistent information.

### 2. **Regulatory Compliance Checks**
- Retrieves country-specific shipping regulations using RAG.
- Ensures compliance with international organizations such as IATA, customs, and industry-specific certifications.

### 3. **Embargo and Restricted Goods Validation**
- Checks whether the destination country has any active embargoes.
- Flags restricted or prohibited items based on global trade laws.
- Assesses risk by evaluating dual-use goods and regulated substances.

### 4. **Shipping Document Verification**
- Confirms the presence of all required documents for customs clearance.
- Cross-checks shipping requirements based on origin and destination countries.
- Validates document types such as commercial invoices, packing lists, and certificates of origin.

### 5. **Temperature and Perishable Goods Monitoring**
- Checks requirements for perishable shipments.
- Validates refrigeration and storage conditions.
- Flags potential risks in packaging and handling.

### 6. **Automated WhatsApp Guidance**
- Guides users step-by-step through document validation.
- Alerts them about missing or incorrect documents.
- Provides real-time feedback based on regulatory compliance data.

## How RAG Enhances the Validation Process
The **Retrieval-Augmented Generation (RAG)** model fetches the latest regulatory data, ensuring that document validation is:

- **Up-to-date**: Always aligned with current global regulations.

- **Comprehensive**: Covers country-specific rules and international shipping guidelines.

- **Reliable**: Minimizes errors and compliance risks.

## Examples of Data Checked
The system evaluates various compliance and trade restrictions, including:

### **1. Embargoed Goods & Trade Restrictions**
- Items prohibited due to embargo policies.
- Goods restricted based on their **use case** (e.g., military-grade, dual-use items).

### **2. Country-Specific Shipping Requirements**
- Export and import document requirements per country.
- Mandatory permits and customs declarations.
- Regulations for handling sensitive goods.

### **3. Perishable & Temperature-Controlled Shipments**
- Temperature and humidity requirements for fresh produce.
- Storage conditions for pharmaceuticals and medical shipments.

## Benefits of the System
- **Reduces shipping delays** due to incomplete documentation.
- **Ensures regulatory compliance** with global trade laws.
- **Minimizes risks** associated with embargoed goods and restricted shipments.
- **Enhances customer satisfaction** by preventing customs rejections.

## License
This project is proprietary and confidential.

## Contact
For more details, contact the development team.
