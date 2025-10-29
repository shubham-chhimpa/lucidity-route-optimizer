from fastapi import APIRouter, Depends, HTTPException
from app.schemas.route import RouteRequest, RouteResponse
from app.api.deps import get_route_optimizer


router = APIRouter()


@router.post("/find-route", response_model=RouteResponse)
async def find_route_endpoint(request: RouteRequest, optimizer=Depends(get_route_optimizer)):
    try:
        best, total = optimizer.best_route(request.source, request.orders)
        return RouteResponse(best_path=best, total_time_mins=total)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


