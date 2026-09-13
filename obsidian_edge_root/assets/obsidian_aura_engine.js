/* 🔱 OBSIDIAN AURA ENGINE v1.2 */
/* Dynamic 4K Video Backgrounds with Real People & Monetization Hub */

const FALLBACK_VIDEO = "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175";

const AURA_OFFERS = [
    { label: '.COM EXCLUSIVE', price: '$14.70', url: 'obsidian_domains.html', img: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=300' },
    { label: 'DELAWARE LLC', price: '$39.00', url: 'obsidian_llc_formation.html', img: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=300' },
    { label: 'GLOBAL MESH', price: 'EARN $', url: 'obsidian_data_sharing.html', img: 'https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=300' },
    { label: 'LEO AI BUILDER', price: 'FREE', url: 'obsidian_leo_builder.html', img: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=300' }
];

/**
 * 🔱 INJECT ADSENSE CONTAINERS
 */
function injectMonetization() {
    const sections = document.querySelectorAll('section');
    if (sections.length > 2) {
        const adContainer = document.createElement('div');
        adContainer.className = 'obsidian-ad-banner aura-fade-up';
        adContainer.innerHTML = `
            <div class="obsidian-ad-label">Advertisement</div>
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-OBSIDIAN_GLOBAL_ADSENSE"
                 data-ad-slot="AUTO_GENERATED"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
        `;
        sections[1].after(adContainer);
        (window.adsbygoogle = window.adsbygoogle || []).push({});
    }
}

/**
 * 🔱 INITIALIZE VIDEO REEL (Horizontal Background)
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

    const overlay = document.createElement('div');
    overlay.className = 'aura-video-overlay';

    container.appendChild(video);
    container.appendChild(overlay);
    document.body.prepend(container);

    try {
        // Search specifically for real people doing professional work/lifestyle
        const page = window.location.pathname.split('/').pop() || 'business';
        const query = `${page} people working office tech blue`;
        const resp = await fetch(`/api/aura/video?query=${encodeURIComponent(query)}`);
        const data = await resp.json();

        video.src = data.success ? data.url : FALLBACK_VIDEO;
    } catch (e) {
        video.src = FALLBACK_VIDEO;
    }

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
    setTimeout(() => {
        ad.style.opacity = '0';
        setTimeout(() => ad.remove(), 500);
    }, 12000);
}

function handleScrollAnimations() {
    const observers = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entries[0].isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
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
    setInterval(spawnAuraAd, 25000);
});
