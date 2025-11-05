# Bitácora

Primero planificamos y organizamos el proyecto en jira con una filosofia SCRUM y dividimos los tres pilares principales de nuestro proyecto (base de datos, backend y frontend) en sprints de 1, 2 y 1 semana respectivamente.

Comenzamos creando el respositorio y la estructura del proyecto. Investigamos acerca de docker, especificamente acerca del docker-compose.yaml y como utilizarlo en nuestro proyecto. Creamos el compose.yaml en la carpeta del proyecto y configuramos la base de datos para posteriormente conectarnos desde dataGrip.

Con el contenedor levantado y configurado, nos conectamos a la base de datos desde dataGrip y ejecutamos los comandos de creacion de tablas. Estos comandos los guardamos en un archivo schema.sql asi cuando alguien clone el respositorio y ejecute nuestro compose.yaml con docker automaticamente se le ejecuten los mismos comandos que usamos nosotros para que funcione nuestra aplicación. Esto es porque pusimos en el compose.yaml que los volumenes del contenedor carguen los archivos data y schema.

Con las tablas ya creadas pasamos a crear los datos que vamos a usar para la verificación y demostración de nuestra aplicación. Insertamos en sus respectivas tablas y verificamos que este todo correcto y que nos permita su correcto uso a futuro.


ENDPOINTS :
# '/login'
[
  [
    1,
    "fmachado@ucu.edu.uy",
    "admin123",
    "10000001"
  ],
  [
    2,
    "afernandez@ucu.edu.uy",
    "ana123",
    "10000002"
  ],
  [
    3,
    "cperez@ucu.edu.uy",
    "carlos123",
    "10000003"
  ],
  [
    4,
    "mrodriguez@ucu.edu.uy",
    "maria123",
    "10000004"
  ]
]

------------------------------
# '/reservas'
[
  [
    1,
    1,
    "2025-10-25",
    1,
    "activa"
  ],
  [
    2,
    2,
    "2025-10-25",
    2,
    "cancelada"
  ],
  [
    3,
    3,
    "2025-10-26",
    3,
    "activa"
  ],
  [
    4,
    4,
    "2025-10-26",
    4,
    "finalizada"
  ]
]

