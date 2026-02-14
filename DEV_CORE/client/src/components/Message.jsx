import React from 'react';
import { motion } from 'framer-motion';
import { User, Cpu } from 'lucide-react';

const Message = ({ text, sender, isLast }) => {
    const isBot = sender === 'bot';

    return (
        <motion.div
            initial={{ opacity: 0, x: isBot ? -20 : 20, y: 10 }}
            animate={{ opacity: 1, x: 0, y: 0 }}
            transition={{ type: "spring", stiffness: 200, damping: 20 }}
            className={`flex w-full mb-4 ${isBot ? 'justify-start' : 'justify-end'}`}
        >
            <div className={`flex max-w-[80%] md:max-w-[60%] items-end ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mb-1 
                    ${isBot ? 'bg-cyan-500/20 mr-2 border border-cyan-500/50 shadow-[0_0_10px_#06b6d4]' : 'bg-purple-500/20 ml-2 border border-purple-500/50 shadow-[0_0_10px_#d946ef]'}`}>
                    {isBot ? <Cpu className="w-4 h-4 text-cyan-400" /> : <User className="w-4 h-4 text-purple-400" />}
                </div>

                {/* Bubble */}
                <div className={`relative px-4 py-3 rounded-2xl glass backdrop-blur-xl border 
                    ${isBot
                        ? 'rounded-bl-none border-cyan-500/30 text-cyan-50 bg-gradient-to-br from-cyan-900/40 to-slate-900/40'
                        : 'rounded-br-none border-purple-500/30 text-purple-50 bg-gradient-to-bl from-purple-900/40 to-slate-900/40'
                    } shadow-lg`}
                >
                    <p className="text-sm md:text-base font-light leading-relaxed tracking-wide">
                        {text}
                    </p>

                    {/* Glow effect */}
                    <div className={`absolute inset-0 rounded-2xl opacity-20 bg-gradient-to-r ${isBot ? 'from-transparent via-cyan-400/20 to-transparent' : 'from-transparent via-purple-400/20 to-transparent'} pointer-events-none`} />
                </div>
            </div>
        </motion.div>
    );
};

export default Message;
