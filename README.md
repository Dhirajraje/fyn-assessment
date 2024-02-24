
# FYN Assessment

A vehicle usage cost pricing calculator.




## Technologies used



![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)


Find more on : [dhiraj.homonovus.in](https://dhiraj.homonovus.in/)
## Initialization

Clone project from git
```bash
  git clone https://github.com/Dhirajraje/fyn-assessment.git
  cd fyn-assessment
```



#### Setting up the backend

I am using `Arch linux` with `linux kernel 6.6` please update the commands as per your host machine. 

Since this is a django project, we recommend to create virtual env.

```bash
python3 -m virtualenv .venv
source ./.venv/bin/activate
```


Install required dependencies using following command

```bash
pip install -r requirements
```
The user (username:`dhirajs`,password:`loremipsum`) is already configured in the tool.

(Optional) To create the new user run follwoing command. username should be at least 4 chars long and password should be 8 chars long.

```bash
python3 manage.py createsuperuser
```

Run the backend service using following command

```bash
python3 manage.py runserver 8000
```
APIs can be viewed at the url: http://localhost:8000/api/schema/swagger-ui/


#### Setting up the frontend

Frontend is written in react and it is located in directory `assessment-fe`

Go to the frontend directory using,

```bash
cd assessment-fe
```

Install required dependencies using 

```bash
npm i
```

Run the frontend service using

```bash
npm run dev -- --open
```

Frontend application can be viewed at url: http://localhost:5173/


## Screenshots

![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h41m04s_screenshot.png)



![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h44m15s_screenshot.png)


![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h44m29s_screenshot.png)



![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h44m47s_screenshot.png)




![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h45m03s_screenshot.png)


![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h45m27s_screenshot.png)




![App Screenshot](https://raw.githubusercontent.com/Dhirajraje/fyn-assessment/master/screenshots/240224_15h43m36s_screenshot.png)