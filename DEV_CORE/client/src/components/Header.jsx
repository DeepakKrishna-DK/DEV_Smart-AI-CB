import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Terminal, Shield } from 'lucide-react';

const Header = () => {
    return (
        <motion.div
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="w-full h-16 glass sticky top-0 z-50 flex items-center justify-between px-6 border-b border-cyan-500/20"
        >
            <div className="flex items-center space-x-3">
                <div className="relative">
                    <div className="absolute -inset-1 bg-cyan-500 rounded-full blur opacity-25 animate-pulse"></div>
                    <Cpu className="text-cyan-400 w-8 h-8 relative z-10" />
                </div>
                <h1 className="text-2xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500 font-mono neon-text">
                    DEV SYSTEM
                </h1>
            </div>
            <div className="flex items-center space-x-4 text-sm font-mono text-cyan-500/80">
                <div className="flex items-center space-x-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_#22c55e]"></span>
                    <span>ONLINE</span>
                </div>
                <div className="glass px-3 py-1 rounded-md border border-cyan-500/20 flex items-center space-x-2">
                    <Shield className="w-4 h-4" />
                    <span>v2.0.0</span>
                </div>
            </div>
        </motion.div>
    );
};

export default Header;
