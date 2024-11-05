import subprocess
import json
import os
import time


# 라인 알림 전송
def send_line_noti(message):
    url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_NOTI_TOKEN', 'NULL')
    headers = {'Authorization': 'Bearer ' + token}

    data = {
        "message": message
    }

    resp = requests.post(url, headers=headers, data=data)


#Docker CPU 가져오기
def get_cpu(num):
    tmp = []
    for num in range(1, num+1):
        r = subprocess.check_output(['docker', 'stats', f'ham-blog-{num}', '--no-stream', '--format', '{{ json . }}'])
        stats = json.loads(r.decode("utf-8"))
        cpu_usage = float(stats["CPUPerc"].strip('%')) 
        tmp.append(cpu_usage)

      
    return tmp

def set_scale(num=1):
    cpu = get_cpu(num)

    while True:
        if len(cpu) >= 1 and len(cpu) <=5:
            if cpu[0] >= 0.01:
                num += 1
                subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={num}'])
                print(f"scale={num} 입니다.")
                time.sleep(10)
                set_scale(num)
                send_line_noti("스케일 아웃이 진행되었습니다.")

            else:
                num -= 1
                subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={num}'])
                time.sleep(10)
                set_scale(num)
                send_line_noti("스케일 인이 진행되었습니다.")
        
        elif len(cpu) > 5:
            if num > 1:
                num -= 1
                subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={num}'])
                time.sleep(10)
                set_scale(num)
                send_line_noti("스케일 인이 진행되었습니다.")

            else:
                print("더이상 내릴 수 없습니다.")
                time.sleep(10)
        
        else:
            print("CPU 정보가 없습니다.")
            time.sleep(10)

set_scale()
