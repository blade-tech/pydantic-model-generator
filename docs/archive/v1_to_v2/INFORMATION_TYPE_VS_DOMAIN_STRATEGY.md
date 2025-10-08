# Information Type vs Domain Organization Strategy

## Executive Summary

**Recommendation**: Organize models **by domain first**, not by information type. Use the existing episode-based provenance system to track whether information came from conversations or documents.

**Key Insight from Research**: Temporal knowledge graphs distinguish between:
- **Episodic data**: Time-stamped observations (conversations, messages, events)
- **Reference data**: Stable facts extracted from episodic sources (entities, relationships)

Your existing architecture already implements this pattern via `episode_ids` provenance tracking.

---

## Problem Statement

You ingest two distinct information types:
1. **Conversations**: Slack messages, emails, chat transcripts
2. **Documentation**: AAOIFI standards, fatwas, business documents, PDFs

You also have multiple domains:
- General business (outcomes, tasks, decisions)
- AAOIFI (Islamic finance standards, Shariah compliance)

**Question**: Should you organize by information type (conversation models vs document models) or by domain (business models vs AAOIFI models)?

---

## Analysis: Information Types Are Provenance, Not Structure

### The Episodic vs Reference Pattern

Based on research into temporal knowledge graphs (Graphiti, Zep, OpenAI Cookbook):

**Episodic Data** (source material):
- Conversations from Slack/email
- Documents uploaded by users
- Meeting transcripts
- PDF standards documents
- Characterized by: time-stamped, immutable, source-specific

**Reference Data** (extracted knowledge):
- BusinessOutcome extracted from a Slack conversation
- AAOIFIStandard extracted from a PDF document
- Actor mentioned in either a conversation or document
- Characterized by: stable entities, relationships, synthesized from episodes

### Your Current Architecture Already Implements This

```python
# From graphmodels/core/provenance.py
class NodeProv(BaseModel):
    node_id: str
    episode_ids: Optional[List[str]]  # Links to source episodes
    created_at: Optional[datetime]
    valid_at: Optional[datetime]
```

**What this means**:
- `BusinessOutcome` can be extracted from a Slack conversation OR a business document
- `AAOIFIStandard` can be extracted from a PDF OR discussed in email threads
- Both point back to their source via `episode_ids`

---

## Recommended Strategy: Domain-First Organization

### ✅ DO: Organize by Domain

```
schemas/
├── core/
│   ├── provenance.yaml      # NodeProv, EdgeProv with episode_ids
│   ├── episodes.yaml         # NEW: Episode model
│   └── types.yaml
├── shared/
│   ├── temporal.yaml
│   └── identity.yaml
└── domains/
    ├── business/
    │   ├── entities.yaml     # BusinessOutcome, BusinessTask, BusinessDecision
    │   ├── edges.yaml        # Requires, Fulfills, AssignedTo
    │   └── enums.yaml
    └── aaoifi/
        ├── entities.yaml     # AAOIFIStandard, ShariaBoard, Fatwa
        ├── edges.yaml        # Cites, Supersedes, References
        └── enums.yaml
```

**Why Domain-First?**
1. **Business logic is domain-specific**: BusinessOutcome has different fields/validation than AAOIFIStandard
2. **Relationships are domain-specific**: Business edges (REQUIRES) vs AAOIFI edges (CITES)
3. **Enums are domain-specific**: TaskStatus vs ComplianceStatus
4. **Query patterns are domain-specific**: "What outcomes are at risk?" vs "What standards cite this fatwa?"

### ✅ DO: Track Information Type via Episodes

Create a new `Episode` model to represent source material:

```yaml
# schemas/core/episodes.yaml
id: https://example.com/schemas/core/episodes
name: episodes
description: Source episodes from which entities are extracted

imports:
  - provenance
  - types

enums:
  SourceType:
    permissible_values:
      conversation:
        description: Extracted from conversations (Slack, email, chat)
      document:
        description: Extracted from documents (PDFs, standards, files)

  SourceSystem:
    permissible_values:
      slack: {}
      email: {}
      upload: {}      # User-uploaded documents
      aaoifi_db: {}   # AAOIFI standard database

classes:
  Episode:
    description: A source episode from which knowledge is extracted
    attributes:
      episode_id:
        identifier: true
        range: string

      source_type:
        range: SourceType
        required: true
        description: Whether this is a conversation or document

      source_system:
        range: SourceSystem
        required: true
        description: System from which episode originated

      content:
        range: string
        description: Raw content of the episode

      metadata:
        range: string
        description: JSON metadata (channel_id, file_name, participants, etc.)

      timestamp:
        range: datetime
        required: true
        description: When episode occurred/was created

      # Document-specific fields
      document_title:
        range: string

      document_url:
        range: string

      # Conversation-specific fields
      channel_id:
        range: string

      participants:
        range: string
        multivalued: true
```

### ✅ DO: Link Entities to Episodes via Provenance

```yaml
# schemas/domains/business/entities.yaml
classes:
  BusinessOutcome:
    mixins:
      - ProvenanceFields  # Includes episode_ids
    attributes:
      outcome_type:
        range: string
      status:
        range: OutcomeStatus
      # ... business-specific fields
```

**Example Usage**:
```python
# Conversation-extracted outcome
outcome1 = BusinessOutcome(
    node_id="outcome_123",
    outcome_type="deliverable",
    status=OutcomeStatus.proposed,
    episode_ids=["episode_slack_456"]  # Points to Slack conversation
)

# Document-extracted outcome
outcome2 = BusinessOutcome(
    node_id="outcome_789",
    outcome_type="deliverable",
    status=OutcomeStatus.approved,
    episode_ids=["episode_doc_101"]  # Points to business document
)

# Query for source type
episode = get_episode("episode_slack_456")
print(episode.source_type)  # "conversation"
```

---

## ❌ DON'T: Create Separate Models by Information Type

### Anti-Pattern 1: Type-Specific Entity Models

```python
# ❌ DON'T DO THIS
class ConversationBusinessOutcome(BusinessOutcome):
    channel_id: str
    participants: List[str]

class DocumentBusinessOutcome(BusinessOutcome):
    document_url: str
    document_title: str
```

**Why Not?**:
- Creates model sprawl (2x entities, 2x edges)
- Breaks registry pattern (which type goes in BUSINESS_ENTITIES?)
- Same business logic duplicated
- Source metadata belongs on Episode, not entity

### Anti-Pattern 2: Separate Domain Hierarchies by Type

```python
# ❌ DON'T DO THIS
domains/
├── conversations/
│   ├── business_outcomes.yaml
│   └── aaoifi_standards.yaml
└── documents/
    ├── business_outcomes.yaml
    └── aaoifi_standards.yaml
```

**Why Not?**:
- A `BusinessOutcome` is a `BusinessOutcome` regardless of source
- An `AAOIFIStandard` can be discussed in conversations AND documented in PDFs
- Duplicates domain logic across information types

---

## Model Sprawl Prevention Strategy

### Principle 1: Entities Are Domain Concepts, Not Source Types

```
✅ GOOD: BusinessOutcome (domain entity, works for any source)
❌ BAD:  ConversationOutcome, DocumentOutcome (source-specific)

✅ GOOD: AAOIFIStandard (domain entity, works for any source)
❌ BAD:  PDFStandard, EmailStandard (source-specific)
```

### Principle 2: Source Metadata Lives in Episodes

```python
# ✅ GOOD: Query for conversation-extracted outcomes
SELECT ?outcome WHERE {
  ?outcome :episode_ids ?episode_id .
  ?episode :episode_id ?episode_id .
  ?episode :source_type "conversation" .
}

# ❌ BAD: Create ConversationBusinessOutcome class
```

### Principle 3: Domain Fields, Not Source Fields

```yaml
# ✅ GOOD: Business domain fields
BusinessOutcome:
  attributes:
    outcome_type: string
    status: OutcomeStatus
    priority: Priority
    confidence: Confidence01

# ❌ BAD: Source-specific fields on entity
BusinessOutcome:
  attributes:
    slack_channel_id: string    # Belongs in Episode
    document_page_number: int   # Belongs in Episode
```

### Principle 4: Use Enums for Source Differentiation When Needed

```yaml
# If extraction logic differs by source, use enum on entity
classes:
  BusinessOutcome:
    attributes:
      extraction_method:
        range: ExtractionMethod
        description: How this entity was extracted

enums:
  ExtractionMethod:
    permissible_values:
      conversation_nlp:
        description: Extracted via NLP from conversation
      document_structure:
        description: Extracted via structured parsing of document
      manual_entry:
        description: Manually entered by user
```

---

## Concrete Example: Business Outcome from Different Sources

### Scenario 1: Outcome Extracted from Slack Conversation

```python
# 1. Create Episode for Slack conversation
slack_episode = Episode(
    episode_id="episode_slack_20250106_001",
    source_type=SourceType.conversation,
    source_system=SourceSystem.slack,
    content="@john we need to launch the new payment feature by Q2. High priority.",
    channel_id="C123ABC",
    participants=["john@example.com", "alice@example.com"],
    timestamp=datetime(2025, 1, 6, 14, 30)
)

# 2. Extract BusinessOutcome from conversation
outcome = BusinessOutcome(
    node_id="outcome_payment_feature",
    outcome_type="deliverable",
    status=OutcomeStatus.proposed,
    priority=Priority.high,
    due_date=datetime(2025, 6, 30),
    episode_ids=["episode_slack_20250106_001"],  # Link to source
    prov_system="slack",
    prov_channel_ids=["C123ABC"]
)
```

### Scenario 2: Same Outcome Mentioned in Business Document

```python
# 1. Create Episode for document
doc_episode = Episode(
    episode_id="episode_doc_20250110_roadmap",
    source_type=SourceType.document,
    source_system=SourceSystem.upload,
    content="Q2 2025 Product Roadmap\n\nPayment Feature: High priority deliverable...",
    document_title="Q2 2025 Product Roadmap.pdf",
    document_url="s3://docs/roadmap-q2.pdf",
    timestamp=datetime(2025, 1, 10, 9, 0)
)

# 2. Update existing outcome OR create duplicate for resolution
outcome_v2 = BusinessOutcome(
    node_id="outcome_payment_feature",  # Same node_id for entity resolution
    outcome_type="deliverable",
    status=OutcomeStatus.approved,  # Status changed in document
    priority=Priority.high,
    due_date=datetime(2025, 6, 30),
    episode_ids=[
        "episode_slack_20250106_001",      # Original conversation
        "episode_doc_20250110_roadmap"     # Supporting document
    ],
    prov_system="upload"
)
```

**Key Points**:
- Same `BusinessOutcome` class for both sources
- Multiple `episode_ids` when entity mentioned in multiple sources
- Episode model captures source-specific metadata (channel_id, document_url)

---

## Scenario 3: AAOIFI Standard from Document vs Email Discussion

### AAOIFI Standard Extracted from PDF

```python
# 1. Create Episode for AAOIFI standard PDF
pdf_episode = Episode(
    episode_id="episode_aaoifi_fas_28",
    source_type=SourceType.document,
    source_system=SourceSystem.aaoifi_db,
    content="FAS 28: Murabaha and Other Deferred Payment Sales\n\nDefinition: ...",
    document_title="FAS 28 - Murabaha.pdf",
    document_url="https://aaoifi.com/standards/fas-28",
    timestamp=datetime(2018, 11, 1)  # Publication date
)

# 2. Extract AAOIFIStandard entity
standard = AAOIFIStandard(
    node_id="aaoifi_fas_28",
    standard_code="FAS 28",
    standard_title="Murabaha and Other Deferred Payment Sales",
    standard_type="Accounting",
    status=StandardStatus.active,
    issued_date=datetime(2018, 11, 1),
    episode_ids=["episode_aaoifi_fas_28"],
    prov_system="aaoifi_db"
)
```

### Same Standard Discussed in Email

```python
# 1. Create Episode for email discussion
email_episode = Episode(
    episode_id="episode_email_20250106_compliance",
    source_type=SourceType.conversation,
    source_system=SourceSystem.email,
    content="Subject: Compliance Review\n\nWe need to ensure FAS 28 compliance for all Murabaha contracts...",
    participants=["compliance@example.com", "finance@example.com"],
    timestamp=datetime(2025, 1, 6, 10, 0)
)

# 2. Update standard with additional episode reference
standard.episode_ids.append("episode_email_20250106_compliance")

# 3. Create edge showing relationship discussed in email
cites_edge = Cites(
    edge_id="edge_cites_001",
    source_node_id="murabaha_contract_001",
    target_node_id="aaoifi_fas_28",
    episode_ids=["episode_email_20250106_compliance"],  # Edge from conversation
    prov_system="email"
)
```

---

## Query Patterns: When You Need Source Type

### Query 1: Find All Outcomes Extracted from Conversations

```cypher
MATCH (o:BusinessOutcome)-[:FROM_EPISODE]->(e:Episode)
WHERE e.source_type = "conversation"
RETURN o.node_id, o.status, e.source_system, e.channel_id
```

### Query 2: Find Documents That Mention This Outcome

```cypher
MATCH (o:BusinessOutcome {node_id: "outcome_payment_feature"})-[:FROM_EPISODE]->(e:Episode)
WHERE e.source_type = "document"
RETURN e.document_title, e.document_url, e.timestamp
ORDER BY e.timestamp DESC
```

### Query 3: Find AAOIFI Standards Only from Official Documents

```cypher
MATCH (s:AAOIFIStandard)-[:FROM_EPISODE]->(e:Episode)
WHERE e.source_type = "document" AND e.source_system = "aaoifi_db"
RETURN s.standard_code, s.standard_title, e.document_url
```

### Query 4: Cross-Reference: Standards Discussed in Conversations

```cypher
MATCH (s:AAOIFIStandard)-[:FROM_EPISODE]->(e:Episode)
WHERE e.source_type = "conversation"
RETURN s.standard_code, COUNT(e) as discussion_count
ORDER BY discussion_count DESC
```

---

## Implementation Checklist

### Phase 1: Create Episode Model (1-2 hours)

- [ ] Create `schemas/core/episodes.yaml` with Episode class
- [ ] Define SourceType enum (conversation, document)
- [ ] Define SourceSystem enum (slack, email, upload, aaoifi_db)
- [ ] Add document-specific fields (title, url)
- [ ] Add conversation-specific fields (channel_id, participants)
- [ ] Generate Pydantic models: `gen-pydantic schemas/core/episodes.yaml`
- [ ] Add Episode to `graphmodels/core/__init__.py`

### Phase 2: Update Provenance System (2-3 hours)

- [ ] Verify `episode_ids` field exists on NodeProv and EdgeProv
- [ ] Create FROM_EPISODE edge type in core/edges.yaml
- [ ] Update documentation explaining episode linkage
- [ ] Add helper methods: `get_episode(episode_id)`, `get_episodes_by_entity(node_id)`

### Phase 3: Update Domain Models (NO changes needed!)

- [ ] Verify BusinessOutcome uses ProvenanceFields mixin (✅ already does)
- [ ] Verify AAOIFIStandard uses ProvenanceFields mixin
- [ ] No new fields needed on domain entities
- [ ] No separate conversation/document model variants

### Phase 4: Update Data Ingestion Pipeline (3-4 hours)

- [ ] Slack ingestion: Create Episode with source_type="conversation"
- [ ] Email ingestion: Create Episode with source_type="conversation"
- [ ] Document upload: Create Episode with source_type="document"
- [ ] AAOIFI import: Create Episode with source_type="document", source_system="aaoifi_db"
- [ ] Entity extraction: Always populate `episode_ids` with source episode

### Phase 5: Add Validation Tests (1-2 hours)

```python
# tests/test_episode_provenance.py
def test_conversation_episode():
    """Test creating episode from Slack conversation."""
    episode = Episode(
        episode_id="test_slack_001",
        source_type=SourceType.conversation,
        source_system=SourceSystem.slack,
        content="Test message",
        channel_id="C123",
        participants=["user1@example.com"],
        timestamp=datetime.now()
    )
    assert episode.source_type == SourceType.conversation

def test_document_episode():
    """Test creating episode from document."""
    episode = Episode(
        episode_id="test_doc_001",
        source_type=SourceType.document,
        source_system=SourceSystem.upload,
        content="Document content",
        document_title="Test.pdf",
        document_url="s3://docs/test.pdf",
        timestamp=datetime.now()
    )
    assert episode.source_type == SourceType.document

def test_outcome_links_to_episodes():
    """Test outcome can link to multiple episodes."""
    outcome = BusinessOutcome(
        node_id="outcome_001",
        episode_ids=["episode_slack_001", "episode_doc_002"]
    )
    assert len(outcome.episode_ids) == 2
```

---

## Migration Strategy: If You Already Have Data

### Option 1: Backfill Episodes from Existing Data

If you already have entities with `prov_system` and `prov_channel_ids`:

```python
# Migration script: backfill_episodes.py
def backfill_episodes_from_entities():
    """Create Episode records from existing entity provenance."""

    entities = session.query(BusinessOutcome).all()

    for entity in entities:
        if entity.prov_system == "slack":
            # Create conversation episode
            for channel_id in entity.prov_channel_ids:
                episode = Episode(
                    episode_id=f"backfill_slack_{channel_id}_{entity.created_at}",
                    source_type=SourceType.conversation,
                    source_system=SourceSystem.slack,
                    channel_id=channel_id,
                    timestamp=entity.created_at,
                    content="[Backfilled from entity provenance]"
                )
                session.add(episode)

                # Link entity to episode
                if not entity.episode_ids:
                    entity.episode_ids = []
                entity.episode_ids.append(episode.episode_id)

    session.commit()
```

### Option 2: Gradual Migration

- Keep existing `prov_system` and `prov_channel_ids` fields (mark as deprecated)
- New ingestion uses Episode model
- Old entities still work via deprecated fields
- Backfill episodes over time

---

## Benefits of This Approach

### ✅ Prevents Model Sprawl
- One `BusinessOutcome` class, not 2+ variants
- One `AAOIFIStandard` class, not 2+ variants
- Domain count stays manageable (business, aaoifi, ...), not exponential (business-conversation, business-document, aaoifi-conversation, aaoifi-document)

### ✅ Flexible Querying
- Can query entities by domain: "All business outcomes"
- Can query entities by source type: "Outcomes from conversations"
- Can query entities by source system: "Outcomes from Slack"
- Can query cross-references: "Documents that mention this standard"

### ✅ Maintains Single Source of Truth
- Entity deduplication works across sources (same node_id)
- Multiple episodes can reference same entity
- Temporal validity tracked via `valid_at`/`invalid_at` on entity, not episode

### ✅ Enables Rich Provenance
- Full conversation/document content stored in Episode
- Metadata (channel_id, document_url) on Episode, not entity
- Can reconstruct "why we know this" by following episode links

### ✅ Domain Logic Stays Clean
- BusinessOutcome validation logic defined once
- AAOIFIStandard relationships defined once
- No "if conversation then X, if document then Y" branching

---

## When You MIGHT Need Type-Specific Models

### Rare Case 1: Extraction Confidence Differs by Type

```yaml
# Only if extraction quality truly differs by source
BusinessOutcome:
  attributes:
    confidence:
      range: Confidence01

    extraction_confidence:
      range: Confidence01
      description: Confidence in extraction process

    extraction_method:
      range: ExtractionMethod
      description: How entity was extracted

enums:
  ExtractionMethod:
    permissible_values:
      conversation_nlp: {}      # May have lower confidence
      document_structured: {}   # May have higher confidence
      manual_entry: {}          # High confidence
```

**Use field on entity, not separate class.**

### Rare Case 2: Some Entities Only Exist in One Source Type

```yaml
# Example: SlackThread entity (only from conversations)
classes:
  SlackThread:
    is_a: ConversationEntity  # Subclass of conversation-specific base
    attributes:
      thread_ts: string
      channel_id: string
      participant_count: integer
```

**Use sparingly. Most entities can exist in any source.**

---

## Summary: The Decision Framework

### Organize by DOMAIN when:
- ✅ Different domains have different business logic (outcomes vs standards)
- ✅ Different domains have different relationships (REQUIRES vs CITES)
- ✅ Different domains have different query patterns
- ✅ Different domains have different validation rules

### Organize by SOURCE TYPE when:
- ❌ Almost never as primary organization
- ✅ Only for truly source-specific entities (e.g., SlackThread, EmailHeader)
- ✅ Use Episode model to track source, not entity class hierarchy

### Your Specific Case:
**Primary Organization**: Domain (business, aaoifi)
**Secondary Tracking**: Episode.source_type (conversation, document)
**Result**: Clean domain models + flexible source querying without model sprawl

---

## Next Steps

1. **Create Episode Model** (1-2 hours)
   - Add `schemas/core/episodes.yaml`
   - Generate Pydantic: `gen-pydantic schemas/core/episodes.yaml`

2. **Update Ingestion Pipelines** (2-4 hours)
   - Slack bot: Create Episode with source_type="conversation"
   - Document processor: Create Episode with source_type="document"
   - Always populate `episode_ids` on extracted entities

3. **Validate with Test Cases** (1 hour)
   - Test conversation → BusinessOutcome
   - Test document → BusinessOutcome
   - Test same entity from both sources

4. **Document Query Patterns** (1 hour)
   - Add example queries to README
   - Show how to filter by source type
   - Show how to cross-reference sources

**Total Effort**: ~8 hours to implement full Episode-based provenance system

---

## Conclusion

**Don't organize by information type.** Your information type (conversation vs document) is provenance metadata, not structural differentiation.

**Do organize by domain.** Business logic, relationships, and query patterns are domain-driven, not source-driven.

**Use Episodes as the bridge.** The Episode model captures source-specific metadata (conversation participants, document URLs) while keeping domain entities clean and focused on business logic.

This approach prevents model sprawl, maintains clean domain boundaries, and provides flexible querying across both dimensions (domain AND source type) when needed.
