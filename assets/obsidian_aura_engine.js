/* 🔱 OBSIDIAN AURA ENGINE v1.3 */
/* Integrated Leo Chat Agent + Dynamic 4K Backgrounds + Monetization */

const FALLBACK_VIDEO = "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175";

const AURA_OFFERS = [
    { label: '.COM EXCLUSIVE', price: '$14.70', url: 'obsidian_domains.html', img: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=300' },
    { label: 'DELAWARE LLC', price: '$39.00', url: 'obsidian_llc_formation.html', img: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=300' },
    { label: 'GLOBAL MESH', price: 'EARN $', url: 'obsidian_data_sharing.html', img: 'https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=300' },
    { label: 'LEO AI BUILDER', price: 'FREE', url: 'obsidian_leo_builder.html', img: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=300' }
];

/**
 * 🔱 LEO CHAT AGENT UI
 */
function initLeoChat() {
    // 1. Create Floating Trigger
    const trigger = document.createElement('div');
    trigger.className = 'leo-chat-trigger';
    trigger.innerHTML = '🤖';
    trigger.onclick = toggleLeoChat;
    document.body.appendChild(trigger);

    // 2. Create Chat Window
    const win = document.createElement('div');
    win.id = 'leoChatWindow';
    win.className = 'leo-chat-window';
    win.innerHTML = `
        <div class="chat-header">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-sm">🤖</div>
                <div>
                    <div class="text-[11px] font-black text-white uppercase tracking-widest">Obsidian Leo™</div>
                    <div class="text-[8px] text-emerald-400 font-bold uppercase">Enterprise AI Node Active</div>
                </div>
            </div>
            <button onclick="toggleLeoChat()" class="text-gray-500 hover:text-white text-xl">&times;</button>
        </div>
        <div class="chat-body" id="leoChatBody">
            <div class="msg msg-leo">Greetings. I am Leo, your AI Business Assistant. How can I assist your business growth today?</div>
        </div>
        <div class="chat-footer">
            <input type="text" id="leoChatInput" class="chat-input" placeholder="Ask Leo anything..." onkeypress="handleChatKey(event)">
        </div>
    `;
    document.body.appendChild(win);
}

function toggleLeoChat() {
    const win = document.getElementById('leoChatWindow');
    const isVisible = win.style.display === 'flex';
    win.style.display = isVisible ? 'none' : 'flex';
}

async function handleChatKey(e) {
    if (e.key === 'Enter') {
        const input = document.getElementById('leoChatInput');
        const text = input.value.trim();
        if (!text) return;

        appendMessage('user', text);
        input.value = '';

        try {
            const resp = await fetch('/api/leo/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text, page: window.location.pathname })
            });
            const data = await resp.json();
            appendMessage('leo', data.reply);
        } catch (err) {
            appendMessage('leo', "My uplink to the ARES core is currently throttled. Please try again or contact tech support at willow.rain.llc@gmail.com.");
        }
    }
}

function appendMessage(role, text) {
    const body = document.getElementById('leoChatBody');
    const msg = document.createElement('div');
    msg.className = `msg msg-${role}`;
    msg.innerText = text;
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
}

/**
 * 🔱 INJECT MONETIZATION
 */
function injectMonetization() {
    const sections = document.querySelectorAll('section');
    if (sections.length > 2) {
        const adContainer = document.createElement('div');
        adContainer.className = 'obsidian-ad-banner aura-fade-up';
        adContainer.innerHTML = `
            <div class="obsidian-ad-label">Advertisement</div>
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-OBSIDIAN_GLOBAL_ADSENSE" data-ad-slot="AUTO_GENERATED" data-ad-format="auto" data-full-width-responsive="true"></ins>
        `;
        sections[1].after(adContainer);
        (window.adsbygoogle = window.adsbygoogle || []).push({});
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
        const resp = await fetch(`/api/aura/video?query=${encodeURIComponent(page + ' people office tech blue')}`);
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

window.addEventListener('DOMContentLoaded', () => {
    initAuraVideo();
    injectMonetization();
    handleScrollAnimations();
    initLeoChat();
    setInterval(spawnAuraAd, 25000);
});
