from flask import Flask, request, render_template

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# 현재는 GET만 허용되었다.
# POST까지 허가를 요청한다면 -> 추가 코드 필요...
# @app.route('/login')  <- GET 만 허가 된것..
# 1개의 url에서 GET방식과 POST방식을 모두 지원하고 싶다 -> Restful 방식 : url을 최소로 사용..

@app.route('/Rolling_in_the_dog/notice', methods=['GET', 'POST'])  # GET, POST 모두 허가
def RITD_Notice():
    # 분기
    if request.method == 'GET':  # GET방식으로 들어오면..
        return render_template('Rolling_in_the_dog/notice.html')
    else:
        return 'POST 방식으로 데이터가 잘 전달 됨.'


@app.route('/Rolling_in_the_dog/TermsOfService', methods=['GET', 'POST'])  # GET, POST 모두 허가
def RITD_TermsOfService():
    # 분기
    if request.method == 'GET':  # GET방식으로 들어오면..
        return render_template('Rolling_in_the_dog/TermsOfService.html')
    else:

        return 'POST 방식으로 데이터가 잘 전달 됨.'


@app.route('/my_house_puppy/TermsOfService', methods=['GET'])  # GET, POST 모두 허가
def myHousePuppyTermsOfserive():
    # 분기
    if request.method == 'GET':  # GET방식으로 들어오면..
        return render_template('my_house_puppy/TermsOfService.html')
    else:
        return render_template('my_house_puppy/TermsOfService.html')

@app.route('/my_house_puppy/notice', methods=['GET'])  # GET, POST 모두 허가
def myHousePuppyNotice():
    # 분기
    if request.method == 'GET':  # GET방식으로 들어오면..
        return render_template('my_house_puppy/notice.html')
    else:
        return render_template('my_house_puppy/notice.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
