from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate

from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

# Define the path to the directory containing your model and tokenizer
mistral_models_path = "C:/Users/PC/Downloads/tokenizer.model"

# Load the tokenizer and model
tokenizer = MistralTokenizer.from_file(f"{mistral_models_path}/tokenizer.model.v3")
model = Transformer.from_folder(mistral_models_path)  # Assuming this handles the entire model directory

# Create a completion request with the user message
completion_request = ChatCompletionRequest(messages=[UserMessage(content="Explain Machine Learning to me in a nutshell.")])

# Encode the request into tokens
tokens = tokenizer.encode_chat_completion(completion_request).tokens

# Generate the response from the model
out_tokens, _ = generate([tokens], model, max_tokens=64, temperature=0.0, eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)

# Decode the output tokens into a readable format
result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])

# Print the generated result
print(result)
