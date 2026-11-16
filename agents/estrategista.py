"""
AGENTE 7 — ESTRATEGISTA DE INOVAÇÃO E CRESCIMENTO (GROWTH & INNOVATION)
Analisa o negócio, identifica gargalos, gera ideias de melhoria contínua,
estratégias de escala e novas fontes de receita com custo zero.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any, List
import uuid

class EstrategistaInovacao(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_7_estrategista",
            name="Estrategista de Inovação e Escala",
            role="Geração de ideias estratégicas, otimização de conversão, expansão de catálogo e crescimento",
            db_manager=db_manager,
            event_bus=event_bus
        )

    def generate_strategic_ideas(self) -> List[Dict[str, Any]]:
        """Gera propostas de alto impacto e baixo custo para alavancar o negócio digital."""
        return [
            {
                "title": "Implementar Order Bump no Checkout (Oferta Complementar)",
                "category": "CONVERSAO",
                "impact": "ALTO (+35% no ticket médio)",
                "effort": "BAIXO (10 minutos na Kiwify)",
                "description": "Ao comprar o 'Kit de Gestão MEI', oferecer na mesma página por apenas R$ 12,90 o 'Manual de Contratos para Prestadores'. Aumenta o faturamento sem gastar nada a mais com atração."
            },
            {
                "title": "Criar Combo / Pacote 'Empreendedor 360' com Preço Âncora",
                "category": "PRODUTO",
                "impact": "ALTO",
                "effort": "MEDIO",
                "description": "Agrupar a Planilha MEI + Guia de Automação + Contratos em um pacote único de R$ 67,00 (mostrando economia de R$ 42,00). Clientes percebem altíssimo valor e pagam mais."
            },
            {
                "title": "Distribuição Orgânica com Cortes Curtos (Instagram Reels / TikTok / Shorts)",
                "category": "DISTRIBUICAO",
                "impact": "ALTO (Alcance viral sem custo de anúncio)",
                "effort": "MEDIO",
                "description": "Gravar vídeos de 30 segundos na tela do computador mostrando a planilha preenchendo automaticamente o fluxo de caixa com a legenda: 'Comente MEI para receber o link'. Tráfego 100% orgânico."
            },
            {
                "title": "Programa de Afiliados na Kiwify (Comissão de 40% a 50%)",
                "category": "ESCALA",
                "impact": "MUITO ALTO",
                "effort": "BAIXO",
                "description": "Habilitar o programa de afiliados na Kiwify. Criadores de conteúdo e páginas sobre negócios podem vender seu kit para a audiência deles em troca de comissão, gerando vendas no piloto automático."
            },
            {
                "title": "Coleta Automática de Depoimentos e Prova Social",
                "category": "CONVERSAO",
                "impact": "MEDIO",
                "effort": "BAIXO",
                "description": "Configurar e-mail automático pós-compra após 3 dias perguntando o que o cliente achou da planilha. Os prints positivos podem ser adicionados à página de vendas para dobrar a confiança."
            }
        ]

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("WORKING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Iniciando ideação estratégica: {task_title}")

        ideas = self.generate_strategic_ideas()
        
        for idea in ideas:
            idea_id = f"idea_{uuid.uuid4().hex[:8]}"
            self.log_audit(
                "STRATEGY", idea_id, "INFO",
                f"Ideia Proposta [{idea['category']}]: {idea['title']} (Impacto: {idea['impact']})"
            )

        output = {
            "total_ideas": len(ideas),
            "proposals": ideas,
            "priority_recommendation": ideas[0]["title"]
        }

        self.db.update_task_status(task_id, "COMPLETED", output)
        self.emit_event("IDEAS_GENERATED", {
            "target_type": "STRATEGY",
            "target_id": task_id,
            "summary": f"O Agente Estrategista gerou {len(ideas)} ideias práticas para alavancar as vendas.",
            "ideas": ideas
        })

        self.set_status("IDLE")
        return output
