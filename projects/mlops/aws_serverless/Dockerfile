# Install python
FROM public.ecr.aws/lambda/python:3.9

# Install poetry
RUN pip install "poetry==1.7.1"

# Install gcc, which is needed to build some packages (psutil) from source
RUN yum install gcc python3-devel -y

# Install dependencies, exclude dev dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

# Copy required files
COPY app ./
# COPY authorizer ./

# Set entry point
CMD ["lambda_predict.lambda_handler"]
