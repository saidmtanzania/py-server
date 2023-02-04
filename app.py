from flask import Flask, request, Response
import pdfplumber

app = Flask(__name__)

todos = []

@app.route("/", methods=["GET"])
def get_todos():
    return {"todos": todos}

@app.route("/todo", methods=["POST"])
def add_todo():
    todo = request.get_json()
    todos.append(todo)
    return {"message": "Todo added successfully"}

@app.route("/<int:index>", methods=["PUT"])
def update_todo(index):
    todo = request.get_json()
    todos[index] = todo
    return {"message": "Todo updated successfully"}

@app.route("/<int:index>", methods=["DELETE"])
def delete_todo(index):
    todos.pop(index)
    return {"message": "Todo deleted successfully"}

@app.route('/pdf/', methods=['POST'])
def add_pdf():
    pdf1 = request.files.get('file1').read()
    pdf2 = request.files.get('file2').read()

    file_name1 = request.form.get('file1Name')
    file_name2 = request.form.get('file2Name')

    with open(f'./pdf/{file_name1}', 'wb') as f:
        f.write(pdf1)
    with open(f'./pdf/{file_name2}', 'wb') as f:
        f.write(pdf2)

    result = []
    with pdfplumber.open(f'./pdf/{file_name1}') as pdf:
        for i in range(0, len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text(x_tolerance=1)
            results = " " + text
            result.append((results))

    string_results = "".join(result)
    lines = string_results.split('\n')
    data = []
    for ele in lines:
        if ele.strip():
            data.append(ele)
    student_reg_phone = []
    for i in range(0, len(data)):
        student = data[i].split(sep=None, maxsplit=-1)
        student_reg_phone.append((student))
    result = []
    with pdfplumber.open(f'./pdf/{file_name2}') as pdf:
        for i in range(0, len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text(x_tolerance=1)
            results = " " + text
            result.append((results))
    string_results = "".join(result)

    lines = string_results.split('\n')
    data = []
    for ele in lines:
        if ele.strip():
            data.append(ele)
    
    student_info = []
    for i in range(0, len(data)):
        student = data[i].split(sep=None, maxsplit=-1)
        student_info.append((student[-3:]))
    import pandas as pd
    data = pd.DataFrame(student_info, columns=['RegNumber', 'Year_study', 'Ada'])
    data = data.replace(',', '', regex=True)
    reg_phone = pd.DataFrame(student_reg_phone, columns=['RegNumber', 'phone_number'])
    data.insert(3, column='page_number', value='Nan')
    new_page = data[data['Ada'].isna()].index.tolist()
    new_page.insert(0, 0)

    for i in range(0, (len(new_page) - 1)):
        data['page_number'][new_page[i]:new_page[i + 1]] = data['RegNumber'][
            new_page[i + 1]]
    data['Message'] = 'Registration number:' + data['RegNumber'] + ',' + 'Ada :' + data['Ada'] + ',' + 'page number: ' + data['page_number'].astype(str)
    result = data.merge(reg_phone, on='RegNumber')
    result = result.drop(['RegNumber', 'Ada', 'Year_study', 'page_number'],axis=1)
    result = result.dropna()

    result.to_json("./res/Result45.json", orient='records')
   
    return Response(result.to_json(orient='records'), mimetype='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)