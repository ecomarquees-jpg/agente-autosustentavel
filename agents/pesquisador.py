"""
AGENTE 2 — PESQUISADOR DE MERCADO
Pesquisa produtos digitais com demanda real, problemas que as pessoas precisam resolver,
concorrência e oportunidades de baixo custo de produção.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any, List
import uuid

class PesquisadorMercado(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_2_pesquisador",
            name="Pesquisador de Mercado",
            role="Pesquisa de nichos, análise de concorrência e identificação de demanda",
            db_manager=db_manager,
            event_bus=event_bus
        )

    def get_market_opportunities_catalog(self) -> List[Dict[str, Any]]:
        """
        Catálogo de oportunidades validadas de produtos digitais
        com custo zero de distribuição e foco em dores reais.
        """
        return [
            {
                "title": "Kit Gestão Financeira MEI & Pequenos Negócios",
                "niche": "Finanças e Empreendedorismo",
                "target_audience": "Microempreendedores Individuais (MEI) e Autônomos",
                "problem_to_solve": "Descontrole de fluxo de caixa, mistura de contas pessoais com da empresa e medo do imposto de renda.",
                "estimated_demand": "ALTA",
                "suggested_price": 27.90,
                "competition_level": "MEDIA",
                "product_type": "SPREADSHEET"
            },
            {
                "title": "Guia Prático de Automação de Tarefas com Ferramentas Gratuitas",
                "niche": "Produtividade & Tecnologia",
                "target_audience": "Profissionais liberais, estudantes e assistentes virtuais",
                "problem_to_solve": "Perda de horas semanais com tarefas manuais repetitivas que poderiam ser automatizadas sem gastar nada.",
                "estimated_demand": "ALTA",
                "suggested_price": 34.90,
                "competition_level": "BAIXA",
                "product_type": "EBOOK"
            },
            {
                "title": "Manual de Contratos Essenciais para Freelancers & Prestadores de Serviço",
                "niche": "Negócios & Jurídico Prático",
                "target_audience": "Freelancers, designers, programadores e consultores",
                "problem_to_solve": "Calotes, falta de escopo definido e insegurança jurídica por não ter contratos profissionais prontos.",
                "estimated_demand": "ALTA",
                "suggested_price": 47.00,
                "competition_level": "MEDIA",
                "product_type": "TEMPLATE"
            },
            {
                "title": "Calculadora Interativa de Precificação de Serviços Digitais",
                "niche": "Precificação e Vendas",
                "target_audience": "Criadores de conteúdo, redatores e prestadores de serviços",
                "problem_to_solve": "Cobrar valor abaixo do mercado por não saber calcular hora técnica, custos fixos e margem de lucro real.",
                "estimated_demand": "MEDIA",
                "suggested_price": 19.90,
                "competition_level": "BAIXA",
                "product_type": "TOOL"
            },
            {
                "title": "Checklist de Segurança Digital & Backup para Pequenas Empresas",
                "niche": "Segurança da Informação",
                "target_audience": "Pequenas empresas, escritórios e consultórios",
                "problem_to_solve": "Vulnerabilidade a golpes de phishing, perda catastrófica de arquivos e falta de rotina de backup segura.",
                "estimated_demand": "MEDIA",
                "suggested_price": 22.50,
                "competition_level": "BAIXA",
                "product_type": "GUIDE"
            }
        ]

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("WORKING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Iniciando pesquisa de mercado: {task_title}")

        catalog = self.get_market_opportunities_catalog()
        
        # Filtra ou seleciona uma oportunidade que ainda não foi cadastrada
        existing_opps = self.db.get_opportunities(limit=50)
        existing_titles = {o["title"] for o in existing_opps}

        selected_opp = None
        for opp in catalog:
            if opp["title"] not in existing_titles:
                selected_opp = opp
                break

        if not selected_opp:
            # Se todas já foram identificadas, cicla a de maior demanda
            selected_opp = catalog[len(existing_opps) % len(catalog)]
            selected_opp = dict(selected_opp)
            selected_opp["title"] = f"{selected_opp['title']} (Versão Especial {len(existing_opps)+1})"

        opp_id = f"opp_{uuid.uuid4().hex[:8]}"
        self.db.add_opportunity(
            opp_id=opp_id,
            title=selected_opp["title"],
            niche=selected_opp["niche"],
            target_audience=selected_opp["target_audience"],
            problem_to_solve=selected_opp["problem_to_solve"],
            estimated_demand=selected_opp["estimated_demand"],
            suggested_price=selected_opp["suggested_price"],
            competition_level=selected_opp["competition_level"]
        )

        output = {
            "opportunity_id": opp_id,
            "opportunity": selected_opp,
            "analysis": {
                "viability_score": 92 if selected_opp["estimated_demand"] == "ALTA" else 80,
                "production_cost": "R$ 0,00 (Produção interna pelo Agente Produtor)",
                "recommended_channels": ["Kiwify", "Gumroad", "Hotmart", "Comunidades Orgânicas"]
            }
        }

        self.db.update_task_status(task_id, "COMPLETED", output)
        self.emit_event("OPPORTUNITY_IDENTIFIED", {
            "target_type": "OPPORTUNITY",
            "target_id": opp_id,
            "summary": f"Oportunidade identificada: {selected_opp['title']} (Preço sugerido: R$ {selected_opp['suggested_price']:.2f})",
            "opportunity_id": opp_id
        })

        self.set_status("IDLE")
        return output
