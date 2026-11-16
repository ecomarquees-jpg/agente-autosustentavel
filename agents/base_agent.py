"""
Classe base para todos os 6 agentes do sistema.
Garante padronização de estados, logs, transições e regras de segurança.
"""
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class BaseAgent:
    def __init__(self, agent_id: str, name: str, role: str, db_manager, event_bus):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.db = db_manager
        self.bus = event_bus
        self.status = "IDLE"
        self.current_task_id: Optional[str] = None
        
        # Registra o agente no banco de dados na inicialização
        self.db.register_or_update_agent(
            agent_id=self.agent_id,
            name=self.name,
            role=self.role,
            status=self.status,
            current_task_id=None
        )

    def set_status(self, status: str, current_task_id: Optional[str] = None):
        self.status = status
        self.current_task_id = current_task_id
        self.db.register_or_update_agent(
            agent_id=self.agent_id,
            name=self.name,
            role=self.role,
            status=self.status,
            current_task_id=current_task_id
        )

    def log_audit(self, target_type: str, target_id: str, severity: str, message: str):
        log_id = f"log_{uuid.uuid4().hex[:8]}"
        self.db.log_audit(
            log_id=log_id,
            agent_name=self.name,
            target_type=target_type,
            target_id=target_id,
            severity=severity,
            message=message
        )

    def emit_event(self, event_type: str, payload: Dict[str, Any]):
        self.bus.publish(event_type, self.name, payload)

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Método a ser implementado por cada agente especializado."""
        raise NotImplementedError("Cada agente especializado deve implementar seu próprio execute_task")
