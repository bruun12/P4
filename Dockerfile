FROM python:3.14 AS base

WORKDIR /src
COPY requirements.txt .

# Install main dependencies
RUN pip install -r requirements.txt

COPY src/ .

FROM base AS test
# Run tests
CMD ["pytest", "-v", "tests/"]

FROM base AS production

CMD [ "python", "main.py" ]