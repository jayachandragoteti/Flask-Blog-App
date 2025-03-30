from .main import main
from .auth import auth
from .blog import blog
# Export the Blueprint to be used in app initialization
__all__ = ["main", "auth", "blog"]
