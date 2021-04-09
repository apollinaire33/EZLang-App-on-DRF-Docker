Docker-compose: move to project folder in your bash-terminal of Docker and run command:<br>
docker-compose up<br>
<br>
Use http://192.168.99.100:8000/ to get to the project site<br>
<br>
<br>
API endpoints:<br>
<br>
For getting access to authorized only/author only use Postman/frontend client providing authorization bearer token<br>
<br>
/api/v1/user/signup - Registration(via Postman/frontend client providing "name" "email" "password" in body)<br>
<br>
/api//token/ - Obtaining token for authorization(via Postman/frontend client providing "email" "password" in body)<br>
<br>
/api/v1/user/user_list/ - User List for all<br>
<br>
/api/v1/quiz_main/quizes/id - Quiz administrating for admin only<br>
<br>
/api/v1/quiz_main/filter/(tasked, finished, failed)/ - Quiz filtering list for certain user<br>
<br>
/api/v1/quiz_main/questions/ - Question administrating for admin only<br>
<br>
/api/v1/quiz_main/answers/id - Answer administrating for admin only<br>
<br>
/api/v1/quiz_main/messages/user_answers/id - Creating user answers only by authenticated<br>
<br>
/api/v1/quiz_main/quiz_takers/id - Quiztaker adminstrating for admin only<br>
<br>
/api/v1/howework/admin/id - Homework adminstrating for admin only<br>
<br>
/api/v1/homework/id - Homework list for specific user<br>
<br>
/api/v1/homework/task_load/id - Loading task by user for its homework<br>
