/* 🔱 OBSIDIAN GLOBAL: HYPER FRAME RUNTIME v1.0 */
(function() {
    function initHyperFrame() {
        const frameHTML = `
            <div id="hyper-frame-container">
                <div class="hf-corner hf-tl"><span class="hf-label">INGRESS_ACTIVE</span></div>
                <div class="hf-corner hf-tr"><span class="hf-label">GRID_SECURE</span></div>
                <div class="hf-corner hf-bl"><span class="hf-label">MAESTAS_ROOT</span></div>
                <div class="hf-corner hf-br"><span class="hf-label">v29.0_TITAN</span></div>
                <div class="hf-scanning-line"></div>
                <div class="hf-pulse"><div class="hf-dot"></div> LIVE_SYNC</div>
                <div class="hf-vitals">
                    <div>HUB: <span id="hf-nodes">USA_CENTRAL</span></div>
                    <div>AURA: <span id="hf-aura">100%</span></div>
                    <div>SIGINT: <span id="hf-sigint">ACTIVE</span></div>
                </div>
            </div>
        `;

        const div = document.createElement('div');
        div.innerHTML = frameHTML;
        document.body.appendChild(div.firstElementChild);

        // Dynamic Vitals Update
        setInterval(() => {
            const nodes = 100 + Math.floor(Math.random() * 5);
            const aura = 98 + Math.floor(Math.random() * 3);
            const nodesEl = document.getElementById('hf-nodes');
            const auraEl = document.getElementById('hf-aura');
            if(nodesEl) nodesEl.innerText = nodes;
            if(auraEl) auraEl.innerText = aura + "%";
        }, 5000);
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        initHyperFrame();
    } else {
        document.addEventListener('DOMContentLoaded', initHyperFrame);
    }
})();
