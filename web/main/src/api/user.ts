import axios from 'axios';
import type { RouteRecordNormalized } from 'vue-router';

export interface LoginData {
  username: string;
  password: string;
}

export interface LoginRes {
  token: string;
}
export function login(data: LoginData) {
  return axios.post<LoginRes>('/api/v1/user/login', data);
}

export interface VerifyData {
  email: string;
}
export function sendVerifyCodeApi(params: VerifyData) {
  return axios.post('/api/v1/user/verify', params);
}
export interface RegisterData {
  username: string;
  password: string;
  email: string;
  code: string;
}
export function registerApi(params: RegisterData) {
  return axios.post('/api/v1/user/register', params);
}

export function getUserInfo() {
  return axios.post('/api/v1/user/info');
}

export function getShareApi(shareId: string) {
  return axios.get(`/api/v1/user/getShare?share_id=${shareId}`);
}

export interface InviterData {
  inviter: string | undefined;
}
export function updateInviterInfoApi(params: InviterData) {
  return axios.post(`/api/v1/user/updateInviterInfo`, params);
}

export function logout() {
  return axios.post<LoginRes>('/api/v1/user/logout');
}

export function getMenuList() {
  return axios.post<RouteRecordNormalized[]>('/api/user/menu');
}
