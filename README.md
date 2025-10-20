🃏 Tarot API – Backend Devathon 2025

Backend del proyecto Tarot de Marsella (tema Halloween)
Construido con FastAPI + Docker, estructurado para ser escalable y fácil de mantener.
Este repositorio constituye la arquitectura base, lista para que cada integrante del equipo desarrolle su parte.
--______________________________________________________________________________________________________
📁 Estructura general del proyecto

tarot_back/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── cards.py
│   │       └── predictions.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── session.py
│   │   └── seed.py
│   ├── models/
│   │   ├── card.py
│   │   └── prediction.py
│   ├── schemas/
│   │   ├── card.py
│   │   └── prediction.py
│   ├── services/
│   │   └── prediction_engine.py
│   └── main.py
│
├── tests/
│   ├── test_cards.py
│   └── test_predictions.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
└── README.md
_____________________________________________________________________

⚙️ Requisitos previos

Docker Desktop instalado y ejecutándose
(Debe verse el ícono de la ballena y decir Engine running).

Puerto 8000 libre (puede cambiarse a 8080 si es necesario).

(Opcional) Git instalado para clonar el repositorio.

__________________________________________________________________

🐳 Uso de Docker – Guía paso a paso
🧩 1. Conceptos básicos

  Imagen → define el entorno de ejecución.

  Contenedor → la instancia activa de esa imagen.

  Volumen → espacio persistente (ej. base de datos o código montado).

  🚀 2. Construir y ejecutar

  Desde la raíz del proyecto usando Powershell (un comando por vez):
  docker compose build
  docker compose up

  Uvicorn running on http://0.0.0.0:8000
  Application startup complete.

Luego, abrí:

Swagger Docs → http://localhost:8000/docs

Healthcheck → http://localhost:8000/health

  Si devuelve:

  {"status": "ok", "message": "running in docker"}

  ####IMPORTANTE: CERRAR DOCKER DESDE LA TERMINAL######
  CTRL + C
  docker compose down

  _______________________________________________________________


  🔁 4. Hot Reload

Cualquier cambio que guardes en los archivos .py
se detecta automáticamente por uvicorn.
Si no recarga, verificá que el docker-compose.yml tenga:

    volumes:
      - .:/app:delegated
_____________________________________________________________________
🧠 5. Acceso al contenedor

Para entrar dentro del contenedor:

docker exec -it tarot_api sh
# Ejemplo dentro:
ls -la app
python --version
exit
___________________________________________________________________
🔧 6. Cambiar el puerto del host

Si el puerto 8000 está ocupado, editá docker-compose.yml:

ports:
  - "8080:8000"

lUEGO:
docker compose down
docker compose up --build

Y accedé a: http://localhost:8080

___________________________________________________________________

🔄 7. Cuándo usar rebuild

Usá rebuild solo si cambian dependencias o el Dockerfile:
  docker compose down
  docker compose build
  docker compose up
Cambios normales en código .py → no requieren rebuild.
___________________________________________________________________
🧩 Endpoints disponibles (MVP base)

| Método | Endpoint           | Descripción                                    | Estado          |
| ------ | ------------------ | ---------------------------------------------- | --------------- |
| GET    | `/health`          | Verifica que el contenedor y la app funcionen  | ✅ Implementado  |
| GET    | `/api/cards`       | Lista las cartas (stub)                        | ⚠️ Devuelve 501 |
| POST   | `/api/predictions` | Recibe 3 cartas y genera una predicción (stub) | ⚠️ Devuelve 501 |
curl -X POST http://localhost:8000/api/predictions \
  -H "Content-Type: application/json" \
  -d '{"card_ids":[1,7,13],"seed":123}'
______________________________________________________________________________________________________


🔮 Tarot de Marsella — Base del proyecto
  🎴 Baraja

    Se utiliza el Tarot de Marsella, compuesto por los 22 Arcanos Mayores.

    Ejemplo de estructura JSON:

    {
  "id": 19,
  "name": "El Sol",
  "arcana": "Mayor",
  "number": 19,
  "keywords": ["claridad", "energía", "éxito"],
  "meaning_upright": "Éxito, vitalidad y claridad.",
  "meaning_reversed": "Exceso de optimismo o expectativas.",
  "energy": 2,
  "image": "https://.../el_sol.png"
}
  La energía de cada carta puede ser:

      +2 → positiva

      0 → neutra

      -2 → negativa


🪄 Predicciones (por implementar)

La predicción sumará las energías de las tres cartas seleccionadas:

Total de energía	Resultado
+4 a +6	Muy positiva
+1 a +3	Positiva leve
0 a -1	Neutral
-2 o menos	Desafíos

(Actual endpoint retorna 501 — aún sin lógica aplicada)
__________________________________________________________________________________

👥 Roles del equipo
| Integrante            | Rol               | Responsabilidades                                   |
| --------------------- | ----------------- | --------------------------------------------------- |
| **Federico Musa**     | Arquitectura / BD | Estructura base, modelado de datos y seed de cartas |
| **Mirko (SrStamm19)** | Repositorio       | Administración de ramas, merges y revisiones        |
| **Tulio**             | Infraestructura   | Configuración de Docker, dependencias y entorno     |
| **V. NietoDev**       | Frontend / Docs   | Integración visual, endpoints y documentación       |


___________________________________________________________________________________

🧪 Tests básicos (stub)

  Ejecutar dentro del contenedor:
    docker compose exec api pytest -v
Casos esperados:

GET /health → 200

GET /api/cards → 501

POST /api/predictions válido → 501

POST /api/predictions con error (menos de 3 cartas) → 422