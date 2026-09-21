import { Routes } from '@angular/router';

// CU1: Autenticación
import { LoginComponent } from './views/cu1_gestionar_autenticacion/login/login.component';
import { RegisterComponent } from './views/cu1_gestionar_autenticacion/register/register.component';
import { RecoverPasswordComponent } from './views/cu1_gestionar_autenticacion/recover-password.component';
import { ResetPasswordComponent } from './views/cu1_gestionar_autenticacion/reset-password.component';

// Dashboard & Layout
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { AdminLayoutComponent } from './views/layout/admin-layout/admin-layout.component';
import { ClientLayoutComponent } from './views/layout/client-layout/client-layout.component';

// CU2: Usuarios y Roles
import { UserListComponent } from './views/cu2_gestionar_usuarios_roles/users/user-list/user-list.component';
import { RoleListComponent } from './views/cu2_gestionar_usuarios_roles/roles/role-list/role-list.component';

// CU3: Clientes
import { CustomerListComponent } from './views/cu3_gestionar_clientes/customers/customer-list/customer-list.component';

// CU4: Sucursales
import { SucursalListComponent } from './views/cu4_gestionar_sucursales/sucursales/sucursal-list/sucursal-list.component';

// CU5: Productos (Poleras)
import { ProductListComponent } from './views/cu5_gestionar_productos/products/product-list/product-list.component';

// CU6: Clasificación de Prendas (Categorías)
import { ClasificacionListComponent } from './views/cu6_gestionar_clasificacion_prendas/categorias/clasificacion-list/clasificacion-list.component';

// CU7: Proveedores y Suministros
import { ProveedorListComponent } from './views/cu7_gestionar_proveedores_productos_suministrados/suppliers/proveedor-list/proveedor-list.component';

// CU08: Catálogo y Disponibilidad Multitienda
import { ProductCatalogComponent } from './views/cu8_consultar_catalogo_disponibilidad/product-catalog/product-catalog.component';

// CU09: Carrito de Compras
import { CartViewComponent } from './views/cu9_gestionar_carrito_compras/cart/cart-view.component';

// CU10: Gestión de Reservas de Prendas
import { MyReservationsComponent } from './views/cu10_gestionar_reservas_prendas/reservations/my-reservations.component';

// CU11: Atender Reservas en Sucursal
import { AdminReservasComponent } from './views/cu11_atender_reservas_sucursal/admin-reservas/admin-reservas.component';

// CU13: Inventario y Movimientos de Poleras
import { InventarioListComponent } from './views/cu13_gestionar_inventario_movimientos/inventario/inventario-list/inventario-list.component';

// CU14: Registrar Ventas Presenciales (POS & Historial)
import { PosVentaComponent } from './views/cu14_registrar_ventas_presenciales/pos/pos-venta/pos-venta.component';
import { VentasListComponent } from './views/cu14_registrar_ventas_presenciales/ventas/ventas-list/ventas-list.component';

// CU15: Realizar Compras Digitales (Tienda Online & Mis Pedidos)
import { TiendaOnlineComponent } from './views/cu15_realizar_compras_digitales/tienda-online/tienda-online.component';
import { MisPedidosWebComponent } from './views/cu15_realizar_compras_digitales/mis-pedidos-web/mis-pedidos-web.component';

import { adminGuard } from './core/guards/admin.guard';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  // CU1: Autenticación
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'recover-password', component: RecoverPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },

  // Dashboard de Reportes y KPIs (Exclusivo Administrador)
  { path: 'dashboard', component: DashboardComponent, canActivate: [adminGuard] },
  { path: 'atencion-reservas', redirectTo: 'admin/reservas', pathMatch: 'full' },

  // Tienda y Portal del Cliente (Layout Omnicanal Boutique)
  {
    path: '',
    component: ClientLayoutComponent,
    children: [
      { path: 'catalogo', component: ProductCatalogComponent },
      { path: 'tienda', redirectTo: 'catalogo', pathMatch: 'full' },
      { path: 'carrito', component: CartViewComponent },
      { path: 'mis-reservas', component: MyReservationsComponent, canActivate: [authGuard] },
      { path: 'mis-pedidos', component: MisPedidosWebComponent, canActivate: [authGuard] },
      { path: 'tienda/mis-pedidos', redirectTo: 'mis-pedidos', pathMatch: 'full' },
      { path: '', redirectTo: 'catalogo', pathMatch: 'full' }
    ]
  },

  // Backoffice / Admin ERP (Protegido por adminGuard)
  {
    path: 'admin',
    component: AdminLayoutComponent,
    canActivate: [adminGuard],
    children: [
      // CU2: Usuarios y Roles
      { path: 'users', component: UserListComponent },
      { path: 'roles', component: RoleListComponent },
      // CU3: Clientes
      { path: 'customers', component: CustomerListComponent },
      // CU4: Sucursales
      { path: 'sucursales', component: SucursalListComponent },
      // CU6: Clasificación de Prendas
      { path: 'categorias', component: ClasificacionListComponent },
      // CU5: Poleras y Productos
      { path: 'products', component: ProductListComponent },
      // CU7: Proveedores
      { path: 'suppliers', component: ProveedorListComponent },
      // CU08: Catálogo
      { path: 'catalogo', component: ProductCatalogComponent },
      // CU09: Carrito
      { path: 'carrito', component: CartViewComponent },
      // CU10: Mis Reservas
      { path: 'mis-reservas', component: MyReservationsComponent },
      // CU11: Atender Reservas
      { path: 'reservas', component: AdminReservasComponent },
      // CU13: Inventario y Kardex
      { path: 'inventario', component: InventarioListComponent },
      // CU14: POS y Ventas
      { path: 'pos', component: PosVentaComponent },
      // CU15: Vitrina & Tienda Unificada
      { path: 'tienda-digital', redirectTo: '/catalogo', pathMatch: 'full' },
      { path: 'ventas', component: VentasListComponent },
      { path: '', redirectTo: 'users', pathMatch: 'full' }
    ]
  },

  { path: '**', redirectTo: 'catalogo' }
];
