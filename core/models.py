"""
Modelos de dados tipados para o ecossistema de agentes digitais autossustentáveis.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

@dataclass
class AgentState:
    id: str
    name: str
    role: str
    status: str  # IDLE, WORKING, AUDITING, BLOCKED, COMPLETED
    current_task: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Task:
    id: str
    title: str
    description: str
    assigned_to: str
    status: str  # PENDING, IN_PROGRESS, COMPLETED, FAILED, AUDITED
    priority: int  # 1 (Alta) a 5 (Baixa)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    finished_at: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None

@dataclass
class Opportunity:
    id: str
    title: str
    niche: str
    target_audience: str
    problem_to_solve: str
    estimated_demand: str  # ALTA, MEDIA, BAIXA
    suggested_price: float
    competition_level: str  # BAIXA, MEDIA, ALTA
    status: str  # IDENTIFIED, SELECTED, ARCHIVED
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Product:
    id: str
    opportunity_id: str
    title: str
    product_type: str  # EBOOK, SPREADSHEET, TEMPLATE, GUIDE, TOOL
    file_path: str
    price: float
    content_summary: str
    status: str  # DRAFT, AUDITED, WAITING_HUMAN_APPROVAL, APPROVED, REJECTED, PUBLISHED
    quality_score: int  # 0 a 100
    audit_notes: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    approved_at: Optional[str] = None

@dataclass
class Campaign:
    id: str
    product_id: str
    title: str
    headline: str
    ad_copy: str
    landing_page_text: str
    suggested_channels: List[str]
    status: str  # CREATED, WAITING_APPROVAL, APPROVED, ARCHIVED
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Transaction:
    id: str
    type: str  # REVENUE, EXPENSE
    category: str
    amount: float
    description: str
    status: str  # REALIZED (Efetivo), PENDING (Pendente), PROJECTION (Projeção)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class AuditLog:
    id: str
    agent_name: str
    target_type: str
    target_id: str
    severity: str  # INFO, WARNING, ERROR, SUCCESS
    message: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class SurvivalDiagnostic:
    id: str
    net_result: float
    realized_revenue: float
    realized_expenses: float
    status: str  # HEALTHY, EQUILIBRIUM, DEFICIT
    recovery_plan: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
