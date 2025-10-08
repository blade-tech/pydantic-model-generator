from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'conversation_task_inference',
     'description': 'Schema for inferring and tracking content creation tasks '
                    'derived from conversations ingested into Neo4j via Graphiti, '
                    'maintaining full provenance of the inference process',
     'id': 'https://example.org/schemas/conversation-task-inference',
     'imports': ['../core/provenance'],
     'name': 'conversation_task_inference',
     'prefixes': {'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'doco': {'prefix_prefix': 'doco',
                           'prefix_reference': 'http://purl.org/spar/doco/'},
                  'fabio': {'prefix_prefix': 'fabio',
                            'prefix_reference': 'http://purl.org/spar/fabio/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'}},
     'source_file': '..\\..\\pydantic_library\\schemas\\overlays\\coversation_to_content_overlay.yaml'} )

class ConversationType(str, Enum):
    """
    Types of conversations
    """
    MEETING = "MEETING"
    """
    Meeting or discussion
    """
    CHAT = "CHAT"
    """
    Chat or instant message
    """
    EMAIL = "EMAIL"
    """
    Email exchange
    """
    INTERVIEW = "INTERVIEW"
    """
    Interview or Q&A session
    """
    BRAINSTORM = "BRAINSTORM"
    """
    Brainstorming session
    """
    OTHER = "OTHER"
    """
    Other conversation type
    """


class TaskStatus(str, Enum):
    """
    Status values for tasks
    """
    PENDING = "PENDING"
    """
    Task is pending and not yet started
    """
    IN_PROGRESS = "IN_PROGRESS"
    """
    Task is currently being worked on
    """
    COMPLETED = "COMPLETED"
    """
    Task has been completed
    """
    CANCELLED = "CANCELLED"
    """
    Task was cancelled
    """
    BLOCKED = "BLOCKED"
    """
    Task is blocked by dependencies
    """


class PriorityLevel(str, Enum):
    """
    Priority levels for tasks
    """
    LOW = "LOW"
    """
    Low priority
    """
    MEDIUM = "MEDIUM"
    """
    Medium priority
    """
    HIGH = "HIGH"
    """
    High priority
    """
    URGENT = "URGENT"
    """
    Urgent priority
    """


class ActivityStatus(str, Enum):
    """
    Status values for activities
    """
    STARTED = "STARTED"
    """
    Activity has started
    """
    IN_PROGRESS = "IN_PROGRESS"
    """
    Activity is in progress
    """
    COMPLETED = "COMPLETED"
    """
    Activity has completed
    """
    FAILED = "FAILED"
    """
    Activity has failed
    """
    PAUSED = "PAUSED"
    """
    Activity is paused
    """


class DerivationType(str, Enum):
    """
    Types of derivation relationships
    """
    TASK_FROM_CONVERSATION = "TASK_FROM_CONVERSATION"
    """
    Task derived from conversation
    """
    CONTENT_FROM_TASK = "CONTENT_FROM_TASK"
    """
    Content derived from task
    """
    INFERENCE = "INFERENCE"
    """
    General inference relationship
    """
    TRANSFORMATION = "TRANSFORMATION"
    """
    Transformation relationship
    """


class IngestionStatus(str, Enum):
    """
    Status values for ingestion processes
    """
    STARTED = "STARTED"
    """
    Ingestion has started
    """
    IN_PROGRESS = "IN_PROGRESS"
    """
    Ingestion is in progress
    """
    COMPLETED = "COMPLETED"
    """
    Ingestion completed successfully
    """
    FAILED = "FAILED"
    """
    Ingestion failed
    """
    PARTIAL = "PARTIAL"
    """
    Ingestion partially completed
    """


class ContentType(str, Enum):
    """
    Types of generated content
    """
    ARTICLE = "ARTICLE"
    """
    Article or blog post
    """
    DOCUMENTATION = "DOCUMENTATION"
    """
    Technical documentation
    """
    REPORT = "REPORT"
    """
    Report or analysis
    """
    SUMMARY = "SUMMARY"
    """
    Summary or abstract
    """
    PRESENTATION = "PRESENTATION"
    """
    Presentation or slides
    """
    CODE = "CODE"
    """
    Code or script
    """
    OTHER = "OTHER"
    """
    Other content type
    """



class ProvenanceFields(ConfiguredBaseModel):
    """
    Provenance mixin for nodes
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/core/provenance',
         'mixin': True})

    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class EdgeProvenanceFields(ConfiguredBaseModel):
    """
    Provenance mixin for edges
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/core/provenance',
         'mixin': True})

    rel_id: Optional[str] = Field(default=None, description="""Stable relationship id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'rel_id',
         'domain_of': ['EdgeProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    derived: Optional[bool] = Field(default=None, description="""Whether derived vs directly extracted""", json_schema_extra = { "linkml_meta": {'alias': 'derived', 'domain_of': ['EdgeProvenanceFields']} })
    derivation_rule: Optional[str] = Field(default=None, description="""Rule or method used for derivation""", json_schema_extra = { "linkml_meta": {'alias': 'derivation_rule', 'domain_of': ['EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class Conversation(ProvenanceFields):
    """
    Source document or communication ingested via Graphiti into Neo4j
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'fabio:Expression',
         'from_schema': 'https://example.org/schemas/conversation-task-inference',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'content': {'name': 'content', 'required': True},
                        'conversation_id': {'identifier': True,
                                            'name': 'conversation_id',
                                            'required': True},
                        'timestamp': {'name': 'timestamp', 'required': True}}})

    conversation_id: str = Field(default=..., description="""Unique identifier for the conversation""", json_schema_extra = { "linkml_meta": {'alias': 'conversation_id', 'domain_of': ['Conversation']} })
    content: str = Field(default=..., description="""The actual content/text of the conversation""", json_schema_extra = { "linkml_meta": {'alias': 'content', 'domain_of': ['Conversation']} })
    timestamp: datetime  = Field(default=..., description="""When the conversation occurred""", json_schema_extra = { "linkml_meta": {'alias': 'timestamp', 'domain_of': ['Conversation', 'IngestionProcess']} })
    source: Optional[str] = Field(default=None, description="""Origin system or platform of the conversation""", json_schema_extra = { "linkml_meta": {'alias': 'source', 'domain_of': ['Conversation']} })
    participants: Optional[list[str]] = Field(default=None, description="""List of participants in the conversation""", json_schema_extra = { "linkml_meta": {'alias': 'participants', 'domain_of': ['Conversation']} })
    conversation_type: Optional[ConversationType] = Field(default=None, description="""Type or category of conversation""", json_schema_extra = { "linkml_meta": {'alias': 'conversation_type', 'domain_of': ['Conversation']} })
    metadata: Optional[str] = Field(default=None, description="""Additional metadata about the conversation""", json_schema_extra = { "linkml_meta": {'alias': 'metadata', 'domain_of': ['Conversation']} })
    derived_tasks: Optional[list[str]] = Field(default=None, description="""Tasks derived from this conversation""", json_schema_extra = { "linkml_meta": {'alias': 'derived_tasks',
         'domain_of': ['Conversation'],
         'inverse': 'derived_from_conversation'} })
    ingested_by: Optional[str] = Field(default=None, description="""Ingestion process that created this conversation""", json_schema_extra = { "linkml_meta": {'alias': 'ingested_by',
         'domain_of': ['Conversation'],
         'inverse': 'generates_conversations'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class Task(ProvenanceFields):
    """
    Actionable work item inferred from conversation content
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://example.org/schemas/conversation-task-inference',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'description': {'name': 'description', 'required': True},
                        'status': {'name': 'status', 'required': True},
                        'task_id': {'identifier': True,
                                    'name': 'task_id',
                                    'required': True},
                        'task_type': {'name': 'task_type', 'required': True}}})

    task_id: str = Field(default=..., description="""Unique identifier for the task""", json_schema_extra = { "linkml_meta": {'alias': 'task_id', 'domain_of': ['Task']} })
    description: str = Field(default=..., description="""Detailed description of the task""", json_schema_extra = { "linkml_meta": {'alias': 'description', 'domain_of': ['Task']} })
    status: TaskStatus = Field(default=..., description="""Current status of the task""", json_schema_extra = { "linkml_meta": {'alias': 'status', 'domain_of': ['Task']} })
    priority: Optional[PriorityLevel] = Field(default=None, description="""Priority level of the task""", json_schema_extra = { "linkml_meta": {'alias': 'priority', 'domain_of': ['Task']} })
    task_type: str = Field(default=..., description="""Type or category of task""", json_schema_extra = { "linkml_meta": {'alias': 'task_type', 'domain_of': ['Task']} })
    created_at: Optional[datetime ] = Field(default=None, description="""When the task was created""", json_schema_extra = { "linkml_meta": {'alias': 'created_at', 'domain_of': ['Task', 'GeneratedContent']} })
    updated_at: Optional[datetime ] = Field(default=None, description="""When the task was last updated""", json_schema_extra = { "linkml_meta": {'alias': 'updated_at', 'domain_of': ['Task']} })
    due_date: Optional[datetime ] = Field(default=None, description="""Deadline for task completion""", json_schema_extra = { "linkml_meta": {'alias': 'due_date', 'domain_of': ['Task']} })
    assignee: Optional[str] = Field(default=None, description="""Person or system assigned to the task""", json_schema_extra = { "linkml_meta": {'alias': 'assignee', 'domain_of': ['Task']} })
    derived_from_conversation: Optional[str] = Field(default=None, description="""Conversation from which this task was derived""", json_schema_extra = { "linkml_meta": {'alias': 'derived_from_conversation',
         'domain_of': ['Task'],
         'inverse': 'derived_tasks'} })
    executes_content_creation: Optional[str] = Field(default=None, description="""Content creation activity that executes this task""", json_schema_extra = { "linkml_meta": {'alias': 'executes_content_creation',
         'domain_of': ['Task'],
         'inverse': 'executes_task'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class ContentCreationActivity(ProvenanceFields):
    """
    Creative process for producing content based on inferred tasks
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/conversation-task-inference',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'activity_id': {'identifier': True,
                                        'name': 'activity_id',
                                        'required': True},
                        'started_at': {'name': 'started_at', 'required': True}}})

    activity_id: str = Field(default=..., description="""Unique identifier for the content creation activity""", json_schema_extra = { "linkml_meta": {'alias': 'activity_id', 'domain_of': ['ContentCreationActivity']} })
    started_at: datetime  = Field(default=..., description="""When the activity started""", json_schema_extra = { "linkml_meta": {'alias': 'started_at', 'domain_of': ['ContentCreationActivity']} })
    ended_at: Optional[datetime ] = Field(default=None, description="""When the activity ended""", json_schema_extra = { "linkml_meta": {'alias': 'ended_at', 'domain_of': ['ContentCreationActivity']} })
    activity_status: Optional[ActivityStatus] = Field(default=None, description="""Current status of the activity""", json_schema_extra = { "linkml_meta": {'alias': 'activity_status', 'domain_of': ['ContentCreationActivity']} })
    creator: Optional[str] = Field(default=None, description="""Person or system performing the activity""", json_schema_extra = { "linkml_meta": {'alias': 'creator', 'domain_of': ['ContentCreationActivity']} })
    tools_used: Optional[list[str]] = Field(default=None, description="""Tools or software used in the activity""", json_schema_extra = { "linkml_meta": {'alias': 'tools_used', 'domain_of': ['ContentCreationActivity']} })
    parameters: Optional[str] = Field(default=None, description="""Configuration parameters for the activity""", json_schema_extra = { "linkml_meta": {'alias': 'parameters', 'domain_of': ['ContentCreationActivity']} })
    executes_task: Optional[str] = Field(default=None, description="""Task being executed by this activity""", json_schema_extra = { "linkml_meta": {'alias': 'executes_task',
         'domain_of': ['ContentCreationActivity'],
         'inverse': 'executes_content_creation'} })
    generates_content: Optional[list[str]] = Field(default=None, description="""Content generated by this activity""", json_schema_extra = { "linkml_meta": {'alias': 'generates_content',
         'domain_of': ['ContentCreationActivity'],
         'inverse': 'generated_by_activity'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class DerivationInferenceRelationship(ProvenanceFields):
    """
    Provenance relationship tracking how tasks and content are derived through inference
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Derivation',
         'from_schema': 'https://example.org/schemas/conversation-task-inference',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'derivation_id': {'identifier': True,
                                          'name': 'derivation_id',
                                          'required': True},
                        'inference_method': {'name': 'inference_method',
                                             'required': True},
                        'inference_timestamp': {'name': 'inference_timestamp',
                                                'required': True}}})

    derivation_id: str = Field(default=..., description="""Unique identifier for the derivation relationship""", json_schema_extra = { "linkml_meta": {'alias': 'derivation_id', 'domain_of': ['DerivationInferenceRelationship']} })
    inference_method: str = Field(default=..., description="""Method or algorithm used for inference""", json_schema_extra = { "linkml_meta": {'alias': 'inference_method', 'domain_of': ['DerivationInferenceRelationship']} })
    inference_timestamp: datetime  = Field(default=..., description="""When the inference was performed""", json_schema_extra = { "linkml_meta": {'alias': 'inference_timestamp',
         'domain_of': ['DerivationInferenceRelationship']} })
    confidence_score: Optional[float] = Field(default=None, description="""Confidence level of the inference (0.0 to 1.0)""", ge=0.0, le=1.0, json_schema_extra = { "linkml_meta": {'alias': 'confidence_score', 'domain_of': ['DerivationInferenceRelationship']} })
    inference_parameters: Optional[str] = Field(default=None, description="""Parameters used in the inference process""", json_schema_extra = { "linkml_meta": {'alias': 'inference_parameters',
         'domain_of': ['DerivationInferenceRelationship']} })
    inference_model: Optional[str] = Field(default=None, description="""Model or system that performed the inference""", json_schema_extra = { "linkml_meta": {'alias': 'inference_model', 'domain_of': ['DerivationInferenceRelationship']} })
    source_entity: Optional[str] = Field(default=None, description="""The entity from which something was derived""", json_schema_extra = { "linkml_meta": {'alias': 'source_entity', 'domain_of': ['DerivationInferenceRelationship']} })
    derived_entity: Optional[str] = Field(default=None, description="""The entity that was derived""", json_schema_extra = { "linkml_meta": {'alias': 'derived_entity', 'domain_of': ['DerivationInferenceRelationship']} })
    relationship_type: Optional[DerivationType] = Field(default=None, description="""Type of derivation relationship""", json_schema_extra = { "linkml_meta": {'alias': 'relationship_type', 'domain_of': ['DerivationInferenceRelationship']} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class IngestionProcess(ProvenanceFields):
    """
    Graphiti data import activity that brings conversations into Neo4j
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Activity',
         'from_schema': 'https://example.org/schemas/conversation-task-inference',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'graphiti_version': {'name': 'graphiti_version',
                                             'required': True},
                        'ingestion_id': {'identifier': True,
                                         'name': 'ingestion_id',
                                         'required': True},
                        'timestamp': {'name': 'timestamp', 'required': True}}})

    ingestion_id: str = Field(default=..., description="""Unique identifier for the ingestion process""", json_schema_extra = { "linkml_meta": {'alias': 'ingestion_id', 'domain_of': ['IngestionProcess']} })
    timestamp: datetime  = Field(default=..., description="""When the conversation occurred""", json_schema_extra = { "linkml_meta": {'alias': 'timestamp', 'domain_of': ['Conversation', 'IngestionProcess']} })
    graphiti_version: str = Field(default=..., description="""Version of Graphiti used for ingestion""", json_schema_extra = { "linkml_meta": {'alias': 'graphiti_version', 'domain_of': ['IngestionProcess']} })
    ingestion_status: Optional[IngestionStatus] = Field(default=None, description="""Status of the ingestion process""", json_schema_extra = { "linkml_meta": {'alias': 'ingestion_status', 'domain_of': ['IngestionProcess']} })
    source_system: Optional[str] = Field(default=None, description="""System from which data was ingested""", json_schema_extra = { "linkml_meta": {'alias': 'source_system', 'domain_of': ['IngestionProcess']} })
    batch_id: Optional[str] = Field(default=None, description="""Batch identifier for grouped ingestions""", json_schema_extra = { "linkml_meta": {'alias': 'batch_id', 'domain_of': ['IngestionProcess']} })
    records_processed: Optional[int] = Field(default=None, description="""Number of records successfully processed""", json_schema_extra = { "linkml_meta": {'alias': 'records_processed', 'domain_of': ['IngestionProcess']} })
    records_failed: Optional[int] = Field(default=None, description="""Number of records that failed processing""", json_schema_extra = { "linkml_meta": {'alias': 'records_failed', 'domain_of': ['IngestionProcess']} })
    configuration: Optional[str] = Field(default=None, description="""Configuration settings for the ingestion""", json_schema_extra = { "linkml_meta": {'alias': 'configuration', 'domain_of': ['IngestionProcess']} })
    generates_conversations: Optional[list[str]] = Field(default=None, description="""Conversations generated by this ingestion process""", json_schema_extra = { "linkml_meta": {'alias': 'generates_conversations',
         'domain_of': ['IngestionProcess'],
         'inverse': 'ingested_by'} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


class GeneratedContent(ProvenanceFields):
    """
    Output artifact produced from content creation activities
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'prov:Entity',
         'from_schema': 'https://example.org/schemas/conversation-task-inference',
         'mixins': ['ProvenanceFields'],
         'slot_usage': {'content_body': {'name': 'content_body', 'required': True},
                        'content_id': {'identifier': True,
                                       'name': 'content_id',
                                       'required': True},
                        'content_type': {'name': 'content_type', 'required': True}}})

    content_id: str = Field(default=..., description="""Unique identifier for the generated content""", json_schema_extra = { "linkml_meta": {'alias': 'content_id', 'domain_of': ['GeneratedContent']} })
    content_type: ContentType = Field(default=..., description="""Type or category of generated content""", json_schema_extra = { "linkml_meta": {'alias': 'content_type', 'domain_of': ['GeneratedContent']} })
    content_body: str = Field(default=..., description="""The actual generated content""", json_schema_extra = { "linkml_meta": {'alias': 'content_body', 'domain_of': ['GeneratedContent']} })
    format: Optional[str] = Field(default=None, description="""Format of the content (e.g., markdown, html, text)""", json_schema_extra = { "linkml_meta": {'alias': 'format', 'domain_of': ['GeneratedContent']} })
    title: Optional[str] = Field(default=None, description="""Title of the generated content""", json_schema_extra = { "linkml_meta": {'alias': 'title', 'domain_of': ['GeneratedContent']} })
    created_at: Optional[datetime ] = Field(default=None, description="""When the task was created""", json_schema_extra = { "linkml_meta": {'alias': 'created_at', 'domain_of': ['Task', 'GeneratedContent']} })
    file_path: Optional[str] = Field(default=None, description="""Path to the content file if stored externally""", json_schema_extra = { "linkml_meta": {'alias': 'file_path', 'domain_of': ['GeneratedContent']} })
    file_size: Optional[int] = Field(default=None, description="""Size of the content file in bytes""", json_schema_extra = { "linkml_meta": {'alias': 'file_size', 'domain_of': ['GeneratedContent']} })
    checksum: Optional[str] = Field(default=None, description="""Checksum for content integrity verification""", json_schema_extra = { "linkml_meta": {'alias': 'checksum', 'domain_of': ['GeneratedContent']} })
    generated_by_activity: Optional[str] = Field(default=None, description="""Activity that generated this content""", json_schema_extra = { "linkml_meta": {'alias': 'generated_by_activity',
         'domain_of': ['GeneratedContent'],
         'inverse': 'generates_content'} })
    derived_from_task: Optional[str] = Field(default=None, description="""Task from which this content was derived""", json_schema_extra = { "linkml_meta": {'alias': 'derived_from_task', 'domain_of': ['GeneratedContent']} })
    node_id: Optional[str] = Field(default=None, description="""Stable citation id (deterministic)""", json_schema_extra = { "linkml_meta": {'alias': 'node_id',
         'domain_of': ['ProvenanceFields'],
         'slot_uri': 'prov:identifier'} })
    prov_system: Optional[str] = Field(default=None, description="""Primary source system (e.g., slack, gdrive, aaoifi_db)""", json_schema_extra = { "linkml_meta": {'alias': 'prov_system',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields'],
         'slot_uri': 'prov:wasAttributedTo'} })
    prov_channel_ids: Optional[list[str]] = Field(default=None, description="""Slack channel IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_channel_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_thread_tss: Optional[list[str]] = Field(default=None, description="""Slack thread timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_thread_tss',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_tss: Optional[list[str]] = Field(default=None, description="""Slack message timestamps""", json_schema_extra = { "linkml_meta": {'alias': 'prov_tss', 'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_permalinks: Optional[list[str]] = Field(default=None, description="""Slack permalinks""", json_schema_extra = { "linkml_meta": {'alias': 'prov_permalinks',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_file_ids: Optional[list[str]] = Field(default=None, description="""Document/file identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'prov_file_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_rev_ids: Optional[list[str]] = Field(default=None, description="""Document revision IDs""", json_schema_extra = { "linkml_meta": {'alias': 'prov_rev_ids',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    prov_text_sha1s: Optional[list[str]] = Field(default=None, description="""SHA1 hashes of source text""", json_schema_extra = { "linkml_meta": {'alias': 'prov_text_sha1s',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_types: Optional[list[str]] = Field(default=None, description="""Document component types (section, paragraph, etc.)""", json_schema_extra = { "linkml_meta": {'alias': 'doco_types',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    doco_paths: Optional[list[str]] = Field(default=None, description="""Document structural paths""", json_schema_extra = { "linkml_meta": {'alias': 'doco_paths',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    page_nums: Optional[list[int]] = Field(default=None, description="""Page numbers""", json_schema_extra = { "linkml_meta": {'alias': 'page_nums',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })
    support_count: Optional[int] = Field(default=None, description="""Number of supporting evidences""", ge=0, json_schema_extra = { "linkml_meta": {'alias': 'support_count',
         'domain_of': ['ProvenanceFields', 'EdgeProvenanceFields']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ProvenanceFields.model_rebuild()
EdgeProvenanceFields.model_rebuild()
Conversation.model_rebuild()
Task.model_rebuild()
ContentCreationActivity.model_rebuild()
DerivationInferenceRelationship.model_rebuild()
IngestionProcess.model_rebuild()
GeneratedContent.model_rebuild()

