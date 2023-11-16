# Echoproof

Echoproof is a simple extension for Ooobabooga's [text-generation-webui](https://github.com/oobabooga/text-generation-webui) that injects recent conversation history into the negative prompt with the goal of minimizing the LLM's tendency to fixate on a single word, phrase, or sentence structure.

## The problem

I have observed that certain tokens will cause LLMs to exhibit an "OCD-like" behavior where future messages become progressively more repetitive. If you are not familiar with this effect, try appending a bunch of emoji 👀😲😔 to a chatbot's reply or forcing it to write in ALL CAPS - it will become a broken record very quickly.

This is certainly true of quantized Llama 2 models in the 7b to 30b paramater range - I'm guessing it's less prevalent in 70b models, but I don't have the hardware to test that.

Existing solutions to address this problem, such as `repitition_penalty`, have shown limited success.

This issue can derail a conversation well before the context window is exhausted, so I believe it is unrelated to another known phenomenon where a model will descend into a "word salad" state once the chat has gone on for too long.

## The solution (?)

What if we just inject the last thing the chatbot said into the negative prompt for its next message? That was the main idea behind Echoproof, and it seems to work pretty well.

After testing this approach for a few weeks, I have refined it with a few additional controls:

- **Last Message Multiplier**: The number of times to add the most recent message into the negative prompt. I have found that 1 is not strong enough to offset the OCD effect, but 3-5 makes a noticeable difference.
- **History Multiplier**: The number of times to add your entire chat history into the negative prompt. If you enable Echoproof from the beginning of a conversation, this feature is probably overkill. However, it might be able to save a conversation that is already starting to go off the rails.
- **History Message Limit**: Caps the aforementioned feature to the last x messages.

Some models are more prone to repitition than others, so you may need to experiment with these settings to find the right balance.

## How to install

Paste the URL of this repo into the "Session" tab of the webui and press enter. Go get a cup of coffee.

## How to use

Load a model with `cfg-cache` enabled and set your `guidance_scale` to a value above 1 in the "Parameters" tab. Otherwise, your negative prompt will not have an effect.