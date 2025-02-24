rules = """Regulatory Requirements: CHAPTER 11—CONVENTION ON INTERNATIONAL TRADE
    IN ENDANGERED SPECIES OF WILD FAUNA AND FLORA
    (CITES)
    11.2.3 Documentation
    Documents and other essential information shall be contained within durable, waterproof envelopes or sleeves if such
    documents are sent with the packages.
    In a shipment with more than one box to more than one importer, each item shall show the appropriate information and
    carry copies of the original permits.
    On package and documentation include:
    (a) name, full address, and telephone number of the consignor and consignee;
    (b) a unique number or mark, especially for shipments with multiple packages (e.g., package #1 of 6), and documentation
    11 accurately describing the contents (quantity and plant names) of each package;
    (c) documentation that accompanies the shipment providing details of the content of each package, especially species
    11.2 names and the quantities of each;
    (d) when possible, labels on each plant with genus and species names;
    (e) copies of any required export and import licence or permits;
    (f) a phytosanitary certificate (this document does not replace the need for CITES permits, unless used in accordance
    with Resolution Conf. 10.2, section VI, and only for those Parties notified by the Secretariat);
    (g) a description of any pesticide treatment that was applied to the plants prior to the export, including the name of the
    pesticide, the rate of application, and the treatment duration (length of time); and
    (h) other applicable information required by the country of destination.
    Each Party to CITES has a Management Authority responsible for issuing permits. This authority should be contacted for
    further information with regard to CITES requirements, both in the exporting country as in the importing country. To contact
    the CITES Management Authorities or to find out about the Scientific Authorities or the Enforcement Focal Points follow
    this link:
    """

prompt_reqired_goods_available = """The content provided in the context is the Air WayBill. 
    Please let me know if the goods mentioned under Nature and Quantity of Goods section belongs to 
    CITES (CONVENTION ON  INTERNATIONAL TRADE IN ENDANGERED SPECIES OF WILD FAUNA AND FLORA )? 
    Please provide a one word answer Yes or No, with bit of an explanation. 
    Also if the Nature and the quality of goods consists of the code PEA it will be classified as CITES"""

prompt_violation_check = """The context provided consists of the Air WayBill content as well as 
    Regulatory Requirememnts. Please highlight if any specific regulations to be followed for the 
    CITES and also highlight violations any, provide the response not exceeding 50 words."""