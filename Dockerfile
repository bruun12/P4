FROM python:3.14 AS base

WORKDIR /app
COPY requirements.txt .

# Install main dependencies
RUN pip install -r requirements.txt

COPY src/ .

FROM base AS test
# Run tests
CMD ["pytest", "-v", "tests/"]

FROM base AS production

CMD [ "python", "main.py" ]

FROM base AS dev

CMD [ "tail -f", "/dev/null" ]