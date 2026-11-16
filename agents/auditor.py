"""
AGENTE 6 — AUDITOR DE QUALIDADE, RISCOS E CONFORMIDADE
Confere qualidade dos produtos, integridade dos arquivos, cálculos financeiros,
ausência de plágio/promessas milagrosas e cumprimento das regras de segurança.
"""
from agents.base_agent import BaseAgent
from typing import Dict, Any
from pathlib import Path
import uuid
import re

class AuditorQualidade(BaseAgent):
    def __init__(self, db_manager, event_bus):
        super().__init__(
            agent_id="agent_6_auditor",
            name="Auditor de Qualidade e Conformidade",
            role="Auditoria de qualidade de produtos, checagem matemática, riscos e conformidade ética",
            db_manager=db_manager,
            event_bus=event_bus
        )

    def audit_product_content(self, product_id: str) -> Dict[str, Any]:
        product = self.db.get_product(product_id)
        if not product:
            return {"score": 0, "approved": False, "notes": "Produto não localizado no banco de dados."}

        file_path = Path(product["file_path"])
        if not file_path.exists():
            return {"score": 0, "approved": False, "notes": f"Arquivo físico ausente no cofre: {file_path}"}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        score = 100
        notes = []

        # 1. Verificação de Regras Críticas do Projeto (Não misturar com criptomoedas)
        crypto_keywords = ["bitcoin", "ethereum", "cripto", "crypto", "blockchain", "token", "nft", "trader"]
        for kw in crypto_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', content, re.IGNORECASE):
                score -= 40
                notes.append(f"VIOLAÇÃO CRÍTICA: Termo proibido '{kw}' detectado. Escopo deve ser estritamente digital tradicional.")

        # 2. Verificação de Promessas Irreais / Risco Comercial
        spam_keywords = ["dinheiro fácil", "fique rico", "sem esforço", "renda passiva garantida", "ganhos rápidos"]
        for sk in spam_keywords:
            if re.search(r'\b' + re.escape(sk) + r'\b', content, re.IGNORECASE):
                score -= 30
                notes.append(f"RISCO DE CONFORMIDADE: Promessa potencialmente enganosa detectada: '{sk}'.")

        # 3. Verificação de Tamanho e Densidade de Conteúdo
        if len(content.strip()) < 150:
            score -= 25
            notes.append("CONTEÚDO CURTO: O material parece superficial e requer enriquecimento.")

        # 4. Verificação de Integridade Estrutural por Tipo
        ptype = product["product_type"]
        if ptype == "SPREADSHEET" and ";" not in content and "," not in content:
            score -= 20
            notes.append("FORMATO INCORRETO: Planilha não possui delimitadores válidos de tabela.")
        elif ptype == "TOOL" and "<html" not in content.lower():
            score -= 20
            notes.append("FORMATO INCORRETO: Ferramenta interativa não contém marcação HTML válida.")
        elif ptype == "TEMPLATE" and ("cláusula" not in content.lower() and "contrato" not in content.lower()):
            score -= 15
            notes.append("ESTRUTURA INCOMPLETA: Modelo de documento não possui cláusulas fundamentais.")

        # 5. Verificação de Precificação Realista
        price = product["price"]
        if price <= 0:
            score -= 30
            notes.append("PREÇO INVÁLIDO: Produto não pode ter preço zero ou negativo.")
        elif price > 150.00:
            notes.append("ALERTA DE PRECIFICAÇÃO: Preço acima de R$ 150,00 pode aumentar o custo de aquisição e atrito de vendas.")

        score = max(0, min(100, score))
        is_approved = score >= 70

        if is_approved:
            notes.append("CONFORMIDADE ATINGIDA: Produto original aprovado em termos de integridade, clareza e segurança.")

        final_notes_str = " | ".join(notes)
        new_status = "AUDITED" if is_approved else "REJECTED"

        self.db.update_product_audit(product_id, score, final_notes_str, new_status)
        
        return {
            "score": score,
            "approved": is_approved,
            "status": new_status,
            "notes": final_notes_str
        }

    def audit_financial_ledger(self) -> Dict[str, Any]:
        """Auditoria matemática e de integridade do livro-caixa."""
        summary = self.db.get_financial_summary()
        issues = []

        if summary["realized_expenses"] < 0:
            issues.append("Despesas negativas encontradas no livro-caixa.")
        if summary["realized_revenue"] < 0:
            issues.append("Receitas negativas encontradas no livro-caixa.")
            
        calculated_net = round(summary["realized_revenue"] - summary["realized_expenses"], 2)
        if calculated_net != summary["net_result"]:
            issues.append(f"Divergência matemática no resultado líquido: {calculated_net} vs {summary['net_result']}.")

        is_healthy = len(issues) == 0
        return {
            "is_healthy": is_healthy,
            "issues": issues,
            "summary": summary
        }

    def execute_task(self, task_id: str, task_title: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.set_status("AUDITING", current_task_id=task_id)
        self.log_audit("TASK", task_id, "INFO", f"Iniciando auditoria: {task_title}")

        product_id = task_data.get("product_id")
        if product_id:
            audit_result = self.audit_product_content(product_id)
            severity = "SUCCESS" if audit_result["approved"] else "WARNING"
            self.log_audit(
                "PRODUCT", product_id, severity,
                f"Auditoria concluída com nota {audit_result['score']}/100. Status: {audit_result['status']}."
            )
            output = audit_result
        else:
            fin_result = self.audit_financial_ledger()
            severity = "SUCCESS" if fin_result["is_healthy"] else "ERROR"
            self.log_audit(
                "FINANCIAL", "LEDGER", severity,
                f"Auditoria contábil finalizada. Integridade: {fin_result['is_healthy']}."
            )
            output = fin_result

        self.db.update_task_status(task_id, "COMPLETED", output)
        self.set_status("IDLE")
        return output
