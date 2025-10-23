# 📜 Contrato de API - Tarot de Marsella

## Información General

- **Nombre:** Tarot API
- **Versión:** 1.0.0
- **Base URL:** `http://localhost:8000`
- **Formato:** JSON
- **Autenticación:** Ninguna (por ahora)
- **Última actualización:** 2025-10-23

---

## 🔗 Endpoints

### 1. Health Check

Verifica que el servicio está activo.

```http
GET /health
```

#### Response exitosa (200)

```json
{
  "status": "ok",
  "message": "running in docker"
}
```

---

### 2. Listar Cartas

Obtiene todas las cartas del Tarot de Marsella (22 Arcanos Mayores).

```http
GET /api/cards
```

#### Response exitosa (200)

```json
[
  {
    "id": 1,
    "name": "El Mago",
    "arcana": "Mayor",
    "number": 1,
    "keywords": ["acción", "poder", "manifestación"],
    "meaning_upright": "Habilidad para manifestar deseos.",
    "meaning_reversed": "Manipulación o falta de dirección.",
    "energy": 2,
    "image": "https://.../el_mago.png"
  },
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
]
```

#### Esquema de Card

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | Identificador único de la carta (1-22) |
| `name` | string | Nombre de la carta |
| `arcana` | string | Tipo de arcano (siempre "Mayor") |
| `number` | integer | Número del arcano (0-21) |
| `keywords` | array[string] | Palabras clave asociadas |
| `meaning_upright` | string | Significado normal |
| `meaning_reversed` | string | Significado invertido |
| `energy` | integer | Valor energético (-2, 0, +2) |
| `image` | string | URL de la imagen |

---

### 3. Generar Predicción

Crea una lectura del tarot basada en 3 cartas seleccionadas.

```http
POST /api/predictions
Content-Type: application/json
```

#### Request Body

```json
{
  "card_ids": [1, 7, 13],
  "seed": 123
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `card_ids` | array[integer] | ✅ Sí | Array con exactamente 3 IDs de cartas válidas (1-22) |
| `seed` | integer | ❌ No | Semilla para reproducibilidad de la predicción |

#### Validaciones

- `card_ids` debe tener exactamente 3 elementos
- Cada ID debe estar entre 1 y 22
- No puede haber IDs duplicados

#### Response exitosa (200)

```json
{
  "id": "pred_abc123",
  "card_ids": [1, 7, 13],
  "cards": [
    {
      "id": 1,
      "name": "El Mago",
      "energy": 2
    },
    {
      "id": 7,
      "name": "El Carro",
      "energy": 2
    },
    {
      "id": 13,
      "name": "La Muerte",
      "energy": 0
    }
  ],
  "total_energy": 4,
  "result": "Muy positiva",
  "interpretation": "Las cartas indican un momento de gran claridad y éxito...",
  "created_at": "2025-10-21T14:30:00Z"
}
```

#### Esquema de Prediction

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | string | ID único de la predicción |
| `card_ids` | array[integer] | IDs de las cartas usadas |
| `cards` | array[object] | Información resumida de cada carta |
| `total_energy` | integer | Suma de energías (-6 a +6) |
| `result` | string | Clasificación del resultado |
| `interpretation` | string | Texto interpretativo generado |
| `created_at` | string (ISO 8601) | Timestamp de creación |

#### Clasificación de Resultados

| Total Energy | Result |
|--------------|--------|
| +4 a +6 | "Muy positiva" |
| +1 a +3 | "Positiva leve" |
| 0 a -1 | "Neutral" |
| -2 o menos | "Desafíos" |

#### Error: Validación (422)

```json
{
  "detail": [
    {
      "loc": ["body", "card_ids"],
      "msg": "ensure this value has at least 3 items",
      "type": "value_error.list.min_items"
    }
  ]
}
```

#### Casos de Error Comunes

| Caso | Código | Response |
|------|--------|----------|
| Menos de 3 cartas | 422 | Detalle de validación |
| Más de 3 cartas | 422 | Detalle de validación |
| IDs fuera de rango | 422 | Detalle de validación |
| IDs duplicados | 422 | Detalle de validación |
| Body malformado | 422 | Detalle de validación |
| Endpoint no implementado | 501 | `{"detail": "Not Implemented"}` |
| Error interno | 500 | `{"detail": "Internal server error"}` |

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | Solicitud exitosa |
| 422 | Unprocessable Entity | Validación fallida |
| 501 | Not Implemented | Endpoint en desarrollo |
| 500 | Internal Server Error | Error del servidor |

---

## 🎯 Reglas de Negocio

### Energías de Cartas

Cada carta tiene un valor energético:
- **+2**: Energía positiva
- **0**: Energía neutra
- **-2**: Energía negativa

Rango total de una predicción: **-6 a +6** (3 cartas × ±2)

### Clasificación de Predicciones

```
+4 a +6  → "Muy positiva"
+1 a +3  → "Positiva leve"
 0 a -1  → "Neutral"
-2 o menos → "Desafíos"
```

---

## 📝 Estado de Implementación

| Endpoint | Estado | Notas |
|----------|--------|-------|
| `GET /health` | ✅ Implementado | Funcionando correctamente |
| `GET /api/cards` | ⚠️ En desarrollo | Retorna 501 temporalmente |
| `POST /api/predictions` | ⚠️ En desarrollo | Retorna 501 temporalmente |

---

## 🔗 Documentación Interactiva

Una vez que el servidor esté corriendo:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

FastAPI genera automáticamente estas documentaciones interactivas.

---

## 📞 Soporte

Para consultas sobre este contrato:
- **Responsable**: Federico Musa (Arquitectura / BD)
- **Issues**: [GitHub Issues](https://github.com/tu-repo/tarot_back/issues)

---

## 📄 Changelog

### v1.0.0 - 2025-10-23
- Versión inicial del contrato
- Definición de 3 endpoints base
- Esquemas de datos establecidos