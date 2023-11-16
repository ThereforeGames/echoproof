"""
Simple extension that injects recent conversation into the negative prompt in order to reduce OCD-like behavior of the assistant fixating on a single word, phrase, or sentence structure.
"""

import gradio as gr
import torch
from transformers import LogitsProcessor

from modules import chat, shared
from modules.text_generation import (
	decode,
	encode,
	generate_reply,
)

params = {
	"display_name": "Echoproof",
	"is_tab": False,
	"debug": False,
	"delimiter":" ",
	"history_multiplier":1,
	"last_msg_multiplier":5,
	"message_limit":0,
	"enable": True,
	"blacklist":""
}

VERSION = "0.1.0"

def state_modifier(state):
	"""
	Modifies the state variable, which is a dictionary containing the input
	values in the UI like sliders and checkboxes.
	"""

	if params["enable"]:
		internal_history = state["history"]["internal"]
		history_length = len(internal_history)
		if params["message_limit"]:
			_min = max(0,history_length - params["message_limit"])
		else:
			_min = 0

		extra_neg = ""
		for idx in range(_min,history_length):
			msg = internal_history[idx]
			extra_neg += msg[1] + params["delimiter"]

		extra_neg *= params["history_multiplier"]

		if params["last_msg_multiplier"] > 1:
			extra_neg += state["history"]["internal"][-1][1] * (params["last_msg_multiplier"] - 1)

		if params["blacklist"]:
			import re
			blacklist = params["blacklist"].split("\n")
			for term in blacklist:
				# Convert glob-style wildcard to regex-style
				term = term.replace("*", ".*")
				extra_neg = re.sub(term, "", extra_neg)

		if params["debug"]:
			print(f"Value of `extra_neg`: {extra_neg}")
		
		state["negative_prompt"] += extra_neg

	return state

def ui():
	"""
	Gets executed when the UI is drawn. Custom gradio elements and
	their corresponding event handlers should be defined here.

	To learn about gradio components, check out the docs:
	https://gradio.app/docs/
	"""
	with gr.Accordion(f"Echoproof v{VERSION}", open=False):

		gr.Markdown("**Note:** You must load a model with `cfg-cache` enabled and set `guidance_scale` to a value > 1 for Echoproof to take effect.")

		with gr.Row():
			enable = gr.Checkbox(value=True,label="Enable")
			enable.change(lambda x: params.update({"enable": x}), enable, None)

			debug = gr.Checkbox(value=False,label="Debug")
			debug.change(lambda x: params.update({"debug": x}), debug, None)

		history_multiplier = gr.Slider(0, 50, label="History Multiplier", info="Adds the conversation history to your negative prompt x times.", value=1, step=1)
		history_multiplier.change(lambda x: params.update({"history_multiplier": x}), history_multiplier, None)

		last_msg_multiplier = gr.Slider(1, 50, label="Last Message Multiplier", info="Adds the most recent message to your negative prompt x times.", value=5, step=1)
		last_msg_multiplier.change(lambda x: params.update({"last_msg_multiplier": x}), last_msg_multiplier, None)

		message_limit = gr.Number(value=10,label="History Message Limit")
		message_limit.change(lambda x: params.update({"message_limit":int(x)}), message_limit, None)

		delimiter = gr.Textbox(value=" ",label="Message Delimiter",info="String that separates each message in the negative prompt.")
		delimiter.change(lambda x: params.update({"delimiter": x}), delimiter, None)

		blacklist = gr.Textbox(value="",lines=3,max_lines=100,label="Blacklist",info="These terms will be excluded from being injected into your negative prompt. Enter one term per line. Supports `*` wildcard as well as regex.")
		blacklist.change(lambda x: params.update({"blacklist": x}), blacklist, None)

		gr.Markdown("If you find this project useful, consider [supporting my work here](https://github.com/sponsors/ThereforeGames). Thank you. ❤️")