import urllib.request, json

data = {
    'question': '이전에 제안했던 1인 개발 모바일 앱 중, "AI 기반 나만의 맞춤 뉴스/콘텐츠 큐레이션 앱"의 구체적인 아키텍처, 기술 스택, 그리고 핵심 기능 구현 방법을 구체적으로 설계해줘',
    'mode': 'accurate'
}

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/compare',
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

resp = urllib.request.urlopen(req, timeout=600)
result = json.loads(resp.read().decode('utf-8'))

with open('test_result_deep.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Test complete. Result saved to test_result_deep.json")
