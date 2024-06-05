from fastapi import FastAPI, Depends, HTTPException
from config.spark import create_spark_session
from routers.v1 import router
from fastapi.middleware.cors import CORSMiddleware
from config.cors_options import configure_cors
from exceptions.http_exception_filter import register_exception_handlers
from config.setting import PORT,HOST


app = FastAPI()

register_exception_handlers(app)

configure_cors(app)

app.include_router(router=router)

async def startup_event():
    await create_spark_session.start()

app.add_event_handler("startup", startup_event)

# Include routers----------->old comment
async def shutdown_event():
    await create_spark_session.stop()

app.add_event_handler("shutdown", shutdown_event)

def main():
    import uvicorn
    uvicorn.run("main:app", host=HOST,
                port=PORT, reload=True, use_colors=True)


if __name__ == "__main__":
    main()

#app.add_event_handler("startup", applications.startup)--------> optional

#@app.on_event("shutdown")-------------> old version (depreciated)
#def shutdown_event():
#    spark.stop()