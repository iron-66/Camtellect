document.addEventListener('DOMContentLoaded', () => {
  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  const revealables = document.querySelectorAll('.reveal');
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealables.forEach((el) => {
      el.classList.add('is-visible');
    });
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.2,
    }
  );

  revealables.forEach((el) => observer.observe(el));

  const modal = document.getElementById('downloadModal');
  const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
  const modalClose = modal?.querySelector('.modal-close');
  const modalWindow = modal?.querySelector('.modal-window');

  const closeModal = () => {
    if (!modal) return;
    modal.classList.remove('is-visible');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
  };

  const openModal = () => {
    if (!modal) return;
    modal.classList.add('is-visible');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
  };

  modalTriggers.forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      openModal();
    });
  });

  modal?.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });
  modalWindow?.addEventListener('click', (event) => event.stopPropagation());
  modalClose?.addEventListener('click', closeModal);
});
