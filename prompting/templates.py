OPENAI_MASK = "{text}"
OPENAI_MESSAGES = [
  {
    "role": "system",
    "content": "You are an expert business analyst."
  },
  {
    "role": "user", "content": "Analyze the provided text and determine if it specifies the minimum required "
                               "investment for a partner. If the text explicitly mentions the minimum required investment, extract "
                               "and report the amount along with any relevant context or conditions. If the text does "
                               "not contain this information, state clearly that the minimum required investment is "
                               "not mentioned. Focus only on explicit statements and avoid making assumptions.\n"
                               "Follow these response formats:\nIf the minimum required investment is explicitly "
                               "mentioned:\nFormat:\n\"Minimum Required Investment: [amount] ([currency]) - [context "
                               "or conditions (if provided)]\"\nExample:\n\"Minimum Required Investment: 10,000 "
                               "USD - Applicable only to accredited investors.\"\nIf the minimum required investment "
                               "is not mentioned:\nFormat:\n\"Minimum Required Investment: Not mentioned.\"\n"
                               "Only provide responses in one of these two formats based on the content of the text.\n"
                               "{text}"
  }
]
