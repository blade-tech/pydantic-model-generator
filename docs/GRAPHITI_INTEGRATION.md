# Graphiti Ingestion Methods: Conversations vs Documents

## Executive Summary

**Yes, the ingestion methods differ** between conversations and documents in Graphiti, primarily through:

1. **EpisodeType parameter**: `EpisodeType.message`, `EpisodeType.text`, or `EpisodeType.json`
2. **Bulk vs single episode ingestion**: Documents typically use `add_episode_bulk()`, conversations use `add_episode()`
3. **Content structure**: Conversations are dialogue format, documents are structured data (JSON) or long-form text

However, the core API is the same: `add_episode()` for both. The differences are in **how you structure the input** and **which type you specify**.

---

## Episode Types in Graphiti

Graphiti supports three `EpisodeType` values:

```python
from graphiti_core.nodes import EpisodeType

# For conversations/chat transcripts
EpisodeType.message

# For unstructured text (articles, documents)
EpisodeType.text

# For structured data (JSON documents, API responses)
EpisodeType.json
```

### When to Use Each Type

| Episode Type | Use Case | Example |
|--------------|----------|---------|
| **EpisodeType.message** | Multi-turn conversations, chat transcripts, dialogues | Slack threads, email exchanges, tutoring sessions |
| **EpisodeType.text** | Single-author unstructured text, articles, notes | Blog posts, meeting notes, journal entries |
| **EpisodeType.json** | Structured data with key-value pairs | Product catalogs, CRM data, assessment results, AAOIFI standards |

**Key Difference**: The type doesn't change the API, but it hints to Graphiti's LLM how to extract entities/relationships from the content structure.

---

## Method 1: Conversations (EpisodeType.message)

### Single Conversation Example

```python
await graphiti.add_episode(
    name="slack_thread_product_discussion",
    episode_body=(
        "User @john: We need to prioritize the payment feature for Q2\n"
        "PM @alice: Agreed. What's the estimated effort?\n"
        "Engineer @bob: About 6 weeks with testing\n"
        "User @john: Let's commit to it. High priority."
    ),
    source=EpisodeType.message,  # ← Conversation type
    source_description="Slack #product-planning channel",
    reference_time=datetime(2025, 1, 6, 14, 30)
)
```

**What Graphiti Extracts**:
- Entities: Person(john), Person(alice), Person(bob), Feature(payment feature)
- Edges: john MENTIONED payment_feature, alice AGREED_WITH john, bob ESTIMATED_EFFORT payment_feature
- Temporal: All with `valid_at` timestamp from conversation date

### Conversation Format Guidelines

**✅ GOOD - Multi-turn dialogue format**:
```python
episode_body = (
    "Speaker1: First message\n"
    "Speaker2: Response to first message\n"
    "Speaker1: Follow-up\n"
)
```

**✅ GOOD - With speaker identifiers**:
```python
episode_body = (
    "@john: I don't understand this requirement\n"
    "@alice: Let me clarify: we need X, Y, and Z\n"
    "@john: Got it, thanks!"
)
```

**❌ BAD - Single message without context**:
```python
episode_body = "The payment feature is high priority"  # Use EpisodeType.text instead
```

### Batch Conversations

For multiple conversations (e.g., ingesting historical Slack messages):

```python
from graphiti_core.models import RawEpisode

slack_threads = [
    {
        "thread_ts": "1704556800.000",
        "channel": "C123ABC",
        "messages": [
            {"user": "john", "text": "What's the status on the API?"},
            {"user": "alice", "text": "Deployed to staging yesterday"}
        ]
    },
    # ... more threads
]

bulk_episodes = []
for thread in slack_threads:
    dialogue = "\n".join([
        f"@{msg['user']}: {msg['text']}"
        for msg in thread['messages']
    ])

    bulk_episodes.append(
        RawEpisode(
            name=f"slack_thread_{thread['thread_ts']}",
            content=dialogue,  # Note: RawEpisode uses 'content', not 'episode_body'
            source=EpisodeType.message,
            source_description=f"Slack channel {thread['channel']}",
            reference_time=datetime.fromtimestamp(float(thread['thread_ts']))
        )
    )

await graphiti.add_episode_bulk(bulk_episodes)
```

**Performance**: Bulk ingestion is significantly faster for historical data (10-15s per episode vs seconds for entire batch).

---

## Method 2: Documents as Unstructured Text (EpisodeType.text)

### Single Document Example

```python
# Example: AAOIFI standard as text
with open("standards/fas-28-murabaha.pdf", "r") as f:
    document_text = f.read()

await graphiti.add_episode(
    name="aaoifi_fas_28",
    episode_body=document_text,  # Full document text
    source=EpisodeType.text,  # ← Unstructured text type
    source_description="AAOIFI FAS 28 Standard Document",
    reference_time=datetime(2018, 11, 1)  # Publication date
)
```

**What Graphiti Extracts**:
- Entities: Standard(FAS 28), Concept(Murabaha), Requirement(disclosure)
- Edges: FAS_28 DEFINES Murabaha, FAS_28 REQUIRES disclosure
- Temporal: `valid_at` from publication date

### When to Use EpisodeType.text

**✅ Use for**:
- Long-form documents (standards, articles, blog posts)
- Meeting notes (single author)
- Business documents (contracts, policies)
- PDF/Word document content after text extraction

**❌ Don't use for**:
- Structured data (use EpisodeType.json)
- Multi-speaker conversations (use EpisodeType.message)

### Document Chunking Strategy

For very long documents, consider chunking:

```python
# Example: Split 100-page standard into sections
sections = extract_sections_from_pdf("aaoifi_standard.pdf")

bulk_episodes = [
    RawEpisode(
        name=f"aaoifi_fas_28_section_{i}",
        content=section['text'],
        source=EpisodeType.text,
        source_description=f"AAOIFI FAS 28 - Section {section['number']}: {section['title']}",
        reference_time=datetime(2018, 11, 1)
    )
    for i, section in enumerate(sections)
]

await graphiti.add_episode_bulk(bulk_episodes)
```

**Why Chunk?**:
- Better LLM extraction quality (smaller context windows)
- More precise provenance (link entities to specific sections)
- Faster processing (parallel extraction)

---

## Method 3: Documents as Structured Data (EpisodeType.json)

### Single Structured Document Example

```python
# Example: AAOIFI standard as structured JSON
standard_data = {
    "standard_code": "FAS 28",
    "title": "Murabaha and Other Deferred Payment Sales",
    "type": "Accounting Standard",
    "issued_date": "2018-11-01",
    "status": "Active",
    "scope": "Application to Islamic financial institutions",
    "key_requirements": [
        "Recognition criteria for Murabaha transactions",
        "Measurement at amortized cost",
        "Disclosure requirements"
    ],
    "references": ["FAS 1", "FAS 2"],
    "supersedes": ["FAS 2 (1995 version)"]
}

await graphiti.add_episode(
    name="aaoifi_fas_28_structured",
    episode_body=json.dumps(standard_data),  # Serialize to JSON string
    source=EpisodeType.json,  # ← Structured data type
    source_description="AAOIFI Standards Database",
    reference_time=datetime(2018, 11, 1)
)
```

**What Graphiti Extracts**:
- Entities: Standard(FAS 28), Concept(Murabaha), Standard(FAS 1), Standard(FAS 2)
- Edges: FAS_28 REFERENCES FAS_1, FAS_28 SUPERSEDES FAS_2_1995
- Attributes: standard_code="FAS 28", status="Active"

### Bulk Structured Documents (Most Common for Documents)

```python
# Example: Bulk load product catalog
product_data = [
    {
        "id": "PROD001",
        "name": "Men's Wool Runners",
        "category": "Footwear",
        "price": 125.00,
        "material": "Wool",
        "in_stock": True
    },
    # ... 100 more products
]

bulk_episodes = [
    RawEpisode(
        name=f"product_{product['id']}",
        content=json.dumps(product),  # Serialize each to JSON
        source=EpisodeType.json,
        source_description="Product catalog",
        reference_time=datetime.now()
    )
    for product in product_data
]

await graphiti.add_episode_bulk(bulk_episodes)
```

**Why Use EpisodeType.json for Documents?**:
- **Better extraction quality**: LLM understands structured schema
- **Preserves relationships**: Keys like "references" → REFERENCES edge
- **Enables validation**: Can enforce schema before ingestion
- **Queryable attributes**: Product price, standard status become searchable

---

## Comparison Table: Conversations vs Documents

| Aspect | Conversations (EpisodeType.message) | Documents (Text) | Documents (JSON) |
|--------|-------------------------------------|------------------|------------------|
| **Episode Type** | `EpisodeType.message` | `EpisodeType.text` | `EpisodeType.json` |
| **Content Format** | Multi-turn dialogue with speakers | Long-form unstructured text | Structured key-value pairs |
| **Typical Sources** | Slack, email, chat, Zoom transcripts | PDFs, articles, meeting notes | APIs, databases, structured exports |
| **Ingestion Method** | Usually `add_episode()` (one at a time) | `add_episode()` or chunked bulk | `add_episode_bulk()` (batch) |
| **Extraction Focus** | Speaker intentions, agreements, mentions | Concepts, definitions, requirements | Attributes, relationships, references |
| **Example Input** | `"@john: Let's prioritize X\n@alice: Agreed"` | `"Chapter 1: Introduction\n\nMurabaha is defined as..."` | `{"standard": "FAS 28", "status": "Active"}` |
| **Reference Time** | Conversation timestamp | Document publication date | Data snapshot timestamp |
| **Source Description** | Channel ID, platform | Document title, author | Database name, API endpoint |

---

## Recommended Ingestion Patterns

### Pattern 1: Real-Time Conversations (Slack Bot)

```python
# Slack event handler
@slack_app.event("message")
async def handle_message(event, say):
    # Get thread context
    thread_ts = event.get("thread_ts", event["ts"])
    thread_messages = await get_thread_messages(thread_ts)

    # Format as dialogue
    dialogue = "\n".join([
        f"@{msg['user']}: {msg['text']}"
        for msg in thread_messages
    ])

    # Ingest to Graphiti
    await graphiti.add_episode(
        name=f"slack_thread_{thread_ts}",
        episode_body=dialogue,
        source=EpisodeType.message,
        source_description=f"Slack #{event['channel']}",
        reference_time=datetime.fromtimestamp(float(thread_ts))
    )
```

### Pattern 2: Historical Conversation Backfill

```python
# Bulk load 1000s of historical Slack messages
async def backfill_slack_history(channel_id: str, start_date: datetime):
    threads = await slack_client.conversations_history(
        channel=channel_id,
        oldest=start_date.timestamp()
    )

    bulk_episodes = []
    for thread in threads:
        dialogue = format_thread_as_dialogue(thread)
        bulk_episodes.append(
            RawEpisode(
                name=f"slack_{channel_id}_{thread['ts']}",
                content=dialogue,
                source=EpisodeType.message,
                source_description=f"Slack #{channel_id}",
                reference_time=datetime.fromtimestamp(float(thread['ts']))
            )
        )

    # Process in batches to avoid memory issues
    for i in range(0, len(bulk_episodes), 100):
        batch = bulk_episodes[i:i+100]
        await graphiti.add_episode_bulk(batch)
```

### Pattern 3: Document Upload (AAOIFI Standards)

```python
# User uploads PDF standard
async def ingest_aaoifi_standard(pdf_path: Path):
    # Extract text and metadata
    text_content = extract_text_from_pdf(pdf_path)
    metadata = extract_standard_metadata(pdf_path)  # Parse header for code, date

    # Create structured episode
    standard_json = {
        "standard_code": metadata["code"],
        "title": metadata["title"],
        "issued_date": metadata["issued_date"],
        "full_text": text_content,  # Include full text for semantic search
        "sections": extract_sections(text_content)
    }

    await graphiti.add_episode(
        name=f"aaoifi_{metadata['code'].replace(' ', '_').lower()}",
        episode_body=json.dumps(standard_json),
        source=EpisodeType.json,
        source_description="AAOIFI Standard Upload",
        reference_time=metadata["issued_date"]
    )
```

### Pattern 4: Email Ingestion

```python
# Email thread (conversation type)
async def ingest_email_thread(thread_id: str):
    emails = await gmail.get_thread(thread_id)

    # Format as dialogue
    dialogue = "\n".join([
        f"{email['from']}: {email['subject']}\n{email['body']}"
        for email in emails
    ])

    await graphiti.add_episode(
        name=f"email_thread_{thread_id}",
        episode_body=dialogue,
        source=EpisodeType.message,
        source_description="Gmail thread",
        reference_time=emails[0]['date']
    )
```

### Pattern 5: Business Document (Unstructured)

```python
# Business proposal document
async def ingest_business_document(doc_path: Path):
    with open(doc_path, "r") as f:
        content = f.read()

    await graphiti.add_episode(
        name=doc_path.stem,
        episode_body=content,
        source=EpisodeType.text,
        source_description=f"Business document: {doc_path.name}",
        reference_time=datetime.fromtimestamp(doc_path.stat().st_mtime)
    )
```

---

## Advanced: Custom Entity/Edge Types by Episode Type

You can customize entity extraction based on episode type:

```python
# For conversations: Focus on people and their intentions
conversation_entity_types = [
    "Person",
    "Company",
    "Feature",
    "Decision",
    "Action"
]

conversation_edge_types = [
    "MENTIONED",
    "AGREED_WITH",
    "DISAGREED_WITH",
    "ASSIGNED_TO",
    "COMMITTED_TO"
]

# For AAOIFI documents: Focus on standards and compliance
document_entity_types = [
    "Standard",
    "Concept",
    "Requirement",
    "Prohibition",
    "Fatwa"
]

document_edge_types = [
    "DEFINES",
    "REFERENCES",
    "SUPERSEDES",
    "REQUIRES",
    "CITES"
]

# Apply when adding episode
await graphiti.add_episode(
    name="slack_discussion",
    episode_body=dialogue,
    source=EpisodeType.message,
    entity_types=conversation_entity_types,
    edge_types=conversation_edge_types
)

await graphiti.add_episode(
    name="aaoifi_standard",
    episode_body=json.dumps(standard),
    source=EpisodeType.json,
    entity_types=document_entity_types,
    edge_types=document_edge_types
)
```

---

## Performance Considerations

### Conversation Ingestion

**Single Episode (Real-Time)**:
- Latency: ~500ms - 2s per message thread
- Use for: Live Slack/email integration
- Optimization: Only ingest complete threads, not individual messages

**Bulk Episodes (Historical)**:
- Throughput: ~100 episodes/minute
- Use for: Backfilling historical chat logs
- Optimization: Batch in groups of 50-100 episodes

### Document Ingestion

**Single Document (Upload)**:
- Latency: ~2-5s per document (depends on size)
- Use for: User uploads, API syncs
- Optimization: Chunk large documents (>10k tokens)

**Bulk Documents (Catalog/Database)**:
- Throughput: ~500-1000 documents/minute (JSON format)
- Use for: Product catalogs, standards libraries
- Optimization: Use `add_episode_bulk()`, parallelize extraction

**Memory Usage**:
- Conversations: Low (text-only)
- Documents (text): Medium (text extraction)
- Documents (JSON): Low (already structured)

---

## Error Handling

### Common Issues by Type

**EpisodeType.message**:
- ❌ **Missing speaker identifiers**: LLM can't determine who said what
  - Fix: Add `@username:` or `Speaker:` prefixes
- ❌ **Single message as dialogue**: Not a conversation
  - Fix: Use `EpisodeType.text` instead

**EpisodeType.text**:
- ❌ **Malformed text extraction**: PDF parsing errors
  - Fix: Validate text quality before ingestion
- ❌ **Too long for LLM context**: Document >100k tokens
  - Fix: Chunk into sections

**EpisodeType.json**:
- ❌ **Invalid JSON**: Serialization errors
  - Fix: Validate with `json.loads()` before `json.dumps()`
- ❌ **Deeply nested objects**: LLM can't extract relationships
  - Fix: Flatten structure to 2-3 levels max

### Retry Strategy

```python
async def ingest_with_retry(episode_data: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            await graphiti.add_episode(**episode_data)
            return
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Integration with Your Pydantic Models

### Linking Episodes to Entities

```python
# After ingesting episode
episode_id = "episode_slack_20250106_001"

# Extract entities from Graphiti
search_results = await graphiti.search(
    query="payment feature discussion",
    num_results=10
)

# Create Pydantic models from extracted entities
for result in search_results:
    if "payment feature" in result.fact.lower():
        outcome = BusinessOutcome(
            node_id=result.source_node_uuid,  # Use Graphiti entity UUID
            outcome_type="deliverable",
            status=OutcomeStatus.proposed,
            episode_ids=[episode_id],  # Link to source episode
            prov_system="slack"
        )
```

### Bidirectional Sync

```python
# 1. Ingest to Graphiti
await graphiti.add_episode(
    name="business_outcome_discussion",
    episode_body=slack_dialogue,
    source=EpisodeType.message
)

# 2. Extract entities from Graphiti
entities = await graphiti.search("business outcomes")

# 3. Create Pydantic models from entities
outcomes = [
    BusinessOutcome(
        node_id=entity.source_node_uuid,
        outcome_type="deliverable",
        episode_ids=[episode_id]
    )
    for entity in entities
]

# 4. Store in your database
session.add_all(outcomes)
session.commit()
```

---

## Summary: Key Differences

### What's Different?

1. **EpisodeType parameter**: `message` vs `text` vs `json`
2. **Content structure**: Dialogue format vs unstructured text vs structured JSON
3. **Typical ingestion pattern**: Real-time single episodes (conversations) vs bulk batch (documents)
4. **Entity extraction focus**: Speaker intentions vs document concepts vs structured attributes

### What's the Same?

- Same API: `add_episode()` or `add_episode_bulk()`
- Same parameters: `name`, `episode_body`, `source_description`, `reference_time`
- Same provenance: All episodes get unique IDs, link to extracted entities
- Same search interface: Query across all episode types

### Recommendation for Your Use Case

**Conversations (Slack/Email)**:
```python
# Real-time ingestion
EpisodeType.message + add_episode()
```

**Documents (AAOIFI Standards)**:
```python
# Batch ingestion with structured metadata
EpisodeType.json + add_episode_bulk()
```

**Documents (Business Docs/Meeting Notes)**:
```python
# Single or batch ingestion as text
EpisodeType.text + add_episode() or add_episode_bulk()
```

---

## Next Steps

1. **Implement Episode Model** (from previous doc)
   - Add `source_type` field matching Graphiti's `EpisodeType`
   - Add `source_system` field (slack, email, upload, aaoifi_db)

2. **Create Ingestion Pipelines**:
   - Slack bot: Real-time `add_episode()` with `EpisodeType.message`
   - AAOIFI import: Batch `add_episode_bulk()` with `EpisodeType.json`
   - Document upload: `add_episode()` with `EpisodeType.text`

3. **Link Graphiti Episodes to Pydantic Models**:
   - Store Graphiti episode UUID in your `Episode.episode_id`
   - Use Graphiti entity UUIDs as your `BusinessOutcome.node_id`
   - Query Graphiti for entity extraction, create Pydantic models from results

4. **Test Both Approaches**:
   - Test conversation ingestion with sample Slack threads
   - Test document ingestion with sample AAOIFI standards
   - Verify entity extraction quality for both types
