'use strict';
const dialogflow = require('@google-cloud/dialogflow');
const structjson = require('./structjson.js');
const config = require('../config/keys');
const { v4: uuidv4 } = require('uuid');
const Groq = require('groq-sdk');

const groq = config.groqAPIKey ? new Groq({ apiKey: config.groqAPIKey }) : null;
if (groq) console.log("[DEV System] Neural Link Status: GROQ AI CORE INITIALIZED (GPT-Capable)");

const projectID = config.googleProjectID;
const sessionId = config.dialogFlowSessionID;
const languageCode = config.dialogFlowSessionLanguageCode;

const credentials = {
    client_email: config.googleClientEmail,
    private_key: config.googlePrivateKey,
};

// FORCE DEMO MODE if credentials are clearly dummies
if (credentials.client_email.includes('dummy') || credentials.private_key.includes('dummy')) {
    console.warn("[DEV System] Dummy credentials detected. Forcing Offline Demo Mode.");
    credentials.private_key = null; // Invalidate to trigger demo logic
}

// Robust Key Formatting Fix & Debugging
if (credentials.private_key) {
    let key = credentials.private_key;

    // Handle JSON stringified input (common copy-paste error)
    if (key.trim().startsWith('{')) {
        try {
            const jsonKey = JSON.parse(key);
            if (jsonKey.private_key) key = jsonKey.private_key;
        } catch (e) {
            console.warn("[DEV System] Failed to parse potentially JSON-formatted private key.");
        }
    }

    // Remove wrapping quotes if present
    if ((key.startsWith('"') && key.endsWith('"')) || (key.startsWith("'") && key.endsWith("'"))) {
        key = key.slice(1, -1);
    }

    // Aggressively unescape newlines: \\n -> \n, then literal \n -> newline
    key = key.replace(/\\n/g, '\n');

    credentials.private_key = key;

    // Debug Log (Security Safe)
    const keyHeader = key.substring(0, 30);
    const hasHeader = key.includes('-----BEGIN PRIVATE KEY-----');
    const hasFooter = key.includes('-----END PRIVATE KEY-----');
    const lineCount = key.split('\n').length;

    console.log(`[DEV System] Diagnostic - Private Key:
    - Starts With: "${keyHeader}..."
    - Valid Header: ${hasHeader}
    - Valid Footer: ${hasFooter}
    - Line Count: ${lineCount} (Should be > 10 for valid keys)`);
}

// Check if operating in Demo/Offline mode (Updated Check)
const isDemoMode = projectID === 'dummy-project-id' || !credentials.private_key || credentials.private_key === 'dummy-private-key';

let sessionClient;
try {
    if (!isDemoMode && credentials.private_key && credentials.private_key !== 'dummy-private-key') {
        sessionClient = new dialogflow.SessionsClient({ projectID, credentials });
    } else {
        console.log("[DEV System] Operating in DEMO MODE (No valid credentials found)");
    }
} catch (err) {
    console.warn("[DEV System] Failed to initialize Dialogflow client, reverting to Demo Mode.", err.message);
}

module.exports = {
    // Generate a consistent mock response structure
    mockResponse: function (text, isError = false, skipAnalysis = false) {
        let responseText = text;
        const lower = text.toLowerCase().trim();

        if (!isError && !skipAnalysis) {
            // Basic "Offline Intelligence"
            console.log(`[MockResponse] Analyzing input: "${lower}"`);
            if (lower.match(/^(hi|hello|hey|greetings)/)) {
                responseText = "Greetings, User. The DEV System is online and ready.";
            } else if (lower.includes("who are you") || lower.includes("what is this")) {
                responseText = "I am the DEV System v2.0.0, an advanced conversational interface. I am currently operating in limited Offline Mode.";
            } else if (lower.includes("status") || lower.includes("help") || lower === "test" || lower === "debug") {
                responseText = "System Status:\nMode: OFFLINE (Local)\nNote: To enable GPT/Gemini-like intelligence, you must connect a valid Dialogflow Agent or OpenAI API.";
            } else if (lower.includes("chatgpt") || lower.includes("gemini")) {
                responseText = "This system is currently designed to use Google Dialogflow. To make it behave like ChatGPT, you would need to integrate the OpenAI API backend.";
            } else if (lower.includes("time")) {
                responseText = `Current System Time: ${new Date().toLocaleTimeString()}`;
            } else if (lower.includes("weather")) {
                responseText = "Atmospheric sensors are offline. Please connect to the global neural network for meteorological data.";
            } else if (lower.includes("chatbot") || lower.includes("what is a bot") || lower.includes("ai")) {
                responseText = "A chatbot is an advanced software simulation of human conversation. The DEV System (v2.0.0) represents the next evolution: a Neural Interface designed to execute commands and process natural language with high precision.";
            } else if (lower.includes("security") || lower.includes("safe")) {
                responseText = "Security Protocols: ACTIVE. All sessions are encrypted with a unique UUID. The system operates in a sandboxed environment to ensure data integrity.";
            } else if (lower.match(/^(what|who|where|how|why|tell me)/)) {
                // Generic handler for questions in demo mode
                responseText = `I do not have access to the external knowledge base for "${text}" while in Offline Mode. Please connect Neural Core for full analysis.`;
            } else {
                responseText = `[OFFLINE RESPONSE] I am currently in Demo Mode. To have full conversations like ChatGPT, please ensure your Dialogflow Agent is created and connected properly.`;
            }
        } else if (groq && !isError) {
            responseText = text; // Just pass through the AI response cleanly
        }

        return [{
            queryResult: {
                fulfillmentMessages: [
                    {
                        text: {
                            text: [responseText]
                        }
                    }
                ],
                intent: {
                    displayName: isError ? 'System Error' : 'Demo Intent',
                },
                allRequiredParamsPresent: true,
            }
        }];
    },

    textQuery: async function (text, userID, parameters = {}) {
        let responses;

        // --- NEW: GROQ AI CORE (Smarter Brain) ---
        if (groq) {
            try {
                console.log(`[Groq] Processing Neural Request: "${text}"`);
                const chatCompletion = await groq.chat.completions.create({
                    messages: [
                        { role: 'system', content: 'You are the DEV System v2.0.0, a high-performance AI assistant. Use a professional, slightly futuristic, and efficient tone. Keep responses concise but helpful.' },
                        { role: 'user', content: text }
                    ],
                    model: 'llama-3.3-70b-versatile',
                });

                const aiResponse = chatCompletion.choices[0]?.message?.content || "Neural Link error: No response from Groq Core.";
                return this.mockResponse(aiResponse, false, true); // Use mockResponse structure to wrap AI text
            } catch (err) {
                console.error("[Groq] Neural Link Failure:", err.message);
                // Fallback to Dialogflow/Demo if Groq fails
            }
        }

        if (isDemoMode || !sessionClient) {
            // Echo back nicely in demo mode
            return this.mockResponse(text);
        }

        try {
            let currentSessionID = sessionId + (userID || uuidv4());
            let sessionPath = sessionClient.projectAgentSessionPath(projectID, currentSessionID);

            const request = {
                session: sessionPath,
                queryInput: {
                    text: {
                        text: text,
                        languageCode: languageCode,
                    },
                },
                queryParams: {
                    payload: {
                        data: parameters
                    }
                }
            };

            if (Object.keys(parameters).length > 0) {
                request.queryParams.payload = structjson.jsonToStructProto(parameters);
            }

            responses = await sessionClient.detectIntent(request);

            // Check for empty responses (The "Nothing" Bug)
            if (responses[0] && responses[0].queryResult &&
                (!responses[0].queryResult.fulfillmentMessages || responses[0].queryResult.fulfillmentMessages.length === 0)) {

                console.log("[DEV System] Neural Core returned empty response. Applying Default Brain Fallback.");
                const fallback = this.mockResponse(text);
                responses[0].queryResult.fulfillmentMessages = fallback[0].queryResult.fulfillmentMessages;
            }

            responses = await this.handleAction(responses);
            return responses;

        } catch (error) {
            console.error("[DEV System] Dialogflow Error:", error.message);
            // Auto-fallback on critical auth errors OR Agent Not Found
            if (error.message.includes('DECODER') ||
                error.message.includes('1E08010C') ||
                error.message.includes('PEM routines') ||
                error.message.includes('NOT_FOUND') ||
                error.message.includes('No DesignTimeAgent')) {

                console.warn("[DEV System] Critical Error: Neural Core unreachable (Auth/Agent missing). Reverting to Offline Demo Mode.");
                sessionClient = null;
                return this.mockResponse(text);
            }
            return this.mockResponse("System Alert: Connection to Neural Core interrupted. " + error.message, true);
        }
    },

    eventQuery: async function (event, userID, parameters = {}) {
        if (isDemoMode || !sessionClient) {
            return this.mockResponse("Welcome to DEV System (v2.0.0). Neural Core: Offline. Ready for input.", false, true);
        }

        try {
            let currentSessionID = sessionId + (userID || uuidv4());
            let sessionPath = sessionClient.projectAgentSessionPath(projectID, currentSessionID);

            const request = {
                session: sessionPath,
                queryInput: {
                    event: {
                        name: event,
                        parameters: structjson.jsonToStructProto(parameters),
                        languageCode: languageCode,
                    },
                }
            };

            let responses = await sessionClient.detectIntent(request);

            // Check for empty responses (The "Nothing" Bug)
            if (responses[0] && responses[0].queryResult &&
                (!responses[0].queryResult.fulfillmentMessages || responses[0].queryResult.fulfillmentMessages.length === 0)) {

                console.log("[DEV System] Neural Core Event returned empty. Applying Default Brain Fallback.");
                const welcomeMsg = groq ? "System initialized. Neural Link (Groq AI) is ACTIVE. Ready for advanced processing." : "System initialized. Welcome to the DEV System (Demo Mode).";
                const fallback = this.mockResponse(event === 'Welcome' ? welcomeMsg : event);
                responses[0].queryResult.fulfillmentMessages = fallback[0].queryResult.fulfillmentMessages;
            }

            responses = await this.handleAction(responses);
            return responses;

        } catch (error) {
            console.error("[DEV System] Dialogflow Event Error:", error.message);
            // Auto-fallback on critical auth errors OR Agent Not Found
            if (error.message.includes('DECODER') ||
                error.message.includes('1E08010C') ||
                error.message.includes('PEM routines') ||
                error.message.includes('NOT_FOUND') ||
                error.message.includes('No DesignTimeAgent')) {

                console.warn("[DEV System] Critical Error: Neural Core unreachable (Auth/Agent missing). Reverting to Offline Demo Mode.");
                sessionClient = null;
                return this.mockResponse("Welcome to DEV System (v2.0.0). Neural Core: Offline (Agent Missing). Ready for input.", false, true);
            }
            return this.mockResponse("System Alert: Initialization Sequence Failed. Reverting to SAFE MODE.", true);
        }
    },

    handleAction: function (responses) {
        return responses;
    }
}