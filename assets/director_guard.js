/* [+] OBSIDIAN DIRECTOR GUARD v1.0 */
/* Restricts sensitive pages to Authorized Director Nodes only. */

(function() {
    const sessionData = localStorage.getItem('obsidian_session');
    const session = sessionData ? JSON.parse(sessionData) : {};

    // [+] Authorized Director Emails
    const directors = ["google_user@obsidian.city", "willow.rain.llc@gmail.com"];
    const email = (session.email || "").toLowerCase();

    const isDirector = directors.includes(email) || email.startsWith("anthony");

    if (!isDirector) {
        console.warn("[ARES] INGRESS DENIED: Unauthorized node attempt on sensitive sector.");
        // Redirect to standard dashboard or home
        window.location.href = 'obsidian_city_dashboard.html';
    } else {
        console.log("[ARES] DIRECTOR IDENTIFIED: Sovereign access granted.");
    }
})();
