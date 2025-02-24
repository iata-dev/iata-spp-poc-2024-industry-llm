rules = """Regulatory Requirements: 1.4.1 When packed in or with dry ice, 
        perishable shipments must be transported in compliance with the current edition of
        the IATA Dangerous Goods Regulations. 1.4
        Dry ice is classified as a dangerous good. When shipped indoors or with cargo as refrigerant, the air waybill must
        contain the relevant information per UN Dangerous Goods Regulations, IATA."""

prompt_reqired_goods_available = """The content provided in the context is the Air WayBill. Please let me know if the goods
             mentioned under Nature and Quantity of Goods section contains Dry Ice or ICE. Please provide a one
             word answer Yes or No."""

prompt_violation_check = """The context provided consists of the Air WayBill content as well as Regulatory 
                    Requirememnts. Please highlight if any specific regulations to be followed for 
                    the Dry Ice. provide the response not exceeding 50 words.
                    """