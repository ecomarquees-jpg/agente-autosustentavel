# Sistema Autossustentável de Negócio Digital com IA

Este sistema implementa uma equipe coordenada de **6 agentes especializados** para pesquisar, criar, divulgar, auditar e gerir financeiramente produtos e serviços digitais originais. O sistema foi desenvolvido com foco em **custo zero de infraestrutura**, **segurança**, **separação contábil estrita** e **supervisão humana obrigatória (*Human-in-the-Loop*)**.

---

## 1. Estrutura de Arquivos Criados

```
auto_digital_business/
├── core/
│   ├── models.py          # Modelos de dados tipados (Agent, Task, Product, Ledger, AuditLog)
│   ├── db.py              # Gerenciador SQLite3 nativo (business.db) com transações e índices
│   └── event_bus.py       # Barramento de eventos e mensageria auditável entre agentes
├── agents/
│   ├── base_agent.py      # Classe abstrata base com governança de estados e auditoria
│   ├── gerente.py         # Agente 1: Gerente Principal (Orquestração e relatórios)
│   ├── pesquisador.py     # Agente 2: Pesquisador de Mercado (Dores e oportunidades)
│   ├── produtor.py        # Agente 3: Produtor Digital (Criação de e-books, planilhas, ferramentas)
│   ├── comercial.py       # Agente 4: Comercial (Copywriting, landing pages e canais)
│   ├── financeiro.py      # Agente 5: Financeiro (Livro-caixa, metas e segregação de receitas)
│   └── auditor.py         # Agente 6: Auditor (Qualidade, matemática, conformidade e riscos)
├── engine/
│   ├── workflow.py        # Orquestrador unificado das rotinas operacionais
│   └── survival.py        # Motor de Sobrevivência Financeira e planos de recuperação
├── dashboard/
│   ├── server.py          # Servidor HTTP nativo e API REST (zero dependências)
│   └── static/
│       ├── index.html     # Painel de controle visual responsivo
│       ├── style.css      # Design System escuro com alta legibilidade
│       └── app.js         # Lógica do cliente web, atualização em tempo real e ações
├── data/
│   ├── business.db        # Banco de dados relacional local
│   └── products_vault/    # Cofre isolado de arquivos originais gerados
├── main.py                # Ponto de entrada CLI e inicializador do servidor
└── README.md              # Documentação completa de uso e operação
```

---

## 2. Como Iniciar o Sistema

O sistema utiliza exclusivamente a **biblioteca padrão do Python 3**, portanto **não requer `pip install` nem dependências externas**.

### Opção A: Iniciar o Painel de Controle Visual (Recomendado)
Para abrir o painel gráfico interativo no navegador:

```powershell
cd C:\Users\User\.gemini\antigravity\scratch\auto_digital_business
python main.py
```
Acesse no seu navegador: **`http://localhost:8080`**

### Opção B: Executar um Ciclo Autônomo via Terminal
```powershell
python main.py --cycle
```

### Opção C: Consultar o Relatório Financeiro e Operacional
```powershell
python main.py --status
```

---

## 3. Como Utilizar Cada Agente

1. **Agente 1 — Gerente Principal:**
   - Orquestra todo o fluxo, dispara as tarefas para os outros agentes e consolida o relatório executivo.
   - Pode ser acionado pelo botão **"⚡ Executar Ciclo Autônomo"** no painel ou via `python main.py --cycle`.

2. **Agente 2 — Pesquisador de Mercado:**
   - Varre oportunidades com demanda comprovada e dor latente (ex: controle financeiro para MEIs, modelos de contratos para freelancers, calculadoras de precificação).
   - Registra dados de concorrência e sugere preços competitivos (entre R$ 19,90 e R$ 47,00).

3. **Agente 3 — Produtor Digital:**
   - Cria o produto físico original dentro de `data/products_vault/`:
     - Planilhas CSV estruturadas prontas para uso.
     - E-books práticos em Markdown com checklists de execução.
     - Modelos jurídicos de contratos de prestação de serviços.
     - Ferramentas interativas autônomas em HTML5/JavaScript.

4. **Agente 4 — Comercial:**
   - Desenvolve a copy persuasiva (estrutura Dor-Solução-Garantia), headlines e gera uma página de apresentação (Landing Page em HTML responsivo).
   - Sugere canais de distribuição com taxa zero fixa (Kiwify, Hotmart, Gumroad e tráfego orgânico).
   - **Regra:** Nunca publica sem aprovação humana expressa.

5. **Agente 5 — Financeiro:**
   - Administra o livro-caixa contábil com segregação rígida:
     - **Dinheiro Recebido (Realized):** Apenas pagamentos confirmados.
     - **Vendas Pendentes (Pending):** Transações em processo de liquidação.
     - **Projeções (Projection):** Orçamento base de R$ 200,00 e estimativas.
   - Bloqueia pagamentos não autorizados.

6. **Agente 6 — Auditor:**
   - Realiza verificação minuciosa em cada produto: integridade do arquivo, ausência de menções a termos proibidos (cripto, promessas enganosas), coerência dos cálculos e densidade técnica.
   - Atribui nota de qualidade de 0 a 100.

---

## 4. Como Acompanhar os Resultados e Aprovações (Supervisão Humana)

1. **Aprovação de Produtos (HITL):**
   - Acesse o painel web ou use a CLI. Na tabela de produtos, clique em **"👁️ Ver Ativo"** para inspecionar o arquivo criado.
   - Clique em **"✅ Aprovar"** ou **"❌ Rejeitar"** para definir o status.
   - Via terminal: `python main.py --approve <PROD_ID>` ou `python main.py --reject <PROD_ID> "<MOTIVO>"`.

2. **Registro de Vendas Reais:**
   - No painel, clique em **"➕ Registrar Venda Real"** ou via terminal:
     ```powershell
     python main.py --sale 34.90 "Venda Guia de Automação via Kiwify"
     ```

3. **Registro de Despesas Reais:**
   - No painel, clique em **"➖ Registrar Despesa"** ou via terminal:
     ```powershell
     python main.py --expense 40.00 "Registro de domínio anual"
     ```

4. **Motor de Sobrevivência Financeira:**
   - Se as receitas realizadas forem inferiores ao custo operacional planejado (R$ 200,00), o banner superior do painel entra em modo **Déficit**, exibindo o diagnóstico das causas e um plano de recuperação em 5 etapas.

---

## 5. Limitações e Custos Previstos

- **Fase 1 (Atual - Simulação Local):**
  - Custo atual: **R$ 0,00**.
  - Não conecta em APIs bancárias reais (segurança garantida; registros manuais auditados).
  - Execução 100% local, protegida e sem dependências externas.
- **Fase 2 (Operação Comercial Real):**
  - Orçamento operacional mensal previsto: **R$ 200,00**.
  - Custos reais possíveis:
    - Plataformas de checkout (Kiwify/Hotmart): **0% custo fixo** (cobram apenas taxa percentual sobre vendas concretizadas).
    - Domínio/Hospedagem opcional: ~R$ 40,00/ano (~R$ 3,33/mês).
    - Tokens de IA adicionais (se conectado a APIs em larga escala): ~R$ 15,00 a R$ 30,00/mês.
    - Reserva para tráfego/testes autorizados: até R$ 150,00/mês.
