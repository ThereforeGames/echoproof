# Echoproof

Echoproof is a simple extension for Ooobabooga's [text-generation-webui](https://github.com/oobabooga/text-generation-webui) that injects recent conversation history into the negative prompt with the goal of minimizing the LLM's tendency to fixate on a single word, phrase, or sentence structure.

## The problem

I have observed that certain tokens will cause LLMs to exhibit an "OCD-like" behavior where future messages become progressively more repetitive. If you are not familiar with this effect, try appending a bunch of emoji 👀😲😔 to a chatbot's reply or forcing it to write in ALL CAPS - it will become a broken record very quickly.

This is certainly true of quantized Llama 2 models in the 7b to 30b parameter range - I'm guessing it's less prevalent in 70b models, but I don't have the hardware to test that.

Existing solutions to address this problem, such as `repetition_penalty`, have shown limited success.

This issue can derail a conversation well before the context window is exhausted, so I believe it is unrelated to another known phenomenon where a model will descend into a "word salad" state once the chat has gone on for too long.

## The solution (?)

What if we just inject the last thing the chatbot said into the negative prompt for its next message? That was the main idea behind Echoproof, and it seems to work pretty well.

A few weeks of testing have led me to refine this approach with these additional features:

### Max Messages
The maximum number of recent messages that will be injected into the negative prompt. This is a hard limit, so if you set it to 5 and your chat history is 10 messages long, only the last 5 messages will be injected.

### Max Multiplier
The maximum multiplier that will be applied to a message (in other words, the repeat count). I have found that passing a message into the negative prompt only once is not enough to offset the OCD effect, but repeating it 3-5 times makes a noticeable difference.

### Scaling
This is the scaling algorithm that will be applied to the multiplier for each message. You can choose between `constant`, `linear`, `exponential` and `logarithmic`.

### Notebook and Default Tab Support

Originally, this extension only supported Chat mode, but it has since been updated to support other modes as well. The `context_delimiter` setting allows you to specify the expected message separator for Notebook and Default tabs, which defaults to `\n`.

### Blacklist

This feature allows you to exclude certain terms from being injected into your negative prompt, with support for `*` wildcard and regex. This is useful if you want to preserve the LLM's understanding of certain words or phrases, for example in complex multi-character scenarios.

## How to install

Paste the URL of this repo into the "Session" tab of the webui and press enter. Go get a cup of coffee.

## How to use

Load a model with `cfg-cache` enabled and set your `guidance_scale` to a value above 1 in the "Parameters" tab. Otherwise, your negative prompt will not have an effect.