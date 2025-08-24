#!/bin/bash

# SSL 인증서 설정 스크립트
# 사용법: ./scripts/ssl-setup.sh your-domain.com your-email@example.com

DOMAIN=$1
EMAIL=$2

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "사용법: $0 <domain> <email>"
    echo "예시: $0 luna.weblog.life luvbliny@gmail.com"
    exit 1
fi

echo "SSL 인증서 설정을 시작합니다..."
echo "도메인: $DOMAIN"
echo "이메일: $EMAIL"

# certbot 디렉토리 생성
mkdir -p data/certbot/conf
mkdir -p data/certbot/www

# docker-compose.prod.yml 파일에서 도메인과 이메일 업데이트
sed -i.bak "s/luna.weblog.life/$DOMAIN/g" docker-compose.prod.yml
sed -i.bak "s/luvbliny@gmail.com/$EMAIL/g" docker-compose.prod.yml

# nginx.conf 파일에서 도메인 업데이트
sed -i.bak "s/luna.weblog.life/$DOMAIN/g" nginx.conf

# 스테이징 환경에서 인증서 테스트
echo "스테이징 환경에서 인증서를 테스트합니다..."
docker compose -f docker-compose.prod.yml run --rm certbot

# 테스트가 성공하면 실제 인증서 발급
echo "실제 인증서를 발급합니다..."
docker compose -f docker-compose.prod.yml run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email $EMAIL --agree-tos --no-eff-email -d $DOMAIN

# nginx 재시작
echo "nginx를 재시작합니다..."
docker compose -f docker-compose.prod.yml restart nginx

echo "SSL 설정이 완료되었습니다!"
echo "https://$DOMAIN 에서 확인하세요."
