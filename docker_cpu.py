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


# 로그 디렉토리를 생성하는 함수
def log_dir():
    log_dir_path = './scale_log'
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)
    return log_dir_path


# 로그 파일을 생성하고 저장하는 함수
def save_log(log_message):
    log_dir_path = log_dir()

    # 현재 시간을 기준으로 파일 이름 생성
    log_file_name = f"log_{time.strftime('%Y%m%d')}.txt"
    log_file_path = os.path.join(log_dir_path, log_file_name)

    # 로그 메시지를 파일에 쓰기
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_message + '\n')


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
    check_time=time.time()

    while True:
        if len(cpu) >= 1 and len(cpu) <5:
            if cpu[0] >= 0.01:
                num += 1
                subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={num}'])
                log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} || ScaleOut || scale: {num} || CPU 사용량: {cpu[0]}%"
                save_log(log_message)
                print(f"scale={num} 입니다.")
                time.sleep(10)
                set_scale(num)
                send_line_noti("스케일 아웃이 진행되었습니다.")

            else:
                num -= 1
                subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={num}'])
                log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} || ScaleIn || scale: {num} || CPU 사용량: {cpu[0]}%"
                save_log(log_message)
                time.sleep(10)
                set_scale(num)
                send_line_noti("스케일 인이 진행되었습니다.")
        
        elif len(cpu) > 4:
            if num > 1:
                num -= 1
                subprocess.run(['docker', 'compose', 'up', '-d','--scale', f'blog={num}'])
                log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} || ScaleIn || scale: {num} || CPU 사용량: {cpu[0]}%"
                save_log(log_message)
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
