
#%%
from IPython.display import Audio
from scipy.io import wavfile
import numpy as np
#%%
file_name = 'C:\\Users\\pyjpa\\Desktop\\aac.wav'
# %%
# Audio(file_name)
# %%
data = wavfile.read(file_name)
framerate = data[0]
sounddata = data[1]
time = np.arange(0,len(sounddata))/framerate
print('Sample rate:',framerate,'Hz')
print('Total time:',len(sounddata)/framerate,'s')
# %%
# !pip install librosa
import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# %%
tokenizer = Wav2Vec2Processor.from_pretrained("ydshieh/wav2vec2-large-xlsr-53-chinese-zh-cn-gpt")
model = Wav2Vec2ForCTC.from_pretrained("ydshieh/wav2vec2-large-xlsr-53-chinese-zh-cn-gpt").to("cuda")
# %%
input_audio, _ = librosa.load(file_name, sr=16000)
# %%
input_values = tokenizer(input_audio, return_tensors="pt").input_values.to("cuda")
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = tokenizer.batch_decode(predicted_ids)[0]
# %%
transcription
# %%
