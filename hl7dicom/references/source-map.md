# Source Map

Use this map to choose the primary standard artifact before reading.

## HL7

- `hl7 hl7v23 Implementation Support Guide HL7 version 2.3.pdf`
Purpose: verify HL7 v2.3 message structures, segment definitions, field usage, and implementation constraints. Use this as the bundled normative HL7 prose source, especially for legacy `ORM^O01` support and shared segment/field interpretation.

- `OMG_O19.xsd`
Purpose: verify HL7 v2.7 XML schema structure for the `OMG_O19` message. Use for message-shape questions such as required segment groups, ordering of `ORC`/`OBR`, timing, specimen, and prior-result nesting.

- `SIU_S12.xsd`
Purpose: verify HL7 v2.7 XML schema structure for the `SIU_S12` scheduling message. Use for message-shape questions involving `SCH`, `RGS`, `AIS`, `AIG`, `AIL`, and `AIP` group layout.

## DICOM

- `DICOM PS3.6 2026a - Data Dictionary.pdf`
Purpose: verify data element dictionary entries, tags, VR, VM, and related identifiers.

- `DICOM PS3.5 2026a - Data Structures and Encoding.pdf`
Purpose: verify value encoding rules, transfer syntax behavior, character set/byte-level constraints, and data structure representation rules.

- `DICOM PS3.7 2026a - Message Exchange.pdf`
Purpose: verify DICOM message service semantics, command sets, status handling, and DIMSE-level interaction details.

- `DICOM PS3.8 2026 - Network Communication Support for Message Exchange.pdf`
Purpose: verify network communication and association behavior for DICOM message exchange.

## Multi-Document Checks

- Use `OMG_O19.xsd` first when the request is about the primary v2.7 order workflow message layout; add the HL7 v2.3 PDF only when the answer also needs legacy/shared segment semantics.
- Use the HL7 v2.3 PDF for `ORM^O01` compatibility questions and explicitly note that the bundled normative text is older than the target v2.7 workflow.
- Use PS3.6 + PS3.5 together when dictionary definitions and encoding semantics are both required.
- Use PS3.7 + PS3.8 together when a question spans DIMSE semantics and transport/association behavior.
