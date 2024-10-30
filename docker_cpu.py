import subprocess
import json
import os

# 컨테이너의 CPU 할당량 설정
cnt = 2

# Docker stats 명령어 실행
r = subprocess.check_output(['docker', 'stats', 'ham-blog-1', '--no-stream', '--format', '{{ json . }}'])

# JSON 문자열을 딕셔너리로 변환
stats = json.loads(r.decode("utf-8"))

# CPU 사용량을 숫자로 변환하고 조건 평가
cpu_usage = float(stats["CPUPerc"].strip('%'))  # '%'를 제거하고 float로 변환

while True:
    if cpu_usage <= 0.01:
    #docker compose up -d --scale blog=1
        subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={cnt}'], capture_output=True, text=True)
        print(f"CPU {cnt} 만큼 할당되었습니다.")
    else:
        print("CPU 사용량이 0.01% 미만입니다.")


#if r.returncode == 0:
#    print(f"{container_name}의 CPU 할당량이 {cpu_scale}로 업데이트되었습니다.")
#else:
#    print(f"오류 발생: {r.stderr.strip()}")

os.system("sleep 10")
