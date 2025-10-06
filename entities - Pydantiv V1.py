"""
Business entity and edge models for Graphiti knowledge graph.

This module defines business-focused entity types and relationships following the
"Working Backwards from Outcomes" philosophy - entities designed to capture evidence
that enables specific business intelligence outcomes.

All fields are Optional as required by Graphiti's schema design.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List

# ============================================================================
# BUSINESS ENTITY TYPES
# ============================================================================

class BusinessOutcome(BaseModel):
    """A business deliverable or goal that needs to be achieved."""
    outcome_type: Optional[str] = Field(None, description="Type of outcome (deliverable, milestone, goal)")
    status: Optional[str] = Field(None, description="Current status (proposed, in_progress, completed, blocked)")
    priority: Optional[str] = Field(None, description="Priority level (low, medium, high, critical)")
    due_date: Optional[str] = Field(None, description="Deadline for completion (ISO format: YYYY-MM-DD or natural language)")
    for_customer: Optional[str] = Field(None, description="Customer or client name")
    in_project: Optional[str] = Field(None, description="Project identifier")
    owner: Optional[str] = Field(None, description="Person responsible")
    confidence_score: Optional[float] = Field(None, description="Confidence in achieving outcome (0-1)")

class BusinessDecision(BaseModel):
    """A crystallized choice or approval that affects business direction."""
    conclusion: Optional[str] = Field(None, description="What was decided")
    rationale: Optional[str] = Field(None, description="Why this decision was made")
    status: Optional[str] = Field(None, description="Status (proposed, approved, rejected, deferred)")
    owner: Optional[str] = Field(None, description="Decision maker")
    approved_by: Optional[str] = Field(None, description="Who approved the decision")
    approved_at: Optional[str] = Field(None, description="When it was approved (ISO format: YYYY-MM-DD or natural language)")
    impact_level: Optional[str] = Field(None, description="Impact level (low, medium, high)")
    reversible: Optional[bool] = Field(None, description="Can this decision be reversed")

class BusinessTask(BaseModel):
    """A unit of work that needs to be completed."""
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field(None, description="Status (todo, in_progress, completed, blocked)")
    priority: Optional[str] = Field(None, description="Priority (low, medium, high)")
    assigned_to: Optional[str] = Field(None, description="Person assigned")
    due_date: Optional[str] = Field(None, description="Task deadline (ISO format: YYYY-MM-DD or natural language)")
    estimated_effort: Optional[str] = Field(None, description="Estimated effort (hours/days)")
    blocking_reason: Optional[str] = Field(None, description="Why task is blocked")
    depends_on: Optional[str] = Field(None, description="Dependencies")

class BusinessHandoff(BaseModel):
    """A transition point where work/context moves between people or teams."""
    context: Optional[str] = Field(None, description="What is being handed off")
    state: Optional[str] = Field(None, description="Current state (pending, acknowledged, accepted, rejected)")
    from_actor: Optional[str] = Field(None, description="Who is handing off")
    to_actor: Optional[str] = Field(None, description="Who is receiving")
    issued_at: Optional[str] = Field(None, description="When handoff was initiated (ISO format: YYYY-MM-DD or natural language)")
    due_at: Optional[str] = Field(None, description="When response is needed (ISO format: YYYY-MM-DD or natural language)")
    acknowledged_at: Optional[str] = Field(None, description="When receiver acknowledged (ISO format: YYYY-MM-DD or natural language)")
    accepted_at: Optional[str] = Field(None, description="When receiver accepted (ISO format: YYYY-MM-DD or natural language)")
    risk_level: Optional[str] = Field(None, description="Risk of being dropped (low, medium, high)")

class BusinessClaim(BaseModel):
    """An assertion or statement made in conversations that may need verification."""
    claim_text: Optional[str] = Field(None, description="The claim being made")
    confidence: Optional[float] = Field(None, description="Confidence level (0-1)")
    source: Optional[str] = Field(None, description="Who made the claim")
    verification_status: Optional[str] = Field(None, description="Status (unverified, verified, refuted)")
    evidence: Optional[str] = Field(None, description="Supporting evidence")

class BusinessContradiction(BaseModel):
    """A conflict between claims or decisions that needs resolution."""
    description: Optional[str] = Field(None, description="What is contradictory")
    severity: Optional[str] = Field(None, description="Severity (low, medium, high)")
    detected_at: Optional[str] = Field(None, description="When contradiction was found (ISO format: YYYY-MM-DD or natural language)")
    resolved: Optional[bool] = Field(None, description="Whether resolved")
    resolution: Optional[str] = Field(None, description="How it was resolved")

class BusinessPrediction(BaseModel):
    """Forward-looking intelligence based on current data."""
    prediction_text: Optional[str] = Field(None, description="What is predicted")
    confidence: Optional[float] = Field(None, description="Confidence level (0-1)")
    timeframe: Optional[str] = Field(None, description="When this is expected")
    based_on: Optional[str] = Field(None, description="What data supports this prediction")
    risk_factors: Optional[str] = Field(None, description="Factors that could change outcome")

class Customer(BaseModel):
    """A business customer or client entity."""
    industry: Optional[str] = Field(None, description="Customer's industry")
    size: Optional[str] = Field(None, description="Company size (small, medium, enterprise)")
    tier: Optional[str] = Field(None, description="Customer tier (bronze, silver, gold)")
    contract_value: Optional[float] = Field(None, description="Annual contract value")
    start_date: Optional[str] = Field(None, description="When they became a customer (ISO format: YYYY-MM-DD or natural language)")
    account_manager: Optional[str] = Field(None, description="Assigned account manager")

class Project(BaseModel):
    """A business project entity."""
    status: Optional[str] = Field(None, description="Project status (planning, active, on_hold, completed)")
    start_date: Optional[str] = Field(None, description="Project start date (ISO format: YYYY-MM-DD or natural language)")
    end_date: Optional[str] = Field(None, description="Planned end date (ISO format: YYYY-MM-DD or natural language)")
    budget: Optional[float] = Field(None, description="Project budget")
    project_manager: Optional[str] = Field(None, description="Project manager name")
    team_size: Optional[int] = Field(None, description="Number of team members")

class Actor(BaseModel):
    """A team member or stakeholder."""
    role: Optional[str] = Field(None, description="Job role or title")
    team: Optional[str] = Field(None, description="Team name")
    department: Optional[str] = Field(None, description="Department")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    expertise: Optional[str] = Field(None, description="Areas of expertise")
    availability: Optional[str] = Field(None, description="Current availability")

# ============================================================================
# BUSINESS EDGE TYPES (RELATIONSHIPS)
# ============================================================================

class Requires(BaseModel):
    """An outcome requires a decision or resource."""
    criticality: Optional[str] = Field(None, description="How critical (low, medium, high)")
    deadline: Optional[str] = Field(None, description="When requirement must be met (ISO format: YYYY-MM-DD or natural language)")
    blocker: Optional[bool] = Field(None, description="Is this blocking progress")

class Fulfills(BaseModel):
    """A task fulfills an outcome."""
    completion_percentage: Optional[float] = Field(None, description="How much this fulfills outcome (0-1)")
    contribution_type: Optional[str] = Field(None, description="Type of contribution")

class BlockedBy(BaseModel):
    """A task is blocked by a claim or risk."""
    blocking_since: Optional[str] = Field(None, description="When blocking started (ISO format: YYYY-MM-DD or natural language)")
    severity: Optional[str] = Field(None, description="Severity (low, medium, high)")
    workaround_exists: Optional[bool] = Field(None, description="Is there a workaround")

class SupportedBy(BaseModel):
    """A decision is supported by claims/evidence."""
    weight: Optional[float] = Field(None, description="How much this supports (0-1)")
    evidence_type: Optional[str] = Field(None, description="Type of evidence")

class Transfers(BaseModel):
    """A handoff transfers a task."""
    transfer_date: Optional[str] = Field(None, description="When transfer occurred (ISO format: YYYY-MM-DD or natural language)")
    acceptance_required: Optional[bool] = Field(None, description="Does receiver need to accept")

class Threats(BaseModel):
    """A contradiction threatens an outcome."""
    threat_level: Optional[str] = Field(None, description="Threat level (low, medium, high)")
    impact_description: Optional[str] = Field(None, description="How it threatens outcome")

class DerivedFrom(BaseModel):
    """A prediction is derived from claims."""
    derivation_method: Optional[str] = Field(None, description="How prediction was derived")
    confidence_contribution: Optional[float] = Field(None, description="How much this contributes (0-1)")

# ============================================================================
# SCHEMA DEFINITIONS
# ============================================================================

# Business entity types dictionary
BUSINESS_ENTITY_TYPES: Dict[str, type[BaseModel]] = {
    "BusinessOutcome": BusinessOutcome,
    "BusinessDecision": BusinessDecision,
    "BusinessTask": BusinessTask,
    "BusinessHandoff": BusinessHandoff,
    "BusinessClaim": BusinessClaim,
    "BusinessContradiction": BusinessContradiction,
    "BusinessPrediction": BusinessPrediction,
    "Customer": Customer,
    "Project": Project,
    "Actor": Actor
}

# Business edge types dictionary
BUSINESS_EDGE_TYPES: Dict[str, type[BaseModel]] = {
    "Requires": Requires,
    "Fulfills": Fulfills,
    "BlockedBy": BlockedBy,
    "SupportedBy": SupportedBy,
    "Transfers": Transfers,
    "Threats": Threats,
    "DerivedFrom": DerivedFrom
}

# Edge type mapping: defines which entities can be connected by which edge types
# Following "Working Backwards from Outcomes" philosophy
BUSINESS_EDGE_TYPE_MAP: Dict[tuple[str, str], List[str]] = {
    # BusinessOutcome relationships
    ("BusinessOutcome", "BusinessDecision"): ["Requires"],
    ("BusinessDecision", "BusinessOutcome"): ["Requires"],

    # BusinessTask relationships
    ("BusinessTask", "BusinessOutcome"): ["Fulfills"],
    ("BusinessTask", "BusinessClaim"): ["BlockedBy"],
    ("BusinessTask", "BusinessContradiction"): ["BlockedBy"],

    # BusinessDecision relationships
    ("BusinessDecision", "BusinessClaim"): ["SupportedBy"],

    # BusinessHandoff relationships
    ("BusinessHandoff", "BusinessTask"): ["Transfers"],
    ("BusinessHandoff", "Actor"): ["Transfers"],

    # BusinessContradiction relationships
    ("BusinessContradiction", "BusinessOutcome"): ["Threats"],

    # BusinessPrediction relationships
    ("BusinessPrediction", "BusinessClaim"): ["DerivedFrom"],

    # Actor relationships (team collaboration)
    ("Actor", "BusinessTask"): ["Fulfills"],
    ("Actor", "BusinessOutcome"): ["Requires"],
    ("Actor", "Project"): ["Fulfills"],

    # Customer relationships
    ("Customer", "BusinessOutcome"): ["Requires"],
    ("Customer", "Project"): ["Requires"],

    # Project relationships
    ("Project", "BusinessOutcome"): ["Fulfills"],
    ("Project", "Actor"): ["Requires"],
}
