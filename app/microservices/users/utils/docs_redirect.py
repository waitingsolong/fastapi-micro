from fastapi import FastAPI
from fastapi.responses import RedirectResponse


def setup_docs_redirects(app: FastAPI):
    # Redirects for docs
    @app.get("/players/docs", include_in_schema=False)
    async def redirect_players_docs():
        return RedirectResponse(url="/users/docs")

    @app.get("/fans/docs", include_in_schema=False)
    async def redirect_fans_docs():
        return RedirectResponse(url="/users/docs")

    # Redirects for redoc
    @app.get("/players/redoc", include_in_schema=False)
    async def redirect_players_redoc():
        return RedirectResponse(url="/users/redoc")

    @app.get("/fans/redoc", include_in_schema=False)
    async def redirect_fans_redoc():
        return RedirectResponse(url="/users/redoc")

    # Redirects for openapi.json
    @app.get("/players/openapi.json", include_in_schema=False)
    async def redirect_players_openapi():
        return RedirectResponse(url="/users/openapi.json")

    @app.get("/fans/openapi.json", include_in_schema=False)
    async def redirect_fans_openapi():
        return RedirectResponse(url="/users/openapi.json")
