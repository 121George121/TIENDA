import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RecoverPasswordComponent } from './auth/recover-password.component';
import { ResetPasswordComponent } from './auth/reset-password.component';
import { AdminLayoutComponent } from './views/admin/admin-layout/admin-layout.component';
import { UserListComponent } from './views/admin/users/user-list/user-list.component';
import { RoleListComponent } from './views/admin/roles/role-list/role-list.component';
import { CustomerListComponent } from './views/admin/customers/customer-list/customer-list.component';
import { SucursalListComponent } from './views/admin/sucursales/sucursal-list/sucursal-list.component';
import { ClasificacionListComponent } from './views/admin/categorias/clasificacion-list/clasificacion-list.component';
import { ProductListComponent } from './views/admin/products/product-list/product-list.component';
import { ProveedorListComponent } from './views/admin/suppliers/proveedor-list/proveedor-list.component';
import { ProductCatalogComponent } from './views/product-catalog/product-catalog.component';
import { CartViewComponent } from './views/cart/cart-view.component';
import { adminGuard } from './core/guards/admin.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'catalogo', component: ProductCatalogComponent },
  { path: 'carrito', component: CartViewComponent },
  { path: 'recover-password', component: RecoverPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  {
    path: 'admin',
    component: AdminLayoutComponent,
    canActivate: [adminGuard],
    children: [
      { path: 'users', component: UserListComponent },
      { path: 'roles', component: RoleListComponent },
      { path: 'customers', component: CustomerListComponent },
      { path: 'sucursales', component: SucursalListComponent },
      { path: 'categorias', component: ClasificacionListComponent },
      { path: 'products', component: ProductListComponent },
      { path: 'catalogo', component: ProductCatalogComponent },
      { path: 'carrito', component: CartViewComponent },
      { path: 'suppliers', component: ProveedorListComponent },
      { path: '', redirectTo: 'users', pathMatch: 'full' }
    ]
  },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login' }
];
