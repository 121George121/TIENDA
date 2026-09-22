// ==============================================================================
// CONFIGURACIÓN DE PRODUCCIÓN - SHOPYN GOLDEN STORE
// Proyecto: ECOMMERCE_TIENDA (Angular SPA)
// ==============================================================================

export const environment = {
  production: true,
  // URL base del backend en Railway en producción.
  // Permite sobreescritura dinámica si se guarda 'API_URL' en localStorage o window.__API_URL__
  get apiUrl(): string {
    if (typeof window !== 'undefined') {
      const customApi = localStorage.getItem('API_URL') || (window as any).__API_URL__;
      if (customApi) return customApi;
    }
    // Reemplaza con tu dominio generado en Railway (ejemplo: https://shopyn-api-production.up.railway.app/api/v1)
    return 'https://web-production-shopyn.up.railway.app/api/v1';
  }
};
