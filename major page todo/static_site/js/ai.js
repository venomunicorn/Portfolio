
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('products-container');
    const searchInput = document.getElementById('search-input');

    const data = await fetchData('ai_products.json');

    if (!data) {
        container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--color-red);">Failed to load products data.</div>';
        return;
    }

    // Sort by rank
    const products = data.sort((a, b) => a.rank - b.rank);
    let searchQuery = '';

    function render() {
        const filtered = products.filter(p =>
            p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            p.description.toLowerCase().includes(searchQuery.toLowerCase())
        );

        // Icons
        const BrainCircuit = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.97-3.284"/><path d="M17.97 14.716A4 4 0 0 1 18 18"/></svg>';
        const DollarSign = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>';
        const Activity = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>';
        const Clock = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';

        if (filtered.length === 0) {
            container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); padding: 2rem;">No products found.</div>';
            return;
        }

        container.innerHTML = filtered.map(product => {
            const complexityClass = product.complexity === 'High' ? 'complexity-high' :
                product.complexity === 'Medium' ? 'complexity-medium' : 'complexity-low';

            return `
                <div class="product-card">
                    <div class="card-header">
                        <div class="icon-box">
                            ${BrainCircuit}
                        </div>
                        <div style="display: flex; flex-direction: column; align-items: flex-end;">
                            <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-family: monospace; margin-bottom: 0.25rem;">Rank</span>
                            <span class="rank-badge">#${product.rank}</span>
                        </div>
                    </div>

                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-desc">${product.description}</p>

                    <div class="metrics">
                        <div class="metric-row">
                            <span class="metric-label">${DollarSign} Revenue</span>
                            <span class="metric-value">${product.revenue}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">${Activity} Complexity</span>
                            <span class="metric-value ${complexityClass}">${product.complexity}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">${Clock} Time to MVP</span>
                            <span class="metric-value">${product.timeToMvp}</span>
                        </div>
                    </div>

                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                        <div class="score-bar-bg">
                            <div class="score-bar-fill" style="width: ${(product.score / 10) * 100}%"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 0.25rem;">
                            <span style="font-size: 0.625rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">Viability Score</span>
                            <span style="font-size: 0.75rem; font-weight: 700; color: var(--color-emerald);">${product.score}/10</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        render();
    });

    render();
});
