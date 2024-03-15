* Описание API
1. POST /registration в эндпоинт для регистрации нового юзера
Request JSON:
{
    "login": str,
    "password": str,
    "first_name": str,
    "second_name": str,
    "skils": list[str], - навыки пользователя (может быть пустым)
    "company": Optional[str] - название компании
}
Response:
"jwt_token"  

2. POST /authorization авторизация пользователя по токену сессии и данным пользователя
Request JSON:
{
    "login": str,
    "password": str,
    "token": str - jwt_token
}  
Response:  
Возвращает либо 400 с инфой о плохом логине, пароле или токене, либо возвращает новый токен.
3. POST /create_post пользователь создает новый пост
Request JSON:
{
    "name": str - название поста
    "text": str - текст поста
    "tags": list[Tags] - список тегов (PROGRAMMING = 1, PYTHON = 2, BACKEND = 3, EDUCATION = 4, TESTS = 5,CTHULHU = 6)
    "token": str - jwt_token
    "new_likes": Optional[int] - опциональное поле с количеством лайков
    "new_dislikes": Optional[int] - опциональное поле с количество дизлайков
    "new_comments": list[str] - список комментариев
}  
Response: null
4. POST /update_post - обновить информацию о посте
Request JSON:
{
    "post_id": - строка с post_id выданным базой данных
    "name": str - новое или старое имя поста
    "text": str - новое или старое имя тела
    "tags": list[Tags] - список тегов
    "token": str - jwt_token
    "new_likes": Optional[int] - опциональное поле с количеством лайков
    "new_dislikes": Optional[int] - опциональное поле с количеством дизлайков
    "new_comments": list[str] - список новых комментариев
}  
Response: null
5. POST /delete_post - удалить пост по его id
Request JSON:
{
    post_id: - строка с post_id, выданным базой данных
    token: - jwt_token
}
Response: null
6. POST /get_posts - список постов
Request JSON:
{
    "author_id": - id пользователя
    "tags": list[Tags]
    "name_search": Optional[str] - опциональная строка поиска по названию или телу
    "pagination_current": int - текущая страница
}
Response JSON:
{
    "posts": Post,
    "new_pagination": int, - новая страница
}
Post {
    post_id: Optional[Any] - post_id выданный бд
    name: str - название поста
    text: str - текст поста
    author_id: Optional[Any] - id автора поста (юзера)
    tags: List[Tags] - список тегов
    comments: List[str] - список комментариев
    likes: int
    dislikes: int
    time: datetime - время создания поста
}