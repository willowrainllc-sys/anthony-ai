/* 🔱 OBSIDIAN AURA ENGINE v1.1 */
/* Handles global 4K background loops, random popups, and smart hints */

const ST_CHARLES_VIDEO = "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175";

const AURA_OFFERS = [
    { label: '.COM SALE', price: '$0.01', url: 'obsidian_domains.html', img: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=200' },
    { label: 'START LLC', price: '$39', url: 'obsidian_llc_formation.html', img: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=200' },
    { label: 'VPS CLOUD', price: '$8.99', url: 'obsidian_vps_hosting.html', img: 'https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=200' },
    { label: 'LEO AI PRO', price: '$24.99', url: 'obsidian_leo_builder.html', img: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=200' }
];

const AURA_HINTS = {
    "domainSearch": "Empire Tip: Register .com, .ai, and .city to lock down your brand territory.",
    "sharingToggle": "Director's Pulse: Keep sharing active to earn credits while you sleep.",
    "custEmail": "Safe Harbor: Your digital assets will be provisioned to this verified address.",
    "leo_builder": "Leo Logic: Describe your app, and our AI constructs the full stack in 60s."
};

/**
 * 🔱 AURA VIDEO INITIALIZER
 */
async function initAuraVideo() {
    // 1. Force Body Transparency to show video
    document.body.style.backgroundColor = 'transparent';

    // 2. Create Video Infrastructure
    const container = document.createElement('div');
    container.className = 'aura-video-container';

    const video = document.createElement('video');
    video.className = 'aura-video-element';
    video.autoplay = true;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.style.opacity = '0'; // Start hidden for fade-in

    const overlay = document.createElement('div');
    overlay.className = 'aura-video-overlay';

    container.appendChild(video);
    container.appendChild(overlay);
    document.body.appendChild(container); // Append to back

    // 3. Select Theme Video
    let videoUrl = ST_CHARLES_VIDEO; // Default: High-Aura St. Charles

    try {
        const page = window.location.pathname.split('/').pop() || 'index';
        if (page !== 'index.html' && page !== '') {
            // Try fetching specific context video from Pexels for sub-pages
            const resp = await fetch(`/api/aura/video?query=${page}+tech+blue`);
            const data = await resp.json();
            if (data.success) videoUrl = data.url;
        }
    } catch (e) { console.warn("[AURA] API offline, using St. Charles Master Loop."); }

    // 4. Load & Play
    video.src = videoUrl;
    video.onloadeddata = () => {
        video.style.opacity = '0.7';
        const playPromise = video.play();
        if (playPromise !== undefined) {
            playPromise.catch(() => {
                // Handle Autoplay Block
                const unlock = () => {
                    video.play();
                    document.removeEventListener('mousedown', unlock);
                };
                document.addEventListener('mousedown', unlock, { once: true });
            });
        }
    };
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
            <span class="aura-ad-label">${offer.label}</span>
            <span class="aura-ad-price">${offer.price}</span>
        </div>
    `;
    ad.onclick = () => { window.location.href = offer.url; };
    document.body.appendChild(ad);
    setTimeout(() => {
        ad.style.opacity = '0';
        setTimeout(() => ad.remove(), 500);
    }, 12000);
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

            if (getComputedStyle(el.parentElement).position === 'static') {
                el.parentElement.style.position = 'relative';
            }
            el.parentElement.appendChild(btn);
            btn.style.top = '-10px';
            btn.style.right = '-10px';

            btn.onmouseenter = () => {
                card.innerHTML = `<div class="text-[10px] font-black text-blue-600 uppercase mb-2">Director's Insight</div><p class="text-slate-700 text-xs font-medium">${AURA_HINTS[id]}</p>`;
                card.style.display = 'block';
            };
            btn.onmouseleave = () => { card.style.display = 'none'; };
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    initAuraVideo();
    initHints();
    setInterval(spawnAuraAd, 20000);
});
