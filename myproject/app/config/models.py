# from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateTimeType, FloatType

# user_data = StructType([
#     StructField("id", IntegerType(), nullable=False),
#     StructField("first_name", StringType(), nullable=False),
#     StructField("last_name", StringType(), nullable=True),
#     StructField("email", StringType(), nullable=False),
#     StructField("encrypted_password", StringType(), nullable=True),
#     StructField("access_token", StringType(), nullable=True),
#     StructField("created_by", IntegerType(), nullable=False),
#     StructField("updated_by", IntegerType(), nullable=True),
#     StructField("last_seen_at", DateTimeType(), nullable=True),
#     StructField("sign_in_count", IntegerType(), nullable=False),
#     StructField("current_sign_in_ip", StringType(), nullable=True),
#     StructField("last_sign_in_ip", StringType(), nullable=True),
#     StructField("current_sign_in_at", DateTimeType(), nullable=True),
#     StructField("last_sign_in_at", DateTimeType(), nullable=True),
#     StructField("created_at", DateTimeType(), nullable=False),
#     StructField("updated_at", DateTimeType(), nullable=True),
#     StructField("deleted_at", DateTimeType(), nullable=True),
# ])