from datetime import time
from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='postgres', user='postgres',password='!QAZ2wsx#EDC', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connection Sucessful')
        break
    except Exception as error:
        print('Connection to database Failed')
        print('Error: ', error)
        time.sleep(2)


my_posts = [{"title" : "title of the post 1", "Content" : "content of post 1", "id" : 1},
            {"title" : "Favourite Animals", "Content" : "I Like Dog", "id" : 2}
            ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

#routing
@app.get("/")
#decorator
def get_User():
    return {"Hello": "Sudip"}

@app.get("/posts")
def get_Post():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_posts(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()

    #For the purpose of saving data into database
    conn.commit()
    
    return {"data" : new_post}
#The order in the column does effect

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail" : post}

@app.get("/posts/{id}")
def get_post(id: int, response : Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str (id)))
    fetch_post = cursor.fetchone()
    print(fetch_post)
    if not fetch_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with ID: {id} was not Found')
    return{"post_detail" : fetch_post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str (id)))
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesnot found.")

    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    update_post = cursor.fetchone()
    conn.commit()
    
    #if the id is not found : 
    if update_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesnot found.")

    return {"data": update_post}
    