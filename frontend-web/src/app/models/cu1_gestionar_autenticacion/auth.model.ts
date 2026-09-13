export interface LoginRequestDTO {
  username: string; // email
  password: string;
}

export interface LoginResponseDTO {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    nombre: string;
    email: string;
    rol?: string;
    rol_id?: number;
    rolid?: number;
    sucursales?: number[];
  };
}

export interface PasswordRecoveryDTO {
  email: string;
}

export interface PasswordResetDTO {
  token: string;
  new_password: string;
}
