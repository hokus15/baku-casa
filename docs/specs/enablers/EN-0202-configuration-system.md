# EN-0202: Configuration System

---

## Objetivo

Introducir un sistema centralizado y tipado para gestionar la configuración de la aplicación a partir de variables de entorno, ficheros y valores por defecto de forma consistente entre entornos, reduciendo ambigüedad operativa y evitando configuraciones divergentes.

Un enabler **NO introduce funcionalidad de dominio visible para el usuario final**.  
Su objetivo es habilitar el desarrollo, la operación o la evolución segura de las features.

---

## Alcance

Este enabler introduce capacidades relacionadas con:

- definición centralizada y tipada de parámetros de configuración
- validación temprana y resolución determinista de configuración entre múltiples fuentes

El enabler afecta principalmente a:

- backend y configuración transversal de runtime y testing

Este enabler **NO introduce cambios funcionales en el dominio**.

---

## Fuera de alcance

- gestión externa de secretos, feature flags o configuración dinámica runtime
- cambios funcionales en la lógica de negocio o definición de nuevas capacidades de dominio

---

## Problema que resuelve

A medida que la aplicación incorpora más componentes, la configuración tiende a dispersarse en múltiples lugares y formatos. Esto provoca inconsistencias entre entornos, dificultades de despliegue y riesgos de errores por configuración incompleta o incorrecta. Sin una fuente única de verdad para los parámetros configurables, el sistema pierde reproducibilidad y aumenta el riesgo de defaults implícitos o divergentes.

---

## Capacidad introducida

Este enabler introduce la siguiente capacidad en el sistema:

- la configuración de la aplicación puede declararse y resolverse de manera tipada y centralizada
- el sistema aplica una precedencia determinista entre variables de entorno, ficheros y valores por defecto
- la aplicación valida la configuración en el arranque, falla de forma temprana ante errores y emite diagnóstico cuando aparecen claves no declaradas

La capacidad debe describirse **en términos de resultado**, no de implementación.

---

## Impacto en el sistema

Áreas potencialmente afectadas:

- configuración de runtime de todos los componentes del backend
- seguridad operativa, testing y despliegue self-hosted por consistencia entre entornos

Si el enabler afecta a múltiples áreas debe indicarse claramente.

---

## Dependencias

Este enabler puede depender de:

- F-0001
- ninguna otra dependencia estructural definida para este enabler

Las dependencias estructurales se definen en:

docs/planning/dependency-graph.yaml

Este documento **NO define dependencias**.

---

## Relación con ADR

Si el enabler depende de decisiones arquitectónicas existentes, debe referenciar los ADR relevantes.

- ADR-0013 — Configuration System
- ADR-0002 — Hexagonal Architecture

Los enablers **NO deben redefinir decisiones arquitectónicas** ya documentadas.

---

## Criterios de aceptación

El enabler se considera completado cuando:

- existe un sistema centralizado de configuración con una definición tipada de parámetros configurables
- la configuración puede resolverse de forma determinista a partir de variables de entorno, ficheros y valores por defecto siguiendo la precedencia `environment variables > config file > defaults`
- la aplicación valida la configuración durante el arranque y reporta el conjunto completo de errores detectados cuando la configuración no es válida
- las claves de configuración no declaradas generan un warning de diagnóstico pero no bloquean el arranque
- la configuración es consistente entre entornos y no depende de convenciones implícitas ni de valores hardcoded dispersos
