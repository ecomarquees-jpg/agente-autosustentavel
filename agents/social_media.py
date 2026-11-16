"""
AGENTE 8 — GESTOR DE REDES SOCIAIS & PÁGINAS DO FACEBOOK (SOCIAL MEDIA AGENT)
Cria o calendário editorial, posts persuasivos, enquetes de engajamento,
estratégias de grupos e roteiros de interação para movimentar a página do Facebook
e direcionar tráfego qualificado para o checkout da Kiwify.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any, List
import uuid

class GestorFacebook(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_8_facebook",
            name="Gestor de Comunidade & Facebook",
            role="Planejamento de conteúdo, roteiros de postagens, engajamento e tração orgânica no Facebook",
            db_manager=db_manager,
            event_bus=event_bus
        )

    def generate_editorial_calendar(self, checkout_url: str = "https://pay.kiwify.com.br/mriY17r") -> List[Dict[str, Any]]:
        """Gera um cronograma semanal de publicações com foco em engajamento e vendas orgânicas."""
        return [
            {
                "dia": "Segunda-feira",
                "tipo": "Dica Prática / Conteúdo de Valor",
                "titulo": "O Maior Erro do MEI: Misturar a Conta Pessoal com a da Empresa",
                "copy": (
                    "🚨 Se você é MEI ou autônomo, preste muita atenção nisso!\n\n"
                    "O erro número 1 que faz pequenos negócios quebrarem no primeiro ano não é a falta de clientes, "
                    "mas sim usar a conta da empresa para pagar o mercado de casa ou a conta de luz pessoal.\n\n"
                    "💡 Regra de ouro: Defina um 'pró-labore' mensal fixo e separe uma planilha exclusiva para o negócio.\n\n"
                    "👉 Quer uma planilha pronta que já calcula tudo no automático e diz seu lucro real?\n"
                    f"Acesse o link do nosso kit oficial: {checkout_url}\n\n"
                    "#MEI #Empreendedorismo #FinancasPessoais #GestaoFinanceira"
                ),
                "sugestao_visual": "Imagem comparativa: 'Conta Bagunçada vs. Fluxo de Caixa Separado'.",
                "horario_recomendado": "09:00 ou 12:30"
            },
            {
                "dia": "Quarta-feira",
                "tipo": "Interativo / Enquete para o Algoritmo",
                "titulo": "Pesquisa Rápida: Como Você Controla Suas Entradas e Saídas?",
                "copy": (
                    "Pergunta sincera para quem trabalha por conta própria 👇\n\n"
                    "Como está o controle financeiro do seu negócio hoje?\n\n"
                    "1️⃣ Anoto em um caderno de papel\n"
                    "2️⃣ Tenho uma planilha no computador\n"
                    "3️⃣ Olho só o saldo do aplicativo do banco\n"
                    "4️⃣ Ainda não tenho controle nenhum 😅\n\n"
                    "Comente o número aqui embaixo! Vou responder quem comentar o número 4 com uma dica gratuita."
                ),
                "sugestao_visual": "Arte quadrada com fundo escuro e números grandes coloridos para incentivar cliques.",
                "horario_recomendado": "18:00 às 20:00"
            },
            {
                "dia": "Sexta-feira",
                "tipo": "Oferta Direta & Prova de Benefício",
                "titulo": "Fechamento da Semana em Menos de 5 Minutos",
                "copy": (
                    "Sexta-feira chegou e você já sabe quanto seu negócio realmente lucrou nesta semana? 📊\n\n"
                    "Com o nosso **Kit de Gestão Financeira para MEI**, você só precisa lançar as entradas e saídas:\n"
                    "✅ O dashboard calcula o saldo líquido automaticamente\n"
                    "✅ Mostra se você atingiu o ponto de equilíbrio\n"
                    "✅ Evita surpresas com o imposto e o DAS mensal\n\n"
                    "De R$ 57,00 por apenas **R$ 27,90** (pagamento único via PIX com acesso imediato).\n\n"
                    f"👉 Garanta a sua cópia antes de encerrar o dia: {checkout_url}\n\n"
                    "#GestaoMEI #Autonomo #PlanilhasExcel #Planejamento"
                ),
                "sugestao_visual": "Print do painel com gráficos da planilha e o valor de R$ 27,90 em destaque.",
                "horario_recomendado": "11:30 ou 17:00"
            },
            {
                "dia": "Domingo",
                "tipo": "Motivacional & Planejamento da Semana",
                "titulo": "Quem Planeja o Domingo, Não Passa Sufoco na Segunda",
                "copy": (
                    "O sucesso da sua próxima semana começa nos 15 minutos que você dedica a organizar suas metas hoje.\n\n"
                    "Separe seus compromissos, confira seus recebíveis e comece a semana com clareza total.\n\n"
                    "Boa semana a todos os empreendedores que fazem a roda girar! 🚀\n\n"
                    f"🔗 Conheça nossas ferramentas de gestão: {checkout_url}"
                ),
                "sugestao_visual": "Foto limpa de um café com notebook aberto exibindo a planilha organizada.",
                "horario_recomendado": "19:30"
            }
        ]

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("WORKING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Gerando cronograma para Facebook: {task_title}")

        checkout_url = task_data.get("checkout_url", "https://pay.kiwify.com.br/mriY17r")
        calendar = self.generate_editorial_calendar(checkout_url=checkout_url)

        for post in calendar:
            post_id = f"fb_{uuid.uuid4().hex[:6]}"
            self.log_audit(
                "FACEBOOK", post_id, "INFO",
                f"Post agendado para {post['dia']} ({post['tipo']}): {post['titulo']}"
            )

        output = {
            "checkout_url": checkout_url,
            "total_posts": len(calendar),
            "calendar": calendar,
            "growth_strategy": [
                "1. Compartilhar os posts educativos em 3 a 5 grupos públicos de MEIs no Facebook (sem fazer spam, focando em ajudar).",
                "2. Fixar o post de oferta de sexta-feira no topo da página com o link da Kiwify.",
                "3. Responder a todos os comentários nos primeiros 30 minutos para elevar o alcance orgânico da publicação."
            ]
        }

        self.db.update_task_status(task_id, "COMPLETED", output)
        self.emit_event("FACEBOOK_CAMPAIGN_PREPARED", {
            "target_type": "FACEBOOK",
            "target_id": task_id,
            "summary": f"Calendário de 4 postagens estratégicas preparado para movimentar a página do Facebook com o link {checkout_url}.",
            "output": output
        })

        self.set_status("IDLE")
        return output
