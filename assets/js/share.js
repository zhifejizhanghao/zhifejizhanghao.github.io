(function () {
  const toast = document.querySelector('[data-toast]');
  const notify = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('visible');
    window.setTimeout(() => toast.classList.remove('visible'), 3000);
  };
  const SHOP_URL = 'https://shop.xinkonyun.cc/';
  document.querySelectorAll('[data-buy]').forEach((button) => {
    button.addEventListener('click', () => {
      window.open(SHOP_URL, '_blank', 'noopener');
    });
  });
  document.querySelectorAll('[data-copy-link]').forEach((button) => {
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(window.location.href); notify('链接已复制。'); }
      catch (_) { notify('请复制浏览器地址栏中的当前链接。'); }
    });
  });
  document.querySelectorAll('[data-share-page]').forEach((button) => {
    button.addEventListener('click', async () => {
      try {
        await navigator.share({ title: document.title, url: window.location.href });
      } catch (_) {
        notify('当前浏览器不支持系统分享，请复制地址栏链接。');
      }
    });
  });
})();
