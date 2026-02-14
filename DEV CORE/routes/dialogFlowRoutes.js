const chatbot = require('../chatbot/chatbot');

module.exports = app => {
    // Health check
    app.get('/', (req, res) => {
        res.send({ status: 'online', system: 'DEV-AI-Core' });
    });

    app.post('/api/df_text_query', async (req, res) => {
        console.log(`[API] Text Query Received: "${req.body.text}" from User: ${req.body.userID}`);
        try {
            const { text, userID, parameters } = req.body;
            let responses = await chatbot.textQuery(text, userID || 'anonymous', parameters);

            console.log(`[API] Sending Response for: "${text}"`);
            res.send(responses[0].queryResult);
        } catch (error) {
            console.error('[API] Error in text query:', error);
            res.status(500).send({ error: 'Internal Server Error' });
        }
    });

    app.post('/api/df_event_query', async (req, res) => {
        try {
            const { event, userID, parameters } = req.body;
            let responses = await chatbot.eventQuery(event, userID || 'anonymous', parameters);
            res.send(responses[0].queryResult);
        } catch (error) {
            console.error('Error in event query:', error);
            res.status(500).send({ error: 'Internal Server Error' });
        }
    });
};