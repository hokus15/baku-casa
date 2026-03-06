# EN-0202: Configuration System

## Objetivo
Introducir un sistema centralizado y tipado para gestionar la configuración de la aplicación (variables de entorno, ficheros, valores por defecto) de forma consistente entre entornos, reduciendo ambigüedad operativa y evitando configuraciones divergentes.

---

## Descripción
A medida que la aplicación incorpora más componentes (persistencia, autenticación, notificaciones, logging, etc.), la configuración tiende a dispersarse en múltiples lugares y formatos. Esto provoca inconsistencias entre entornos, dificultades de despliegue y riesgos de errores por configuración incompleta o incorrecta.

Este enabler define un sistema de configuración único que permita:
- declarar parámetros de configuración de manera tipada
- aplicar valores por defecto de forma explícita
- soportar múltiples fuentes (variables de entorno, ficheros, defaults)
- validar configuración en el arranque para fallar de forma temprana ante errores

El sistema debe ser consistente y reproducible para los distintos entornos (dev, test, prod) sin introducir decisiones de implementación en esta fase.

---

## Root afectado
- `backend/`

---

## Incluye
- Definición de un “source of truth” centralizado para configuración de la aplicación.
- Configuración tipada:
  - tipos explícitos (por ejemplo strings, ints, booleans, URLs)
  - validaciones de rango/formato cuando aplique
- Soporte de múltiples fuentes de configuración:
  - variables de entorno
  - ficheros de configuración
  - valores por defecto definidos explícitamente
- Reglas de precedencia entre fuentes (orden determinista).  
  - Política global fija de precedencia: `environment variables > config file > defaults`.
- Separación clara de configuración por entorno (por ejemplo `dev`, `test`, `prod`).
- Validación y carga de configuración durante el arranque:
  - fallar temprano si falta configuración requerida
  - fallar temprano si la configuración no es válida
  - si existen errores de validación, el sistema debe fallar el arranque reportando el **conjunto completo de errores detectados**, no solo el primero.
- Manejo de claves de configuración no declaradas:
  - las claves no declaradas están permitidas
  - deben generar un **warning de diagnóstico**
  - no deben bloquear el arranque de la aplicación
- Requisitos de configuración:
  - solo existen **claves requeridas globales**
  - no se definen mínimos obligatorios de claves específicos por entorno
- Convenciones para:
  - nombres estables de claves de configuración
  - compatibilidad con despliegues self-hosted (incluyendo Docker)
- Garantía de que el sistema de configuración no introduce dependencias que violen la arquitectura hexagonal.

---

## Fuera de alcance
- Gestión de secretos externa (vaults, KMS, etc.).
- Sistemas de feature flags.
- Configuración dinámica runtime (hot reload).
- Cambios funcionales en la lógica de negocio.

---

## Notas de arquitectura
- La configuración debe ser consumible por componentes de Infrastructure/Adapters sin filtrar detalles hacia Domain.
- La configuración de testing debe ser segura y explícita para evitar uso accidental de entornos persistentes.
- La definición tipada y validada mejora la reproducibilidad del desarrollo y despliegue.

---

## Criterios de aceptación
1. Existe un sistema centralizado de configuración con una definición tipada de parámetros.
2. La configuración puede resolverse de forma determinista a partir de variables de entorno, ficheros y defaults.
3. Existen reglas de precedencia claras y documentadas entre las fuentes de configuración (`environment variables > config file > defaults`).
4. La aplicación valida la configuración en el arranque y falla de forma temprana ante errores, reportando el conjunto completo de errores detectados.
5. Las claves de configuración no declaradas generan un warning pero no bloquean el arranque.
6. Solo existen claves requeridas globales; no hay mínimos obligatorios específicos por entorno.
7. La configuración es consistente entre entornos (`dev`, `test`, `prod`) y no depende de convenciones implícitas.
8. El sistema de configuración respeta la arquitectura hexagonal y no introduce dependencias indebidas en Domain.