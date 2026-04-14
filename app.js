document.addEventListener('DOMContentLoaded', () => {
  const subBtn = document.getElementById('subscribe-btn');
  const subBtnPremium = document.getElementById('subscribe-premium-btn');

  if (subBtn) {
    subBtn.addEventListener('click', () => {
      // Plus tard : appeler une fonction serveless (Netlify / Cloudflare Pages) qui renvoie vers Stripe Checkout
      alert("Bientôt : intégration Stripe. Tu peux tester l’interface.");
    });
  }

  if (subBtnPremium) {
    subBtnPremium.addEventListener('click', () => {
      alert("Bientôt : abonnement Premium via Stripe.");
    });
  }
});
