/* 🔱 OBSIDIAN AURA ENGINE v1.0 */
/* Handles random in-ad popups with authentic imagery and contextual hints */

const AURA_OFFERS = [
    {
        label: '.COM SALE',
        price: '$0.01',
        url: 'obsidian_domains.html',
        img: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=200&h=200&auto=format&fit=crop' // People in office
    },
    {
        label: 'START LLC',
        price: '$39',
        url: 'obsidian_llc_formation.html',
        img: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=200&h=200&auto=format&fit=crop' // Professional man
    },
    {
        label: 'VPS CLOUD',
        price: '$8.99',
        url: 'obsidian_vps_hosting.html',
        img: 'https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=200&h=200&auto=format&fit=crop' // Tech team
    },
    {
        label: 'LEO AI PRO',
        price: '$24.99',
        url: 'obsidian_leo_builder.html',
        img: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=200&h=200&auto=format&fit=crop' // Students working
    },
    {
        label: 'WP HELP',
        price: '$49',
        url: 'obsidian_wordpress_support.html',
        img: 'https://images.unsplash.com/photo-1521791136064-7986c2920216?q=80&w=200&h=200&auto=format&fit=crop' // Handshake
    }
];

const AURA_HINTS = {
    "domainSearch": "Pro Tip: Register multiple extensions (.com, .city, .ai) to protect your brand globally.",
    "sharingToggle": "Director's Note: Every GB shared strengthens the Sovereign Mesh and earns you direct credits.",
    "custEmail": "Security First: We use PQC encryption to deliver your assets to this verified inbox.",
    "leo_builder": "Empire Logic: Describe your business once, and Leo AI generates your landing page, logo, and LLC documents.",
    "searchTermInput": "Global Ingress: Searching across all 1,200+ top-level domain registries simultaneously."
};

function spawnAuraAd() {
    if (Math.random() > 0.4) return; // 40% chance to spawn

    const offer = AURA_OFFERS[Math.floor(Math.random() * AURA_OFFERS.length)];
    const ad = document.createElement('div');
    ad.className = 'aura-ad-icon';

    // Random Position (Safe edges, avoiding top nav and bottom nav)
    const x = Math.random() * (window.innerWidth - 120) + 60;
    const y = Math.random() * (window.innerHeight - 300) + 150;

    ad.style.left = `${x}px`;
    ad.style.top = `${y}px`;

    ad.innerHTML = `
        <img src="${offer.img}" class="aura-ad-img" alt="Offer">
        <div class="aura-ad-info">
            <span class="aura-ad-label">${offer.label}</span>
            <span class="aura-ad-price">${offer.price}</span>
        </div>
    `;

    ad.onclick = () => { window.location.href = offer.url; };

    document.body.appendChild(ad);

    // Auto-remove after 10 seconds with fade
    setTimeout(() => {
        ad.style.opacity = '0';
        ad.style.transform = 'scale(0.5)';
        setTimeout(() => ad.remove(), 500);
    }, 10000);
}

function initHints() {
    const card = document.createElement('div');
    card.className = 'aura-hint-card';
    card.id = 'auraHintCard';
    document.body.appendChild(card);

    Object.keys(AURA_HINTS).forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            const btn = document.createElement('div');
            btn.className = 'aura-hint-btn';
            btn.innerText = '?';

            // Adjust position slightly
            btn.style.top = '-12px';
            btn.style.right = '-12px';

            if (getComputedStyle(el.parentElement).position === 'static') {
                el.parentElement.style.position = 'relative';
            }
            el.parentElement.appendChild(btn);

            btn.onmouseenter = () => {
                card.innerHTML = `
                    <div class="text-[10px] font-black text-blue-600 uppercase tracking-widest mb-2">Director's Insight</div>
                    <p class="text-slate-700 text-xs font-medium leading-relaxed">${AURA_HINTS[id]}</p>
                    <div class="mt-4 pt-4 border-t border-slate-100 text-[8px] text-slate-400 font-bold uppercase">Obsidian City Global Support</div>
                `;
                card.style.display = 'block';
            };

            btn.onmouseleave = () => { card.style.display = 'none'; };
        }
    });
}

/**
 * 🔱 AURA VIDEO PLAYER:
 * Fetches dynamic tech loops from Pexels and applies them as background.
 */
async function initAuraVideo() {
    // 1. Create Container & Overlay
    const container = document.createElement('div');
    container.className = 'aura-video-container';

    const overlay = document.createElement('div');
    overlay.className = 'aura-video-overlay';

    const video = document.createElement('video');
    video.className = 'aura-video-element';
    video.autoplay = true;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;

    container.appendChild(video);
    container.appendChild(overlay);
    document.body.prepend(container);

    try {
        // 2. Fetch High-Aura Content
        const pageType = window.location.pathname.split('/').pop() || 'tech';
        const resp = await fetch(`/api/aura/video?query=${pageType}+abstract+blue`);
        const data = await resp.json();

        if (data.success) {
            video.src = data.url;
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.catch(() => {
                    document.body.addEventListener('click', () => { video.play(); }, { once: true });
                });
            }
        }
    } catch (err) {
        console.warn("[AURA] Video pipeline delayed. Using static grid fallback.");
    }
}

window.addEventListener('DOMContentLoaded', () => {
    initAuraVideo();
    initHints();
    // Spawn ads periodically
    setTimeout(spawnAuraAd, 5000);
    setInterval(spawnAuraAd, 20000);
});
