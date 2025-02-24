rules = """The operator may refuse perishable shipments which emit obnoxious odors.

When packed in or with dry ice, perishable shipments must be transported in compliance with the current edition of
the IATA Dangerous Goods Regulations. 

Perishable shipments will not be accepted if the Air Waybill contains unreasonable instructions or specific
conditions such as “Keep under refrigeration at all times” and “Maintain at below 5°C”. Stakeholders other than the
operator must also be involved in the set-up of special operating procedures.

If the shipment is accompanied by health certificates or other official permits, etc., these should be listed as accompanying
documents in the “Handling Information” box of the Air Waybill. The documents should be firmly attached to the Air Waybill
and not enclosed with the goods.
The “Nature and Quantity of Goods” box should show an accurate description, such as “Chilled Meat (Lamb)” or
“Fish–Frozen.” See completed Air Waybill example below.


UC—LATAM CARGO
UC-01 The following information must appear on the air waybills for perishable cargo:
• The exact description of the perishable product: e.g. “fresh salmon”, “fresh flowers”, etc.
• It is recommended to include a 24-hour telephone number for all perishable cargo. 3 • The “Handling Information” box on the Air Waybill for perishable cargo shipment may be supported by the following
16
information (Special Handling Code, followed by the temperature range, either):
3.1 ○ COL (+2°C to +8°C) where possible
○ CRT (+15°C to 25°C) where possible
• Only one temperature range is allowed per air waybill and the temperature range must match with the booking and
label. If there are any discrepancies, the shipment will remain “On hold” until the customer corrects this information.
• Dry ice is classified as a dangerous good. When shipped indoors or with cargo as refrigerant, the air waybill must
contain the relevant information (ex, UN 1845, Carbon dioxide, solid. 2 x 20 kg), per UN Dangerous Goods
Regulations, IATA.

UC-04 Perishable cargo shipments will not be accepted for carriage collect.
UC-05 Perishable goods with strong odors or leaks will not be accepted for transportation.
UC-06 The packaging must be able to withstand a stacking height of up to 3 meters with boxes of the same weight for
at least 24 hours, without the bottom packaging collapsing.
UC-07 All packages containing perishable goods must be labeled with the IATA standard label for perishable products
or any other equivalent label evidencing that the content is perishable. 

7.1 Air Waybill
OPERATOR VARIATIONS: EK-01, FZ-01
It is essential that Air Waybills for perishable shipments be complete and accurate in all respects. The “Shipper’s Name
and Address” and “Consignee’s Name and Address” boxes must show the full name and address, not abbreviated
versions. It is recommended that phone numbers are shown for both Shipper and consignee.

Dry ice is classified as dangerous goods. When shipped in or with perishable cargo as a refrigerant, the Air Waybill must
contain the entries required under the IATA Dangerous Goods Regulations."""

prompt_reqired_goods_available = """The content provided in the context is the Air WayBill. Please let me 
    know if the goods mentioned under Nature and Quantity of Goods section is a perishable goods or 
    Non-Perishable goods. Pleaes provide me the response Yes if Perishable goods and No if it is 
    non-perishable goods"""

prompt_violation_check = """The context provided consists of the Air WayBill content as well as Regulatory 
                    Requirememnts. Please validate if the Air WayBil content is meeting the provided
                    Regulatory requirents. Include any violations related to temperature.
                    Highlight only if there are any violations with the response
                    not exceesing 50 words.
                    """