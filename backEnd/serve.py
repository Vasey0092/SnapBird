from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from all import CommonOcr
import time
import os
import json
import random
import zipfile
import base64
import io

from setpath import *
from utils import determine_file_type
from GPT.GPT import chat

app = Flask(__name__)
CORS(app, supports_credentials=True)

fileNames = os.listdir(picPath)+os.listdir(pdfPath) + \
    os.listdir(pptPath)+os.listdir(excelPath)+os.listdir(wordPath)

fileTypes = []
for fileName in fileNames:
    fileTypes.append(determine_file_type(fileName))

print('current fileName:', fileNames)
print('current fileType:', fileTypes)


def get_files_base64_andRemove(directory):  # 从zip提取文件，转base64，并删除源文件
    base64_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as file_to_encode:
                file_content = file_to_encode.read()
                base64_content = base64.b64encode(file_content).decode('utf-8')
                base64_files.append((file, base64_content))
            if os.path.exists(file_path):
                os.remove(file_path)
    return base64_files


def clearDir(directory):  # 清空文件夹
    file_names = os.listdir(directory)
    for item in file_names:
        file_path = os.path.join(directory, item)
        os.remove(file_path)


def handleMutipleOperation(operations):  # 按需调用api，返回文件base64列表
    while operations:  # 将返回的结果提取并存储，改变res路径
        opt = operations.pop(0)
        if opt == '1':  # 模型调用ocr还没想好怎么写，而且目前代码不支持并行操作请求，即每次只能完成一个请求
            try:
                result = recognize()
                result = result.json['results']
            except Exception as e:
                print(e)
        elif opt == '2':
            try:
                print('modal is calling opt2')
                result = table()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '3':
            try:
                print('modal is calling opt3')
                result = cropEnhance()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '4':
            try:
                print('modal is calling opt4')
                result = img_to_word()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '5':
            try:
                print('modal is calling opt5')
                result = pdf_to_word()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '6':
            try:
                print('modal is calling opt6')
                result = pdf_to_excel()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '7':
            try:
                print('modal is calling opt7')
                result = pdf_to_ppt()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '8':
            try:
                print('modal is calling opt8')
                result = pdf_to_image()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '9':
            try:
                print('modal is calling opt9')
                result = word_to_pdf()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '10':
            try:
                print('modal is calling opt10')
                result = excel_to_pdf()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '11':
            try:
                print('modal is calling opt11')
                result = img_to_pdf()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        elif opt == '12':
            try:
                print('modal is calling opt12')
                result = word_to_img()
                clearDir(modelTempPath)
                result = result.json['results']
                for item in result:
                    fileName = item['file_name']
                    file_path = os.path.join(modelTempPath, fileName)
                    file_data = base64.b64decode(item['res'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
            except Exception as e:
                print(e)
        # 不要忘了最后清理modelTemp文件夹
    results = []
    filenames = os.listdir(modelTempPath)
    for filename in filenames:
        with open(os.path.join(modelTempPath, filename), 'rb') as file:
            file_content = file.read()
        file_content = base64.b64encode(file_content).decode('utf-8')
        results.append({
            'file_name': str(random.randint(100, 999))+filename,
            'res': file_content
        })
    clearDir(modelTempPath)
    return results


@app.route('/chat', methods=['GET'])  # 目前缺少文件类型合法性鉴别
def gpt_chat():
    if not fileNames:
        return jsonify({'response': '请先上传文件哦', 'results': []})
    try:
        message = request.args.get('message')
        if not message:
            return jsonify({'error': 'no message carried!'})
        response = chat(message)
        if response:
            try:  # 对gpt模块响应进行处理
                print(response)
                response = json.loads(response)
                if response['type'] == 'operation':
                    results = handleMutipleOperation(
                        response['content'].split(','))

                    return jsonify({'response': '当然可以！以上是您的文件处理结果 :)',
                                    'results': results
                                    })
                elif response['type'] == 'rejection':
                    return jsonify({'response': response['content'], 'results': []})
            except Exception as e:
                print('erro in serve/chat/response_processing', e)
                return jsonify({'response': 'erro in serve/chat/response_processing', 'results': []})
        else:
            print('gpt session is unavilible.')
            return jsonify({'response': 'gpt session is unavilible.', 'results': []})
    except Exception as e:
        print('error in serve/gpt_chat/chat', e)
        return jsonify({'response': 'error in serve/gpt_chat/chat', 'results': []})


@app.route('/upload', methods=['POST'])  # 逐个上传文件，根据文件类型分类存储
def upload_file():
    uploaded_file = request.files['file']
    fileNames.append(uploaded_file.filename)
    print('upload file:', uploaded_file.filename)
    if uploaded_file.filename != '':
        fileType = determine_file_type(uploaded_file.filename)
        fileTypes.append(fileType)
        if fileType == 'images':
            uploaded_file.save(picPath+uploaded_file.filename)
        elif fileType == 'ppt':
            uploaded_file.save(pptPath+uploaded_file.filename)
        elif fileType == 'word':
            uploaded_file.save(wordPath+uploaded_file.filename)
        elif fileType == 'pdf':
            uploaded_file.save(pdfPath+uploaded_file.filename)
        elif fileType == 'excel':
            uploaded_file.save(excelPath+uploaded_file.filename)
        else:
            print('unkown type of file!')
        return jsonify({'message': 'File has been uploaded successfully'})
    return jsonify({'message': 'No file was uploaded'})


@app.route('/delFile', methods=['GET'])  # 单个删除文件
def del_file():
    index = int(request.args.get('index'))
    print('index:', index)
    print('fileupload:', fileNames)
    fileType = fileTypes.pop(index)
    fileName = fileNames.pop(index)
    if fileType == 'images':
        os.remove(picPath+fileName)
    elif fileType == 'ppt':
        os.remove(pptPath+fileName)
    elif fileType == 'word':
        os.remove(wordPath+fileName)
    elif fileType == 'pdf':
        os.remove(pdfPath+fileName)
    elif fileType == 'excel':
        os.remove(excelPath+fileName)
    else:
        print('unkown type of file!')
        return jsonify({'message': 'ubkonwn file'})
    print(fileNames)
    return jsonify({'message': 'File has been removed successfully'})


@app.route('/recognize', methods=['GET'])  # 批量文字识别image->文本
def recognize():
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(picPath)
            dirpath = picPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})

    results = []

    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            texts = common_ocr.recognize()
            if texts:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename,
                    'texts': texts
                })
            else:
                print('something went wrong with main/recognize.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/tableRecognize', methods=['GET'])  # 表格识别image->excel
def table():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(picPath)  # 列出目录下所有文件
            dirpath = picPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            excel = common_ocr.tableRecognize()
            if excel:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.xls',
                    'res': excel
                })
            else:
                print('something went wrong with all/tableRecognize.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/cropEnhance', methods=['GET'])  # 图像切边增强image->image
def cropEnhance():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(picPath)  # 列出目录下所有文件
            dirpath = picPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.crop_enhance_image()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename,
                    'res': res
                })
            else:
                print('something went wrong with all/crop_enhance_image.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/waterMarkRemove', methods=['GET'])  # 去水印image->image
def waterMarkRemove():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(picPath)  # 列出目录下所有文件
            dirpath = picPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.watermark_remove()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename,
                    'res': res
                })
            else:
                print('something went wrong with all/waterMarkRemove.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/word_to_img', methods=['GET'])  # word转image
def word_to_img():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(wordPath)  # 列出目录下所有文件
            dirpath = wordPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.word_to_img()
            if res:
                zip_bytes = base64.b64decode(res)
                # 使用io.BytesIO创建一个类文件对象
                zip_stream = io.BytesIO(zip_bytes)
                # 使用zipfile读取类文件对象
                with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
                    zip_ref.extractall(tempPath)
                base64_files = get_files_base64_andRemove(tempPath)
                for item in base64_files:
                    results.append({
                        'file_name': str(random.randint(100, 999))+item[0]+'.jpg',
                        'res': item[1]
                    })
            else:
                print('something went wrong with all/word_to_img.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/img_to_pdf', methods=['GET'])  # image转pdf
def img_to_pdf():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(picPath)  # 列出目录下所有文件
            dirpath = picPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.img_to_pdf()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.pdf',
                    'res': res,
                })
            else:
                print('something went wrong with all/img_to_pdf.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/excel_to_pdf', methods=['GET'])  # excel转pdf
def excel_to_pdf():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(excelPath)  # 列出目录下所有文件
            dirpath = excelPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.excel_to_pdf()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.pdf',
                    'res': res,
                })
            else:
                print('something went wrong with all/excel_to_pdf.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/word_to_pdf', methods=['GET'])  # word转pdf
def word_to_pdf():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(wordPath)  # 列出目录下所有文件
            dirpath = wordPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.word_to_pdf()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.pdf',
                    'res': res,
                })
            else:
                print('something went wrong with all/word_to_pdf.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/pdf_to_image', methods=['GET'])  # pdf转图片
def pdf_to_image():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(pdfPath)  # 列出目录下所有文件
            dirpath = pdfPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.pdf_to_img()
            if res:
                zip_bytes = base64.b64decode(res)
                # 使用io.BytesIO创建一个类文件对象
                zip_stream = io.BytesIO(zip_bytes)
                # 使用zipfile读取类文件对象
                with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
                    zip_ref.extractall(tempPath)
                base64_files = get_files_base64_andRemove(tempPath)
                for item in base64_files:
                    results.append({
                        'file_name': str(random.randint(100, 999))+item[0]+'.jpg',
                        'res': item[1]
                    })

            else:
                print('something went wrong with all/pdf_to_img.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/pdf_to_ppt', methods=['GET'])  # pdf转ppt
def pdf_to_ppt():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(pdfPath)  # 列出目录下所有文件
            dirpath = pdfPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.pdf_to_ppt()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.ppt',
                    'res': res,
                })
            else:
                print('something went wrong with all/pdf_to_ppt.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/pdf_to_excel', methods=['GET'])  # pdf转excel
def pdf_to_excel():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(pdfPath)  # 列出目录下所有文件
            dirpath = pdfPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.pdf_to_excel()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.xls',
                    'res': res,
                })
            else:
                print('something went wrong with all/pdf_to_excel.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/pdf_to_word', methods=['GET'])  # pdf转word
def pdf_to_word():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(pdfPath)  # 列出目录下所有文件
            dirpath = pdfPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.pdf_to_word()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.doc',
                    'res': res,
                })
            else:
                print('something went wrong with all/pdf_to_word.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


@app.route('/img_to_word', methods=['GET'])  # 图片转word
def img_to_word():
    results = []
    try:
        files = os.listdir(modelTempPath)
        if not files:
            files = os.listdir(picPath)  # 列出目录下所有文件
            dirpath = picPath
        else:
            dirpath = modelTempPath
    except Exception as e:
        return jsonify({'message': 'Error listing input directory', 'error': str(e)})
    for i, filename in enumerate(files):
        file_path = os.path.join(dirpath, filename)
        try:
            common_ocr = CommonOcr(file_path)
            res = common_ocr.img_to_word()
            if res:
                results.append({
                    'file_name': str(random.randint(100, 999))+filename+'.doc',
                    'res': res,
                })
            else:
                print('something went wrong with all/img_to_word.')
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            results.append({
                'file_name': str(random.randint(100, 999))+filename,
                'error': str(e)
            })
    return jsonify({
        'message': 'Files processed successfully',
        'results': results
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)
