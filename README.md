# IATA Strategic Partnership Program - Data and Tecnology POC 
# Industry LLM Project


## Context 

Large Language Models (LLM’s) exploded into the mainstream
in late 2022 with the release of OpenAI’s ChatGPT-3.5—a
seemingly all-knowing, human-like chat interface that captured
the public’s imagination. Early use cases may have focused
on content creation, but LLM’s are evolving rapidly and
stakeholder across the aviation world are keen to understand
their applicability to real-world challenges.

To this end, in 2024 IATA has taken the lead by convening a Proof-ofConcept (POC) working group composed of representatives
from IATA Member Airlines and strategic partners from the
technology industry. This group was tasked with identifying,
building and evaluating a use case to illustrate how LLM’s
could be harnessed to address real-world challenges in
aviation beyond the obvious chat bot like solutions that most
people imagine when hearing about an LLM. 

This code repository contains the practical results of the working group as it set out
to explores the applicability of LLMs specifically in the cargo acceptance process, serving as a stepping stone towards further leveraging LLMs for regulatory compliance across the airline industry.

For more details please refer to the official website where 
you will find the accompagnying POC paper giving full context about this initiative -  [IATA SPP Data and Technology POC](https://www.iata.org/en/programs/innovation/data-tech/#tab-3.)

## Architecure

Given the diverse range of IATA Strategic Partners
contributing to this POC, the working group chose to develop
multiple back-end modules to achieve the same functionality.
This approach showcases the unique strengths of different
cloud platforms while also demonstrating that the challenge
is universal and can be addressed effectively using various
technology stacks to achieve similar results.

In terms of contribution—Infosys, Microsoft, SITA and
Snowflake each delivered a back-end component that
performs the document ingestion through various channels
for classification, information extraction, data validation,
and compliance checking as well as a Retrieval Augmented
Generation (RAG) like knowledge base approach on a subset
of IATA PCR standards that are relevant to this use case as well
as specific regulations prepared by the participating airlines
(All Nippon Airways, LATAM and Qatar Airways).

In terms of user interaction we wanted to focus on a different
LLM interaction paradigm that goes beyond the traditional
chat screen. As such the front-end part of the POC was
delivered by Dreamix and it is composed of a simple mobile
app that allows the user to take pictures of documents and
displays the validation status. A second user interface is a
SITA delivered WhatsApp channel that allows for the same
interaction but within the messaging app. The front end
communicates with an integration layer delivered by Qatar
Airways IT that dispatches the requests via a set of standard
APIs between the different modules.

![POC Arhitecture](/assets/POC_Architecture.png)

## Structure

```
/containers/
├── backend-infosys/        # Infosys delivered LLM based container. Works with integration component.
├── backend-microsoft/      # Standalone Microsoft delivered container. Comes with Streamlit app.
├── backend-sita/           # Standalone SITA delivered container. Comes with Whatsapp interface.
├── backend-snowflake/      # Snwoflake delivered LLM based container. Works with integration component.
├── frontend/               # Dreamix web app
└── integration/            # Qatar Airways delivered middlelayer between web app and Snowflake/ Infosys backends.
```

## License 

This sample code is made available under the MIT-0 license. See the LICENSE file.