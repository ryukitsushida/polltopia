from enum import Enum


class Provider(Enum):
    LOCAL = "local"
    GOOGLE = "google"
    GITHUB = "github"


type ProviderType = Provider
