import fastapi

router = fastapi.APIRouter()


@router.get('/')
def index():
    return 'hello FastAPI'


@router.get('/favicon.ico')
def favicon():
    return fastapi.responses.RedirectResponse(url='/static/img/favicon.ico')
