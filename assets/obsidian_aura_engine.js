/* 🔱 OBSIDIAN AURA ENGINE v1.3 */
/* Integrated Obsidian AI Chat Agent + Dynamic 4K Backgrounds + Monetization */

const FALLBACK_VIDEO = "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175";

const AURA_OFFERS = [
    { label: '.COM EXCLUSIVE', price: '$14.70', url: 'obsidian_domains.html', img: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=300' },
    { label: 'DELAWARE LLC', price: '$39.00', url: 'obsidian_llc_formation.html', img: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=300' },
    { label: 'GLOBAL MESH', price: 'EARN $', url: 'obsidian_data_sharing.html', img: 'https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=300' },
    { label: 'LEO AI BUILDER', price: 'FREE', url: 'obsidian_obsidian_ai_builder.html', img: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=300' }
];

/**
 * 🔱 AURA API HELPER:
 * Automatically resolves endpoint based on environment (Local File vs Server).
 */
function getApiUrl(endpoint) {
    const isLocalFile = window.location.protocol === 'file:';
    const base = isLocalFile ? 'http://localhost:8080' : '';
    return base + endpoint;
}


/**
 * 🔱 LEO CHAT AGENT UI
 */
function initObsidianAIChat() {
    // 1. Create Floating Trigger
    const trigger = document.createElement('div');
    trigger.className = 'obsidian_ai-chat-trigger';
    // 🔱 High-Aura "Godfather" Thumbnail Mascot
    trigger.innerHTML = `<img src="https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=100&h=100&auto=format&fit=crop" style="width:100%; height:100%; border-radius:50%; object-fit:cover; border: 2px solid #3b82f6; box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);">`;
    trigger.onclick = toggleObsidianAIChat;
    document.body.appendChild(trigger);

    // 2. Create Chat Window
    const win = document.createElement('div');
    win.id = 'obsidian_aiChatWindow';
    win.className = 'obsidian_ai-chat-window';
    win.innerHTML = `
        <div class="chat-header">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-sm">🤖</div>
                <div>
                    <div class="text-[11px] font-black text-white uppercase tracking-widest">Obsidian AI</div>
                    <div class="text-[8px] text-emerald-400 font-bold uppercase">Enterprise AI Node Active</div>
                </div>
            </div>
            <button onclick="toggleObsidianAIChat()" class="text-gray-500 hover:text-white text-xl">&times;</button>
        </div>
        <div class="chat-body" id="obsidian_aiChatBody">
            <div class="msg msg-obsidian_ai">Greetings. I am Obsidian AI, your AI Business Assistant. How can I assist your business growth today?</div>
        </div>
        <div class="chat-footer">
            <input type="text" id="obsidian_aiChatInput" class="chat-input" placeholder="Ask Obsidian AI anything..." onkeypress="handleChatKey(event)">
        </div>
    `;
    document.body.appendChild(win);
}

function toggleObsidianAIChat() {
    const win = document.getElementById('obsidian_aiChatWindow');
    if (!win) return;

    // Using computed style for robustness if inline style is missing
    const currentDisplay = window.getComputedStyle(win).display;
    if (currentDisplay === 'none') {
        win.style.display = 'flex';
        win.classList.add('visible');
    } else {
        win.style.display = 'none';
        win.classList.remove('visible');
    }
}

/**
 * 🔱 AURA HINTS: Tooltip system for key features
 */
const AURA_HINTS = {
    "sharingToggle": "Director's Note: Every GB shared strengthens the Global Mesh and earns you direct credits.",
    "custEmail": "Security First: We use PQC encryption to deliver your assets to this verified inbox."
};

function initHints() {
    const card = document.createElement('div');
    card.className = 'aura-hint-card glass';
    card.id = 'auraHintCard';
    document.body.appendChild(card);

    Object.keys(AURA_HINTS).forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            const btn = document.createElement('div');
            btn.className = 'aura-hint-btn';
            btn.innerText = '?';

            // Adjust position
            btn.style.top = '-12px';
            btn.style.right = '-12px';

            if (getComputedStyle(el.parentElement).position === 'static') {
                el.parentElement.style.position = 'relative';
            }
            el.parentElement.appendChild(btn);

            btn.onmouseenter = () => {
                card.innerHTML = `
                    <div class="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-2">Director's Insight</div>
                    <p class="text-white text-xs font-medium leading-relaxed">${AURA_HINTS[id]}</p>
                `;
                card.style.display = 'block';
            };

            btn.onmouseleave = () => { card.style.display = 'none'; };
        }
    });
}

async function handleChatKey(e) {
    if (e.key === 'Enter') {
        const input = document.getElementById('obsidian_aiChatInput');
        const text = input.value.trim();
        if (!text) return;

        appendMessage('user', text);
        input.value = '';

        try {
            const resp = await fetch(getApiUrl('/api/obsidian_ai/chat'), {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text, page: window.location.pathname })
            });
            const data = await resp.json();
            appendMessage('obsidian_ai', data.reply);
        } catch (err) {
            appendMessage('obsidian_ai', "My uplink to the ARES core is currently throttled. Please ensure the Private Server is running or contact tech support.");
        }
    }
}

function appendMessage(role, text) {
    const body = document.getElementById('obsidian_aiChatBody');
    const msg = document.createElement('div');
    msg.className = `msg msg-${role}`;
    msg.innerText = text;
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
}

/**
 * 🔱 INJECT MONETIZATION (AdSense & Fallbacks)
 */
function injectMonetization() {
    const sections = document.querySelectorAll('section');
    if (sections.length > 2) {
        const adContainer = document.createElement('div');
        adContainer.className = 'obsidian-ad-banner aura-fade-up';

        // Use Empire Fallback if AdSense is pending or blocked
        adContainer.innerHTML = `
            <div class="obsidian-ad-label">Advertisement</div>
            <div id="obsidianAdFallback" class="flex items-center gap-10 px-8 w-full h-full cursor-pointer" onclick="window.location.href='obsidian_llc_formation.html'">
                <div class="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center text-xl">🏛️</div>
                <div>
                    <div class="text-[10px] font-black text-blue-400 uppercase tracking-widest">Empire Partner Offer</div>
                    <div class="text-sm font-black text-white">Form your LLC for $39 + Free Domain. Claim yours today.</div>
                </div>
                <div class="ml-auto bg-white text-black px-4 py-2 rounded-lg font-black text-[10px] uppercase">Claim Offer</div>
            </div>
            <ins class="adsbygoogle" style="display:none" data-ad-client="ca-pub-OBSIDIAN_GLOBAL_ADSENSE" data-ad-slot="AUTO_GENERATED" data-ad-format="auto" data-full-width-responsive="true"></ins>
        `;
        sections[1].after(adContainer);

        // Attempt to load AdSense. If it fails or returns no ads, the fallback remains visible.
        try {
            (window.adsbygoogle = window.adsbygoogle || []).push({});
            // Add a small check: if adsbygoogle has status, we can hide fallback.
        } catch (e) {
            console.warn("[AURA] AdSense handshake delayed. Empire Fallback Active.");
        }
    }
}

/**
 * 🔱 INITIALIZE VIDEO BACKGROUND
 */
async function initAuraVideo() {
    document.body.style.backgroundColor = 'transparent';
    const container = document.createElement('div');
    container.className = 'aura-video-container';

    const video = document.createElement('video');
    video.className = 'aura-video-element';
    video.autoplay = true;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;

    // Reliability Sources
    const sourceVimeo = document.createElement('source');
    sourceVimeo.src = FALLBACK_VIDEO;
    sourceVimeo.type = 'video/mp4';
    video.appendChild(sourceVimeo);

    const overlay = document.createElement('div');
    overlay.className = 'aura-video-overlay';

    container.appendChild(video);
    container.appendChild(overlay);
    document.body.prepend(container);

    try {
        const page = window.location.pathname.split('/').pop() || 'business';
        const resp = await fetch(getApiUrl(`/api/aura/video?query=${encodeURIComponent(page + ' people office tech blue')}`));
        const data = await resp.json();
        if (data.success) {
            const newSource = document.createElement('source');
            newSource.src = data.url;
            newSource.type = 'video/mp4';
            video.prepend(newSource);
            video.load();
        }
    } catch (e) {}
    video.onloadeddata = () => { video.style.opacity = '1'; };
}

/**
 * 🔱 SECURITY PULSE: Floating Hacking & Safety Tips
 */
const SECURITY_TIPS = [
    "Tip: Use hardware security keys (FIDO2) for absolute identity sovereignty.",
    "Fact: 95% of breaches start with phishing. Always verify the sender's origin.",
    "Tip: Enable PQC (Post-Quantum Cryptography) for long-term data protection.",
    "Fact: Public Wi-Fi is a major ingress point for sniffers. Use the Obsidian Mesh.",
    "Tip: Rotate your backend API keys every 90 days to minimize exposure."
];

function spawnSecurityPulse() {
    if (Math.random() > 0.5) return;

    const tip = SECURITY_TIPS[Math.floor(Math.random() * SECURITY_TIPS.length)];
    const pulse = document.createElement('div');
    pulse.className = 'aura-fade-up glass p-6 rounded-2xl fixed bottom-32 left-8 z-[1000000] max-w-xs shadow-2xl';
    pulse.style.background = 'rgba(15, 23, 42, 0.9)';
    pulse.style.border = '1px solid rgba(59, 130, 246, 0.3)';

    pulse.innerHTML = `
        <div class="flex items-center gap-4">
            <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-sm shadow-lg">🛡️</div>
            <div>
                <div class="text-[9px] font-black text-blue-400 uppercase tracking-widest">Security Pulse</div>
                <div class="text-[11px] text-white font-medium leading-tight mt-1">${tip}</div>
            </div>
        </div>
    `;

    document.body.appendChild(pulse);
    setTimeout(() => pulse.classList.add('visible'), 100);

    setTimeout(() => {
        pulse.classList.remove('visible');
        setTimeout(() => pulse.remove(), 800);
    }, 8000);
}

/**
 * 🔱 CONNECTION PULSE: Promoting Social Matrix
 */
function spawnConnectionPulse() {
    if (Math.random() > 0.6) return;

    const connections = [
        { name: "GitHub", url: "https://github.com/willowrainllc-sys", icon: "💻", sub: "Core Repositories" },
        { name: "X / Twitter", url: "https://x.com/willowrainllc", icon: "🐦", sub: "Global Updates" },
        { name: "Discord", url: "https://discord.gg/obsidiancity", icon: "💬", sub: "Join the Mesh" }
    ];

    const conn = connections[Math.floor(Math.random() * connections.length)];
    const pulse = document.createElement('div');
    pulse.className = 'aura-fade-up glass p-6 rounded-2xl fixed bottom-32 right-8 z-[1000000] max-w-xs shadow-2xl cursor-pointer';
    pulse.style.background = 'rgba(37, 99, 235, 0.9)';
    pulse.style.border = '1px solid rgba(255, 255, 255, 0.2)';
    pulse.onclick = () => window.open(conn.url, '_blank');

    pulse.innerHTML = `
        <div class="flex items-center gap-4 text-white">
            <div class="w-8 h-8 bg-black/20 rounded-lg flex items-center justify-center text-sm">${conn.icon}</div>
            <div>
                <div class="text-[9px] font-black uppercase tracking-widest opacity-80">Connection Pulse</div>
                <div class="text-[11px] font-black leading-tight mt-1">${conn.name}: ${conn.sub}</div>
            </div>
        </div>
    `;

    document.body.appendChild(pulse);
    setTimeout(() => pulse.classList.add('visible'), 100);

    setTimeout(() => {
        pulse.classList.remove('visible');
        setTimeout(() => pulse.remove(), 800);
    }, 6000);
}

function spawnAuraAd() {
    if (Math.random() > 0.4) return;
    const offer = AURA_OFFERS[Math.floor(Math.random() * AURA_OFFERS.length)];
    const ad = document.createElement('div');
    ad.className = 'aura-ad-icon';
    ad.style.left = `${Math.random() * (window.innerWidth - 150) + 75}px`;
    ad.style.top = `${Math.random() * (window.innerHeight - 300) + 150}px`;
    ad.innerHTML = `
        <img src="${offer.img}" class="aura-ad-img">
        <div class="aura-ad-info">
            <span class="aura-ad-label-sub">${offer.label}</span>
            <span class="aura-ad-price">${offer.price}</span>
        </div>
    `;
    ad.onclick = () => { window.location.href = offer.url; };
    document.body.appendChild(ad);
    setTimeout(() => { ad.style.opacity = '0'; setTimeout(() => ad.remove(), 500); }, 12000);
}

function handleScrollAnimations() {
    const observers = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
    }, { threshold: 0.1 });
    document.querySelectorAll('.aura-fade-up, .base44-card').forEach(el => {
        el.classList.add('aura-fade-up');
        observers.observe(el);
    });
}

/**
 * 🔱 INJECT NEWS TICKER
 */
function injectNewsTicker() {
    const ticker = document.createElement('div');
    ticker.className = 'obsidian-news-ticker';

    const newsItems = [
        "Obsidian AI builds 1,000th empire node this hour",
        "St. Charles Global HQ confirms 99.9% uptime for Edge Mesh",
        ".COM wholesale prices holding steady at $14.70",
        "New LLC formation protocol reduces state filing time by 40%",
        "ARES strike engine neutralizes 502 Bad Gateway desync"
    ];

    let itemsHtml = '';
    newsItems.forEach(item => {
        itemsHtml += `<div class="news-item"><span class="news-tag">BREAKING</span> ${item}</div>`;
    });

    ticker.innerHTML = `<div class="news-scroll">${itemsHtml}${itemsHtml}</div>`;

    const header = document.querySelector('header');
    if (header) header.after(ticker);
}

/**
 * 🔱 CONTEXTUAL LINK ENGINE (Sovrn/Skimlinks Hybrid)
 * Automatically scans text for brand keywords and injects monetized links.
 */
const BRAND_KEYWORDS = {
    "domain": "obsidian_domains.html",
    "vps": "obsidian_vps_hosting.html",
    "llc": "obsidian_llc_formation.html",
    "ai": "obsidian_ai_builder.html",
    "host": "obsidian_hosting_landing.html"
};

function injectContextualLinks() {
    const paragraphs = document.querySelectorAll('p, li');
    paragraphs.forEach(p => {
        let html = p.innerHTML;
        Object.keys(BRAND_KEYWORDS).forEach(key => {
            const regex = new RegExp(`\\b(${key})\\b`, 'gi');
            html = html.replace(regex, `<a href="${BRAND_KEYWORDS[key]}" class="text-blue-600 font-bold hover:underline">$1</a>`);
        });
        p.innerHTML = html;
    });
}

/**
 * 🔱 INJECT SPONSORED CONTENT (Native Recommendation Widget)
 */
function injectSponsoredContent() {
    const footer = document.querySelector('footer');
    if (!footer) return;

    const grid = document.createElement('div');
    grid.className = 'obsidian-sponsored-grid aura-fade-up';

    const partners = [
        { title: "Scale Your Real Estate Portfolio via Sniping", label: "Obsidian Estates", img: "https://images.unsplash.com/photo-1560518883-ce09059eeffa?q=80&w=400" },
        { title: "Get Industrial Ad Ingress with Ad Burst", label: "Partner Offer", img: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=400" },
        { title: "The Private Guide to Post-Quantum Identity", label: "Empire Reading", img: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=400" }
    ];

    let cardsHtml = '';
    partners.forEach(p => {
        cardsHtml += `
            <div class="sponsored-card" onclick="window.location.href='index.html'">
                <img src="${p.img}" class="sponsored-img" alt="Sponsor">
                <div class="sponsored-info">
                    <span class="sponsored-label">${p.label}</span>
                    <h4 class="sponsored-title">${p.title}</h4>
                </div>
            </div>
        `;
    });

    grid.innerHTML = `
        <div class="w-full mb-10">
            <h3 class="text-xl font-black text-slate-900 tracking-tighter uppercase">Recommended for Your Empire</h3>
        </div>
        ${cardsHtml}
    `;
    footer.before(grid);
}

window.addEventListener('DOMContentLoaded', () => {
    initAuraVideo();
    injectMonetization();
    injectNewsTicker();
    injectSponsoredContent();
    injectContextualLinks();
    handleScrollAnimations();
    initObsidianAIChat();
    initHints();

    // 🔱 Periodic Security & Connection Pulses
    setInterval(spawnSecurityPulse, 30000);
    setInterval(spawnConnectionPulse, 45000);
    setTimeout(spawnSecurityPulse, 5000);
    setTimeout(spawnConnectionPulse, 15000);

    // 🔱 Restricted Ads: Only spawn pop-ups on the Main Storefront
    const page = window.location.pathname.split('/').pop();
    if (page === 'index.html' || page === '') {
        setInterval(spawnAuraAd, 25000);
    }
});
