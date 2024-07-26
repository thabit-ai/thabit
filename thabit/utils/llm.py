# Initialize OpenAI API for each model
def initialize_openai(model_config):
    """
    Initialize OpenAI API for each model
    """
    openai.api_key = model_config["api_key"]
    params = model_config.copy()
    del params["provider"]
    del params["model"]
    del params["endpoint"]
    del params["api_key"]
    del params["model_short_name"]
    return params


# Asynchronous function to call the AI model
async def call_ai_model(session, model, model_short_name, context, openai_params):
    prompt = "You are a helpful AI assistant. I will ask you a question and I want you to return the direct answer without explaining. If the question is about a number, yes/no, or a simple true/false, return required value with no explanation."
    url = model["endpoint"]
    headers = {
        "Authorization": f"Bearer {model['api_key']}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model["model"],
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": context},
        ],
        **openai_params,
    }
    async with session.post(url, headers=headers, json=data) as response:
        result = await response.json()
        return result["choices"][0]["message"]["content"].strip()
