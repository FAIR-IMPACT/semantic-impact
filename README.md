# Semantic Impact
Semantic Impact framework for AI-powered ontology alignment. 

# Acknowledgements
Semantic Impact is in active development, please find below the acknowledgements for resources and contributions from the ongoing projects.

Region | Project  | Funding information | Work Package |
| ------------- | ------------- | ------------- | ------------- |
| EU | [FAIR-Impact]([http://odissei-data.nl](https://www.fair-impact.eu)) | Horizon 2020 GA 101057344 | WP6 |

# Quick start
Note: This is Proof of Concept of ontology alignment service, all mappings should be checked by human.
```
pip3 install -r requirements.txt
cd src
python3 cli_codemeta.py
```
Expected results:
```
CodeMeta field: programmingLanguage
programmingLanguage ['P3966', 'P277']
        P3966 "programming paradigm" https://www.wikidata.org/wiki/Property:P3966
        P277 "programmed in" https://www.wikidata.org/wiki/Property:P277
CodeMeta field: runtimePlatform
runtimePlatform ['P400']
        P400 "platform" https://www.wikidata.org/wiki/Property:P400
```

# Extended Demo

Input field in Codemeta schema: funding.

Output contains a list of predicted fields from schema.org:
```
{
    "response": "Okay, let's analyze the provided knowledge base and select relevant properties for describing a \u201cfunding\u201d concept.\n\n
Here's a breakdown of the relevant properties and their relevance:\n\n*
`funding` (labeled as 'funding'): This is the core property. It represents the fundamental concept of providing financial or other support.  The description clearly states it\u2019s a property related to grants and sponsorship.\n\n*   `Grant` (labeled as 'Grant'): This is critically important because the knowledge base defines \"funding\" in terms of grants.  A grant is the *vehicle* for funding, and the `Grant` property links the concept of funding to a specific grant.\n\n*   `funder` (labeled as 'funder'): This property specifies *who* is providing the funding.  It's a key element in understanding the source of the funding, relating to the `Grant` property.\n\n*
`FundingAgency` (labeled as 'FundingAgency'): This is related to the `funder` property. It describes the organization *implementing* the funding schemes, often managing the granting process.  This adds context to the funding relationship.\n\n*
`FundingScheme` (labeled as 'FundingScheme'):  This property describes the guidelines and mechanisms within which funding is provided, again tying into the `Grant` and related concepts.  It\u2019s relevant because funding isn't just random support; it operates within a structured scheme.\n\n*   `amount` (as a `MonetaryAmount`): Crucially, any funding relationship *must* be associated with a monetary value. The `amount` property links the funding to a quantifiable value, likely an instance of the `MonetaryAmount` class.\n\n\n**
Explanation of Relevance:**\n\nThese properties work together to create a comprehensive representation of funding.  The relationships between them (e.g., `Grant` supports `fundedItem`, `funder` provides `Grant`, `FundingAgency` manages `FundingScheme`) represent the core aspects of how funding operates within the defined knowledge domain.\n\nDo you want me to elaborate on any specific aspect, or perhaps provide an example of how these properties would be used in a particular scenario?",
    "mappings": [
        "https://schema.org/funding",
        "https://schema.org/Grant",
        "https://schema.org/funder",
        "https://schema.org/FundingAgency",
        "https://schema.org/FundingScheme",
        "https://schema.org/amount",
        "https://schema.org/MonetaryAmount",
        "https://schema.org/fundedItem"
    ]
}
```

# Benchmarks

Available manually curated semantic mappings from [RDA Metadata Schemes WG](https://rd-alliance.github.io/Research-Metadata-Schemas-WG/):
* EOSC/EDMI
* ISO-19115-1
* Dataverse
* DCAT-AP
* DCATv3
* Datacite
* RIF-CS
* DC
* BioSchema
* B2FIND
* DDI
* SPASE
* CodeMeta
* ECRIN Clinical Research Metadata Schem

# Credits

This work is being done in collaboration between DANS-KNAW, Universidad Politécnica de Madrid, CODATA, Danmarks Tekniske Universitet and the Digital Curation Centre (DCC) at the University of Edinburgh. 
