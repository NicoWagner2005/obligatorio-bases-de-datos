# Bitácora

Primero planificamos y organizamos el proyecto en jira con una filosofia SCRUM y dividimos los tres pilares principales de nuestro proyecto (base de datos, backend y frontend) en sprints de 1, 2 y 1 semana respectivamente.

Comenzamos creando el respositorio y la estructura del proyecto. Investigamos acerca de docker, especificamente acerca del docker-compose.yaml y como utilizarlo en nuestro proyecto. Creamos el compose.yaml en la carpeta del proyecto y configuramos la base de datos para posteriormente conectarnos desde dataGrip.

Con el contenedor levantado y configurado, nos conectamos a la base de datos desde dataGrip y ejecutamos los comandos de creacion de tablas. Estos comandos los guardamos en un archivo schema.sql asi cuando alguien clone el respositorio y ejecute nuestro compose.yaml con docker automaticamente se le ejecuten los mismos comandos que usamos nosotros para que funcione nuestra aplicación. Esto es porque pusimos en el compose.yaml que los volumenes del contenedor carguen los archivos data y schema.

Con las tablas ya creadas pasamos a crear los datos que vamos a usar para la verificación y demostración de nuestra aplicación. Insertamos en sus respectivas tablas y verificamos que este todo correcto y que nos permita su correcto uso a futuro.


fuentes: https://docs.docker.com - https://fastapi.tiangolo.com - https://pypi.org/project/bcrypt/
--------------------------
## FRONTEND:


Desarrollado con React, incialmente creamos la página de login, intentando ser fiel al estilo de las páginas ya existentes de la UCU. Desde esta página se podrá iniciar sesión para acceder a los distintos servicios. Luego de eso fueron creadas las siguientes páginas, con un diseño "placeholder" básico, imaginando lo que será la página de acuerdo a los servicios/funcionalidades que ofrecen: menuDeUsuario, reservarSalon, consultarReservas, consultarSanciones.
De momento, las funcionalidades que dependen de la base de datos y el backend, contienen una funcionalidad "placeholder", que permite probar la página de manera mas interactiva, sin estar vinculada a los datos que necesita. Un ejemplo de esto es que la función de iniciar sesión está hardcodeada a un usuario y contraseña especificos, pero de esta manera podemos probar como es iniciar sesión, y qué pasa cuando el usuario y/o contraseña introducidos son incorrectos.
