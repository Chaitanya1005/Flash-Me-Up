/* eslint-disable no-undef */
const API_BASE = 'https://flash-me-up.onrender.com/api';

export const api = {
  createUser: async (email) => {
    const res = await fetch(`${API_BASE}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    return res.json();
  },
  
  uploadDocument: async (userId, file) => {
    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('file', file);
    
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error("Upload failed");
    return res.json();
  },
  
  getDueFlashcards: async (userId) => {
    const res = await fetch(`${API_BASE}/flashcards/due/${userId}?limit=20`);
    return res.json();
  },
  
  submitReview: async (flashcardId, score) => {
    const res = await fetch(`${API_BASE}/flashcards/${flashcardId}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ flashcard_id: flashcardId, score })
    });
    return res.json();
  },

  getStats: async (userId) => {
    const res = await fetch(`${API_BASE}/stats/${userId}`);
    return res.json();
  },

  getUserDocuments: async (userId) => {
    const res = await fetch(`${API_BASE}/documents/user/${userId}`);
    return res.json();
  },

  getDocumentFlashcards: async (documentId) => {
    const res = await fetch(`${API_BASE}/flashcards/document/${documentId}`);
    return res.json();
  }
};
