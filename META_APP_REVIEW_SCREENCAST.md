# Meta App Review — Guion de grabación de pantalla

## Estado de preparación

La grabación solo es válida cuando el flujo usa Meta Graph API de forma real. No presentes
una interfaz simulada. La demostración debe crear una publicación real en una página de
prueba controlada por el propietario y luego leerla nuevamente desde Meta.

## Permisos demostrados

| Permiso | Acción visible en el video |
|---|---|
| `pages_show_list` | La aplicación recupera y muestra las páginas administradas por el usuario. |
| `pages_manage_posts` | El usuario selecciona una página, confirma y publica un post de prueba. |
| `pages_read_engagement` | La aplicación lee el post creado y muestra ID, mensaje, fecha y enlace. |

## Preparación antes de grabar

1. Completa Business Verification cuando Meta la exija.
2. Configura Facebook Login y la URI exacta:
   `https://jadelapp-meta.streamlit.app/`
3. Añade en Streamlit Secrets:
   - `META_APP_ID`
   - `META_APP_SECRET`
   - `META_REDIRECT_URI`
   - `META_GRAPH_VERSION`
4. Confirma que la cuenta usada en el video:
   - tiene un rol dentro de la app mientras esté en modo desarrollo;
   - administra una página de prueba;
   - puede crear y eliminar publicaciones en esa página.
5. Abre la app en una ventana limpia del navegador.
6. Cierra gestores de contraseñas, notificaciones, correo, terminales y paneles con secretos.
7. Prepara un mensaje de prueba sin datos personales.
8. Configura la grabación a 1080p y mueve el cursor lentamente.

## Duración recomendada

Entre 3 y 5 minutos. No aceleres las partes donde se autoriza o usa cada permiso.

## Guion exacto

### 00:00–00:15 — Identificación

Mostrar la URL completa de la app y decir:

> Esta es Jadel Pages API en el dominio jadelapp-meta.streamlit.app. La aplicación permite
> que un administrador autorizado seleccione una página de Facebook y publique contenido
> únicamente después de una confirmación explícita.

### 00:15–00:35 — Privacidad y control

Abrir brevemente:

- `?view=privacy`
- `?view=data-deletion`

Decir:

> La aplicación publica su política de privacidad y las instrucciones de eliminación de
> datos. Los tokens no se muestran ni se guardan en el repositorio.

### 00:35–01:10 — Facebook Login

Abrir `?view=review-demo`, pulsar **Continuar con Facebook** y mostrar la pantalla de
consentimiento.

Decir:

> Se solicitan solo pages_show_list, pages_read_engagement y pages_manage_posts. El usuario
> puede cancelar o autorizar. No se solicitan permisos de anuncios, mensajes o grupos.

No muestres App Secret, tokens, Streamlit Secrets ni la consola del navegador.

### 01:10–01:40 — `pages_show_list`

Después del login, mostrar la lista devuelta por la aplicación y seleccionar manualmente
la página de prueba.

Decir:

> La aplicación usa pages_show_list para recuperar únicamente las páginas que administra
> la persona autenticada. No conecta una página automáticamente; el usuario debe elegirla.

### 01:40–02:30 — `pages_manage_posts`

Escribir o revisar un mensaje de prueba, marcar la confirmación y pulsar **Publicar**.

Mensaje recomendado:

> [Meta App Review Test] Publicación autorizada desde Jadel Pages API.

Decir:

> La aplicación usa pages_manage_posts únicamente después de que el usuario selecciona la
> página, revisa el contenido y confirma la operación.

### 02:30–03:15 — `pages_read_engagement`

Mostrar el resultado leído nuevamente desde Meta: ID, mensaje, fecha y enlace permanente.
Abrir el enlace en Facebook y comprobar que el post existe.

Decir:

> La aplicación usa pages_read_engagement para leer y confirmar el contenido publicado por
> la página seleccionada y mostrar el resultado al administrador.

### 03:15–03:45 — Limpieza y desconexión

Volver a la app, eliminar la publicación de prueba y pulsar **Desconectar sesión**.

Decir:

> La publicación de prueba puede eliminarse y los tokens se eliminan de la memoria de la
> sesión. La aplicación no realiza publicaciones automáticas en esta demostración.

## Texto para la descripción de uso

### `pages_show_list`

Jadel Pages API utiliza `pages_show_list` después de Facebook Login para mostrar al usuario
las páginas que administra. El usuario selecciona manualmente una página antes de realizar
cualquier otra acción. La aplicación no conecta páginas no seleccionadas.

### `pages_manage_posts`

Jadel Pages API utiliza `pages_manage_posts` para publicar contenido que el administrador
ha escrito, revisado y confirmado expresamente. La publicación se envía únicamente a la
página seleccionada. La aplicación no publica automáticamente en la demostración.

### `pages_read_engagement`

Jadel Pages API utiliza `pages_read_engagement` para leer y confirmar la publicación creada
por la página seleccionada, mostrando su identificador, mensaje, fecha y enlace permanente
al administrador autorizado.

## Instrucciones para el revisor

1. Abra `https://jadelapp-meta.streamlit.app/?view=review-demo`.
2. Pulse **Continuar con Facebook**.
3. Autorice los permisos solicitados.
4. Seleccione una página que administre.
5. Revise el mensaje, marque la confirmación y pulse **Publicar**.
6. Compruebe la información leída y abra el enlace de Facebook.
7. Elimine el post de prueba y desconecte la sesión.

Si el entorno de revisión requiere una cuenta específica, proporcione credenciales válidas
en las notas privadas de App Review, nunca en GitHub ni dentro del video.

## Motivos de rechazo que este guion evita

- Mostrar solo la página principal.
- Mostrar Graph API Explorer o Postman en lugar de la aplicación.
- No mostrar la pantalla de consentimiento.
- No demostrar cada permiso con una acción real.
- Publicar manualmente desde Facebook.
- Ocultar el resultado final.
- Solicitar permisos que la aplicación no usa.
- Mostrar tokens, App Secret o credenciales.
- Entregar una URL que requiere acceso no documentado.
- Usar un video diferente de los pasos escritos para el revisor.

## Control final

- [ ] La app está desplegada y accesible.
- [ ] Facebook Login funciona desde la URL pública.
- [ ] La URI de redirección coincide exactamente.
- [ ] La cuenta administra una página de prueba.
- [ ] La publicación aparece realmente en Facebook.
- [ ] La app lee el post y muestra el enlace.
- [ ] La eliminación del post funciona.
- [ ] No aparecen secretos ni datos privados.
- [ ] El video coincide con las instrucciones enviadas.
- [ ] Se solicita solo el conjunto mínimo de permisos.
