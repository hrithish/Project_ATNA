# #business logic and db updates
# from config.constants import SPARK_FORMAT
# from spark import SparkSession

# async def createLookup():
#     data = [("Alice", 1), ("Bob", 2), ("Cathy", 3)]
#     df = SparkSession.builder.getOrCreate().createDataFrame(data, ["Name", "Value"])
#     df.write.format(SPARK_FORMAT).save(path)
#     return {"status": "success"}

from pyspark.sql import SparkSession
from exceptions import UnauthorizedException, NotFoundException
from datetime import datetime as dt
from schemas.session import SignInParams
from utils.jwt_utils import create_access_token
from utils.password_utils import verify_password
from config.spark import get_delta_table_path

def get_user_by_email(email: str, spark: SparkSession):
    user_df = spark.read.format("delta").load(get_delta_table_path("users")).filter(f"email == '{email}'")
    user = user_df.collect()
    if not user:
        raise NotFoundException("User not found")
    return user[0]

def signin(params: SignInParams, user_ip: str, spark: SparkSession):
    user = get_user_by_email(params.email, spark)
    is_valid_pass = verify_password(params.password, user.encrypted_password)
    if not is_valid_pass:
        raise UnauthorizedException("Invalid email or password")
    access_token = create_access_token({"id": user.id, "email": user.email})

    

    # Update user information (sign-in metadata)
 
    
    user_data = {
        "id":user.id,
        "email":user.email,
        "encrypted_password": user.encrypted_password,
        "access_token": access_token,
        "last_sign_in_ip": user.current_sign_in_ip,
        "current_sign_in_ip": user_ip,
        "last_sign_in_at": user.current_sign_in_at,
        "current_sign_in_at": dt.datetime.utcnow(),
        "last_seen_at": dt.datetime.utcnow(),
        "sign_in_count": user.sign_in_count + 1
    }

    user.access
    
    user_df = spark.createDataFrame([user_data])
    user_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(get_delta_table_path("users"))

    logged_in_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }

    return {"access_token": access_token, "data": logged_in_user}

def signout(current_user, spark: SparkSession):
    user_df = spark.read.format("delta").load(get_delta_table_path("users")).filter(f"id == {current_user.id}")
    user = user_df.collect()[0]
    user.access_token = None
    
    user_data = {
        "id": user.id,
        "email": user.email,
        "encrypted_password": user.encrypted_password,
        "access_token": None,
        "last_sign_in_ip": user.last_sign_in_ip,
        "current_sign_in_ip": user.current_sign_in_ip,
        "last_sign_in_at": user.last_sign_in_at,
        "current_sign_in_at": user.current_sign_in_at,
        "last_seen_at": user.last_seen_at,
        "sign_in_count": user.sign_in_count

    }


    
    user_df = spark.createDataFrame([user_data])
    user_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(get_delta_table_path("users"))

    return {"message": "Successfully signed out"}



