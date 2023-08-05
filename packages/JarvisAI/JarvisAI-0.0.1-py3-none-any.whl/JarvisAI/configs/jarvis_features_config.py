
jarvis_features_config = [
  {
    "regex": "weather|temperature|wind|clouds|rainy",
    "import": "jarvis_ai.features.weather.weather",
    "function_name": "weather_app"
  },
  {
    "regex": "setup|set up",
    "import": "jarvis_ai.features.setup.user_setup",
    "function_name": "setup_mode"
  },
  {
    "regex": "tell me date|date|today is what day",
    "import": "jarvis_ai.features.date_time.jarvis_date_time",
    "function_name": "tell_me_date"
  },
  {
    "regex": "time",
    "import": "jarvis_ai.features.date_time.jarvis_date_time",
    "function_name": "tell_me_time"
  }
]
