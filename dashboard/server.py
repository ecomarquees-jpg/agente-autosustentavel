"""
Servidor Web HTTP nativo para o Painel de Controle e API REST.
Zero dependências de terceiros (utiliza http.server e json da biblioteca padrão do Python).
"""
import http.server
import json
import urllib.parse
from pathlib import Path
from typing import Dict, Any

STATIC_DIR = Path(__file__).resolve().parent / "static"

class DashboardRequestHandler(http.server.BaseHTTPRequestHandler):
    workflow = None  # Injetado na inicialização do servidor

    def _send_json(self, status_code: int, data: Dict[str, Any]):
        response_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response_bytes)

    def _send_file(self, file_path: Path, content_type: str):
        if not file_path.exists():
            self.send_error(404, "Arquivo não encontrado")
            return
        with open(file_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        elif path == "/landing":
            landing_file = STATIC_DIR.parent.parent / "data" / "products_vault" / "landing_page_kit_mei.html"
            self._send_file(landing_file, "text/html; charset=utf-8")
        elif path == "/static/style.css":
            self._send_file(STATIC_DIR / "style.css", "text/css; charset=utf-8")
        elif path == "/static/app.js":
            self._send_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")
        elif path == "/api/status":
            data = self.workflow.get_dashboard_data()
            data["transactions"] = self.workflow.db.get_transactions(limit=20)
            self._send_json(200, data)
        elif path == "/api/product_preview":
            query = urllib.parse.parse_qs(parsed.query)
            prod_id = query.get("id", [None])[0]
            if not prod_id:
                self._send_json(400, {"error": "Parâmetro 'id' ausente"})
                return
            product = self.workflow.db.get_product(prod_id)
            if not product:
                self._send_json(404, {"error": "Produto não encontrado"})
                return
            
            fpath = Path(product["file_path"])
            file_content = ""
            if fpath.exists():
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    file_content = f.read()
            else:
                file_content = "(Arquivo não encontrado no cofre)"

            self._send_json(200, {
                "id": product["id"],
                "title": product["title"],
                "product_type": product["product_type"],
                "file_path": product["file_path"],
                "file_content": file_content
            })
        else:
            self.send_error(404, "Rota não encontrada")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = {}
        if content_len > 0:
            raw_body = self.rfile.read(content_len).decode('utf-8')
            try:
                post_data = json.loads(raw_body)
            except Exception:
                post_data = {}

        if path == "/api/action/run_cycle":
            result = self.workflow.run_cycle()
            self._send_json(200, {"success": True, "result": result})
        elif path == "/api/action/approve":
            prod_id = post_data.get("product_id")
            reason = post_data.get("reason", "Aprovado via Painel Web")
            if not prod_id:
                self._send_json(400, {"error": "ID do produto ausente"})
                return
            success = self.workflow.approve_product(prod_id, reason)
            self._send_json(200, {"success": success})
        elif path == "/api/action/reject":
            prod_id = post_data.get("product_id")
            reason = post_data.get("reason", "Rejeitado via Painel Web")
            if not prod_id:
                self._send_json(400, {"error": "ID do produto ausente"})
                return
            success = self.workflow.reject_product(prod_id, reason)
            self._send_json(200, {"success": success})
        elif path == "/api/action/sale":
            amount = float(post_data.get("amount", 0.0))
            desc = post_data.get("description", "Venda de produto digital")
            if amount <= 0:
                self._send_json(400, {"error": "Valor inválido"})
                return
            tx_id = self.workflow.register_real_sale(amount, desc)
            self._send_json(200, {"success": True, "transaction_id": tx_id})
        elif path == "/api/action/expense":
            amount = float(post_data.get("amount", 0.0))
            desc = post_data.get("description", "Despesa operacional")
            if amount <= 0:
                self._send_json(400, {"error": "Valor inválido"})
                return
            tx_id = self.workflow.register_real_expense(amount, desc)
            self._send_json(200, {"success": True, "transaction_id": tx_id})
        elif path == "/api/action/survival_check":
            diag = self.workflow.trigger_survival_check()
            self._send_json(200, {"success": True, "diagnostic": diag})
        elif path == "/api/action/start_loop":
            res = self.workflow.start_autonomous_loop()
            self._send_json(200, {"success": True, "result": res})
        elif path == "/api/action/stop_loop":
            res = self.workflow.stop_autonomous_loop()
            self._send_json(200, {"success": True, "result": res})
        else:
            self.send_error(404, "Ação não encontrada")

def run_server(workflow, port: int = 8080):
    DashboardRequestHandler.workflow = workflow
    for p in [port, port + 1, port + 2]:
        try:
            server = http.server.ThreadingHTTPServer(('127.0.0.1', p), DashboardRequestHandler)
            print(f"[SERVIDOR] Painel de Controle disponível em: http://localhost:{p}")
            return server, p
        except OSError:
            print(f"[AVISO] Porta {p} ocupada, tentando próxima...")
    raise RuntimeError("Nenhuma porta disponível para o servidor.")
