"""
AGENTE 4 — COMERCIAL
Prepara anúncios, páginas de apresentação (landing pages), descrições de vendas e canais de divulgação.
Não publica nem vende sem autorização humana expressa.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any, List
import uuid

class AgenteComercial(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_4_comercial",
            name="Agente Comercial",
            role="Copywriting, estratégias de lançamento, páginas de vendas e canais de divulgação",
            db_manager=db_manager,
            event_bus=event_bus
        )

    def generate_sales_assets(self, product: Dict[str, Any]) -> Dict[str, Any]:
        title = product["title"]
        price = product["price"]
        ptype = product["product_type"]

        headline = f"Como dominar {title} e economizar dezenas de horas sem gastar com softwares caros"
        
        ad_copy = f"""🔥 Cansado de perder tempo e dinheiro com processos desorganizados?

Chegou o {title}!
Desenvolvido especificamente para quem busca eficiência prática e resultados imediatos no seu negócio ou rotina diária.

O que você recebe:
✅ Acesso imediato ao material original completo
✅ Modelos prontos para aplicar no primeiro dia
✅ Suporte a ferramentas gratuitas (zero custo adicional de mensalidades)
✅ Garantia incondicional de qualidade e satisfação

💰 Por apenas R$ {price:.2f} (Pagamento único, sem assinaturas)
👉 Toque no link abaixo para conferir a apresentação completa e destravar sua cópia!"""

        landing_page_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{title} — Apresentação Oficial</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; }}
        .container {{ max-width: 720px; margin: 0 auto; background: #1e293b; padding: 36px; border-radius: 16px; border: 1px solid #334155; }}
        .badge {{ background: #0284c7; color: #fff; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; display: inline-block; }}
        h1 {{ font-size: 2rem; color: #38bdf8; margin: 16px 0 12px; line-height: 1.3; }}
        p.subtitle {{ color: #94a3b8; font-size: 1.1rem; line-height: 1.5; }}
        .benefits {{ background: #0f172a; padding: 20px; border-radius: 10px; margin: 24px 0; border: 1px solid #1e293b; }}
        .benefits li {{ margin: 10px 0; color: #e2e8f0; }}
        .price-box {{ text-align: center; padding: 24px; background: #022c22; border: 2px solid #059669; border-radius: 12px; margin-top: 30px; }}
        .price-tag {{ font-size: 2.2rem; font-weight: 800; color: #34d399; margin: 10px 0; }}
        .btn {{ display: inline-block; width: 100%; box-sizing: border-box; text-align: center; background: #10b981; color: #022c22; padding: 16px; font-size: 1.15rem; font-weight: bold; border-radius: 8px; text-decoration: none; margin-top: 14px; cursor: pointer; }}
        .notice {{ margin-top: 20px; font-size: 0.85rem; color: #64748b; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">Lançamento Digital Oficial</span>
        <h1>{headline}</h1>
        <p class="subtitle">Um pacote completo, direto ao ponto e pronto para aplicar. Elimine o atrito e foque no que realmente traz retorno.</p>
        
        <div class="benefits">
            <h3>O que está incluso nesta solução:</h3>
            <ul>
                <li><strong>Material 100% Original:</strong> Criado por especialistas técnicos e auditado.</li>
                <li><strong>Compatibilidade Imediata:</strong> Funciona nos seus softwares habituais sem instalação de pacotes pesados.</li>
                <li><strong>Checklist de Aplicação:</strong> Roteiro passo a passo para executar em menos de 30 minutos.</li>
            </ul>
        </div>

        <div class="price-box">
            <div style="color: #a7f3d0; font-size: 0.95rem; text-transform: uppercase; font-weight: 600;">Condição Especial de Lançamento</div>
            <div class="price-tag">R$ {price:.2f}</div>
            <div style="color: #6ee7b7; font-size: 0.85rem;">Pagamento Único • Acesso Imediato</div>
            <a class="btn" href="#comprar">Garantir Meu Acesso Agora</a>
        </div>

        <div class="notice">
            Aviso de Segurança: Este anúncio e produto passam por supervisão humana permanente antes de qualquer divulgação pública externa.
        </div>
    </div>
</body>
</html>"""

        suggested_channels = [
            "Kiwify / Hotmart (Checkout de alta conversão sem custo fixo inicial)",
            "Gumroad (Distribuição internacional ou direta para produtos técnicos)",
            "Comunidades Orgânicas (Grupos de MEIs, freelancers e redes de profissionais)",
            "Perfil Institucional / Conteúdo em Redes Sociais com tráfego 100% orgânico"
        ]

        return {
            "headline": headline,
            "ad_copy": ad_copy,
            "landing_page_html": landing_page_html,
            "suggested_channels": suggested_channels
        }

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("WORKING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Criando ativos comerciais para: {task_title}")

        product_id = task_data.get("product_id")
        product = self.db.get_product(product_id)
        if not product:
            self.set_status("BLOCKED")
            raise ValueError(f"Produto {product_id} não encontrado para criação de campanha.")

        assets = self.generate_sales_assets(product)
        camp_id = f"camp_{uuid.uuid4().hex[:8]}"

        self.db.add_campaign(
            camp_id=camp_id,
            product_id=product_id,
            title=f"Campanha de Lançamento: {product['title']}",
            headline=assets["headline"],
            ad_copy=assets["ad_copy"],
            landing_page_text=assets["landing_page_html"],
            suggested_channels=assets["suggested_channels"],
            status="WAITING_APPROVAL"
        )

        output = {
            "campaign_id": camp_id,
            "headline": assets["headline"],
            "channels": assets["suggested_channels"],
            "status": "WAITING_APPROVAL (Aguardando autorização humana antes de publicar)"
        }

        self.db.update_task_status(task_id, "COMPLETED", output)
        self.emit_event("CAMPAIGN_PREPARED", {
            "target_type": "CAMPAIGN",
            "target_id": camp_id,
            "summary": f"Campanha comercial preparada para '{product['title']}'. Aguardando aprovação humana.",
            "campaign_id": camp_id
        })

        self.set_status("IDLE")
        return output
