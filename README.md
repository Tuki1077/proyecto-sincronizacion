# proyecto-sincronizacion
Repositorio para el proyecto de sincronización para Sistemas Operativos UFM

Keneth Ruiz 20210104
Juan Luis Fernandez 20200112

# Sistema de Sincronización de Procesos

Este proyecto implementa un sistema de sincronización de procesos utilizando sockets para la comunicación entre un servidor y un cliente en diferentes computadoras. El sistema se basa en el problema clásico del buffer limitado, utilizando semáforos para la sincronización.

## Características

- **Servidor (Listener):** Inicializa un servidor que escucha en un puerto específico, maneja un buffer limitado de solicitudes y utiliza múltiples hilos para procesar estas solicitudes en paralelo.
- **Cliente:** Permite a los usuarios conectar con el servidor para enviar solicitudes de escaneo de directorios. El cliente puede reintentar automáticamente si el servidor está ocupado.

## Requisitos

- Python 3.6 o superior
- Acceso a una red local o configuración para pruebas locales

## Configuración y Ejecución

### Servidor

Para iniciar el servidor, usa el siguiente comando desde la terminal, especificando el puerto, el tamaño del buffer y el número de hilos:

```bash
python3 server.py <puerto> <elementos en buffer> <hilos>
```
### Cliente

Para iniciar el cliente, usa el siguiente comando desde la terminal, especificando el ip, el puerto y el path:

```bash
python3 client.py <ip> <puerto> <path>
