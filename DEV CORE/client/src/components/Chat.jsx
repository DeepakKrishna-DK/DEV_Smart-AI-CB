import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, StopCircle } from 'lucide-react';
import Message from './Message';
import Header from './Header';
import TypingIndicator from './TypingIndicator';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const hasIdentified = useRef(false);

    // Persistent User Session
    const [userID] = useState(() => {
        const stored = localStorage.getItem('dev_system_uuid');
        if (stored) return stored;

        // Simple random ID generator since crypto.randomUUID might not be available in all older browsers, 
        // but we targeting modern.
        const newID = "user-" + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        localStorage.setItem('dev_system_uuid', newID);
        return newID;
    });

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    useEffect(() => {
        if (!hasIdentified.current) {
            hasIdentified.current = true;
            eventQuery('Welcome');
        }
    }, []);

    const textQuery = async (text) => {
        // Send user message
        const userMsg = {
            who: 'user',
            content: {
                text: {
                    text: [text]
                }
            }
        };

        setMessages(prev => [...prev, userMsg]);
        setIsTyping(true);

        try {
            const res = await axios.post('/api/df_text_query', { text, userID });
            console.log("Frontend textQuery received:", res.data);

            // Process responses
            if (res.data.fulfillmentMessages) {
                const botMsgs = res.data.fulfillmentMessages.map(msg => ({
                    who: 'bot',
                    content: msg
                }));
                setMessages(prev => [...prev, ...botMsgs]);
            } else {
                console.warn("No fulfillmentMessages in textQuery response:", res.data);
            }

            setIsTyping(false);

        } catch (error) {
            console.error('Error fetching chat response:', error);
            setIsTyping(false);
            setMessages(prev => [...prev, {
                who: 'bot',
                content: {
                    text: {
                        text: ["System Alert: Neural Core Communication Interrupted (CODE: DEMO_FALLBACK)."]
                    }
                }
            }]);
        }
    };

    const eventQuery = async (event) => {
        setIsTyping(true);
        try {
            const res = await axios.post('/api/df_event_query', { event, userID });
            console.log("Frontend received response:", res.data);

            // Process responses
            if (res.data.fulfillmentMessages) {
                const botMsgs = res.data.fulfillmentMessages.map(msg => ({
                    who: 'bot',
                    content: msg
                }));
                setMessages(prev => [...prev, ...botMsgs]);
            } else {
                console.warn("No fulfillmentMessages found in response");
            }

            setIsTyping(false);
        } catch (error) {
            console.error('Error handling event query:', error);
            setIsTyping(false);
            setMessages(prev => [...prev, {
                who: 'bot',
                content: {
                    text: {
                        text: ["Initialization sequence failed. Please verify neural link (Backend Connection)."]
                    }
                }
            }]);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    const handleSend = () => {
        if (inputValue.trim() === '') return;
        textQuery(inputValue);
        setInputValue('');
    };

    const renderMessage = (msg, i) => {
        // Handle different message types later (cards etc.)
        // For now text only
        if (msg.content && msg.content.text && msg.content.text.text) {
            return <Message key={i} text={msg.content.text.text[0]} sender={msg.who} />;
        } else {
            // Fallback for rich content not yet implemented
            return null;
        }
    };

    return (
        <div className="flex flex-col h-screen overflow-hidden bg-slate-950 relative">
            {/* Background elements */}
            <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
                <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" style={{ clipPath: "polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" }}></div>
            </div>

            <Header />

            <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 scrollbar-thin scrollbar-thumb-cyan-900 scrollbar-track-transparent">
                <AnimatePresence>
                    {messages.map((msg, i) => renderMessage(msg, i))}
                </AnimatePresence>
                {isTyping && (
                    <div className="flex justify-start">
                        <TypingIndicator />
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 md:p-6 glass border-t border-white/5 backdrop-blur-xl z-20">
                <div className="flex items-center space-x-3 max-w-4xl mx-auto">
                    <div className="relative flex-1 group">
                        <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg blur opacity-30 group-hover:opacity-60 transition duration-1000 group-hover:duration-200"></div>
                        <input
                            ref={inputRef}
                            className="relative w-full bg-slate-900 text-slate-100 placeholder-slate-500 border border-slate-700/50 rounded-lg py-3 px-4 focus:outline-none focus:ring-1 focus:ring-cyan-500/50 transition-all duration-300 font-mono tracking-wide"
                            placeholder="Type command..."
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={handleKeyPress}
                            autoFocus
                        />
                    </div>

                    <button
                        onClick={handleSend}
                        className="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-cyan-500 to-blue-500 group-hover:from-cyan-500 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-cyan-200 dark:focus:ring-cyan-800"
                    >
                        <span className="relative px-5 py-2.5 transition-all ease-in duration-75 bg-slate-900 rounded-md group-hover:bg-opacity-0 flex items-center">
                            <Send className="w-5 h-5 text-cyan-400 group-hover:text-white transition-colors" />
                        </span>
                    </button>
                    {/* Mic button placeholder */}
                    <button className="hidden md:flex items-center justify-center w-12 h-12 rounded-full border border-slate-700/50 hover:bg-slate-800/50 transition-colors group">
                        <Mic className="w-5 h-5 text-slate-500 group-hover:text-cyan-400 transition-colors" />
                    </button>

                </div>
                <div className="text-center mt-2 text-xs text-slate-500 font-mono">
                    System initialized. Connection secure.
                </div>
            </div>
        </div>
    );
};

export default Chat;
