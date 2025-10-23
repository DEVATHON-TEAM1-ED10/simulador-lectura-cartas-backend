# 🤝 Acuerdos de Interfaz - Tarot API

## Contexto

Este documento define el contrato de comunicación entre el **Frontend** (cliente web) y el **Backend** (FastAPI) para la aplicación de Tarot de Marsella.

**Responsables:**
- **Frontend**: V. NietoDev
- **Backend**: Federico Musa
- **Última actualización**: 2025-10-23

---

## 1. Protocolo de Comunicación

### Configuración Base

- **Protocolo:** HTTP/HTTPS
- **Formato de datos:** JSON
- **Encoding:** UTF-8
- **Content-Type:** `application/json`

### Headers Requeridos

Todas las requests deben incluir:

```http
Content-Type: application/json
Accept: application/json
```

---

## 2. Flujos de Interacción

### 🎬 Flujo 1: Inicialización de la Aplicación

```
1. Frontend inicia la app
   ↓
2. Frontend → GET /health
   Backend → 200 {"status": "ok"}
   ↓
3. Frontend → GET /api/cards
   Backend → 200 + [22 cartas]
   ↓
4. Frontend renderiza el mazo completo
```

**Acuerdos:**
- Backend debe responder `/api/cards` en **menos de 2 segundos**
- Frontend implementará timeout de **5 segundos**
- Si falla `/health`, mostrar mensaje de error y no continuar

---

### 🎴 Flujo 2: Selección de Cartas

```
1. Usuario selecciona carta (click)
   ↓
2. Frontend valida:
   - ¿Ya tiene 3 cartas? → No permite más selecciones
   - ¿Carta ya seleccionada? → La deselecciona
   ↓
3. Cuando tiene exactamente 3:
   - Habilita botón "Generar Predicción"
```

**Acuerdos:**
- Frontend **NO** llama al backend hasta tener 3 cartas válidas
- Frontend valida localmente:
  - ✅ Exactamente 3 cartas
  - ✅ Sin duplicados
  - ✅ IDs válidos (1-22)

---

### 🔮 Flujo 3: Generar Predicción

```
1. Usuario presiona "Generar Predicción"
   ↓
2. Frontend:
   - Deshabilita botón
   - Muestra loading/spinner
   - Prepara payload
   ↓
3. Frontend → POST /api/predictions
   {
     "card_ids": [1, 7, 13],
     "seed": 42  // opcional
   }
   ↓
4. Backend:
   - Valida datos
   - Calcula energía
   - Genera interpretación
   ↓
5. Backend → 200 + predicción completa
   ↓
6. Frontend:
   - Oculta loading
   - Renderiza resultado con animación
   - Habilita opción "Nueva lectura"
```

**Acuerdos:**
- Backend debe responder en **menos de 3 segundos**
- Frontend implementará timeout de **10 segundos**
- Si timeout, mostrar: "El servidor tardó demasiado, intenta nuevamente"

---

## 3. Manejo de Errores

### Responsabilidades del Frontend

#### Validaciones Pre-envío

Antes de llamar a `/api/predictions`, validar:

```javascript
function validarSeleccion(cardIds) {
  // ✅ Exactamente 3 cartas
  if (cardIds.length !== 3) {
    return { valido: false, error: "Debes seleccionar 3 cartas" };
  }
  
  // ✅ Sin duplicados
  if (new Set(cardIds).size !== 3) {
    return { valido: false, error: "No puedes seleccionar la misma carta dos veces" };
  }
  
  // ✅ IDs válidos (1-22)
  if (cardIds.some(id => id < 1 || id > 22)) {
    return { valido: false, error: "IDs de cartas inválidos" };
  }
  
  return { valido: true };
}
```

#### Manejo de Respuestas del Backend

```javascript
async function generarPrediccion(cardIds) {
  try {
    const response = await fetch('/api/predictions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ card_ids: cardIds }),
      signal: AbortSignal.timeout(10000) // timeout 10s
    });
    
    // Manejo por código de estado
    switch (response.status) {
      case 200:
        const prediction = await response.json();
        mostrarPrediccion(prediction);
        break;
        
      case 422:
        const errorValidacion = await response.json();
        mostrarError("Error de validación", errorValidacion.detail);
        break;
        
      case 501:
        mostrarMensaje("Esta funcionalidad está en desarrollo");
        break;
        
      case 500:
        mostrarError("Error del servidor", "Intenta nuevamente en unos momentos");
        break;
        
      default:
        mostrarError("Error inesperado", `Código: ${response.status}`);
    }
    
  } catch (error) {
    if (error.name === 'TimeoutError') {
      mostrarError("Tiempo de espera agotado", "El servidor tardó demasiado");
    } else if (error.name === 'TypeError') {
      mostrarError("Error de conexión", "No se pudo conectar con el servidor");
    } else {
      mostrarError("Error inesperado", error.message);
    }
  }
}
```

### Responsabilidades del Backend

#### Siempre Retornar JSON Estructurado

```python
# ✅ Correcto
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# ❌ Incorrecto - no retornar HTML o plain text
```

#### Formato de Errores Estándar

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

---

## 4. Estados de la UI

### Loading States

| Acción | Frontend | Backend | Timeout Frontend |
|--------|----------|---------|------------------|
| Cargar cartas | Skeleton/Spinner | < 2 segundos | 5 segundos |
| Generar predicción | Loading overlay | < 3 segundos | 10 segundos |

### Error States

```
❌ Error de red
   → "No se pudo conectar con el servidor"
   → Botón "Reintentar"

❌ Error 422
   → Mostrar mensaje específico del backend
   → Botón "Entendido"

❌ Error 501
   → "Esta funcionalidad está en desarrollo"
   → Sin botón de reintento

❌ Error 500
   → "Error del servidor, intenta en unos momentos"
   → Botón "Reintentar"
```

---

## 5. Convenciones de Datos

### IDs de Cartas

- **Tipo:** `integer`
- **Rango:** 1 a 22 (inclusive)
- **Invariante:** Corresponden a los 22 Arcanos Mayores

### Timestamps

- **Formato:** ISO 8601
- **Ejemplo:** `"2025-10-21T14:30:00Z"`
- **Timezone:** Siempre UTC (terminado en Z)

**Frontend:**
```javascript
// Parsear timestamp
const fecha = new Date(prediction.created_at);
console.log(fecha.toLocaleString()); // Muestra en hora local del usuario
```

### Valores de Energía

| Valor | Significado |
|-------|-------------|
| -2 | Negativa |
| 0 | Neutra |
| +2 | Positiva |

**Total de predicción:** -6 a +6

### Clasificación de Resultados

Valores exactos que retorna el backend:

```javascript
const RESULTADOS = {
  MUY_POSITIVA: "Muy positiva",
  POSITIVA_LEVE: "Positiva leve",
  NEUTRAL: "Neutral",
  DESAFIOS: "Desafíos"
};
```

**Acuerdo:**
- Frontend puede usar estos strings para mostrar:
  - Colores diferentes
  - Iconos específicos
  - Animaciones acordes
- Backend **siempre** retorna uno de estos 4 valores exactos

---

## 6. Performance y Caché

### Caché de Cartas

```javascript
// Frontend puede cachear las cartas en sessionStorage
async function obtenerCartas() {
  const cacheKey = 'tarot_cards';
  const cached = sessionStorage.getItem(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const response = await fetch('/api/cards');
  const cards = await response.json();
  
  sessionStorage.setItem(cacheKey, JSON.stringify(cards));
  return cards;
}
```

**Acuerdos:**
- Las cartas no cambian durante la sesión
- Frontend **puede y debe** cachearlas localmente
- Backend no necesita implementar cache headers (por ahora)

### Optimizaciones Futuras

- **Compresión:** Backend enviará `Content-Encoding: gzip` (a implementar)
- **Rate Limiting:** No implementado por ahora
- **Paginación:** No necesaria (solo 22 cartas)

---

## 7. Testing del Contrato

### Casos de Prueba Críticos

Ambos equipos deben verificar estos casos:

#### ✅ Happy Path

```javascript
// Test: Predicción exitosa
POST /api/predictions
Body: { "card_ids": [1, 7, 13] }

Espera:
- Status: 200
- Body contiene: id, card_ids, cards, total_energy, result, interpretation, created_at
- total_energy es un número entre -6 y 6
- result es uno de: "Muy positiva", "Positiva leve", "Neutral", "Desafíos"
```

#### ❌ Error Cases

```javascript
// Test 1: Menos de 3 cartas
POST /api/predictions
Body: { "card_ids": [1, 7] }
Espera: 422

// Test 2: Más de 3 cartas
Body: { "card_ids": [1, 7, 13, 19] }
Espera: 422

// Test 3: IDs duplicados
Body: { "card_ids": [1, 1, 7] }
Espera: 422

// Test 4: IDs fuera de rango
Body: { "card_ids": [0, 7, 13] }
Espera: 422

// Test 5: ID inválido (mayor a 22)
Body: { "card_ids": [1, 7, 99] }
Espera: 422

// Test 6: Campo faltante
Body: { "seed": 123 }
Espera: 422

// Test 7: JSON malformado
Body: "{ card_ids: [1,7,13]"  // Sin comillas en clave
Espera: 422
```

### Suite de Tests Compartida

Ambos equipos usarán el mismo archivo de casos de prueba:

📄 `tests/integration/api_contract_tests.json`

```json
{
  "test_cases": [
    {
      "name": "Predicción exitosa con 3 cartas válidas",
      "request": {
        "method": "POST",
        "endpoint": "/api/predictions",
        "body": { "card_ids": [1, 7, 13] }
      },
      "expected": {
        "status": 200,
        "body_schema": "Prediction"
      }
    }
    // ... más casos
  ]
}
```

---

## 8. Ambientes

### Desarrollo Local

```
Backend:  http://localhost:8000
Frontend: http://localhost:3000  (o el puerto configurado)
```

### Staging (Futuro)

```
Backend:  https://staging-api.tarot-marsella.com
Frontend: https://staging.tarot-marsella.com
```

### Producción (Futuro)

```
Backend:  https://api.tarot-marsella.com
Frontend: https://tarot-marsella.com
```

**Acuerdo:**
- Frontend usará variable de entorno `VITE_API_URL` (o similar)
- **NUNCA** hardcodear URLs
- Configuración por ambiente:

```javascript
// .env.development
VITE_API_URL=http://localhost:8000

// .env.production
VITE_API_URL=https://api.tarot-marsella.com
```

---

## 9. Versionado de la API

### Estrategia Actual

- **Sin versionado en URLs** por ahora
- Si hay cambios, se coordinan entre equipos antes de implementar

### Cambios Permitidos (No-Breaking)

Estos pueden hacerse sin aviso previo:

- ✅ Agregar campos nuevos al response
- ✅ Agregar endpoints nuevos
- ✅ Agregar parámetros opcionales
- ✅ Mejorar mensajes de error

### Cambios que Requieren Coordinación (Breaking)

Estos **DEBEN** avisarse con al menos 1 semana de anticipación:

- ❌ Eliminar campos existentes
- ❌ Cambiar tipos de datos
- ❌ Cambiar estructura de respuestas
- ❌ Cambiar códigos de estado
- ❌ Cambiar valores de enumeraciones

**Proceso:**
1. Backend crea issue en GitHub describiendo el cambio
2. Frontend revisa y aprueba
3. Se acuerda fecha de implementación
4. Backend implementa en rama separada
5. Frontend adapta su código
6. Se hace merge coordinado

---

## 10. Comunicación entre Equipos

### Canales

- **GitHub Issues**: Para bugs y features
- **Pull Requests**: Para cambios en contratos
- **[Especificar canal]**: Para consultas rápidas (Discord/Slack/Telegram)

### Responsables

| Área | Responsable |
|------|-------------|
| Contrato de API | Federico Musa |
| Integración Frontend | V. NietoDev |
| Infraestructura | Tulio |
| Repositorio | Mirko (SrStamm19) |

### Reportar Problemas

#### Frontend encuentra error en el backend

```markdown
**Título**: [BUG] POST /api/predictions retorna 500 con IDs válidos

**Descripción**:
- Endpoint: POST /api/predictions
- Body enviado: {"card_ids": [1, 7, 13]}
- Status recibido: 500
- Esperado: 200

**Pasos para reproducir**:
1. Seleccionar cartas 1, 7 y 13
2. Hacer click en "Generar Predicción"
3. Ver error en consola

**Logs del navegador**:
```
[adjuntar screenshot o logs]
```
```

#### Backend encuentra inconsistencia en frontend

Similar pero desde perspectiva del backend.

---

## ✅ Checklist de Integración

Antes de considerar la integración completa:

### Frontend

- [ ] Maneja todos los códigos de estado (200, 422, 501, 500)
- [ ] Muestra errores de forma amigable al usuario
- [ ] Implementa timeouts (5s para cards, 10s para predictions)
- [ ] Valida datos antes de enviar al backend
- [ ] Cachea las cartas en sessionStorage
- [ ] UI muestra loading states apropiados
- [ ] Tests de integración pasando

### Backend

- [ ] Retorna siempre JSON estructurado
- [ ] Valida todos los inputs según el contrato
- [ ] Responde en menos de 3 segundos
- [ ] Logs de errores implementados
- [ ] Tests unitarios pasando
- [ ] Tests de integración pasando
- [ ] CORS configurado correctamente

### Conjunto

- [ ] Suite de tests compartida ejecutándose en CI/CD
- [ ] Documentación Swagger accesible
- [ ] README actualizado con instrucciones de integración
- [ ] Variables de ambiente documentadas

---

## 📚 Referencias

- [Contrato de API completo](./API_CONTRACT.md)
- [Guía de integración](./INTEGRATION_GUIDE.md)
- [Swagger UI](http://localhost:8000/docs)

---

## 📝 Changelog

### v1.0.0 - 2025-10-23
- Versión inicial de los acuerdos
- Definición de flujos de comunicación
- Establecimiento de responsabilidades por equipo