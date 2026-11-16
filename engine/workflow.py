"""
Orquestrador central do sistema de negócio digital.
Instancia o banco, barramento, agentes e expõe métodos unificados para CLI e Servidor Web.
"""
from pathlib import Path
from core.db import DatabaseManager
from core.event_bus import EventBus
from engine.survival import SurvivalEngine

from agents.pesquisador import PesquisadorMercado
from agents.produtor import ProdutorDigital
from agents.auditor import AuditorQualidade
from agents.comercial import AgenteComercial
from agents.financeiro import AgenteFinanceiro
from agents.gerente import GerentePrincipal
from agents.estrategista import EstrategistaInovacao
from agents.social_media import GestorFacebook

from typing import Dict, Any, Optional

class BusinessWorkflow:
    def __init__(self, db_path: Optional[Path] = None):
        self.db = DatabaseManager(db_path=db_path) if db_path else DatabaseManager()
        self.bus = EventBus(self.db)
        self.survival = SurvivalEngine(self.db, self.bus)

        # Inicializa a equipe de agentes especializados
        self.pesquisador = PesquisadorMercado(self.db, self.bus)
        self.produtor = ProdutorDigital(self.db, self.bus)
        self.auditor = AuditorQualidade(self.db, self.bus)
        self.comercial = AgenteComercial(self.db, self.bus)
        self.financeiro = AgenteFinanceiro(self.db, self.bus)
        self.estrategista = EstrategistaInovacao(self.db, self.bus)
        self.social_media = GestorFacebook(self.db, self.bus)
        
        self.gerente = GerentePrincipal(
            db_manager=self.db,
            event_bus=self.bus,
            pesquisador=self.pesquisador,
            produtor=self.produtor,
            comercial=self.comercial,
            financeiro=self.financeiro,
            auditor=self.auditor,
            survival_engine=self.survival
        )

    def run_strategy_ideas(self) -> Dict[str, Any]:
        """Agente 7: Gera ideias estratégicas para alavancar faturamento e expansão."""
        import uuid
        t_id = f"task_{uuid.uuid4().hex[:6]}"
        self.db.create_task(t_id, "Gerar Ideias de Melhoria e Crescimento", "Mapear order bumps, combos e táticas de tráfego", "Estrategista de Inovação", priority=2)
        return self.estrategista.execute_task(t_id, "Ideação Estratégica do Negócio", {})

    def run_facebook_calendar(self, checkout_url: str = "https://pay.kiwify.com.br/mriY17r") -> Dict[str, Any]:
        """Agente 8: Gera calendário editorial com copies prontas para a página do Facebook."""
        import uuid
        t_id = f"task_{uuid.uuid4().hex[:6]}"
        self.db.create_task(t_id, "Planejar Conteúdo para Facebook", f"Criar cronograma de posts com link {checkout_url}", "Gestor de Comunidade & Facebook", priority=2)
        return self.social_media.execute_task(t_id, "Cronograma Semanal do Facebook", {"checkout_url": checkout_url})

    def run_cycle(self) -> Dict[str, Any]:
        """Executa um ciclo autônomo completo de pesquisa, criação, auditoria e finanças."""
        return self.gerente.run_autonomous_cycle()

    def start_autonomous_loop(self, interval_seconds: int = 300) -> Dict[str, Any]:
        """Inicia o loop 100% autônomo em segundo plano."""
        import threading, time
        if getattr(self, "_loop_running", False):
            return {"status": "ALREADY_RUNNING", "interval_seconds": getattr(self, "_loop_interval", 300)}
        
        self._loop_running = True
        self._loop_interval = interval_seconds

        def _loop():
            while getattr(self, "_loop_running", False):
                try:
                    self.run_cycle()
                except Exception as e:
                    print(f"[ERRO NO LOOP AUTÔNOMO]: {e}")
                time.sleep(self._loop_interval)

        thread = threading.Thread(target=_loop, daemon=True)
        thread.start()
        return {"status": "LOOP_STARTED", "interval_seconds": interval_seconds}

    def stop_autonomous_loop(self) -> Dict[str, Any]:
        self._loop_running = False
        return {"status": "LOOP_STOPPED"}

    def is_autonomous_loop_running(self) -> bool:
        return getattr(self, "_loop_running", False)

    def approve_product(self, product_id: str, reason: str = "Aprovado pelo administrador humano") -> bool:
        """Ação humana: aprova um produto para comercialização."""
        product = self.db.get_product(product_id)
        if not product:
            return False
        self.db.set_product_approval(product_id, approved=True, reason=reason)
        self.db.log_audit(
            log_id=f"audit_{product_id[:8]}",
            agent_name="SupervisaoHumana",
            target_type="PRODUCT",
            target_id=product_id,
            severity="SUCCESS",
            message=f"Produto '{product['title']}' formalmente APROVADO para divulgação."
        )
        return True

    def reject_product(self, product_id: str, reason: str = "Rejeitado pelo administrador humano") -> bool:
        """Ação humana: rejeita um produto."""
        product = self.db.get_product(product_id)
        if not product:
            return False
        self.db.set_product_approval(product_id, approved=False, reason=reason)
        self.db.log_audit(
            log_id=f"audit_{product_id[:8]}",
            agent_name="SupervisaoHumana",
            target_type="PRODUCT",
            target_id=product_id,
            severity="WARNING",
            message=f"Produto '{product['title']}' REJEITADO pelo administrador: {reason}"
        )
        return True

    def register_real_sale(self, amount: float, description: str) -> str:
        """Registra uma venda confirmada e compensada."""
        tx_id = self.financeiro.register_real_sale(amount, description)
        self.survival.evaluate_sustainability()
        return tx_id

    def register_real_expense(self, amount: float, description: str) -> str:
        """Registra um custo operacional real pago."""
        tx_id = self.financeiro.register_real_expense(amount, description)
        self.survival.evaluate_sustainability()
        return tx_id

    def trigger_survival_check(self) -> Dict[str, Any]:
        return self.survival.evaluate_sustainability()

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Retorna os dados consolidados para o Painel de Controle."""
        return {
            "agents": self.db.get_agents(),
            "finances": self.db.get_financial_summary(),
            "products": self.db.get_products(),
            "campaigns": self.db.get_campaigns(),
            "opportunities": self.db.get_opportunities(limit=10),
            "recent_tasks": self.db.get_recent_tasks(limit=12),
            "audit_logs": self.db.get_audit_logs(limit=20),
            "survival": self.db.get_latest_survival_diagnostic(),
            "facebook_calendar": self.social_media.generate_editorial_calendar(),
            "strategic_ideas": self.estrategista.generate_strategic_ideas(),
            "autonomous_loop_running": self.is_autonomous_loop_running()
        }
