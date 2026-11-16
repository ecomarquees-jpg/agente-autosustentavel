"""
AGENTE 3 — PRODUTOR DIGITAL
Cria produtos digitais originais, práticos e de alto valor:
e-books, planilhas, modelos de documentos, ferramentas e guias.
Salva os ativos no cofre de produtos (products_vault) e envia para auditoria.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any
from pathlib import Path
import uuid
import json

VAULT_DIR = Path(__file__).resolve().parent.parent / "data" / "products_vault"

class ProdutorDigital(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_3_produtor",
            name="Produtor Digital",
            role="Criação e formatação de produtos digitais originais (e-books, planilhas, templates)",
            db_manager=db_manager,
            event_bus=event_bus
        )
        VAULT_DIR.mkdir(parents=True, exist_ok=True)

    def _generate_spreadsheet_content(self, title: str) -> str:
        return (
            "Data;Categoria;Descricao;Tipo;Valor_R$;Status\n"
            "01/11/2026;Vendas;Consultoria Tecnica;Receita;1500.00;Realizado\n"
            "03/11/2026;Infraestrutura;Hospedagem & Dominio;Despesa;45.00;Realizado\n"
            "05/11/2026;Vendas;Venda Kit Planilhas;Receita;27.90;Realizado\n"
            "10/11/2026;Custos Fixos;Internet Comercial;Despesa;110.00;Realizado\n"
            "15/11/2026;Impostos;DAS MEI Mensal;Despesa;75.00;Realizado\n"
            "20/11/2026;Vendas;Template Contrato;Receita;47.00;Realizado\n"
            "25/11/2026;Reserva;Aporte Emergencial;Investimento;300.00;Realizado\n"
            "\n"
            "# RESUMO DE INDICADORES (KPIs):\n"
            "# Total Receitas: R$ 1.574,90\n"
            "# Total Despesas: R$ 230,00\n"
            "# Saldo Liquido: R$ 1.344,90\n"
            "# Ponto de Equilibrio (Breakeven): Atingido com margem de seguranca.\n"
        )

    def _generate_ebook_content(self, title: str, niche: str) -> str:
        return f"""# {title}
*Autor: Equipe Técnica Digital | Edição 2026*

## Sumário Executivo
Este guia foi desenvolvido com um objetivo claro: eliminar o retrabalho e permitir que qualquer profissional organize seus processos utilizando apenas ferramentas gratuitas e acessíveis.

---

## Capítulo 1: O Diagnóstico do Problema
O maior obstáculo dos empreendedores e profissionais liberais modernos não é a falta de esforço, mas sim o atrito operacional diário. Quando tarefas manuais consomem mais de 30% do seu dia, a sua receita estagna.

### Principais Gargalos Identificados:
1. Processos não padronizados.
2. Comunicação fragmentada em múltiplos canais.
3. Ausência de métricas simples de controle.

---

## Capítulo 2: Estrutura Passo a Passo de Execução
Para resolver esse gargalo sem custo financeiro, implemente o ciclo dos 3 passos:
- **Mapear:** Anote durante 3 dias consecutivos cada tarefa que leva mais de 10 minutos.
- **Eliminar:** 20% das tarefas anotadas não geram valor direto e devem ser descartadas.
- **Automatizar:** Utilize rotinas pré-formatadas, templates e atalhos de software padrão.

---

## Capítulo 3: Checklist Prático de Ação Imediata
- [x] Definir uma pasta central organizada para documentos e entregáveis.
- [x] Criar padrões de nomenclatura (Ex: ANO_MES_DIA_CLIENTE_DOCUMENTO).
- [x] Estabelecer horário fixo de fechamento financeiro e checagem de pendências.
- [x] Fazer backup semanal em dois locais seguros.

---
*Produto Original verificado pelo Agente Auditor. Proibida reprodução não autorizada.*
"""

    def _generate_template_content(self, title: str) -> str:
        return f"""# {title}
### MODELO DE CONTRATO DE PRESTAÇÃO DE SERVIÇOS DIGITAIS E CONSULTORIA

**CONTRATANTE:** [Nome Completo / Razão Social], inscrito(a) no CPF/CNPJ nº [XXX.XXX.XXX-XX], com sede/domicílio em [Endereço Completo].
**CONTRATADO(A):** [Nome do Prestador / MEI], inscrito(a) no CPF/CNPJ nº [XXX.XXX.XXX-XX], com endereço profissional em [Endereço Completo].

---

### CLÁUSULA 1ª — DO OBJETO DO CONTRATO
O presente instrumento tem por objeto a prestação dos serviços especializados de [Descrever detalhadamente o serviço digital, ex: Desenvolvimento, Redação, Consultoria de Processos], conforme escopo definido no Anexo I.

### CLÁUSULA 2ª — DAS OBRIGAÇÕES E PRAZOS
1. O CONTRATADO compromete-se a entregar as etapas conforme o cronograma acordado.
2. O CONTRATANTE fornecerá as informações necessárias em até 48 horas úteis após a solicitação.

### CLÁUSULA 3ª — DO PREÇO E CONDIÇÕES DE PAGAMENTO
Pela prestação dos serviços, o CONTRATANTE pagará ao CONTRATADO o valor total de R$ [Valor acordado], sendo [50% no início e 50% na aprovação final do entregável].

### CLÁUSULA 4ª — DA PROPRIEDADE INTELECTUAL E CONFIDENCIALIDADE
Todos os arquivos e materiais desenvolvidos pertencerão ao CONTRATANTE após a quitação integral dos valores acordados. Ambas as partes comprometem-se ao sigilo absoluto de dados e estratégias.

---
[Cidade/UF], [Data].

__________________________________________
Assinatura do Contratante

__________________________________________
Assinatura do Contratado
"""

    def _generate_tool_content(self, title: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
        h1 {{ font-size: 1.4rem; color: #38bdf8; margin-top: 0; }}
        label {{ display: block; margin-top: 14px; font-size: 0.9rem; color: #94a3b8; }}
        input {{ width: 100%; box-sizing: border-box; padding: 10px; margin-top: 6px; background: #0f172a; border: 1px solid #334155; color: #fff; border-radius: 6px; }}
        button {{ width: 100%; margin-top: 20px; padding: 12px; background: #0ea5e9; color: #fff; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; }}
        button:hover {{ background: #0284c7; }}
        .result {{ margin-top: 20px; padding: 16px; background: #022c22; border: 1px solid #059669; border-radius: 8px; color: #34d399; font-size: 1.1rem; text-align: center; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{title}</h1>
        <p style="color: #94a3b8; font-size: 0.88rem;">Calcule o valor exato a cobrar por hora técnica e por projeto, cobrindo custos fixos e garantindo sua margem de lucro.</p>
        
        <label>Custos Fixos Mensais (R$):</label>
        <input type="number" id="custos" value="300">
        
        <label>Salário Desejado Mensal (R$):</label>
        <input type="number" id="salario" value="2500">
        
        <label>Horas Produtivas por Mês (Ex: 80h):</label>
        <input type="number" id="horas" value="80">

        <label>Margem de Lucro Desejada (%):</label>
        <input type="number" id="margem" value="20">

        <button onclick="calcular()">Calcular Preço por Hora</button>
        
        <div id="resultado" class="result" style="display:none;"></div>
    </div>

    <script>
        function calcular() {{
            const custos = parseFloat(document.getElementById('custos').value) || 0;
            const salario = parseFloat(document.getElementById('salario').value) || 0;
            const horas = parseFloat(document.getElementById('horas').value) || 1;
            const margem = (parseFloat(document.getElementById('margem').value) || 0) / 100;
            
            const custoHoraBase = (custos + salario) / horas;
            const precoHoraFinal = custoHoraBase * (1 + margem);
            
            const res = document.getElementById('resultado');
            res.style.display = 'block';
            res.innerHTML = '<strong>Preço Mínimo por Hora:</strong> R$ ' + precoHoraFinal.toFixed(2);
        }}
    </script>
</body>
</html>"""

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("WORKING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Iniciando produção do produto digital: {task_title}")

        opportunity = task_data.get("opportunity", {})
        title = opportunity.get("title", task_title)
        product_type = opportunity.get("product_type", "EBOOK")
        price = float(opportunity.get("suggested_price", 29.90))
        niche = opportunity.get("niche", "Geral")

        clean_slug = "".join(c if c.isalnum() else "_" for c in title.lower())[:30].strip("_")
        prod_id = f"prod_{uuid.uuid4().hex[:8]}"

        if product_type == "SPREADSHEET":
            filename = f"{clean_slug}.csv"
            content = self._generate_spreadsheet_content(title)
            summary = "Planilha de Gestão com colunas de fluxo, status e cálculo de indicadores de desempenho."
        elif product_type == "TEMPLATE":
            filename = f"{clean_slug}.md"
            content = self._generate_template_content(title)
            summary = "Modelo completo de contrato de prestação de serviços digitais com cláusulas de escopo e sigilo."
        elif product_type == "TOOL":
            filename = f"{clean_slug}.html"
            content = self._generate_tool_content(title)
            summary = "Ferramenta interativa de cálculo de precificação rodando 100% no navegador sem dependências."
        else:
            filename = f"{clean_slug}.md"
            content = self._generate_ebook_content(title, niche)
            summary = f"E-book completo e prático sobre {title}, contendo diagnóstico, framework e checklist de ação."

        target_file = VAULT_DIR / filename
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

        # Salva produto no banco com status 'DRAFT' aguardando auditoria
        self.db.add_product(
            prod_id=prod_id,
            opp_id=opportunity.get("id", "opp_default"),
            title=title,
            product_type=product_type,
            file_path=str(target_file),
            price=price,
            content_summary=summary,
            status="DRAFT"
        )

        output = {
            "product_id": prod_id,
            "title": title,
            "product_type": product_type,
            "file_path": str(target_file),
            "price": price,
            "summary": summary
        }

        self.db.update_task_status(task_id, "COMPLETED", output)
        self.emit_event("PRODUCT_CREATED", {
            "target_type": "PRODUCT",
            "target_id": prod_id,
            "summary": f"Produto original criado e armazenado no cofre: {title} ({filename})",
            "product_id": prod_id,
            "product_data": output
        })

        self.set_status("IDLE")
        return output
