from .views import views
from .auth import auth
from .users import users
from .posts import posts
from .comments import comments
from .dengue import dengue_bp



__all__ = [
    'views',
    'auth',
    'users',
    'posts',
    'comments',
    'dengue_bp',  
    'aids_pag_info_bp',
    'saude_mental_page_info_db',
    'gripe_covid_info_db',
    'campanha_do_sono_info_db',
    'historico_db',
]
