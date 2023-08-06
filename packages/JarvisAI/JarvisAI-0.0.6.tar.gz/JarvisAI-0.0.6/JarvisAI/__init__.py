DEV_MODE = True
MIC_MODE = False

if DEV_MODE:
    import configs
    import jarvis
    import action
else:
    from . import configs
    from . import jarvis
    from . import action

# all packages and lib import
import spacy
import os


# Load NLP Spacy Model
try:
    nlp = spacy.load('en_core_web_lg')
except Exception as e:
    print(e)
    print("We will download it for only first time. Please wait and grab a cup of coffee.")
    print("Speed may depend on your internet connection")
    os.system('python -m spacy download en_core_web_lg')
    print("Model has been downloaded successfully, please restart JarvisAI")


# ML Models
models = {
    'spacy_nlp': nlp
}

features_config = configs.features_config
jarvis.start(features_config, action, models, MIC_MODE, DEV_MODE)
