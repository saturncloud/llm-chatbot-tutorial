from typing import Optional

import torch
from fastchat.conversation import Conversation, SeparatorStyle
from fastchat.serve.inference import generate_stream
from transformers import PreTrainedModel, PreTrainedTokenizerFast, LlamaForCausalLM, LlamaTokenizer


class StreamlitChatLoop:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model: Optional[PreTrainedModel] = None
        self.tokenizer: Optional[PreTrainedTokenizerFast] = None
        self.system_prompt: Optional[str] = """
        A chat between a curious user and an artificial intelligence assistant.
        The assistant gives helpful, detailed, and polite answers to the user's questions.\n
        """
        self.clear_conversation()

    def clear_conversation(self):
        self.conv: Conversation = Conversation(
            name='vicuna_v1.1',
            system=self.system_prompt,
            roles=['USER', 'ASSISTANT'],
            messages=[],
            offset=0,
            sep_style=SeparatorStyle.ADD_COLON_TWO,
            sep=' ',
            sep2='</s>',
            stop_str=None,
            stop_token_ids=None
        )

    def load_models(self):
        model = LlamaForCausalLM.from_pretrained(
            self.model_path,
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        tokenizer = LlamaTokenizer.from_pretrained(self.model_path)
        self.model = model
        self.tokenizer = tokenizer

    def take_user_input(self, user_input: str):
        conv = self.conv
        conv.append_message(conv.roles[0], user_input)
        conv.append_message(conv.roles[1], None)

    def loop(self):
        prompt = self.conv.get_prompt()
        gen_params = {
            "model": self.model_path,
            "prompt": prompt,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
            "max_new_tokens": 512,
            "stop": self.conv.stop_str,
            "stop_token_ids": self.conv.stop_token_ids,
            "echo": False,
        }
        output_stream = generate_stream(self.model, self.tokenizer, gen_params, 0)
        output_text = ""
        for outputs in output_stream:
            output_text = outputs["text"]
            output_text = output_text.strip().split(" ")
            output_text = " ".join(output_text)
            yield output_text
        final_out = output_text
        self.conv.messages[-1][-1] = final_out.strip()
