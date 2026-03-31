FROM public.ecr.aws/lambda/python:3.9

# Install ADB
RUN yum install -y android-tools

# Copy code
COPY app.py ${LAMBDA_TASK_ROOT}

# Run handler
CMD ["app.lambda_handler"]