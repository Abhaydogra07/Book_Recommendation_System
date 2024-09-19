from flask import Flask,render_template,request
import pickle
import numpy as np
popular_df = pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)
@app.route('/')
def  index():
  return render_template('index.html',book_name = list(popular_df['Book-Title'].values),
                         author=list(popular_df['Book-Author'].values),
                         image=list(popular_df['Image-URL-M'].values),
                         votes=list(popular_df['num_ratings'].values),
                         rating=list(popular_df['avg_rating'].values),
                         )

@app.route('/recommened')
def recommened_ui():
      return render_template('recommened.html')
@app.route('/recommened_books',methods=['post'])
def recommened():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)



    return render_template('recommened.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)