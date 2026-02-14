import React from 'react';
import Chat from './components/Chat';

function App() {
  return (
    <div className="w-full h-screen bg-slate-950 text-slate-200 font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      <Chat />
    </div>
  );
}

export default App;
