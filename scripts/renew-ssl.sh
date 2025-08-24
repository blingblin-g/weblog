#!/bin/bash

# SSL 인증서 자동 갱신 스크립트
# cron에 등록하여 매일 실행: 0 12 * * * /path/to/scripts/renew-ssl.sh

echo "SSL 인증서 갱신을 확인합니다..."

# 인증서 갱신 시도
docker compose -f docker-compose.prod.yml run --rm certbot renew

# nginx 재시작 (인증서가 갱신된 경우)
docker compose -f docker-compose.prod.yml restart nginx

echo "SSL 인증서 갱신 완료"
