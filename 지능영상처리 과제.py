import cv2
import numpy as np

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ','ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

cnt = 0


def korean_to_be_englished(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            ## 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가')) // 588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    return r_lst

base = np.zeros((256,768,3), np.uint8)
base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)

text_l = korean_to_be_englished("이것은 문장이다")
base_x, base_y = 0, 0
base_x_ny = 25
    
for s_lst in text_l:
    files = []
    print(s_lst)
    if len(s_lst) == 3:
        files.append("./Font/1-first/" + str(CHOSUNG_LIST.index(s_lst[0])+1).zfill(2) + ".png")
        files.append("./Font/2-mid/" + str(JUNGSUNG_LIST.index(s_lst[1])+1).zfill(2) + ".png")
        if(JONGSUNG_LIST.index(s_lst[2]) != 0):
            files.append("./Font/3-last/" + str(JONGSUNG_LIST.index(s_lst[2])-1).zfill(2) + ".png")
    else:
        continue
    cnt = 0
    for file in files:
        print(file)
        src = cv2.imread(file)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        cnt += 1
        ret, res = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

        # 2
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(res)
        print(int(ret))

        dst = np.zeros(src.shape, dtype=src.dtype)
        for i in range(1, int(ret)):  # 분할영역 표시
            r = np.random.randint(256)
            g = np.random.randint(256)
            b = np.random.randint(256)
            dst[labels == i] = [b, g, r]

        
        if cnt == 1:
            for i in range(1, int(ret)):
                x, y, width, height, area = stats[i]
                cv2.rectangle(dst, (x, y), (x + width, y + height), (0, 0, 255), 2)
                roi = res[y:y + height, x:x + width]
                print(base_y,height,base_x,width)
                base[base_y:base_y + height, base_x:base_x + width] = roi.copy()
                base_x += 20
            base_x += int(width/2)
        elif cnt == 2:
            for i in range(1, int(ret)):
                x, y, width, height, area = stats[i]
                cv2.rectangle(dst, (x, y), (x + width, y + height), (0, 0, 255), 2)
                roi = res[y:y + height, x:x + width]
                print(base_y,height,base_x,width)
                if not (s_lst[1] in ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',] ):
                    base_x = base_x + int(width/2)
                    base[base_y:base_y + height, base_x:base_x + width] = roi.copy()
                    base_x += width +20
                else:
                    base_x = base_x - width - 10                
                    base[base_y+35:base_y+35 + height, base_x:base_x + width] = roi.copy()    
                    base_x += width +20
                
        else:
            base_y += 50
            for i in range(1, int(ret)):
                x, y, width, height, area = stats[i]
                cv2.rectangle(dst, (x, y), (x + width, y + height), (0, 0, 255), 2)
                roi = res[y:y + height, x:x + width]                
                print(base_y,height,base_x_ny,width)
                base[base_y:base_y + height, base_x_ny:base_x_ny + width] = roi.copy()
            base_y -= 50
            base_x_ny += width
        
        
    base_x_ny += int(base_x/2)
cv2.imshow('base', base)
cv2.waitKey()
cv2.destroyAllWindows()
