"""
Pytest-based validation tests for AAOIFI standards models.

Tests entity creation, canonical URI mappings, edge validation,
and OutcomeSpec validation queries.
"""

import pytest
from datetime import date
from pydantic import ValidationError

# Import AAOIFI models
from generated.pydantic.overlays.aaoifi_standards_models import (
    Document,
    Section,
    Paragraph,
    Concept,
    ContractType,
    Rule,
    Agent,
    HasComponent,
    About,
    EvidenceOf,
    AttributedTo,
)

# Import glue utilities
from generated.pydantic.overlays.aaoifi_standards_glue import (
    AAOIFI_NODE_URI,
    AAOIFI_EDGE_URI,
    AAOIFI_ENTITY_TYPES,
    AAOIFI_EDGE_TYPES,
    AAOIFI_EDGE_TYPE_MAP,
    validate_edge_type,
    get_allowed_edges,
    get_entity_uri,
    get_edge_uri,
)


class TestAAOIFIEntityCreation:
    """Test AAOIFI entity models can be created with valid data."""

    def test_document_creation(self):
        """Test Document entity with required fields."""
        doc = Document(
            title="AAOIFI Sharia Standard No. 59",
            edition="2023",
            issued=date(2023, 1, 1),
            source_url="https://aaoifi.com/standards/ss-59",
            language="en",
            node_id="AAOIFI-SS-59-EN-2023"
        )

        assert doc.title == "AAOIFI Sharia Standard No. 59"
        assert doc.edition == "2023"
        assert doc.node_id == "AAOIFI-SS-59-EN-2023"

    def test_section_creation(self):
        """Test Section entity."""
        section = Section(
            label="Introduction",
            order=1,
            node_id="AAOIFI-SS-59-INTRO"
        )

        assert section.label == "Introduction"
        assert section.order == 1

    def test_paragraph_creation(self):
        """Test Paragraph entity with page numbers."""
        para = Paragraph(
            section_id="AAOIFI-SS-59-INTRO",
            ordinal=1,
            text="This standard addresses the permissibility of Murabaha transactions.",
            page_from=5,
            page_to=5,
            node_id="AAOIFI-SS-59-INTRO-P1"
        )

        assert para.text.startswith("This standard")
        assert para.page_from == 5

    def test_concept_creation(self):
        """Test Concept entity with SKOS metadata."""
        concept = Concept(
            curie="if:Murabaha",
            pref_label="Murabaha",
            alt_labels=["Cost-plus sale", "Mark-up sale"],
            definition="A sale contract where the seller discloses the cost and profit margin",
            node_id="CONCEPT-MURABAHA"
        )

        assert concept.curie == "if:Murabaha"
        assert len(concept.alt_labels) == 2

    def test_contract_type_creation(self):
        """Test ContractType entity."""
        contract = ContractType(
            curie="if:MurabahaContract",
            pref_label="Murabaha Contract",
            definition="A sales contract with disclosed cost-plus pricing",
            node_id="CONTRACT-MURABAHA"
        )

        assert contract.pref_label == "Murabaha Contract"

    def test_rule_creation(self):
        """Test Rule entity with normative effect."""
        rule = Rule(
            title="Disclosure requirement",
            text="The seller must disclose the original cost to the buyer",
            article_no="Art. 4(1)",
            normative_effect="requires",
            node_id="RULE-DISCLOSURE"
        )

        assert rule.normative_effect == "requires"
        assert rule.article_no == "Art. 4(1)"

    def test_agent_creation(self):
        """Test Agent entity."""
        agent = Agent(
            name="AAOIFI",
            homepage="https://aaoifi.com",
            node_id="AGENT-AAOIFI"
        )

        assert agent.name == "AAOIFI"


class TestAAOIFIEdgeCreation:
    """Test AAOIFI edge models."""

    def test_has_component_edge(self):
        """Test HasComponent relationship."""
        edge = HasComponent(
            order=1,
            rel_id="DOC-SECTION-1"
        )

        assert edge.order == 1

    def test_about_edge(self):
        """Test About relationship with weight."""
        edge = About(
            weight=0.95,
            rel_id="PARA-CONCEPT-1"
        )

        assert edge.weight == 0.95

    def test_evidence_of_edge(self):
        """Test EvidenceOf relationship with quote."""
        edge = EvidenceOf(
            quote="The seller must disclose...",
            page_from=12,
            page_to=12,
            rel_id="RULE-PARA-1"
        )

        assert edge.quote.startswith("The seller")

    def test_attributed_to_edge(self):
        """Test AttributedTo relationship."""
        edge = AttributedTo(
            role="issuer",
            rel_id="DOC-AGENT-1"
        )

        assert edge.role == "issuer"


class TestCanonicalURIMappings:
    """Test canonical ontology URI mappings."""

    def test_entity_uris(self):
        """Test all entity types have canonical URIs."""
        assert get_entity_uri("Document") == "http://purl.org/spar/fabio/SpecificationDocument"
        assert get_entity_uri("Section") == "http://purl.org/spar/doco/Section"
        assert get_entity_uri("Paragraph") == "http://purl.org/spar/doco/Paragraph"
        assert get_entity_uri("Concept") == "http://www.w3.org/2004/02/skos/core#Concept"
        assert get_entity_uri("ContractType") == "https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/Contract"
        assert get_entity_uri("Rule") == "https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/ContractualElement"
        assert get_entity_uri("Agent") == "http://www.w3.org/ns/prov#Agent"

    def test_edge_uris(self):
        """Test all edge types have canonical URIs."""
        assert get_edge_uri("HasComponent") == "http://purl.org/dc/terms/hasPart"
        assert get_edge_uri("About") == "http://purl.org/dc/terms/subject"
        assert get_edge_uri("EvidenceOf") == "http://www.w3.org/ns/prov#wasDerivedFrom"
        assert get_edge_uri("AttributedTo") == "http://www.w3.org/ns/prov#wasAttributedTo"

    def test_uri_prefixes(self):
        """Test URIs use expected ontology prefixes."""
        doc_uri = get_entity_uri("Document")
        assert "fabio" in doc_uri

        section_uri = get_entity_uri("Section")
        assert "doco" in section_uri

        agent_uri = get_entity_uri("Agent")
        assert "prov" in agent_uri


class TestGraphitiTypeRegistries:
    """Test Graphiti type registry dictionaries."""

    def test_entity_type_registry(self):
        """Test all entity types are registered."""
        assert "Document" in AAOIFI_ENTITY_TYPES
        assert "Section" in AAOIFI_ENTITY_TYPES
        assert "Paragraph" in AAOIFI_ENTITY_TYPES
        assert "Concept" in AAOIFI_ENTITY_TYPES
        assert "ContractType" in AAOIFI_ENTITY_TYPES
        assert "Rule" in AAOIFI_ENTITY_TYPES
        assert "Agent" in AAOIFI_ENTITY_TYPES

        assert len(AAOIFI_ENTITY_TYPES) == 7

    def test_edge_type_registry(self):
        """Test all edge types are registered."""
        assert "HasComponent" in AAOIFI_EDGE_TYPES
        assert "About" in AAOIFI_EDGE_TYPES
        assert "EvidenceOf" in AAOIFI_EDGE_TYPES
        assert "AttributedTo" in AAOIFI_EDGE_TYPES

        assert len(AAOIFI_EDGE_TYPES) == 4

    def test_entity_classes_are_correct(self):
        """Test entity registry maps to correct Pydantic classes."""
        assert AAOIFI_ENTITY_TYPES["Document"] == Document
        assert AAOIFI_ENTITY_TYPES["Section"] == Section
        assert AAOIFI_ENTITY_TYPES["Paragraph"] == Paragraph


class TestEdgeTypeValidation:
    """Test edge type validation functions."""

    def test_document_section_component(self):
        """Test Document → Section HasComponent relationship."""
        assert validate_edge_type("Document", "Section", "HasComponent") == True
        assert get_allowed_edges("Document", "Section") == ["HasComponent"]

    def test_section_paragraph_component(self):
        """Test Section → Paragraph HasComponent relationship."""
        assert validate_edge_type("Section", "Paragraph", "HasComponent") == True

    def test_paragraph_concept_about(self):
        """Test Paragraph → Concept About relationship."""
        assert validate_edge_type("Paragraph", "Concept", "About") == True

    def test_rule_paragraph_evidence(self):
        """Test Rule → Paragraph EvidenceOf relationship."""
        assert validate_edge_type("Rule", "Paragraph", "EvidenceOf") == True

    def test_document_agent_attribution(self):
        """Test Document → Agent AttributedTo relationship."""
        assert validate_edge_type("Document", "Agent", "AttributedTo") == True

    def test_invalid_edge_type(self):
        """Test validation rejects invalid edge types."""
        assert validate_edge_type("Document", "Paragraph", "HasComponent") == False
        assert validate_edge_type("Section", "Agent", "About") == False

    def test_get_allowed_edges_empty(self):
        """Test get_allowed_edges returns empty list for invalid pairs."""
        assert get_allowed_edges("Section", "Agent") == []


class TestOutcomeSpecValidation:
    """Test that generated models support OutcomeSpec validation queries."""

    def test_document_retrieval_fields(self):
        """Validation query: test_document_retrieval

        Expected fields: id, title, edition, issued
        Expected relations: AttributedTo
        """
        doc = Document(
            title="Test Standard",
            edition="2023",
            issued=date(2023, 1, 1),
            node_id="TEST-DOC"
        )
        agent = Agent(
            name="Test Issuer",
            node_id="TEST-AGENT"
        )
        attribution = AttributedTo(
            role="issuer",
            rel_id="TEST-ATTR"
        )

        # Verify all required fields exist
        assert hasattr(doc, 'node_id')  # Maps to 'id' in query
        assert hasattr(doc, 'title')
        assert hasattr(doc, 'edition')
        assert hasattr(doc, 'issued')
        assert hasattr(agent, 'name')

    def test_document_structure_traversal(self):
        """Validation query: test_document_structure

        Expected relations: HasComponent (Document→Section→Paragraph)
        """
        doc = Document(title="Test", node_id="DOC")
        section = Section(label="Intro", order=1, node_id="SEC")
        para = Paragraph(section_id="SEC", ordinal=1, text="Text", node_id="PARA")

        # Verify structural fields exist
        assert hasattr(section, 'label')
        assert hasattr(section, 'order')
        assert hasattr(para, 'ordinal')
        assert hasattr(para, 'text')

    def test_topical_tagging(self):
        """Validation query: test_topical_tagging

        Expected relations: About (Paragraph→Concept)
        """
        para = Paragraph(section_id="SEC", ordinal=1, text="Test", node_id="PARA")
        concept = Concept(curie="if:Test", pref_label="Test Concept", node_id="CONCEPT")
        about_edge = About(rel_id="PARA-CONCEPT")

        assert hasattr(concept, 'pref_label')

    def test_rule_provenance(self):
        """Validation query: test_rule_provenance

        Expected fields: article_no, normative_effect, page_from, page_to
        Expected relations: EvidenceOf (Rule→Paragraph)
        """
        rule = Rule(
            title="Test Rule",
            article_no="Art. 1",
            normative_effect="requires",
            text="Test text",
            node_id="RULE"
        )
        para = Paragraph(
            section_id="SEC",
            ordinal=1,
            text="Source text",
            page_from=10,
            page_to=11,
            node_id="PARA"
        )
        evidence = EvidenceOf(
            quote="Source text",
            page_from=10,
            page_to=11,
            rel_id="RULE-PARA"
        )

        # Verify all required fields exist
        assert hasattr(rule, 'article_no')
        assert hasattr(rule, 'normative_effect')
        assert hasattr(para, 'page_from')
        assert hasattr(para, 'page_to')
        assert hasattr(evidence, 'quote')

    def test_contract_type_rules(self):
        """Validation query: test_contract_type_rules

        Expected relations: About (Paragraph→ContractType), EvidenceOf (Rule→Paragraph)
        """
        para = Paragraph(section_id="SEC", ordinal=1, text="Contract text", node_id="PARA")
        contract = ContractType(
            curie="if:TestContract",
            pref_label="Test Contract",
            node_id="CONTRACT"
        )
        rule = Rule(
            title="Contract Rule",
            normative_effect="requires",
            text="Rule text",
            node_id="RULE"
        )

        assert hasattr(contract, 'pref_label')
        assert hasattr(rule, 'normative_effect')


class TestProvenanceFields:
    """Test provenance tracking fields work across all entities."""

    def test_document_provenance(self):
        """Test Document has full provenance fields."""
        doc = Document(
            title="Test",
            node_id="DOC-123",
            prov_system="aaoifi_db",
            prov_file_ids=["file-001"],
            support_count=3
        )

        assert doc.node_id == "DOC-123"
        assert doc.prov_system == "aaoifi_db"
        assert doc.support_count == 3

    def test_edge_provenance(self):
        """Test edges have edge-specific provenance."""
        edge = EvidenceOf(
            rel_id="EDGE-123",
            prov_system="extraction_pipeline",
            derived=True,
            derivation_rule="llm_extraction_v1",
            quote="Test quote",
            page_from=10,
            page_to=10
        )

        assert edge.derived == True
        assert edge.derivation_rule == "llm_extraction_v1"


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
