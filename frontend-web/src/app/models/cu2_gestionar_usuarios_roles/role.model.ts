export interface Rol {
  id: number;
  nombre: string;
  descripcion?: string;
  permisos?: string[];
}

export interface RolCreateDTO {
  nombre: string;
  descripcion?: string;
  permisos?: string[];
}

export interface PermisoCategoria {
  categoria: string;
  permisos: {
    clave: string;
    nombre: string;
    descripcion: string;
  }[];
}

export const LISTA_PERMISOS_SISTEMA: PermisoCategoria[] = [
  {
    categoria: 'Gestión de Usuarios',
    permisos: [
      { clave: 'USUARIOS_LISTAR', nombre: 'Ver Usuarios', descripcion: 'Permite consultar la lista y detalles de usuarios' },
      { clave: 'USUARIOS_CREAR', nombre: 'Crear Usuarios', descripcion: 'Permite registrar nuevos usuarios en el sistema' },
      { clave: 'USUARIOS_EDITAR', nombre: 'Editar Usuarios', descripcion: 'Permite modificar la información de los usuarios' },
      { clave: 'USUARIOS_ESTADO', nombre: 'Activar/Desactivar Usuarios', descripcion: 'Permite cambiar el estado activo/inactivo' },
      { clave: 'USUARIOS_ROL', nombre: 'Asignar Roles', descripcion: 'Permite modificar el rol asignado a un usuario' }
    ]
  },
  {
    categoria: 'Gestión de Roles y Permisos',
    permisos: [
      { clave: 'ROLES_LISTAR', nombre: 'Ver Roles', descripcion: 'Permite ver los roles disponibles en la plataforma' },
      { clave: 'ROLES_CREAR', nombre: 'Crear Roles', descripcion: 'Permite crear nuevos roles con descripciones' },
      { clave: 'ROLES_EDITAR', nombre: 'Editar Roles', descripcion: 'Permite editar la información de roles' },
      { clave: 'ROLES_PERMISOS', nombre: 'Gestionar Permisos', descripcion: 'Permite asignar/quitar permisos a un rol' }
    ]
  },
  {
    categoria: 'Catálogo de Productos',
    permisos: [
      { clave: 'PRODUCTOS_LISTAR', nombre: 'Ver Productos', descripcion: 'Permite explorar el catálogo de productos' },
      { clave: 'PRODUCTOS_CREAR', nombre: 'Crear Productos', descripcion: 'Permite agregar nuevos productos' },
      { clave: 'PRODUCTOS_EDITAR', nombre: 'Editar Productos', descripcion: 'Permite modificar precios y stock de productos' },
      { clave: 'PRODUCTOS_ELIMINAR', nombre: 'Eliminar Productos', descripcion: 'Permite dar de baja productos' }
    ]
  },
  {
    categoria: 'Órdenes y Ventas',
    permisos: [
      { clave: 'ORDENES_LISTAR', nombre: 'Ver Todas las Órdenes', descripcion: 'Permite administrar los pedidos del sistema' },
      { clave: 'ORDENES_GESTIONAR', nombre: 'Cambiar Estado de Órdenes', descripcion: 'Permite procesar y despachar órdenes' }
    ]
  },
  {
    categoria: 'Auditoría y Bitácora (CU20)',
    permisos: [
      { clave: 'BITACORA_LISTAR', nombre: 'Consultar Bitácora', descripcion: 'Permite visualizar el historial de actividades y eventos del sistema' },
      { clave: 'BITACORA_EXPORTAR', nombre: 'Exportar Bitácora', descripcion: 'Permite descargar reportes de auditoría en formato CSV' }
    ]
  }
];
