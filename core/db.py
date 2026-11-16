"""
Gerenciador do banco de dados relacional SQLite (business.db).
Armazena o estado completo dos agentes, tarefas, oportunidades, produtos, finanças e auditoria.
Zero dependências externas.
"""
import sqlite3
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "business.db"

class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Agentes
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'IDLE',
                current_task_id TEXT,
                updated_at TEXT NOT NULL
            );
            """)

            # 2. Tarefas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                assigned_to TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                priority INTEGER NOT NULL DEFAULT 3,
                created_at TEXT NOT NULL,
                finished_at TEXT,
                output_data TEXT
            );
            """)

            # 3. Oportunidades de Mercado
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                niche TEXT NOT NULL,
                target_audience TEXT NOT NULL,
                problem_to_solve TEXT NOT NULL,
                estimated_demand TEXT NOT NULL,
                suggested_price REAL NOT NULL,
                competition_level TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'IDENTIFIED',
                created_at TEXT NOT NULL
            );
            """)

            # 4. Produtos Digitais
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                opportunity_id TEXT,
                title TEXT NOT NULL,
                product_type TEXT NOT NULL,
                file_path TEXT NOT NULL,
                price REAL NOT NULL,
                content_summary TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'DRAFT',
                quality_score INTEGER NOT NULL DEFAULT 0,
                audit_notes TEXT,
                created_at TEXT NOT NULL,
                approved_at TEXT
            );
            """)

            # 5. Campanhas Comerciais
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                title TEXT NOT NULL,
                headline TEXT NOT NULL,
                ad_copy TEXT NOT NULL,
                landing_page_text TEXT NOT NULL,
                suggested_channels TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'CREATED',
                created_at TEXT NOT NULL
            );
            """)

            # 6. Livro Caixa / Finanças
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ledger (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL, -- REVENUE ou EXPENSE
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL, -- REALIZED, PENDING, PROJECTION
                created_at TEXT NOT NULL
            );
            """)

            # 7. Logs de Auditoria
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                agent_name TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                severity TEXT NOT NULL, -- INFO, WARNING, ERROR, SUCCESS
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """)

            # 8. Diagnósticos de Sobrevivência
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS survival_diagnostics (
                id TEXT PRIMARY KEY,
                net_result REAL NOT NULL,
                realized_revenue REAL NOT NULL,
                realized_expenses REAL NOT NULL,
                status TEXT NOT NULL, -- HEALTHY, EQUILIBRIUM, DEFICIT
                recovery_plan TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """)

            conn.commit()

    # --- Métodos de Agentes ---
    def register_or_update_agent(self, agent_id: str, name: str, role: str, status: str = 'IDLE', current_task_id: Optional[str] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO agents (id, name, role, status, current_task_id, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = excluded.status,
                current_task_id = excluded.current_task_id,
                updated_at = excluded.updated_at;
            """, (agent_id, name, role, status, current_task_id, now))
            conn.commit()

    def get_agents(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agents ORDER BY id ASC")
            return [dict(row) for row in cursor.fetchall()]

    # --- Métodos de Tarefas ---
    def create_task(self, task_id: str, title: str, description: str, assigned_to: str, priority: int = 3) -> str:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO tasks (id, title, description, assigned_to, status, priority, created_at)
            VALUES (?, ?, ?, ?, 'PENDING', ?, ?)
            """, (task_id, title, description, assigned_to, priority, now))
            conn.commit()
            return task_id

    def update_task_status(self, task_id: str, status: str, output_data: Optional[Dict[str, Any]] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            finished_at = datetime.now().isoformat() if status in ('COMPLETED', 'FAILED', 'AUDITED') else None
            output_json = json.dumps(output_data, ensure_ascii=False) if output_data else None
            cursor.execute("""
            UPDATE tasks
            SET status = ?, finished_at = ?, output_data = ?
            WHERE id = ?
            """, (status, finished_at, output_json, task_id))
            conn.commit()

    def get_recent_tasks(self, limit: int = 15) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                if item.get("output_data"):
                    try:
                        item["output_data"] = json.loads(item["output_data"])
                    except Exception:
                        pass
                results.append(item)
            return results

    # --- Métodos de Oportunidades ---
    def add_opportunity(self, opp_id: str, title: str, niche: str, target_audience: str, problem_to_solve: str,
                        estimated_demand: str, suggested_price: float, competition_level: str) -> str:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO opportunities (id, title, niche, target_audience, problem_to_solve, estimated_demand, suggested_price, competition_level, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'IDENTIFIED', ?)
            """, (opp_id, title, niche, target_audience, problem_to_solve, estimated_demand, suggested_price, competition_level, now))
            conn.commit()
            return opp_id

    def get_opportunities(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM opportunities ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    def update_opportunity_status(self, opp_id: str, status: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE opportunities SET status = ? WHERE id = ?", (status, opp_id))
            conn.commit()

    # --- Métodos de Produtos ---
    def add_product(self, prod_id: str, opp_id: str, title: str, product_type: str, file_path: str,
                    price: float, content_summary: str, status: str = 'DRAFT') -> str:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO products (id, opportunity_id, title, product_type, file_path, price, content_summary, status, quality_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
            """, (prod_id, opp_id, title, product_type, file_path, price, content_summary, status, now))
            conn.commit()
            return prod_id

    def update_product_audit(self, prod_id: str, quality_score: int, audit_notes: str, status: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE products
            SET quality_score = ?, audit_notes = ?, status = ?
            WHERE id = ?
            """, (quality_score, audit_notes, status, prod_id))
            conn.commit()

    def set_product_approval(self, prod_id: str, approved: bool, reason: str = ""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            new_status = 'APPROVED' if approved else 'REJECTED'
            notes_append = f" | Supervisão Humana: {'Aprovado' if approved else 'Rejeitado'} ({reason})"
            cursor.execute("""
            UPDATE products
            SET status = ?, approved_at = ?, audit_notes = audit_notes || ?
            WHERE id = ?
            """, (new_status, now if approved else None, notes_append, prod_id))
            conn.commit()

    def get_products(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
            return [dict(r) for r in cursor.fetchall()]

    def get_product(self, prod_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (prod_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    # --- Métodos de Campanhas ---
    def add_campaign(self, camp_id: str, product_id: str, title: str, headline: str, ad_copy: str,
                     landing_page_text: str, suggested_channels: List[str], status: str = 'WAITING_APPROVAL') -> str:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            channels_json = json.dumps(suggested_channels, ensure_ascii=False)
            cursor.execute("""
            INSERT INTO campaigns (id, product_id, title, headline, ad_copy, landing_page_text, suggested_channels, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (camp_id, product_id, title, headline, ad_copy, landing_page_text, channels_json, status, now))
            conn.commit()
            return camp_id

    def get_campaigns(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                try:
                    item["suggested_channels"] = json.loads(item["suggested_channels"])
                except Exception:
                    pass
                results.append(item)
            return results

    # --- Métodos de Finanças (Ledger) ---
    def add_transaction(self, trans_id: str, trans_type: str, category: str, amount: float,
                        description: str, status: str = 'REALIZED') -> str:
        """
        Status aceitos:
        - REALIZED: Dinheiro efetivo em conta / pago comprovadamente
        - PENDING: Venda aguardando compensação de pagamento
        - PROJECTION: Estimativa / projeção de receita ou custo
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO ledger (id, type, category, amount, description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (trans_id, trans_type.upper(), category, float(amount), description, status.upper(), now))
            conn.commit()
            return trans_id

    def get_financial_summary(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Receitas Efetivas (REALIZED)
            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM ledger WHERE type = 'REVENUE' AND status = 'REALIZED'")
            realized_revenue = cursor.fetchone()[0]

            # 2. Vendas Pendentes (PENDING)
            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM ledger WHERE type = 'REVENUE' AND status = 'PENDING'")
            pending_revenue = cursor.fetchone()[0]

            # 3. Projeções de Receita (PROJECTION)
            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM ledger WHERE type = 'REVENUE' AND status = 'PROJECTION'")
            projected_revenue = cursor.fetchone()[0]

            # 4. Despesas Efetivas (REALIZED)
            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM ledger WHERE type = 'EXPENSE' AND status = 'REALIZED'")
            realized_expenses = cursor.fetchone()[0]

            # 5. Despesas Planejadas / Orçamento Base
            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM ledger WHERE type = 'EXPENSE' AND status = 'PROJECTION'")
            projected_expenses = cursor.fetchone()[0]

            # Métricas calculadas
            net_result = realized_revenue - realized_expenses
            available_balance = net_result  # Considera base zero inicial se não houver aporte
            target_monthly = 300.00
            target_min = 200.00
            progress_percent = min(100.0, round((realized_revenue / target_monthly) * 100, 1)) if target_monthly > 0 else 0

            # Status de Sobrevivência
            if realized_revenue >= target_min:
                survival_status = "HEALTHY" if net_result >= 100.0 else "EQUILIBRIUM"
            else:
                survival_status = "DEFICIT"

            return {
                "available_balance": round(available_balance, 2),
                "realized_revenue": round(realized_revenue, 2),
                "pending_revenue": round(pending_revenue, 2),
                "projected_revenue": round(projected_revenue, 2),
                "realized_expenses": round(realized_expenses, 2),
                "projected_expenses": round(projected_expenses, 2),
                "net_result": round(net_result, 2),
                "monthly_target": target_monthly,
                "min_target": target_min,
                "target_progress_percent": progress_percent,
                "survival_status": survival_status
            }

    def get_transactions(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ledger ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    # --- Logs de Auditoria ---
    def log_audit(self, log_id: str, agent_name: str, target_type: str, target_id: str, severity: str, message: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO audit_logs (id, agent_name, target_type, target_id, severity, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (log_id, agent_name, target_type, target_id, severity.upper(), message, now))
            conn.commit()

    def get_audit_logs(self, limit: int = 25) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    # --- Diagnósticos de Sobrevivência ---
    def record_survival_diagnostic(self, diag_id: str, net_result: float, realized_revenue: float,
                                   realized_expenses: float, status: str, recovery_plan: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
            INSERT INTO survival_diagnostics (id, net_result, realized_revenue, realized_expenses, status, recovery_plan, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (diag_id, net_result, realized_revenue, realized_expenses, status, recovery_plan, now))
            conn.commit()

    def get_latest_survival_diagnostic(self) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM survival_diagnostics ORDER BY created_at DESC LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None
