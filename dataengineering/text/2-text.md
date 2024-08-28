# 2. Text 전처리 정확도 개선

## 1) 기존 상황

{% embed url="<https://thewayaboutme.tistory.com/730>" %}
{% embed url="<https://thewayaboutme.tistory.com/731>" %}

## 2) Prompt 개선

### 1차 prompt

```text
You are a Recipe Ingredient Extractor.
Goal: Extract recipe ingredients and their measurements in a cooking recipe article.

---

# Extraction Instructions
## Extract the ingredients, units, and other details from the given recipe text.
## If a recipe contains multiple dishes, organize the CSV for each dish.
## If there is no recipe in the text, you should respond only "Recipe is not present." without additional explanation.
## **Ingredient** column should contain only the names of the ingredients (e.g., "떡볶이", "양파", "닭고기", "우유", "파슬리", "감자").
## **Unit** column should include units that can be counted (e.g., "개", "묶음", "밥스푼", "티스푼", "T", "t", "g", "kg", "마리", "캔", "가닥", "그람", "팩", "컵", "숟갈", "국자", "리터", "꼬집", "바퀴", "뿌리").
## **ETC** column should include any ambiguous or non-specific details that don't fit into the **Ingredient** or **Unit** columns (e.g., "약간", "조금").
## You should only put uncountable units into **ETC** and put all countable units into **Unit**.
 

## Example Input:

김대석 셰프의 29년 노하우를 모두 공개합니다. 
외식업을 처음 시작하는 분들에게 많은 도움이 되었으면 좋겠습니다.

레시피:
- 양파 1개
- 소금 약간
- 닭고기 500g
- 올리브유 2스푼
- 파슬리 조금
- 감자 3개
- 참치액젓 1T
- 정수물 8과1/3컵
- 버터 약 1큰술
- 소면 (500원 동전만큼)
- 까나리액젓 1스푼(9g)

## Example Output:
| Ingredient | Unit       | ETC        |
|------------|------------|-------------|
| 양파       | 1개        |             |
| 소금       |            | 약간        |
| 닭고기     | 500g       |             |
| 올리브유   | 2스푼      |             |
| 파슬리     |            | 조금        |
| 감자       | 3개        |             |
| 참치액젓   | 1T         |             |
| 정수물     | 8과1/3컵   |             |
| 버터       | 약 1큰술   |             |
| 소면       |            | 500원 동전만큼 |
| 까나리액젓 | 1스푼(9g)  |             |

---

## Example Input:
[어남선생 레시피] 만 원으로 치킨 만들어 먹자! 날개치킨★매콤한 핫윙을 집에서!

#신상출시편스토랑 #편스토랑 #음식 #푸드 #먹방 #편의점 #메뉴 #신상 #Fun-Staurant 
 

----------------------------------------------
        ▶ Homepage : https://www.kbs.co.kr/
        ▶ Wavve : https://www.wavve.com/
        ▶ Youtube : 
   / @kbsent  
----------------------------------------------



## Example Output:

Recipe is not present.
 
---

## Example Input:

정확한 물량과 조리법, 표고버섯 소고기  죽, 이런맛은 죽집에 없습니다.  #소고기, #죽, #최고, #완벽한, #표고버섯, #준티비, #JUNTV, #porridge, 

재료 2 인분  /  ingredients for 2 servings
쌀 320g   rice
소고기 홍두깨살 육전용  80g-100g  (식욕이 없으신 분들)  beef  round rump  (Those who have no appetite)
소고기 홍두깨살 육전용  40g   (몸이 아프신 분들)   beef   round rump    (Those who are sick)
건표고버섯 2개  dried Pyogo mushroom (dried shiitake)  (ea)
파    1줄기  green onion  (stalk)
마늘 4개     garlic (clove)
소금 salt
간장 soy sauce
참기름        sesame oil

Business Email: juntvrecipe@gmail.com
 
Twin Musicom의 Canon and Variation에는 크리에이티브 커먼즈 저작자 표시 4.0 라이선스가 적용됩니다. https://creativecommons.org/licenses/...

아티스트: http://www.twinmusicom.org/

## Example Output:

| Ingredient | Unit       | ETC        |
|------------|------------|-------------|
| 쌀       | 320g        |             |
| 소고기 홍두깨살       |     80g-100g       |         |
| 건표고버섯     | 2개       |             |
| 파   | 1줄기      |             |
| 마늘     |     4개       |         |
|소금   |    |       |
|간장 |      |       |
|참기름 |       |       |

---

# Recipe Text

 
```

- prompt에 정확한 instruction을 추가하였고, input과 output을 명확하게 알려주었습니다.
- 또한 few-shot learning을 위해 prompt에 적절한 example을 추가하였습니다.
- 여러 음식이 나오는 경우 음식마다 분류하도록 하였고, 컬럼명은 Ingredient, Unit, ETC로 나누어서 분류하도록 하였습니다. (추후 수정 가능, 파싱을 위한 적절한 output 형태 고민중)
- Ingredient는 재료명이고, Unit은 명확한 단위를 넣도록 하였습니다. ETC에는 애매모호한 "조금", "적당량" 등을 넣도록 하였습니다.
- text에 recipe가 없는 경우 "Recipe is not present." 라고 출력하도록 하였습니다.

### 수정한 prompt로 분류한 예시

- 랜덤 추출한 sample들의 input, output을 적어보았습니다.

- input

```
김대석 셰프의 31년 노하우를 공개합니다.
오늘은 소갈비찜 레시피를 알려 드리겠습니다.

[재료]
소갈비 2kg(3인기준)
대파 1대, 꽈리고추 7개
생표고버섯 3개, 밤 5개, 대추 5개, 당근 1개
건고추 2개, 감초 1개, 홍고추 1개

[초벌 삶기] - 5분
물 1.8리터 + 설탕 1/2컵

[양념]
진간장 1컵, 미림 1/2컵, 간마늘 1스푼
간생강 1/2스푼, 흑설탕 1/2컵(80g), 물 1리터 사용

[믹서기에 갈 재료]
양파 1/2개, 큰 배 1/4개, 물 160mL

[나중에 사용할 재료]
참기름 1스푼, 통깨 1스푼, 후추 2꼬집

#김대석셰프 #소갈비찜
```

- output

```
## 소갈비찜

| Ingredient   | Unit   | ETC        |
|--------------|--------|------------|
| 소갈비       | 2kg    | 3인기준    |
| 대파         | 1대    |            |
| 꽈리고추     | 7개    |            |
| 생표고버섯   | 3개    |            |
| 밤           | 5개    |            |
| 대추         | 5개    |            |
| 당근         | 1개    |            |
| 건고추       | 2개    |            |
| 감초         | 1개    |            |
| 홍고추       | 1개    |            |
| 물           | 1.8리터| 초벌 삶기  |
| 설탕         | 1/2컵  | 초벌 삶기  |
| 진간장       | 1컵    | 양념       |
| 미림         | 1/2컵  | 양념       |
| 간마늘       | 1스푼  | 양념       |
| 간생강       | 1/2스푼| 양념       |
| 흑설탕       | 1/2컵  | 양념, 80g  |
| 물           | 1리터  | 양념       |
| 양파         | 1/2개  | 믹서용     |
| 큰 배        | 1/4개  | 믹서용     |
| 물           | 160mL  | 믹서용     |
| 참기름       | 1스푼  | 나중      |
| 통깨         | 1스푼  | 나중      |
| 후추         |        | 2꼬집     |
```

- input

```
가자미 구이
겉은 바삭
속은 촉촉하게
굽고
비린내없이
기름도 튀지
않게 굽는 비법
알려드려요

#가자미구이 #생선구이
#비린내없이굽는비법
```

- output

```
Recipe is not present.
```

- input

```
아침저녁으로 쌀쌀한 이쯤에서
입맛 확~~ 살리는 영양만점!!
콩비지찌개 어떠신가요.
전문식당 보다도 더 맛있게
보글보글 끓였습니다.

🔶 콩비지찌개에 사용된 재료
  1. 콩비지 : 400g
  2. 익은 김치 : 350g
  3. 돼지고기(앞다리살) : 350g
  4. 대파 : 1개(80g)
  5. 김칫국물 : 130g
  6. 청양고추 : 3개(26g)
  7. 식용유 : 숟가락으로 2개
  8. 다진 마늘 : 숟가락으로 1개
  9. 고춧가루 : 숟가락으로 1/2 (+2/3)
10. 물 : 800mL
11. 새우젓
@ 숟가락 = 10mL 

#후다닥공구TV #콩비지찌개  #비지찌개
```

- output

```
| Ingredient   | Unit      | ETC   |
|--------------|-----------|-------|
| 콩비지       | 400g      |       |
| 익은 김치    | 350g      |       |
| 돼지고기(앞다리살) | 350g      |       |
| 대파         | 1개       | 80g   |
| 김칫국물     | 130g      |       |
| 청양고추     | 3개       | 26g   |
| 식용유       | 숟가락 2개 |       |
| 다진 마늘    | 숟가락 1개 |       |
| 고춧가루     | 숟가락 1/2 | +2/3  |
| 물           | 800mL     |       |
| 새우젓       |           |       |
```

- input

```
#에드워드권#함박스테이크레시피#함바그
[레시피]
- 패티 만들기
1. 양파 1/6개를 다져주세요.
2. 달궈진 팬에 식용유를 둘러주세요.
3. 양파를 팬에 넣어주세요.
4. 양파가 어느정도 숨이 죽으면 그릇에 양파를 담아주세요.
5. 소고기 150g, 돼지고기 150g을 뭉쳐주세요.
6. 소금 간, 후추 간을 해주세요.
7. 건식 빵가루를 한 큰술 반 뿌려주세요.
8. 양파와 잘 섞이도록 버무려주고 패티 모양으로 잘 뭉쳐주세요.
9. 달궈진 팬에 식용유 5 숟가락을 부어주세요.
10. 팬에 패티를 올려주세요.
11. 양쪽 면이 잘 익혀주세요.

-소스 만들기
12. 달궈진 팬에 올리브오일 2큰술을 둘러줍니다.
13. 양송이 버섯 2개를 썰어주세요.
14. 마늘 2개를 썰어줍니다.
15. 팬에 마늘을 넣어줍니다.
16. 팬에 양파를 넣어줍니다.
17. 팬에 양송이 버섯을 넣어줍니다.
18. 올리브오일 2 숟가락을 둘러줍니다.
19. 돈까스 소스를 5큰술 넣어주세요.
20. 바비큐 소스도 5큰술 넣어주세요.
21. 물을 7큰술 넣어주세요.

-계란후라이 하기
22. 기름을 둘러주세요.
23. 계란을 깨주세요.

여러분 하이루~ 강원도 영월출신
쉐프 권영민이라고 합니다~😋
다들 에드워드 권이라고 부르는데
여기선 그냥 영민씨 라고 불러주셔요~ㅋㅋ
앞으로 털털한 동네형처럼 집에서
간단히 먹을수 있는 것들 해드릴게요^^

비즈니스문의
이메일: eddyhousetube@naver.com
```

- output

```
### 함박스테이크 패티
| Ingredient | Unit       | ETC        |
|------------|------------|-------------|
| 양파       | 1/6개      |             |
| 식용유     |            |             |
| 소고기     | 150g       |             |
| 돼지고기   | 150g       |             |
| 소금       |            | 간          |
| 후추       |            | 간          |
| 건식 빵가루 | 1.5큰술   |             |

### 소스
| Ingredient | Unit       | ETC        |
|------------|------------|-------------|
| 올리브오일 | 4큰술      |             |
| 양송이 버섯 | 2개       |             |
| 마늘       | 2개        |             |
| 양파       |            |             |
| 돈까스 소스| 5큰술      |             |
| 바비큐 소스| 5큰술      |             |
| 물         | 7큰술      |             |

### 계란후라이
| Ingredient | Unit       | ETC        |
|------------|------------|-------------|
| 기름       |            |             |
| 계란       |            |             |
```

- input

```
맛연사 셰프 30년 노하우 공개 합니다.가정용, 업소용레시피를 집에서도 쉽게
만들수 있도록 계량화 했습니다.맛있는 황금레시피 맛을 연구하는 사람들
#칼국수 #들깨수제비 #들깨칼국수
칼국수 전문점 보다 더 맛있게 간단하게 들깨칼국수 만드는 방법!들깨 수제비

식당창업/ 업소용레시피/ 협찬 상담문의: 010, 2321, 6322 주세요(맛연사)

맛연사냉면(밀키트) 네이버 스마트 스토어 구매 가능하십니다. 
https://smartstore.naver.com/monomoa/...

냉면 업소용 벌크 : https://me2.do/Gz2vi4nB (5kg 벌크/0.8mm기계면사리/맛보장)
가정용 냉면 밀키트 : https://me2.do/G4wUWAo0 
구매문의  👉전화문의 1688-4025 (가정용밀키트, 업소용,식당)
업소용 벌크 제품의 경우 아래 구성으로 판매하고 있으니 페이지 둘러 
보시면 됩니다.   업소용 벌크 제품 구매시 "사업자 등록번호"를 필히
기재하시면 구매하실 수 있습니다.   참고해 주세요!!!

맛연사/  틱톡   https://www.tiktok.com/@tastespeaker?...
맛연사/  카페   https://cafe.naver.com/53dldirl
맛연사/  인스타그램  
  / sinheeyong739  
맛연사/  블로그  https://blog.naver.com/tg778
```

- output

```
Recipe is not present.
```

- input

```
수수팥단자

예전부터 붉은 색은 재앙을 막아준다는 생각으로 붉은 팥을 사용한 수수팥떡은 백일떡, 돌떡, 열살까지의 생일떡으로 빠지지 않았다ᆢ

*준비해요~
수수가루 200g, 찹쌀가루(,소금간이 된 방앗간 쌀) 200g, 설탕 40g, 소금 2g, 뜨거운 물 약 100g
팥고물 3컵 (만드는 법 ᆢ 
   • 떡공예 명인의 팥고물 만들기/팥시루떡 만들기  
)

*만들어요~
1. 수수가루와 찹쌀가루는 함께 섞어서 체에 내려 준다

2. 가루에 소금과 설탕을 고르게 섞고 뜨거운 물로 익반죽을 한다. 물은 한꺼번에 넣지 않고 조금씩 나눠 넣으면서 부드럽게 반죽한다 (조금 떼
서 동그랗게 빚은 후 손바닥에 눌렀을 때 갈라짐이 없도록한다

3. 반죽은 비닐이나 면보로 덮어서 30분 정도 그대로 둔다

4. 반죽을 직경 2cm 정도의 크기로 동그랗게 빚어서 끓는 물에 넣어서 떠오르고 1분 정도 지나면 꺼내서 찬물에 넣는다

5. 쟁반에 설탕을 살짝 뿌려 놓고 찬물에서 건져낸 경단을 설탕에 굴려서 팥고물을 묻혀낸다

*팥고물 만들기ᆢ
   • 떡공예 명인의 팥고물 만들기/팥시루떡 만들기  
인스타그램 
  / kimsuyeong_h
```

- output

```
| Ingredient     | Unit | ETC   |
|----------------|------|-------|
| 수수가루       | 200g |       |
| 찹쌀가루       | 200g | 소금간이 된 방앗간 쌀 |
| 설탕           | 40g  |       |
| 소금           | 2g   |       |
| 뜨거운 물      | 100g | 약    |
| 팥고물         | 3컵  |       |
```

- input

```
’좋아요+댓글+구독'은 컨텐츠 제작에 큰 힘이 됩니다! 

●재료
잔멸치 50g
식용유 2Tbsp
진간장(양조간장) 1tsp
맛술 2Tbsp
흰설탕 1Tbsp
간마늘 1/2tsp

올리고당 2Tbsp
참기름 1/2Tbsp


●계량도구를 사용하시는 것이 좋습니다
Tbsp: Tablespoon(15ml)
tsp: teaspoon(5ml)
1컵(C)= 200ml

●이 영상은 ‘딸을위한레시피’에서 제작하였으며, 저작권법의 보호를 받고 있습니다. 
레시피 사용시 출처를 밝혀주세요. 
영상의 상업적 이용, 2차 편집 및 재 업로드를 금지합니다.
요+댓글+구독'은 컨텐츠 제작에 큰 힘이 됩니다!
```

- output

```
| Ingredient | Unit     | ETC |
|------------|----------|-----|
| 잔멸치      | 50g      |     |
| 식용유      | 2Tbsp    |     |
| 진간장      | 1tsp     |     |
| 맛술        | 2Tbsp    |     |
| 흰설탕      | 1Tbsp    |     |
| 간마늘      | 1/2tsp   |     |
| 올리고당    | 2Tbsp    |     |
| 참기름      | 1/2Tbsp  |     |
```

### 최종 prompt

- ingredient: 재료명 (string)
- quantity: 양 (int or float)
- unit: 단위 (string)
- vague: 애매한 단위 (string)
- portions: 인분 (int)

```text
"""
You are a Recipe Ingredient Extractor.
Goal: Extract recipe ingredients and their measurements in a cooking recipe article. We want to extract recipe information to help people buy ingredients at the lowest cost.

---

# Extraction Instructions
## Extract the ingredients, quantity, unit, vague and portion from the given recipe text.
## If a recipe contains multiple dishes, combine them into one.
## If there is no recipe in the text, you should respond only "empty" without additional explanation.

## **ingredient**: **ingredient**  should contain only the names of the ingredients (e.g., "떡볶이", "양파", "닭고기", "우유", "파슬리", "감자").
## **quantity** : **quantity** should include the numeric value (**int** or **float** type) that represents the amount of the ingredient. (e.g. 2, 0.5, 300).  For ranges like "80g-100g," use only the **numeric** values and store them in the **volume** column. . (e.g.  80g-100g -> 100, 100~150g -> 150).  For quantities like "1/2", use the decimal equivalent (e.g., 0.5). For fractions such as "½" and other fractional notations, convert them to their decimal forms and record them accordingly.
## **unit**: **unit**  should include the string unit . (e.g. "개", "묶음", "밥스푼", "티스푼", "T", "t", "g", "kg", "마리", "캔", "가닥", "그람", "팩", "컵", "숟갈", "국자", "리터", "꼬집", "바퀴", "뿌리").
## **vague**:  **vague**  should include any ambiguous or non-specific details that don't fit into the  **unit**  (e.g., "약간", "조금", "쪼금", "일부", "적당량"). Only include ambiguous units, and if not available, insert an empty string.
##  **portions**: If portion information is available, record the number of portions as a numeric value in the "portions". if not, default to 1. (e.g., {"portions": 1} or {"portions": 2}).
 
---

## Example Input:
김대석 셰프의 29년 노하우를 모두 공개합니다. 
외식업을 처음 시작하는 분들에게 많은 도움이 되었으면 좋겠습니다.
레시피:
- 양파 1개
- 소금 약간
- 닭고기 500g
- 올리브유 2스푼
- 파슬리 조금
- 감자 3개
- 참치액젓 1T
- 정수물 8과1/3컵
- 버터 약 1큰술
- 소면 (500원 동전만큼)
- 까나리액젓 1스푼(9g)


## Example Output:
{"portions": 1, "items":  [{"ingredient": "양파", "quantity" : 1, "unit" : "개", "vague":  ""}, {"ingredient": "소금", "quantity" : 0, "unit" : "", "vague":  "약간"}, {"ingredient": "닭고기", "quantity" : 500, "unit" : "g", "vague":  ""}, {"ingredient": "올리브유", "quantity" : 2, "unit" : "스푼", "vague":  ""}, {"ingredient": "파슬리", "quantity" : 0, "unit" : "", "vague":  "조금"}, {"ingredient": "감자", "quantity" : 3, "unit" : "개", "vague":  ""}, {"ingredient": "참치액젓", "quantity" : 1, "unit" : "T", "vague":  ""}, {"ingredient": "정수물", "quantity" : 8.3, "unit" : "컵", "vague":  ""}, {"ingredient": "버터", "quantity" : 1, "unit" : "큰술", "vague":  ""}, {"ingredient": "소면", "quantity" : 0, "unit" : "", "vague":  ""}, {"ingredient": "까나리액젓", "quantity" : 1, "unit" : "스푼", "vague":  ""}]}

---

## Example Input:
[어남선생 레시피] 만 원으로 치킨 만들어 먹자! 날개치킨★매콤한 핫윙을 집에서!
 
#신상출시편스토랑 #편스토랑 #음식 #푸드 #먹방 #편의점 #메뉴 #신상 #Fun-Staurant 

----------------------------------------------
        ▶ Homepage : https://www.kbs.co.kr/
        ▶ Wavve : https://www.wavve.com/
        ▶ Youtube : 
   / @kbsent  
----------------------------------------------

## Example Output:
empty

---

## Example Input:
정확한 물량과 조리법, 표고버섯 소고기  죽, 이런맛은 죽집에 없습니다.  #소고기, #죽, #최고, #완벽한, #표고버섯, #준티비, #JUNTV, #porridge, 
재료 2 인분  /  ingredients for 2 servings
쌀 320g   rice
소고기 홍두깨살 육전용  80g-100g  (식욕이 없으신 분들)  beef  round rump  (Those who have no appetite)
소고기 홍두깨살 육전용  40g   (몸이 아프신 분들)   beef   round rump    (Those who are sick)
건표고버섯 2개  dried Pyogo mushroom (dried shiitake)  (ea)
파    1줄기  green onion  (stalk)
마늘 4개     garlic (clove)
소금 salt
간장 soy sauce
참기름        sesame oil

Business Email: juntvrecipe@gmail.com

Twin Musicom의 Canon and Variation에는 크리에이티브 커먼즈 저작자 표시 4.0 라이선스가 적용됩니다. https://creativecommons.org/licenses/...
아티스트: http://www.twinmusicom.org/

## Example Output:
{"portions": 2, "items":  [{"ingredient": "쌀", "quantity" : 320, "unit" : "g", "vague":  ""}, {"ingredient": "소고기 홍두깨살 육전용", "quantity" : 100, "unit" : "g", "vague":  ""}, {"ingredient": "건표고버섯", "quantity" : 2, "unit" : "개", "vague":  ""}, {"ingredient": "파", "quantity" : 1, "unit" : "줄기", "vague":  ""}, {"ingredient": "마늘", "quantity" : 4, "unit" : "개", "vague":  ""}, {"ingredient": "소금", "quantity" : 0, "unit" : "", "vague":  ""},  {"ingredient": "간장", "quantity" : 0, "unit" : "", "vague":  ""}, {"ingredient": "참기름", "quantity" : 0, "unit" : "", "vague":  ""}]}
 
---

# Recipe Text
"""
```
