import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';

const BASE_URL =
  (typeof process !== 'undefined' && process.env.NEXT_PUBLIC_API_URL) ||
  'http://localhost:8000';

const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
});

// Response interceptor — normalize errors before they reach calling code
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string; message?: string }>) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred';
    return Promise.reject({ message, status: error.response?.status });
  }
);

// ===== Retry wrapper (exponential backoff, skips 4xx non-timeout errors) =====
async function withRetry<T>(
  fn: () => Promise<T>,
  retries = 2,
  delayMs = 800
): Promise<T> {
  try {
    return await fn();
  } catch (err) {
    const status = (err as { status?: number })?.status;
    // Don't retry on client errors (4xx) except 429 (rate limit)
    if (status && status >= 400 && status < 500 && status !== 429) throw err;
    if (retries <= 0) throw err;
    await new Promise((r) => setTimeout(r, delayMs));
    return withRetry(fn, retries - 1, delayMs * 1.5);
  }
}

// ===== API methods =====

export interface ChatPayload {
  question: string;
  session_id: string;
}

export async function chat(question: string, sessionId = 'default') {
  return withRetry(() =>
    api
      .post<unknown>('/chat', { question, session_id: sessionId })
      .then((r) => r.data)
  );
}

export async function uploadCSV(
  file: File,
  onProgress?: (percent: number) => void
) {
  const formData = new FormData();
  formData.append('file', file);

  return withRetry(() =>
    api
      .post('/upload/csv', formData, {
        // Let Axios set the Content-Type automatically so the
        // multipart boundary is included correctly.
        headers: { 'Content-Type': undefined },
        timeout: 120000,
        onUploadProgress: (e) => {
          if (onProgress && e.total) {
            onProgress(Math.round((e.loaded / e.total) * 100));
          }
        },
      })
      .then((r) => r.data)
  );
}

export async function getTransactions() {
  return withRetry(() => api.get('/transactions').then((r) => r.data));
}

export async function getReports() {
  return withRetry(() => api.get('/reports').then((r) => r.data));
}

export async function getGoals() {
  return withRetry(() => api.get('/goals').then((r) => r.data));
}

export async function getForecast() {
  return withRetry(() => api.get('/forecast').then((r) => r.data));
}

export async function getHealth() {
  return withRetry(() => api.get('/health').then((r) => r.data), 1, 500);
}

export const apiClient = api;
export const API_BASE_URL = BASE_URL;
