/* -------------------------------------------------
   motion.js – Editorial Tech Scroll & Reveal Engine
   IntersectionObserver with viewport check & reduced-motion
   ------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) {
        document.querySelectorAll('[data-anim]').forEach(el => el.classList.add('visible'));
        return;
    }

    document.documentElement.classList.add('js-motion-active');

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                obs.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px'
    });

    document.querySelectorAll('[data-anim]').forEach(el => {
        const type = el.dataset.anim || 'fade-up';
        el.classList.add('anim', 'anim-' + type);
        
        // If element is already in viewport, show immediately
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            el.classList.add('visible');
        } else {
            observer.observe(el);
        }
    });

    /* Sticky topbar background on scroll */
    const topbar = document.getElementById('topbar');
    if (topbar) {
        window.addEventListener('scroll', () => {
            topbar.classList.toggle('scrolled', window.scrollY > 20);
        }, { passive: true });
    }

    /* Smooth scroll for anchors */
    document.querySelectorAll('.scroll-link').forEach(link => {
        link.addEventListener('click', e => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});
