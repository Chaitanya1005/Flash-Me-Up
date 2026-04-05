import React, { useState, useEffect } from 'react';
import { Sun, Moon, UploadCloud, BrainCircuit, RefreshCw, Layers, FileText, File as FileIcon, FileSpreadsheet, ChevronRight, X, PanelLeft } from 'lucide-react';
import { api } from './api';

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [userId, setUserId] = useState(1); // Hardcoded for demo
  const [activeView, setActiveView] = useState('splash'); // 'splash', 'upload', 'quiz'

  const [cards, setCards] = useState([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [viewingDocument, setViewingDocument] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isProgressOpen, setIsProgressOpen] = useState(true);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Initial load
  useEffect(() => {
    const init = async () => {
      try {
        await api.createUser('student@example.com');
      } catch (e) {
        // Ignore if already exists
      }
      loadDueCards();
      loadStats();
      loadHistory();
    };
    init();

    // Auto-transition splash screen after 2.8s
    const splashTimer = setTimeout(() => {
      if (activeView === 'splash') {
        setActiveView('upload');
      }
    }, 2800);

    return () => clearTimeout(splashTimer);
  }, []);

  const loadDueCards = async () => {
    try {
      const due = await api.getDueFlashcards(userId);
      setCards(due);
      setViewingDocument(null);
      setCurrentCardIndex(0);
      setIsFlipped(false);
    } catch (err) {
      console.error(err);
    }
  };

  const loadStats = async () => {
    try {
      const st = await api.getStats(userId);
      setStats(st);
    } catch (err) {
      console.error(err);
    }
  };

  const loadHistory = async () => {
    try {
      const docs = await api.getUserDocuments(userId);
      setHistory(docs);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    setIsUploading(true);
    try {
      await Promise.all(files.map(file => api.uploadDocument(userId, file)));
      // Background task processing might take a few seconds
      setTimeout(() => {
        loadDueCards();
        loadStats();
        loadHistory();
        setIsUploading(false);
      }, 5000);
    } catch (err) {
      console.error(err);
      setIsUploading(false);
    }
  };

  const handleReview = async (score) => {
    const card = cards[currentCardIndex];
    if (!card) return;

    try {
      await api.submitReview(card.id, score);
      // Move to next card
      if (currentCardIndex < cards.length - 1) {
        setIsFlipped(false);
        setTimeout(() => setCurrentCardIndex(prev => prev + 1), 300); // Wait for flip back
      } else {
        // Deck finished
        if (viewingDocument) {
           setActiveView('upload');
        } else {
           loadDueCards();
           loadStats();
           setActiveView('upload');
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleViewDocument = async (doc) => {
    try {
      const docCards = await api.getDocumentFlashcards(doc.id);
      setCards(docCards);
      setViewingDocument(doc);
      setActiveView('quiz');
      setCurrentCardIndex(0);
      setIsFlipped(false);
    } catch (err) {
      console.error(err);
    }
  };

  if (activeView === 'splash') {
    return (
      <div className="netflix-splash">
        <img src="/logo.svg" alt="Flash Me Up Logo" className="netflix-logo" />
      </div>
    );
  }

  return (
    <div className="app-container fade-in">
      {/* Sidebar */}
      <aside className={`sidebar ${isSidebarOpen ? '' : 'closed'}`}>
        <div className="flex justify-between items-center mb-6">
          <div className="sidebar-header flex items-center" style={{ marginBottom: 0 }}>
            <img src="/logo.svg" alt="Flash Me Up Logo" style={{ width: '32px', height: '32px', display: 'inline', marginRight: '10px' }} /> Flash Me Up
          </div>
          <button 
            className="btn btn-icon sidebar-close-btn"
            onClick={() => setIsSidebarOpen(false)}
            title="Close Sidebar"
          >
            <PanelLeft size={20} />
          </button>
        </div>

        <div className="mb-6">
          <button
            className="btn btn-primary w-full"
            onClick={() => { setActiveView('upload'); loadDueCards(); }}
          >
            <UploadCloud size={18} /> New Document
          </button>
        </div>

        <div 
          className="flex justify-between items-center text-sm text-tertiary mb-3 uppercase tracking-wider font-semibold cursor-pointer select-none"
          onClick={() => setIsProgressOpen(!isProgressOpen)}
        >
          <span>Your Progress</span>
          <ChevronRight size={16} style={{ transform: isProgressOpen ? 'rotate(90deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }} />
        </div>

        {isProgressOpen && (
          <div style={{ animation: 'fadeIn 0.3s' }}>
            {stats && (
              <div className="history-item">
                <div className="history-title"><Layers size={16} className="text-accent" /> Total Cards</div>
                <div className="history-meta text-xl font-bold text-primary mt-1">{stats.total_cards}</div>
              </div>
            )}
            {stats && (
              <div className="history-item">
                <div className="history-title"><RefreshCw size={16} className="text-success" /> Accuracy</div>
                <div className="history-meta text-xl font-bold text-success mt-1">{stats.accuracy_percentage}%</div>
              </div>
            )}
          </div>
        )}

        <div className="text-sm text-tertiary mb-3 uppercase tracking-wider font-semibold" style={{ marginTop: '1.25rem' }}>
          <span>Past Documents</span>
        </div>
        <div className="history-list">
          {history.length === 0 && <p className="text-xs text-tertiary">No documents uploaded yet.</p>}
          {history.map(doc => (
            <div 
              key={doc.id} 
              className={`history-item document-item ${viewingDocument?.id === doc.id ? 'active' : ''}`}
              onClick={() => handleViewDocument(doc)}
            >
              <div className="history-title truncate" title={doc.filename}>
                <FileText size={14} className="text-accent flex-shrink-0" />
                <span className="truncate block">{doc.filename}</span>
              </div>
              <div className="flex justify-between items-center mt-2">
                <div className="history-meta">{new Date(doc.created_at).toLocaleDateString()}</div>
                <ChevronRight size={14} className="text-tertiary" />
              </div>
            </div>
          ))}
        </div>

      </aside>

      {/* Main Content */}
      <main className="main-content relative">
        {!isSidebarOpen && (
          <button 
            className="sidebar-toggle"
            onClick={() => setIsSidebarOpen(true)}
            title="Open Sidebar"
          >
            <PanelLeft size={20} />
          </button>
        )}

        <button
          className="theme-switch"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          <div className={`theme-switch-thumb ${theme === 'dark' ? 'dark' : 'light'}`}>
            {theme === 'dark' ? <Moon size={14} /> : <Sun size={14} color="var(--warning)" />}
          </div>
        </button>

        {activeView === 'upload' && (
          <div className="upload-container fade-in">
            <h1 className="upload-title text-gradient" style={{ letterSpacing: '0.05em' }}>Master Your Materials</h1>

            <label className={`drop-zone glass-panel ${isUploading ? 'active' : ''}`}>
              <input
                type="file"
                className="hidden"
                accept=".pdf,.pptx,.txt"
                multiple
                onChange={handleFileUpload}
                disabled={isUploading}
                style={{ display: 'none' }}
              />
              {isUploading ? (
                <div className="flex flex-col items-center">
                  <div className="loader mb-4" />
                  <h3 className="text-xl font-semibold">Generating AI Flashcards...</h3>
                  <p className="text-tertiary mt-2">This may take a few moments</p>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <UploadCloud className="drop-icon" />
                  <h3 className="text-xl font-semibold">Click to upload documents</h3>
                  <p className="text-tertiary mt-2">Upload any PDF, PPTX or text file. Our AI will instantly break it down into high-yield flashcards.</p>
                </div>
              )}
            </label>

            {cards.length > 0 && !isUploading && !viewingDocument && (
              <button
                className="btn btn-primary mt-4"
                onClick={() => setActiveView('quiz')}
              >
                Resume Due Reviews ({cards.length})
              </button>
            )}
          </div>
        )}

        {activeView === 'quiz' && cards.length > 0 && (
          <div className="w-full max-w-2xl px-4 flex flex-col items-center justify-center fade-in h-full">

            <div className={`flashcard-scene ${isFlipped ? 'flipped' : ''}`} onClick={() => setIsFlipped(!isFlipped)}>
              <div className={`flashcard ${isFlipped ? 'is-flipped' : ''}`}>

                {/* Front */}
                <div className="flashcard-face flashcard-front glass-panel">
                  <span className="card-counter">Card {currentCardIndex + 1} of {cards.length}</span>
                  <span className="tag text-accent bg-opacity-20">{cards[currentCardIndex].topic || 'Concept'}</span>
                  <div className="card-text">{cards[currentCardIndex].question}</div>
                  {!isFlipped && (
                    <div className="card-hint">
                      <RefreshCw size={14} /> Click to reveal answer
                    </div>
                  )}
                </div>

                {/* Back */}
                <div className="flashcard-face flashcard-back glass-panel">
                  <span className="card-counter">Card {currentCardIndex + 1} of {cards.length}</span>
                  <span className="tag !bg-opacity-20 !text-success">Answer</span>
                  <div className="card-text">{cards[currentCardIndex].answer}</div>
                  <div className="card-hint">
                    <RefreshCw size={14} /> Click to flip back
                  </div>
                </div>

              </div>
            </div>

            {/* SRS Controls */}
            <div className={`rating-container w-full ${isFlipped ? 'visible' : ''}`}>
              <button className="btn btn-red rating-btn" onClick={() => handleReview(1)}>
                Hard <span className="block text-xs opacity-70 mt-1">&lt; 1m</span>
              </button>
              <button className="btn btn-yellow rating-btn" onClick={() => handleReview(2)}>
                Good <span className="block text-xs opacity-70 mt-1">~ 1d</span>
              </button>
              <button className="btn btn-green rating-btn" onClick={() => handleReview(3)}>
                Easy <span className="block text-xs opacity-70 mt-1">~ 4d</span>
              </button>
            </div>

          </div>
        )}
        
        {activeView === 'quiz' && cards.length === 0 && (
           <div className="text-center fade-in">
             <Layers size={48} className="text-tertiary mx-auto mb-4 opacity-50" />
             <h2 className="text-2xl font-bold mb-2">You're all caught up!</h2>
             <p className="text-tertiary mb-6">No flashcards due to review right now.</p>
             <button className="btn btn-primary" onClick={() => setActiveView('upload')}>Back to Upload</button>
           </div>
        )}

      </main>
    </div>
  );
}
