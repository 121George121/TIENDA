import { Routes } from '@angular/router';

// CU1: Autenticación
import { LoginComponent } from './views/cu1_gestionar_autenticacion/login/login.component';
import { RecoverPasswordComponent } from './views/cu1_gestionar_autenticacion/recover-password.component';
import { ResetPasswordComponent } from './views/cu1_gestionar_autenticacion/reset-password.component';

// Dashboard & Layout
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { AdminLayoutComponent } from './views/layout/admin-layout/admin-layout.component';

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

// CU13: Inventario y Movimientos de Poleras
import { InventarioListComponent } from './views/cu13_gestionar_inventario_movimientos/inventario/inventario-list/inventario-list.component';

// CU14: Registrar Ventas Presenciales (POS & Historial)
import { PosVentaComponent } from './views/cu14_registrar_ventas_presenciales/pos/pos-venta/pos-venta.component';
import { VentasListComponent } from './views/cu14_registrar_ventas_presenciales/ventas/ventas-list/ventas-list.component';

// CU15: Realizar Compras Digitales (Tienda Online & Mis Pedidos)
import { TiendaOnlineComponent } from './views/cu15_realizar_compras_digitales/tienda-online/tienda-online.component';
import { MisPedidosWebComponent } from './views/cu15_realizar_compras_digitales/mis-pedidos-web/mis-pedidos-web.component';

import { adminGuard } from './core/guards/admin.guard';

export const routes: Routes = [
  // CU1
  { path: 'login', component: LoginComponent },
  { path: 'recover-password', component: RecoverPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },

  // Dashboard
  { path: 'dashboard', component: DashboardComponent },

  // CU15: Tienda Online & Compras Digitales
  { path: 'tienda', component: TiendaOnlineComponent },
  { path: 'tienda/mis-pedidos', component: MisPedidosWebComponent },

  // Backoffice / Admin
  {
    path: 'admin',
    component: AdminLayoutComponent,
    canActivate: [adminGuard],
    children: [
      // CU2
      { path: 'users', component: UserListComponent },
      { path: 'roles', component: RoleListComponent },
      // CU3
      { path: 'customers', component: CustomerListComponent },
      // CU4
      { path: 'sucursales', component: SucursalListComponent },
      // CU6
      { path: 'categorias', component: ClasificacionListComponent },
      // CU5
      { path: 'products', component: ProductListComponent },
      // CU7
      { path: 'suppliers', component: ProveedorListComponent },
      // CU13
      { path: 'inventario', component: InventarioListComponent },
      // CU14
      { path: 'pos', component: PosVentaComponent },
      { path: 'ventas', component: VentasListComponent },
      // CU15 Shortcut in admin
      { path: 'tienda-digital', component: TiendaOnlineComponent },
      { path: '', redirectTo: 'users', pathMatch: 'full' }
    ]
  },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];
