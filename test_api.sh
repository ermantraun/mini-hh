#!/bin/bash

BASE_URL="http://45.80.71.98:8000"

# Если нужен токен после логина
AUTH_TOKEN=""

# Тестовые данные
REGISTER_PAYLOAD='{"email":"test@example.com","password":"password123"}'
LOGIN_PAYLOAD='{"email":"test@example.com","password":"password123"}'
RESUME_CREATE_PAYLOAD='{"title":"My Resume","content":"This is my resume content"}'
RESUME_UPDATE_PAYLOAD='{"title":"Updated Resume","content":"Updated content"}'
IMPROVE_PAYLOAD='{}' # Тут пустой объект, если эндпоинт не требует данных

echo "=== Регистрация ==="
curl -s -X POST "$BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d "$REGISTER_PAYLOAD" -w "\nHTTP_CODE: %{http_code}\n"

echo "=== Логин ==="
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "$LOGIN_PAYLOAD")

# Извлекаем токен
AUTH_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "Получен токен: $AUTH_TOKEN"

AUTH_HEADER="-H \"Authorization: Bearer $AUTH_TOKEN\""

echo "=== Создание резюме ==="
RESUME_RESPONSE=$(curl -s -X POST "$BASE_URL/resumes" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -d "$RESUME_CREATE_PAYLOAD")

RESUME_ID=$(echo $RESUME_RESPONSE | jq -r '.id')
echo "Создано резюме с ID: $RESUME_ID"

echo "=== Получение списка резюме ==="
curl -s "$BASE_URL/resumes" -H "Authorization: Bearer $AUTH_TOKEN" -w "\nHTTP_CODE: %{http_code}\n"

echo "=== Получение резюме по ID ==="
curl -s "$BASE_URL/resumes/$RESUME_ID" -H "Authorization: Bearer $AUTH_TOKEN" -w "\nHTTP_CODE: %{http_code}\n"

echo "=== Обновление резюме ==="
curl -s -X PUT "$BASE_URL/resumes/$RESUME_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -d "$RESUME_UPDATE_PAYLOAD" -w "\nHTTP_CODE: %{http_code}\n"

echo "=== Улучшение резюме ==="
curl -s -X POST "$BASE_URL/resumes/$RESUME_ID/improvements/improve" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -d "$IMPROVE_PAYLOAD" -w "\nHTTP_CODE: %{http_code}\n"

echo "=== Список улучшений ==="
curl -s "$BASE_URL/resumes/$RESUME_ID/improvements" \
    -H "Authorization: Bearer $AUTH_TOKEN" -w "\nHTTP_CODE: %{http_code}\n"

echo "=== Удаление резюме ==="
curl -s -X DELETE "$BASE_URL/resumes/$RESUME_ID" \
    -H "Authorization: Bearer $AUTH_TOKEN" -w "\nHTTP_CODE: %{http_code}\n"
