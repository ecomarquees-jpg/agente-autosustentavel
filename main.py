"""
Ponto de entrada principal do Sistema de Agentes de Negócio Digital Autossustentável.
Permite executar ciclos via linha de comando ou iniciar o Painel de Controle visual.
Zero dependências externas.
"""
import sys
import os
import argparse
import time
from pathlib import Path

# Adiciona o diretório raiz ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from engine.workflow import BusinessWorkflow
from dashboard.server import run_server

def print_status(workflow: BusinessWorkflow):
    data = workflow.get_dashboard_data()
    fin = data["finances"]
    survival = data["survival"] or {}

    print("\n" + "=" * 65)
    print("       SISTEMA AUTOSSUSTENTÁVEL — NEGÓCIO DIGITAL")
    print("=" * 65)
    
    print("\n[FINANÇAS & METAS (R$)]")
    print(f"  • Saldo em Caixa Efetivo:     R$ {fin['available_balance']:.2f}")
    print(f"  • Receita Realizada (Paga):   R$ {fin['realized_revenue']:.2f}")
    print(f"  • Vendas Pendentes:           R$ {fin['pending_revenue']:.2f}")
    print(f"  • Despesas Efetivas:          R$ {fin['realized_expenses']:.2f}")
    print(f"  • Orçamento Base Planejado:   R$ {fin['projected_expenses']:.2f} / mês")
    print(f"  • Resultado Líquido:          R$ {fin['net_result']:.2f}")
    print(f"  • Meta Mensal Desejada:       R$ {fin['monthly_target']:.2f} (+R$ 100,00 de lucro)")
    print(f"  • Progresso da Meta:          {fin['target_progress_percent']}%")
    print(f"  • Status de Sobrevivência:    {fin['survival_status']}")

    print("\n[EQUIPE DE AGENTES]")
    for a in data["agents"]:
        print(f"  • {a['name']:<32} | Status: {a['status']:<10} | Tarefa: {a['current_task_id'] or 'Ocioso'}")

    print("\n[PRODUTOS DIGITAIS]")
    if not data["products"]:
        print("  (Nenhum produto cadastrado ainda)")
    else:
        for p in data["products"]:
            print(f"  • [{p['status']:<22}] {p['title']} (R$ {p['price']:.2f} | Nota Auditoria: {p['quality_score']}/100)")

    print("\n[DIAGNÓSTICO DE SOBREVIVÊNCIA FINANCEIRA]")
    plan = survival.get("recovery_plan", "Nenhum diagnóstico registrado.")
    print("  " + plan.replace("\n", "\n  "))
    print("=" * 65 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Sistema de Agentes para Negócio Digital Autossustentável")
    parser.add_argument("--cycle", action="store_true", help="Executa um ciclo autônomo completo de pesquisa, criação e auditoria")
    parser.add_argument("--status", action="store_true", help="Exibe o relatório executivo e financeiro no terminal")
    parser.add_argument("--dashboard", action="store_true", help="Inicia o Painel de Controle visual no navegador")
    parser.add_argument("--auto", action="store_true", help="Ativa o loop 100% autônomo em segundo plano (24/7)")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)), help="Porta para o Painel Web (padrão: 8080 ou $PORT)")
    parser.add_argument("--sale", nargs=2, metavar=("VALOR", "DESCRICAO"), help="Registra uma venda real e compensada (Ex: --sale 34.90 'Venda Kiwify')")
    parser.add_argument("--expense", nargs=2, metavar=("VALOR", "DESCRICAO"), help="Registra uma despesa operacional paga (Ex: --expense 45.00 'Dominio')")
    parser.add_argument("--approve", metavar="PROD_ID", help="Aprova um produto pelo ID (Ação humana HITL)")
    parser.add_argument("--reject", nargs=2, metavar=("PROD_ID", "MOTIVO"), help="Rejeita um produto pelo ID")

    args = parser.parse_args()
    workflow = BusinessWorkflow()

    if args.sale:
        val = float(args.sale[0])
        desc = args.sale[1]
        tx_id = workflow.register_real_sale(val, desc)
        print(f"[SUCESSO] Venda real registrada: ID {tx_id} | Valor: R$ {val:.2f} ({desc})")
        return

    if args.expense:
        val = float(args.expense[0])
        desc = args.expense[1]
        tx_id = workflow.register_real_expense(val, desc)
        print(f"[AVISO] Despesa real registrada: ID {tx_id} | Valor: R$ {val:.2f} ({desc})")
        return

    if args.approve:
        success = workflow.approve_product(args.approve)
        if success:
            print(f"[SUCESSO] Produto {args.approve} formalmente APROVADO pela supervisão humana!")
        else:
            print(f"[ERRO] Produto {args.approve} não encontrado.")
        return

    if args.reject:
        prod_id, reason = args.reject
        success = workflow.reject_product(prod_id, reason)
        if success:
            print(f"[AVISO] Produto {prod_id} REJEITADO pela supervisão humana: {reason}")
        else:
            print(f"[ERRO] Produto {prod_id} não encontrado.")
        return

    if args.cycle:
        print("[INÍCIO] Disparando ciclo autônomo entre os 6 agentes...")
        res = workflow.run_cycle()
        print(f"[CONCLUÍDO] Ciclo {res['cycle_id']} finalizado.")
        print_status(workflow)
        return

    if args.status:
        print_status(workflow)
        return

    # Modo padrão: inicia o servidor web do painel
    if args.auto:
        print("[AUTONOMIA 24/7] Ativando loop autônomo contínuo dos agentes em segundo plano...")
        workflow.start_autonomous_loop(interval_seconds=300)

    print("[INICIALIZAÇÃO] Iniciando Painel de Controle Visual...")
    server, active_port = run_server(workflow, port=args.port)
    print(f"\n========================================================")
    print(f"  PAINEL DE CONTROLE ATIVO: http://localhost:{active_port}")
    print(f"  Pressione Ctrl+C para encerrar o servidor.")
    print(f"========================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[ENCERRAMENTO] Servidor finalizado com sucesso.")

if __name__ == "__main__":
    main()
