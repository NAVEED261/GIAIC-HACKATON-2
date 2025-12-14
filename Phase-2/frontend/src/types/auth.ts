export interface User {
  id: string
  email: string
  name: string
  created_at: string
  updated_at: string
  is_active: boolean
}

export interface SignupRequest {
  email: string
  password: string
  name: string
}

export interface SignupResponse {
  id: string
  email: string
  name: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface RefreshTokenRequest {
  refresh_token: string
}

export interface RefreshTokenResponse {
  access_token: string
  token_type: string
}

export interface CurrentUserResponse {
  id: string
  email: string
  name: string
  created_at: string
  updated_at: string
  is_active: boolean
}

export interface AuthError {
  detail: string
  status_code: number
}
