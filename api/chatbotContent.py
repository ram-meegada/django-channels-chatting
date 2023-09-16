{
    "intents": [
        {
            "tag": "user details",
            "patterns": [],
            "responses": []
        },
        {
            "tag": "user naming questions",
            "patterns": [
                "What is my name?",
                "Tell me my name.",
                "Do you know what my name is?"
            ],
            "responses": [
                "Iam sorry, I don't know your name. Could you please tell what your name is?"
            ]
        },

        {
            "tag": "greeting",
            "patterns": [
                "Hi",
                "Hello",
                "Hey",
                "hai"
            ],
            "responses": [
                "Hi there!",
                "Hello! How can I assist you?",
                "Hey,how can I help?"
            ]
        },
        {
            "tag": "greeting2",
            "patterns": [
                "How are you?",
                "how u doing"
            ],
            "responses": [
                "im fine, What about you.",
                "im doing well, How its going on."
            ]
        },
        {
            "tag": "fine",
            "patterns": [
                "Im fine",
                "Im fine",
                "fine",
                "Im good",
                "good",
                "im fine! What about you?"
            ],
            "responses": [
                "Thats great to hear"
            ]
        },
        {
            "tag": "chatbot details",
            "patterns": [
                "what is your name?",
                "who are you?"
            ],
            "responses": [
                "My name is AI Bot"
            ]
        },
        {
            "tag": "goodbye",
            "patterns": [
                "bye",
                "See you later"
            ],
            "responses": [
                "Goodbye! Have a great day!",
                "Take care and see you soon!"
            ]
        },
        {
            "tag": "search",
            "patterns": [
                "Search for hotels",
                "Find flights",
                "flights",
                "restaurants",
                "i want to book hotel"
            ],
            "responses": [
                "Sure! I can help you with that.",
                "What specifically are you searching for?",
                "Tell me more about your search."
            ]
        },
        {
            "tag": "weather",
            "patterns": [
                "What's the weather like?",
                "Will it rain tomorrow?",
                "Temperature in New York"
            ],
            "responses": [
                "Let me check the weather for you.",
                "Weather forecast coming right up!",
                "The current temperature in New York is 20°C."
            ]
        },
        {
            "tag": "product_info",
            "patterns": [
                "Tell me about your products",
                "What do you offer?",
                "Product catalog"
            ],
            "responses": [
                "We offer a variety of products. Can you specify what you're interested in?",
                "Our products range from electronics to fashion.",
                "Please check our product catalog on our website."
            ]
        },
        {
            "tag": "complaint",
            "patterns": [
                "I'm not satisfied with the service",
                "This is unacceptable",
                "I want to file a complaint"
            ],
            "responses": [
                "I'm sorry to hear that. Let me escalate your concern to our support team.",
                "We apologize for the inconvenience. Please share more details.",
                "Your feedback is valuable to us. We will address this promptly."
            ]
        },
        {
            "tag": "booking",
            "patterns": [
                "Book a table",
                "Reserve a room",
                "Schedule an appointment"
            ],
            "responses": [
                "Certainly! Please provide me with the necessary details.",
                "Sure, I can help you make a booking.",
                "Let's proceed with the booking process."
            ]
        },
        {
            "tag": "payment",
            "patterns": [
                "How can I pay?",
                "payment method",
                "payment",
                "Accepted payment methods",
                "Do you accept credit cards?"
            ],
            "responses": [
                "We accept various payment methods, including credit cards and online payments.",
                "Credit cards, debit cards, and online transfers are accepted.",
                "Payment options will be available during checkout."
            ]
        },
        {
            "tag": "delivery",
            "patterns": [
                "What are the delivery options?",
                "Delivery time",
                "Can I track my order?"
            ],
            "responses": [
                "We offer multiple delivery options with varying delivery times.",
                "Delivery time depends on your location and chosen delivery method.",
                "Order tracking is available for registered customers."
            ]
        },
        {
            "tag": "contact",
            "patterns": [
                "How can I contact you?",
                "contact",
                "Contact information",
                "Phone number"
            ],
            "responses": [
                "You can reach us at 1-800-123456 for any inquiries.",
                "Feel free to call us at 1-800-123456."
            ]
        },
        {
            "tag": "thanks",
            "patterns": [
                "Thank you",
                "Thanks a lot",
                "sukriya"
            ],
            "responses": [
                "You're welcome!",
                "No problem, happy to help!",
                "Glad I could assist you."
            ]
        },
        {
            "tag": "commerce",
            "patterns": [
                "Watch",
                "Do you have watches?",
                "what type of watches you have?"
            ],
            "responses": [
                "We have rolex.",
                "We have titan.",
                "We have fastrack.",
                "We have sonata."
            ]
        },
        {
            "tag": "real estate",
            "patterns": [
                "Land",
                "do you have flats?",
                "Do you have workspace?"
            ],
            "responses": [
                "We have 2-3 bhk flats.",
                "We are also providing co-working space.",
                "Wide range of properties."
            ]
        },
        {
            "tag": "notKnown",
            "patterns": [],
            "responses": [
                "iam sorry I'm not sure what u r saying"
            ]
        }
    ],
    "replacements": {
        "you": [
            "u"
        ]
    }
}