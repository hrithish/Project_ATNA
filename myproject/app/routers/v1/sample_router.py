# from fastapi import APIRouter
# from app.services.lookup import createLookup
# from app.config.spark import read_from_delta, save_to_delta
# from pyspark.sql import SparkSession

# sample_router = APIRouter()
# #handle req and res
# @sample_router.get("/delta/read")
# async def read_delta():
#     df = read_from_delta("/path/to/delta-table") #---------->until configuration set up correctly on local 
#     return df.show()

# @sample_router.post("/delta/write")
# async def write_delta():
#     try:
#         return await createLookup()
#     except Exception as e:
#         raise
    
from exceptions.custom_errors import (
    InternalServerError,
    NotFoundException,
    SessionException,
)
from fastapi import APIRouter, Depends, Body, HTTPException, status, Request
from schemas import SignInParams
from services import lookup
from dependencies import authenticate_token_and_get_user
from fastapi.responses import JSONResponse
from config.spark import create_spark_session

session_router = APIRouter(tags=['Session']) #/ sample_router changed to session_router

spark = create_spark_session()

@session_router.post('/signin')
async def login_for_access_token(
    request: Request, params: SignInParams = Body()
):
    try:
        user = lookup.signin(params, request.client.host, spark)
        headers = {"Authorization": f"Bearer {user['access_token']}"}
        return JSONResponse(
            content=user["data"], status_code=status.HTTP_200_OK, headers=headers
        )
    except NotFoundException:
        raise SessionException("Invalid email or password")
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError(
            "Sorry something went wrong on our end!, Please try again later"
        )


@session_router.delete('/signout')
async def signout(
    current_user=Depends(authenticate_token_and_get_user)
):
    try:
        result = lookup.signout(current_user, spark)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        raise e
    except Exception:
        raise InternalServerError(
            "Sorry something went wrong on our end!, Please try again later"
        )


# @app.get('/users/{user_id}')
# async def read_user(user_id: int):
#     try:
#         user = get_user_by_id(user_id)
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# @app.put('/users/{user_id}')
# async def update_user_info(user_id: int, update_data: dict):
#     try:
#         user = update_user(user_id, update_data)
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# @app.delete('/users/{user_id}')
# async def remove_user(user_id: int):
#     try:
#         result = delete_user(user_id)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)