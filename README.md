# claude-initer

Claude Code Routine을 주기적으로 트리거하는 스크립트입니다.

## 동작

매일 KST 기준 `07:05`, `12:05`, `17:05`, `22:03`에 지정된 Anthropic API 엔드포인트에 POST 요청을 보냅니다.

## 환경변수

| 변수              | 설명               |
|-----------------|------------------|
| `TRIGGER_URL`   | 트리거 엔드포인트 URL    |
| `TRIGGER_TOKEN` | Anthropic API 토큰 |

## 배포

GitHub Secrets에 `SSH_HOST`, `SSH_USERNAME`, `SSH_PASSWORD`, `TRIGGER_URL`, `TRIGGER_TOKEN`을 설정한 뒤 `main` 브랜치에 push하면 자동으로 서버에 배포됩니다.

## 로컬 실행

```bash
pip install -r requirements.txt
TRIGGER_URL=... TRIGGER_TOKEN=... python trigger.py
```

## License

MIT
