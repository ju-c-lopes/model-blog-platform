function updateReadingBar() {
    const readingBar = document.getElementById("reading-bar");
    const content = document.querySelector(".post-detail-page .post-content");
    if (!readingBar || !content) return;

    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const windowHeight = document.documentElement.clientHeight;
    const contentTop = content.getBoundingClientRect().top + scrollTop;
    const contentHeight = content.offsetHeight;

    // 0% no topo da página; 100% quando o fim de .post-content alcança o rodapé da viewport.
    const end = Math.max(contentTop + contentHeight - windowHeight, 1);
    const percent = scrollTop >= end ? 100 : (scrollTop / end) * 100;

    readingBar.style.width = `${Math.min(100, Math.max(0, percent))}%`;
}

window.addEventListener("scroll", updateReadingBar, { passive: true });
window.addEventListener("resize", updateReadingBar, { passive: true });
document.addEventListener("DOMContentLoaded", updateReadingBar);
