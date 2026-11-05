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

// === 弹窗（从 applezhanghao.github.io 移植）===
(function () {
  const popupOverlay = document.getElementById('popupOverlay');
  if (!popupOverlay) return;

  // 页面解析完后先渲染网页，再延迟弹出
  window.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
      popupOverlay.classList.add('show');
    }, 300);
  });

  // 点击遮罩层不关闭（强制引导），如需点击遮罩关闭可取消下面注释
  /*
  popupOverlay.addEventListener('click', function (e) {
    if (e.target === popupOverlay) {
      popupOverlay.classList.remove('show');
    }
  });
  */
})();
