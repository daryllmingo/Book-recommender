import pickle
import streamlit as st
import numpy as np

st.set_page_config(page_title="Book Recommender System", layout="wide")
model = pickle.load(open('artifacts/model.pkl', 'rb'))
books_name = pickle.load(open('artifacts/books_name.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))


st.markdown("""
    <style>
        
        body {
            font-family: Arial, sans-serif;
        }


        .header {
            font-size: 48px;
            color: #dde8a9; 
            text-align: center;
            margin-top: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); 
        }
        .s_head{
            font-size: 32px;
            color:  #94d5d6;
            text-align: justify;
            margin-top: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); 
                
        }

        .css-18e3th9 {
            background-color: rgba(243, 244, 246, 0.9); 
        }

       
        .book-title {
            font-size: 16px;
            font-weight: bold;
            color: #512f87; 
        }
    </style>
""", unsafe_allow_html=True)


st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Home", "Recommend Books"])


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])
    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)
    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_url.append(url)

    return poster_url


def recommend_books(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=7)

    poster_url = fetch_poster(suggestion)
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    return books_list, poster_url

if pages == "Home":
    st.markdown('<div class="header">Welcome to the Book Recommender System</div>', unsafe_allow_html=True)
    st.markdown('<div class="s_head">Find your next favorite book! Go to the Recommend Books page to get started.</div>', unsafe_allow_html=True)
    
elif pages == "Recommend Books":
    st.markdown('<div class="header">Book Recommender System</div>', unsafe_allow_html=True)
    
    selected_books = st.selectbox("Search for books", books_name)
    if st.button('Show Recommendation'):
        recommendation_books, poster_url = recommend_books(selected_books)
        cl1, cl2, cl3, cl4, cl5, cl6 = st.columns(6)

        with cl1:
            st.markdown(f'<div class="book-title">{recommendation_books[1]}</div>', unsafe_allow_html=True)
            st.image(poster_url[1])
        with cl2:
            st.markdown(f'<div class="book-title">{recommendation_books[2]}</div>', unsafe_allow_html=True)
            st.image(poster_url[2])
        with cl3:
            st.markdown(f'<div class="book-title">{recommendation_books[3]}</div>', unsafe_allow_html=True)
            st.image(poster_url[3])
        with cl4:
            st.markdown(f'<div class="book-title">{recommendation_books[4]}</div>', unsafe_allow_html=True)
            st.image(poster_url[4])
        with cl5:
            st.markdown(f'<div class="book-title">{recommendation_books[5]}</div>', unsafe_allow_html=True)
            st.image(poster_url[5])
        with cl6:
            st.markdown(f'<div class="book-title">{recommendation_books[6]}</div>', unsafe_allow_html=True)
            st.image(poster_url[6])


