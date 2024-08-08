FROM golang:1.22 AS go_builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY src/backend/ .

RUN go build -o main .



FROM python:3.11 AS python_builder

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/nlp/ nlp/
COPY src/vector/ vector/
COPY src/confluence/ confluence/
COPY src/rag/ rag/
COPY src/llm/ llm/

FROM python:3.11

COPY --from=go_builder /app/main /app/main
COPY --from=python_builder /app /app

EXPOSE 8080

CMD ["/app/main"]