# SHORTY-SHELL
Practica numero 1 topicos especiales en telemática

### Integrantes:

- Isabel Piedrahita
- Santiago Santacruz
- Duvan andres ramirez


## 1. Especificación del Servicio

El presente es un servicio de acortar y generar códigos QR para links de internet. Esto se hizo con la intención de que el usuario pueda enviar los links al servidor para después generar unos más cortos y además compartir el código QR por terminal para su uso.

Para efectos de facilidad de uso se desarrolló una shell interactiva llamada ShortyShell para el cliente, en la que se implementaron además de los comandos básicos de ShortyShell comandos de ayuda para el usuario. Estos comandos de ayuda listan la sintaxis correcta de cada una de estas operaciones y explican lo que cada una hace. Las instrucciones para llamar a estas ayudas son visibles cuando el cliente accede a ShortyShell.

Finalmente, algunas consideraciones adicionales sobre el servicio. El comportamiento del servidor se presta para manejar a multiples clientes de manera concurrente por medio de threads, cada cliente puede conectarse y desconectarse del servidor en el momento que lo considere. Por último, para garantizar la transparencia en operaciones, tanto el servidor como el cliente generan un log en donde sus actividades son visibles y fácilmente rastreables.


## 2. Vocabulario del Mensaje

ShortyShell utiliza una misma estructura de mensaje para todas sus comunicaciones;
| Mensaje | Descripción   |
|------|------|
| SHORT <URL> | Recorta un URL  |
| QR <URL> | Genera un QR con el URL |
| REQUESTS | Lista todos los Requests hechos, teniendo en cuenta Request |
| bye | termina la sesión |

## 3. Regla de Procedimientos

La estructura general del protocolo se explica en el siguiente diagrama.


![image](https://user-images.githubusercontent.com/46933082/129646563-6540094b-d36d-40c8-8ff7-3c1fadba9ac3.png)


Los mensajes que puede enviar el cliente están definidos de la siguiente forma. En la tabla verá significado semántico en la columna de procedimiento, mientras que en la columna de URL encontrará el URL correspondiente, en la que es muy fácil deducir a que se refiere el código y por ende no se pondrá entre paréntesis su significado. Todas estas peticiones de cliente son independientes entre si y el servidor no requiere mantener información de estado para manejar estas.

Los mensajes recibidos son todos muy similares en estructura, contienen un output que representa la información que se le debe mostrar al cliente. Este output es una string. Siempre que se envía un mensaje, se debe esperar un mensaje de respuesta.

Los errores en ShortyShell se manejan mediante la captura de excepciones, hay principalmente tres tipos de error, error de conección y error en tipo de dato. Los errores de coneccion se manejan levantando una excepción de tipo RuntimeError("socket connection broken"), no retornan nada al cliente. Los mensajes de falla en tipo de dato se manejan capturando la excepción y retornando al usuario un mensaje de error que quiere decir que alguno de los valores ingresados no se encuentra en la forma correcta.A continuación hay una tabla con cada error y los mensajes que imprime en la consola interactiva.
| Error | Mensaje   |
|------|------|
| Error de conexión |  |
| Error de tipo |  |

### 4. Regla de protocolo

Para la comunicacion entre los diferentes nodos y cliente, al manejarlo por un IPC de tipo independiente, el cual no se ve afectada la ejecuccion de los otros procesos mientras esta cooperando. El Inter-process comunication (IPC), es el mecanismo el cual nos permite cominicarnos y sincronizar las acciones entre los diferentes nodos. En nuestra arquitectura de comunicacion, estamos implementando la de sockets, por medio de la capa de transporte TCP. Esto lo hacemos ya que TCP es un protocolo confiable, y va a esperar un largo, largo tiempo antes de rendirse con una conexión.

https://docs.python.org/es/3/howto/sockets.html
https://www.geeksforgeeks.org/inter-process-communication-ipc/
