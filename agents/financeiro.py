"""
AGENTE 5 — FINANCEIRO
Controlador financeiro e tesouraria contábil.
Diferencia estritamente Receita Realizada (compensada), Vendas Pendentes e Projeções.
Monitora a sustentabilidade do negócio e bloqueia qualquer despesa sem autorização humana.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any
import uuid

class AgenteFinanceiro(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_5_financeiro",
            name="Agente Financeiro",
            role="Gestão contábil, livro-caixa, metas financeiras e segregação de receitas reais vs projeções",
            db_manager=db_manager,
            event_bus=event_bus
        )
        self._ensure_baseline_budget()

    def _ensure_baseline_budget(self):
        """Garante que a despesa operacional planejada de R$ 200/mês conste como Projeção no banco."""
        summary = self.db.get_financial_summary()
        if summary["projected_expenses"] == 0:
            self.db.add_transaction(
                trans_id=f"tx_budget_base",
                trans_type="EXPENSE",
                category="CUSTO_OPERACIONAL_PLANEJADO",
                amount=200.00,
                description="Orçamento operacional mensal base planejado (meta de sustentabilidade)",
                status="PROJECTION"
            )

    def register_real_sale(self, amount: float, description: str, category: str = "VENDAS_DIGITAIS") -> str:
        """Registra uma venda real e efetivamente compensada em conta bancária."""
        tx_id = f"tx_rev_{uuid.uuid4().hex[:8]}"
        self.db.add_transaction(
            trans_id=tx_id,
            trans_type="REVENUE",
            category=category,
            amount=amount,
            description=description,
            status="REALIZED"
        )
        self.log_audit("FINANCIAL", tx_id, "SUCCESS", f"Receita real confirmada: R$ {amount:.2f} ({description})")
        self.emit_event("REVENUE_REGISTERED", {
            "target_type": "FINANCIAL",
            "target_id": tx_id,
            "summary": f"Venda realizada: R$ {amount:.2f} - {description}",
            "amount": amount
        })
        return tx_id

    def register_real_expense(self, amount: float, description: str, category: str = "OPERACIONAL") -> str:
        """Registra uma despesa real aprovada e paga pelo usuário."""
        tx_id = f"tx_exp_{uuid.uuid4().hex[:8]}"
        self.db.add_transaction(
            trans_id=tx_id,
            trans_type="EXPENSE",
            category=category,
            amount=amount,
            description=description,
            status="REALIZED"
        )
        self.log_audit("FINANCIAL", tx_id, "WARNING", f"Despesa real registrada: R$ {amount:.2f} ({description})")
        self.emit_event("EXPENSE_REGISTERED", {
            "target_type": "FINANCIAL",
            "target_id": tx_id,
            "summary": f"Despesa paga: R$ {amount:.2f} - {description}",
            "amount": amount
        })
        return tx_id

    def record_pending_sale(self, amount: float, description: str) -> str:
        """Registra uma venda pendente de compensação na plataforma."""
        tx_id = f"tx_pend_{uuid.uuid4().hex[:8]}"
        self.db.add_transaction(
            trans_id=tx_id,
            trans_type="REVENUE",
            category="VENDAS_DIGITAIS",
            amount=amount,
            description=description,
            status="PENDING"
        )
        self.log_audit("FINANCIAL", tx_id, "INFO", f"Venda pendente de liquidação: R$ {amount:.2f} ({description})")
        return tx_id

    def generate_financial_report(self) -> Dict[str, Any]:
        summary = self.db.get_financial_summary()
        
        # Diferenciação clara exigida no projeto:
        # 1. Dinheiro recebido
        # 2. Vendas pendentes
        # 3. Projeções
        report = {
            "dinheiro_recebido_efetivo": summary["realized_revenue"],
            "vendas_pendentes_liquidacao": summary["pending_revenue"],
            "projecao_receita_total": summary["projected_revenue"],
            "despesas_efetivas_pagas": summary["realized_expenses"],
            "despesas_planejadas_orcamento": summary["projected_expenses"],
            "saldo_liquido_em_caixa": summary["net_result"],
            "meta_mensal_desejada": summary["monthly_target"],
            "meta_minima_breakeven": summary["min_target"],
            "progresso_meta_percent": summary["target_progress_percent"],
            "status_sustentabilidade": summary["survival_status"],
            "alerta": "Nenhum gasto ou movimentação financeira pode ser efetuado sem autorização humana expressa."
        }
        return report

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("WORKING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Atualizando consolidação financeira: {task_title}")

        report = self.generate_financial_report()
        self.db.update_task_status(task_id, "COMPLETED", report)

        self.emit_event("FINANCIAL_STATUS_UPDATED", {
            "target_type": "FINANCIAL",
            "target_id": task_id,
            "summary": f"Relatório financeiro gerado: Saldo Líquido R$ {report['saldo_liquido_em_caixa']:.2f} | Status: {report['status_sustentabilidade']}",
            "report": report
        })

        self.set_status("IDLE")
        return report
