"""
Motor de Sobrevivência Financeira do Negócio Digital.
Analisa a sustentabilidade com base no custo operacional planejado (R$ 200,00)
e nas receitas reais realizadas. Se houver déficit, gera diagnósticos e planos de recuperação.
"""
from typing import Dict, Any
import uuid

class SurvivalEngine:
    def __init__(self, db_manager, event_bus):
        self.db = db_manager
        self.bus = event_bus

    def evaluate_sustainability(self) -> Dict[str, Any]:
        summary = self.db.get_financial_summary()
        realized_revenue = summary["realized_revenue"]
        realized_expenses = summary["realized_expenses"]
        net_result = summary["net_result"]
        min_target = summary["min_target"]  # R$ 200,00

        diag_id = f"diag_{uuid.uuid4().hex[:8]}"

        if realized_revenue >= min_target and net_result >= 100.0:
            status = "HEALTHY"
            plan = (
                "SITUAÇÃO FINANCEIRA SAUDÁVEL:\n"
                f"- A receita realizada (R$ {realized_revenue:.2f}) superou a meta mínima (R$ {min_target:.2f}).\n"
                f"- O lucro líquido atingiu R$ {net_result:.2f}, superando a meta de R$ 100,00 positivos.\n"
                "Ações recomendadas:\n"
                "1. Manter rigor no controle de despesas operacionais (não aumentar custos fixos).\n"
                "2. Reinvestir tempo na otimização de produtos que já demonstraram tração.\n"
                "3. Continuar utilizando canais de divulgação orgânicos e sem custo fixo."
            )
        elif realized_revenue >= min_target and net_result >= 0.0:
            status = "EQUILIBRIUM"
            plan = (
                "SITUAÇÃO DE EQUILÍBRIO OPERACIONAL (BREAKEVEN):\n"
                f"- A receita realizada (R$ {realized_revenue:.2f}) cobriu os custos, mas o lucro líquido é de R$ {net_result:.2f} (meta: R$ 100,00).\n"
                "Ações recomendadas:\n"
                "1. Oferecer ofertas complementares (order bump / produtos de R$ 19 a R$ 29).\n"
                "2. Otimizar as headlines e copies comerciais para elevar a taxa de conversão.\n"
                "3. Preservar o caixa sem contratação de novas ferramentas ou gastos discricionários."
            )
        else:
            status = "DEFICIT"
            deficit_amount = abs(min_target - realized_revenue) if realized_revenue < min_target else abs(net_result)
            plan = (
                f"🚨 PROTOCOLO DE SOBREVIVÊNCIA FINANCEIRA ATIVADO (DÉFICIT: R$ {deficit_amount:.2f}):\n"
                "O negócio ainda não atingiu a receita mínima de R$ 200,00/mês para cobrir o custo operacional planejado.\n\n"
                "DIAGNÓSTICO E PLANO DE RECUPERAÇÃO EM 5 ETAPAS:\n"
                "1. [DIAGNÓSTICO DO PROBLEMA]: Falta de tração inicial em canais orgânicos ou catálogo incipiente.\n"
                "2. [CONTENÇÃO IMEDIATA]: Manter custo fixo em R$ 0,00. Nenhuma ferramenta paga pode ser contratada.\n"
                "3. [PIVOT DE PRODUTO]: O Agente 2 (Pesquisador) deve mapear micro-produtos de impulso (R$ 15,00 a R$ 27,00) de alta necessidade imediata (ex: planilhas práticas e modelos de documentos).\n"
                "4. [DISPARO COMERCIAL]: O Agente 4 (Comercial) deve revisar as páginas e focar 100% em comunidades orgânicas e fóruns sem custo de anúncio.\n"
                "5. [SUPERVISÃO HUMANA]: Apresentar opções ao usuário para validação manual dos novos nichos antes de qualquer lançamento."
            )

        # Salvar diagnóstico no banco
        self.db.record_survival_diagnostic(
            diag_id=diag_id,
            net_result=net_result,
            realized_revenue=realized_revenue,
            realized_expenses=realized_expenses,
            status=status,
            recovery_plan=plan
        )

        severity = "SUCCESS" if status == "HEALTHY" else ("WARNING" if status == "EQUILIBRIUM" else "ERROR")
        self.db.log_audit(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            agent_name="SurvivalEngine",
            target_type="FINANCIAL_SURVIVAL",
            target_id=diag_id,
            severity=severity,
            message=f"Diagnóstico de Sobrevivência: Status {status} | Receita R$ {realized_revenue:.2f} / Meta R$ {min_target:.2f}"
        )

        return {
            "diagnostic_id": diag_id,
            "status": status,
            "net_result": net_result,
            "realized_revenue": realized_revenue,
            "min_target": min_target,
            "recovery_plan": plan
        }
