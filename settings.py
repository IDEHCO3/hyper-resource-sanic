import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "src")
MODELS_DIR = os.path.join(SOURCE_DIR, "models")
ROUTERS_DIR = os.path.join(SOURCE_DIR, "routes")
CONTEXTS_DIR = os.path.join(SOURCE_DIR, "contexts")
RESOURCES_DIR = os.path.join(SOURCE_DIR, "resources")
VOCAB_DIR = os.path.join(SOURCE_DIR, "hyper_resource", "context", "hyper-resource.jsonld")