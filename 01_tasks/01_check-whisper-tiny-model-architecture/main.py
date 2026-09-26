import whisper

# Load the whisper tiny model using the whisper library
model = whisper.load_model("tiny")

print(model)