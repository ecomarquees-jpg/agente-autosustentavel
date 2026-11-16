// Dashboard Client Logic - Agente Autossustentável

async function fetchStatus() {
    try {
        const res = await fetch('/api/status');
        if (!res.ok) throw new Error("Erro na requisição da API");
        const data = await res.json();
        renderDashboard(data);
    } catch (err) {
        console.error("Falha ao atualizar dados do painel:", err);
    }
}

function renderDashboard(data) {
    const fin = data.finances || {};
    const agents = data.agents || [];
    const products = data.products || [];
    const opps = data.opportunities || [];
    const tasks = data.recent_tasks || [];
    const transactions = data.transactions || [];
    const auditLogs = data.audit_logs || [];
    const survival = data.survival || {};

    // 0. Botão de Modo 100% Autônomo
    const loopBtn = document.getElementById('btn-auto-loop');
    isLoopRunning = !!data.autonomous_loop_running;
    if (loopBtn) {
        if (isLoopRunning) {
            loopBtn.className = 'btn btn-secondary';
            loopBtn.innerHTML = '🟢 Modo 100% Autônomo: ATIVO (24/7)';
        } else {
            loopBtn.className = 'btn btn-dark';
            loopBtn.innerHTML = '⚪ Modo 100% Autônomo: DESATIVADO';
        }
    }

    // 1. KPIs Financeiros
    document.getElementById('kpi-balance').textContent = `R$ ${(fin.available_balance || 0).toFixed(2)}`;
    document.getElementById('kpi-revenue').textContent = `R$ ${(fin.realized_revenue || 0).toFixed(2)}`;
    document.getElementById('kpi-expenses').textContent = `R$ ${(fin.realized_expenses || 0).toFixed(2)}`;
    
    const netEl = document.getElementById('kpi-net');
    const netVal = fin.net_result || 0;
    netEl.textContent = `R$ ${netVal.toFixed(2)}`;
    netEl.className = 'kpi-value ' + (netVal >= 100 ? 'text-green' : (netVal >= 0 ? 'text-blue' : 'text-red'));

    const progress = fin.target_progress_percent || 0;
    document.getElementById('kpi-progress').textContent = `${progress}%`;
    document.getElementById('kpi-progress-bar').style.width = `${progress}%`;

    // 2. Banner de Sobrevivência Financeira
    const banner = document.getElementById('survival-banner');
    const bTitle = document.getElementById('survival-status-title');
    const bDesc = document.getElementById('survival-status-desc');

    const sStatus = survival.status || fin.survival_status || 'DEFICIT';
    banner.className = 'banner ' + (sStatus === 'HEALTHY' ? 'banner-healthy' : (sStatus === 'EQUILIBRIUM' ? 'banner-equilibrium' : 'banner-deficit'));

    if (sStatus === 'HEALTHY') {
        bTitle.textContent = '✅ NEGÓCIO AUTOSSUSTENTÁVEL (META DE R$ 300 ATINGIDA)';
    } else if (sStatus === 'EQUILIBRIUM') {
        bTitle.textContent = '⚖️ PONTO DE EQUILÍBRIO (BREAKEVEN DE R$ 200 COBERTO)';
    } else {
        bTitle.textContent = '🚨 PROTOCOLO DE SOBREVIVÊNCIA FINANCEIRA ATIVADO';
    }
    bDesc.textContent = survival.recovery_plan || 'Nenhum plano gerado ainda. Execute um ciclo de auditoria contábil.';

    // 3. Agentes
    const agentsGrid = document.getElementById('agents-grid');
    agentsGrid.innerHTML = '';
    document.getElementById('agents-count').textContent = `${agents.length} Agentes Ativos`;

    agents.forEach(a => {
        const card = document.createElement('div');
        card.className = 'agent-card';
        const badgeClass = a.status === 'WORKING' ? 'badge-working' : (a.status === 'AUDITING' ? 'badge-warning' : 'badge-idle');
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="agent-name">${a.name}</span>
                <span class="badge ${badgeClass}">${a.status}</span>
            </div>
            <div class="agent-role">${a.role}</div>
            <div style="font-size:0.75rem; color:#64748b;">Tarefa: ${a.current_task_id || 'Aguardando ordens'}</div>
        `;
        agentsGrid.appendChild(card);
    });

    // 4. Produtos e Aprovação Humana
    const pTbody = document.getElementById('products-tbody');
    pTbody.innerHTML = '';
    const waitingCount = products.filter(p => p.status === 'WAITING_HUMAN_APPROVAL').length;
    document.getElementById('products-waiting-badge').textContent = `${waitingCount} Aguardando Aprovação`;

    if (products.length === 0) {
        pTbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum produto gerado ainda. Clique em "Executar Ciclo Autônomo" acima.</td></tr>';
    } else {
        products.forEach(p => {
            const tr = document.createElement('tr');
            let statusBadge = 'badge-idle';
            if (p.status === 'APPROVED') statusBadge = 'badge-success';
            else if (p.status === 'WAITING_HUMAN_APPROVAL') statusBadge = 'badge-warning';
            else if (p.status === 'REJECTED') statusBadge = 'badge-danger';

            let actionHtml = `
                <button class="btn btn-sm btn-outline" onclick="previewProduct('${p.id}')">👁️ Ver Ativo</button>
            `;

            if (p.status === 'WAITING_HUMAN_APPROVAL') {
                actionHtml += `
                    <button class="btn btn-sm btn-secondary" onclick="approveProduct('${p.id}')">✅ Aprovar</button>
                    <button class="btn btn-sm btn-danger" onclick="rejectProduct('${p.id}')">❌ Rejeitar</button>
                `;
            }

            tr.innerHTML = `
                <td><strong>${p.product_type}</strong><br><small class="text-muted">${p.id}</small></td>
                <td><strong>${p.title}</strong><br><small class="text-muted">${p.content_summary || ''}</small></td>
                <td>R$ ${p.price.toFixed(2)}</td>
                <td><span class="badge ${p.quality_score >= 80 ? 'badge-success' : 'badge-warning'}">${p.quality_score}/100</span></td>
                <td><span class="badge ${statusBadge}">${p.status}</span></td>
                <td style="display:flex; gap:6px; flex-wrap:wrap;">${actionHtml}</td>
            `;
            pTbody.appendChild(tr);
        });
    }

    // 4.1 Calendário de Facebook (Agente 8)
    const fbGrid = document.getElementById('fb-calendar-grid');
    if (fbGrid) {
        fbGrid.innerHTML = '';
        const fbCal = data.facebook_calendar || [];
        const countBadge = document.getElementById('fb-posts-count');
        if (countBadge) countBadge.textContent = `${fbCal.length} Posts Prontos`;
        fbCal.forEach(post => {
            const card = document.createElement('div');
            card.className = 'fb-card';
            card.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="badge badge-info">${post.dia}</span>
                    <span style="font-size:0.75rem; color:#94a3b8;">🕒 ${post.horario_recomendado}</span>
                </div>
                <div style="font-weight:700; font-size:0.92rem; margin:4px 0 8px; color:#38bdf8;">${post.titulo}</div>
                <textarea class="fb-copy-textarea" id="copy-${post.dia}" readonly>${post.copy}</textarea>
                <div style="font-size:0.75rem; color:#64748b; margin-top:6px;"><strong>Arte:</strong> ${post.sugestao_visual}</div>
                <button class="btn btn-sm btn-secondary" style="margin-top:10px; width:100%; justify-content:center;" onclick="copyPostCopy('${post.dia}')">📋 Copiar Post do ${post.dia}</button>
            `;
            fbGrid.appendChild(card);
        });
    }

    // 4.2 Ideias Estratégicas (Agente 7)
    const ideasGrid = document.getElementById('ideas-grid');
    if (ideasGrid) {
        ideasGrid.innerHTML = '';
        const ideas = data.strategic_ideas || [];
        const ideasBadge = document.getElementById('ideas-count');
        if (ideasBadge) ideasBadge.textContent = `${ideas.length} Ideias de Escala`;
        ideas.forEach(idea => {
            const card = document.createElement('div');
            card.className = 'idea-card';
            card.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span class="badge badge-warning">${idea.category}</span>
                    <span style="font-size:0.72rem; color:#10b981; font-weight:700;">⚡ ${idea.impact}</span>
                </div>
                <div style="font-weight:700; font-size:0.92rem; margin:4px 0; color:#f8fafc;">${idea.title}</div>
                <p style="font-size:0.82rem; color:#94a3b8; line-height:1.4;">${idea.description}</p>
                <div style="font-size:0.72rem; color:#64748b; margin-top:6px;">Esforço: ${idea.effort}</div>
            `;
            ideasGrid.appendChild(card);
        });
    }

    // 5. Oportunidades
    const oppList = document.getElementById('opportunities-list');
    oppList.innerHTML = '';
    if (opps.length === 0) {
        oppList.innerHTML = '<p class="text-muted">Nenhuma oportunidade registrada ainda.</p>';
    } else {
        opps.forEach(o => {
            const item = document.createElement('div');
            item.className = 'list-item';
            item.innerHTML = `
                <div class="list-item-title">${o.title} <span class="badge badge-info" style="font-size:0.65rem;">${o.niche}</span></div>
                <div class="list-item-sub"><strong>Dor:</strong> ${o.problem_to_solve}</div>
                <div class="list-item-sub">Demanda: <strong>${o.estimated_demand}</strong> | Preço Sugerido: <strong>R$ ${o.suggested_price.toFixed(2)}</strong></div>
            `;
            oppList.appendChild(item);
        });
    }

    // 6. Tarefas Recentes
    const tList = document.getElementById('tasks-list');
    tList.innerHTML = '';
    if (tasks.length === 0) {
        tList.innerHTML = '<p class="text-muted">Nenhuma tarefa executada ainda.</p>';
    } else {
        tasks.forEach(t => {
            const item = document.createElement('div');
            item.className = 'list-item';
            const badgeClass = t.status === 'COMPLETED' ? 'badge-success' : 'badge-warning';
            item.innerHTML = `
                <div style="display:flex; justify-content:space-between;">
                    <span class="list-item-title">${t.title}</span>
                    <span class="badge ${badgeClass}">${t.status}</span>
                </div>
                <div class="list-item-sub">Responsável: <strong>${t.assigned_to}</strong> | Prioridade: P${t.priority}</div>
            `;
            tList.appendChild(item);
        });
    }

    // 7. Livro Caixa
    const txTbody = document.getElementById('transactions-tbody');
    txTbody.innerHTML = '';
    if (transactions.length === 0) {
        txTbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Nenhuma transação contábil registrada.</td></tr>';
    } else {
        transactions.slice(0, 8).forEach(tx => {
            const tr = document.createElement('tr');
            const isRev = tx.type === 'REVENUE';
            let tagBadge = tx.status === 'REALIZED' ? 'badge-success' : (tx.status === 'PENDING' ? 'badge-warning' : 'badge-info');
            tr.innerHTML = `
                <td><span class="badge ${isRev ? 'badge-success' : 'badge-danger'}">${tx.type}</span></td>
                <td>${tx.description}</td>
                <td class="${isRev ? 'text-green' : 'text-red'}"><strong>R$ ${tx.amount.toFixed(2)}</strong></td>
                <td><span class="badge ${tagBadge}">${tx.status}</span></td>
            `;
            txTbody.appendChild(tr);
        });
    }

    // 8. Trilha de Auditoria
    const aTbody = document.getElementById('audit-table');
    aTbody.innerHTML = '';
    if (auditLogs.length === 0) {
        aTbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Nenhum evento registrado.</td></tr>';
    } else {
        auditLogs.slice(0, 8).forEach(log => {
            const tr = document.createElement('tr');
            let sBadge = 'badge-idle';
            if (log.severity === 'SUCCESS') sBadge = 'badge-success';
            else if (log.severity === 'WARNING') sBadge = 'badge-warning';
            else if (log.severity === 'ERROR') sBadge = 'badge-danger';
            else if (log.severity === 'INFO') sBadge = 'badge-info';

            tr.innerHTML = `
                <td><strong>${log.agent_name}</strong></td>
                <td><span class="badge ${sBadge}">${log.severity}</span></td>
                <td style="font-size:0.8rem;">${log.message}</td>
            `;
            aTbody.appendChild(tr);
        });
    }
}

// Ações do Usuário
async function toggleAutonomousLoop() {
    const action = isLoopRunning ? 'stop_loop' : 'start_loop';
    const btn = document.getElementById('btn-auto-loop');
    if (btn) btn.innerHTML = '⏳ Alterando modo...';
    try {
        const res = await fetch(`/api/action/${action}`, { method: 'POST' });
        await fetchStatus();
    } catch (e) {
        alert('Erro ao alterar modo autônomo: ' + e.message);
    }
}

async function runAutonomousCycle() {
    const btn = document.getElementById('btn-run-cycle');
    btn.disabled = true;
    btn.textContent = '⏳ Executando Ciclo...';
    try {
        const res = await fetch('/api/action/run_cycle', { method: 'POST' });
        const result = await res.json();
        console.log('Ciclo autônomo concluído:', result);
        await fetchStatus();
    } catch (e) {
        console.error('Erro ao executar ciclo autônomo:', e);
    } finally {
        btn.disabled = false;
        btn.textContent = '⚡ Executar Ciclo Autônomo';
    }
}

async function approveProduct(id) {
    if (!confirm('Deseja realmente APROVAR este produto digital para o catálogo?')) return;
    try {
        const res = await fetch('/api/action/approve', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product_id: id })
        });
        await fetchStatus();
    } catch (e) {
        alert('Erro ao aprovar produto: ' + e.message);
    }
}

async function rejectProduct(id) {
    const reason = prompt('Informe o motivo da rejeição:');
    if (!reason) return;
    try {
        const res = await fetch('/api/action/reject', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product_id: id, reason: reason })
        });
        await fetchStatus();
    } catch (e) {
        alert('Erro ao rejeitar produto: ' + e.message);
    }
}

async function previewProduct(id) {
    try {
        const res = await fetch(`/api/product_preview?id=${id}`);
        const data = await res.json();
        document.getElementById('preview-title').textContent = `${data.title} (${data.product_type})`;
        document.getElementById('preview-content').textContent = data.file_content || 'Arquivo não encontrado.';
        document.getElementById('modal-preview').classList.add('active');
    } catch (e) {
        alert('Erro ao carregar pré-visualização: ' + e.message);
    }
}

function closePreviewModal() {
    document.getElementById('modal-preview').classList.remove('active');
}

// Modais Financeiros
function openSaleModal() { document.getElementById('modal-sale').classList.add('active'); }
function closeSaleModal() { document.getElementById('modal-sale').classList.remove('active'); }

async function submitRealSale() {
    const amount = parseFloat(document.getElementById('sale-amount').value);
    const desc = document.getElementById('sale-desc').value.trim();
    if (!amount || amount <= 0 || !desc) {
        alert('Preencha um valor válido e a descrição da venda recebida.');
        return;
    }
    try {
        await fetch('/api/action/sale', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ amount, description: desc })
        });
        closeSaleModal();
        document.getElementById('sale-amount').value = '';
        document.getElementById('sale-desc').value = '';
        await fetchStatus();
    } catch (e) {
        alert('Erro ao registrar venda: ' + e.message);
    }
}

function openExpenseModal() { document.getElementById('modal-expense').classList.add('active'); }
function closeExpenseModal() { document.getElementById('modal-expense').classList.remove('active'); }

async function submitRealExpense() {
    const amount = parseFloat(document.getElementById('expense-amount').value);
    const desc = document.getElementById('expense-desc').value.trim();
    if (!amount || amount <= 0 || !desc) {
        alert('Preencha um valor válido e a descrição da despesa paga.');
        return;
    }
    try {
        await fetch('/api/action/expense', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ amount, description: desc })
        });
        closeExpenseModal();
        document.getElementById('expense-amount').value = '';
        document.getElementById('expense-desc').value = '';
        await fetchStatus();
    } catch (e) {
        alert('Erro ao registrar despesa: ' + e.message);
    }
}

async function triggerSurvivalCheck() {
    try {
        await fetch('/api/action/survival_check', { method: 'POST' });
        await fetchStatus();
    } catch (e) {
        console.error(e);
    }
}

function copyPostCopy(day) {
    const el = document.getElementById(`copy-${day}`);
    if (el) {
        el.select();
        navigator.clipboard.writeText(el.value).then(() => {
            alert(`Texto do post de ${day} copiado para a área de transferência! Pronto para colar no Facebook.`);
        }).catch(() => {
            document.execCommand('copy');
            alert(`Texto do post de ${day} copiado!`);
        });
    }
}

// Inicialização e Polling a cada 5 segundos
fetchStatus();
setInterval(fetchStatus, 5000);
