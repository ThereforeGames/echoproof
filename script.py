"""
Simple extension that injects recent conversation into the negative prompt in order to reduce OCD-like behavior of the assistant fixating on a single word, phrase, or sentence structure.
"""

import gradio as gr
import torch, math
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
	"context_delimiter":"\\n",
	"negative_delimiter":" ",
	"max_messages":10,
	"max_multiplier":4,
	"scaling":"exponential",
	"enable": True,
	"blacklist":"",
	"tab":"chat"
}

VERSION = "0.3.0"

def state_modifier(state):
	"""
	Modifies the state variable, which is a dictionary containing the input
	values in the UI like sliders and checkboxes.
	"""
	
	# print("Call to `state_modifier()`")
	# print(f"State: {state}")

	if params["enable"]:
		if params["tab"]=="chat":
			internal_history = state["history"]["internal"]
		elif params["tab"]=="notebook":
			internal_history = state["textbox-notebook"].split("\n")
		elif params["tab"]=="default":
			internal_history = state["textbox-default"].split("\n")

		if params["blacklist"]:
			import re
			blacklist = params["blacklist"].split("\n")
			for term in blacklist:
				# Convert glob-style wildcard to regex-style
				term = term.replace("*", ".*")
				for idx, msg in enumerate(internal_history):
					if params["tab"]=="chat": msg = msg[1]
					new_msg = re.sub(term, "", msg)
					if params["debug"] and msg != new_msg: print(f"Replaced `{msg}` with `{new_msg}`")
					msg = new_msg

					if params["tab"]=="chat": internal_history[idx] = (internal_history[idx][0], msg)
					else: internal_history[idx] = msg

		# Remove empty strings from internal_history
		internal_history = list(filter(None, internal_history))

		history_length = len(internal_history)

		_min = max(0,history_length - params["max_messages"]) if params["max_messages"] else 0

		extra_neg = ""
		total_messages = history_length - _min
		for idx in range(_min,history_length):
			msg = internal_history[idx]
			if params["tab"]=="chat": msg = msg[1]

			# Linear scaled repeats
			relative_idx = idx - _min + 1

			if params["scaling"]=="constant":
				multiplier = params["max_multiplier"]
			elif params["scaling"]=="linear":
				multiplier = round(relative_idx / total_messages * params["max_multiplier"])
			elif params["scaling"]=="exponential":
				multiplier = round(params["max_multiplier"] * math.pow((relative_idx / total_messages), 2))
			elif params["scaling"]=="logarithmic":
				multiplier = round(params["max_multiplier"] * math.log(relative_idx + 1) / math.log(total_messages + 1))

			if params["debug"]: print(f"Multiplier for message #{relative_idx}/{total_messages}: {multiplier}")

			extra_neg += (msg + params["negative_delimiter"]) * multiplier

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

		
		with gr.Row():
			max_messages = gr.Slider(1, 50, label="Max Messages", info="Adds the most recent x messages to your negative prompt.", value=10, step=1)
			max_messages.change(lambda x: params.update({"max_messages": x}), max_messages, None)

			max_multiplier = gr.Slider(0, 50, label="Max Multiplier", info="The maximum number of times a message will be added to the negative prompt.", value=4, step=1)
			max_multiplier.change(lambda x: params.update({"max_multiplier": x}), max_multiplier, None)

		scaling = gr.Radio(value="exponential",label="Scaling",info="How the multiplier scales with the number of messages.",choices=["constant","linear","exponential","logarithmic"])
		scaling.change(lambda x: params.update({"scaling": x}), scaling, None)


		with gr.Row():
			context_delimiter = gr.Textbox(value="\\n",label="Context Delimiter",info="Expected history format for Default and Notebook tabs.")
			context_delimiter.change(lambda x: params.update({"context_delimiter": x}), context_delimiter, None)

			delimiter = gr.Textbox(value=" ",label="Negative Delimiter",info="String that separates each message in the negative prompt.")
			delimiter.change(lambda x: params.update({"negative_delimiter": x}), delimiter, None)

		blacklist = gr.Textbox(value="",lines=3,max_lines=100,label="Blacklist",info="These terms will be excluded from being injected into your negative prompt. Enter one term per line. Supports `*` wildcard as well as regex.")
		blacklist.change(lambda x: params.update({"blacklist": x}), blacklist, None)

		tab = gr.Radio(value="chat",label="Tab",info="Due to a limitation of the extension framework, you must specify the current WebUI tab here.",choices=["chat","default","notebook"])
		tab.change(lambda x: params.update({"tab": x}), tab, None)

		gr.Markdown("If you find this project useful, consider [supporting my work here](https://github.com/sponsors/ThereforeGames). Thank you. ❤️")