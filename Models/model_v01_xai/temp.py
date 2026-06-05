from tensorflow.keras.models import load_model
model = load_model("btcm-mdl-v01-xai.keras")
print(model.summary())
