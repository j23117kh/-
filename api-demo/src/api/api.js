import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' }
});

export const fetchAllItems = () => apiClient.get('/items').then(res => res.data);
export const fetchItem = (id) => apiClient.get(`/items/${id}`).then(res => res.data);
export const addItem = (data) => apiClient.post('/items', data).then(res => res.data);
export const updateItem = (id, data) => apiClient.put(`/items/${id}`, data).then(res => res.data);
export const deleteItem = (id) => apiClient.delete(`/items/${id}`);