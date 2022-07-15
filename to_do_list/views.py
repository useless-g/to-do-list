from fastapi import APIRouter

router = APIRouter()

# routes = APIRouter()
# routes.include_router(router, prefix='/todo')


@router.get('/{id}')
def get_task(id: int):
    pass


@router.get('/')
def get_all():
    pass
