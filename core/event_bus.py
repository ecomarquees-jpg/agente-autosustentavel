"""
Barramento local de eventos para comunicação desacoplada entre os agentes.
Registra eventos no log de auditoria para rastreabilidade 100% auditável.
"""
from typing import Callable, Dict, List, Any
import uuid
from datetime import datetime

class EventBus:
    def __init__(self, db_manager):
        self.db = db_manager
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, source_agent: str, payload: Dict[str, Any]):
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()
        
        event_data = {
            "id": event_id,
            "type": event_type,
            "source": source_agent,
            "payload": payload,
            "timestamp": timestamp
        }

        # Registrar automaticamente no log de auditoria
        severity = payload.get("severity", "INFO")
        summary_msg = f"[{event_type}] Disparado por {source_agent}: {payload.get('summary', str(payload)[:100])}"
        self.db.log_audit(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            agent_name=source_agent,
            target_type=payload.get("target_type", "SYSTEM"),
            target_id=payload.get("target_id", event_id),
            severity=severity,
            message=summary_msg
        )

        # Notificar inscritos
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    self.db.log_audit(
                        log_id=f"log_{uuid.uuid4().hex[:8]}",
                        agent_name="EventBus",
                        target_type="HANDLER_ERROR",
                        target_id=event_id,
                        severity="ERROR",
                        message=f"Erro ao processar evento {event_type}: {str(e)}"
                    )
