"""Test script for Pydantic V2 core foundation."""

from graphmodels.core import (
    ModelBase,
    NodeProv,
    EdgeProv,
    generate_node_id,
    generate_edge_id,
    generate_text_hash,
    ENTITY_TYPES,
    EDGE_TYPES,
    ProvenanceSystem,
)


def test_id_generation():
    """Test deterministic ID generation."""
    print("Testing ID generation...")

    # Test node ID generation
    node_id = generate_node_id(
        "Paragraph", {"doc_id": "SS-59", "ordinal": 45}, group_id="AAOIFI-SS-59-EN-2023"
    )
    print(f"  Node ID: {node_id}")
    assert node_id == "AAOIFI-SS-59-EN-2023:Paragraph:SS-59:45"

    # Test edge ID generation
    edge_id = generate_edge_id("IsPartOf", "Paragraph:P1", "Section:S1")
    print(f"  Edge ID: {edge_id}")
    assert edge_id == "IsPartOf:Paragraph:P1=>Section:S1"

    # Test text hash
    text_hash = generate_text_hash("The seller must disclose cost and profit.")
    print(f"  Text hash: {text_hash[:16]}...")
    assert len(text_hash) == 40  # SHA1 is 40 hex chars

    print("[PASS] ID generation tests passed\n")


def test_provenance_models():
    """Test provenance mixin models."""
    print("Testing provenance models...")

    # Create a node with provenance
    class TestNode(NodeProv):
        text: str

    node = TestNode(
        node_id="AAOIFI-SS-59-EN-2023:Paragraph:SS-59:45",
        entity_type="Paragraph",
        text="The seller must disclose cost and profit.",
        prov_system=ProvenanceSystem.AAOIFI,
        prov_file_ids=["ss-59-en.json"],
        page_nums=[27],
        support_count=1,
    )

    print(f"  Node ID: {node.node_id}")
    print(f"  Entity Type: {node.entity_type}")
    print(f"  Provenance System: {node.prov_system}")
    print(f"  Support Count: {node.support_count}")

    # Create an edge with provenance
    class TestEdge(EdgeProv):
        pass

    edge = TestEdge(
        rel_id="IsPartOf:Paragraph:P45=>Section:S4",
        prov_system=ProvenanceSystem.AAOIFI,
        derived=False,
    )

    print(f"  Edge ID: {edge.rel_id}")
    print(f"  Derived: {edge.derived}")

    print("[PASS] Provenance model tests passed\n")


def test_registries():
    """Test entity and edge type registries."""
    print("Testing registries...")

    # Register an entity type
    class Paragraph(NodeProv):
        text: str
        ordinal: int

    ENTITY_TYPES.register(
        "Paragraph",
        Paragraph,
        canonical_uri="http://purl.org/spar/doco/Paragraph",
    )

    # Register an edge type
    EDGE_TYPES.register(
        "IsPartOf",
        "Paragraph",
        "Section",
        canonical_uri="http://purl.org/dc/terms/isPartOf",
    )

    # Test retrieval
    model = ENTITY_TYPES.get_model("Paragraph")
    print(f"  Registered entity type: {model.__name__}")
    print(f"  Entity URI: {ENTITY_TYPES.get_uri('Paragraph')}")

    edge_uri = EDGE_TYPES.get_uri("IsPartOf")
    print(f"  Edge URI: {edge_uri}")

    is_valid = EDGE_TYPES.is_valid("IsPartOf", "Paragraph", "Section")
    print(f"  Edge validation: {is_valid}")

    valid_targets = EDGE_TYPES.get_valid_targets("IsPartOf", "Paragraph")
    print(f"  Valid targets: {valid_targets}")

    print("[PASS] Registry tests passed\n")


def test_strict_validation():
    """Test strict validation behavior."""
    print("Testing strict validation...")

    class StrictModel(ModelBase):
        name: str
        count: int

    # Valid model
    valid = StrictModel(name="test", count=42)
    print(f"  Valid model: {valid}")

    # Test extra field rejection
    try:
        invalid = StrictModel(name="test", count=42, extra="not allowed")
        print("  [FAIL] Should have rejected extra field")
    except Exception as e:
        print(f"  [PASS] Correctly rejected extra field: {type(e).__name__}")

    # Test type coercion rejection (strict mode)
    try:
        invalid = StrictModel(name="test", count="42")  # string instead of int
        print("  [FAIL] Should have rejected type mismatch")
    except Exception as e:
        print(f"  [PASS] Correctly rejected type mismatch: {type(e).__name__}")

    print("[PASS] Strict validation tests passed\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Pydantic V2 Core Foundation Tests")
    print("=" * 60 + "\n")

    test_id_generation()
    test_provenance_models()
    test_registries()
    test_strict_validation()

    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)
