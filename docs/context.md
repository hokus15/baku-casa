# Contexto del Sistema

## 1. Dominio

Baku.Casa es una aplicación para la gestión de alquileres de inmuebles en España dirigida a propietarios particulares.

El sistema está orientado a la administración de contratos de arrendamiento, control financiero asociado y cumplimiento de obligaciones fiscales derivadas del alquiler.

---

## 2. Marco Legal y Territorial

- Ámbito geográfico: España.
- Moneda: Euro (EUR).
- Calendario: Gregoriano.
- Normativa fiscal relevante: IRPF, IVA (Modelo 303).
- Los porcentajes y reglas fiscales deben alinearse con normativa española vigente.

El sistema no contempla inicialmente soporte multi-país.

---

## 3. Modelo Operativo

- Sistema self-hosted.
- Uso en red local (LAN).
- No orientado a SaaS público.
- Inicialmente modelo de usuario único.
- Interacción principal vía API HTTP y bot de mensajería.

---

## 4. Restricciones Externas

- Debe poder ejecutarse en hardware limitado (ej. Raspberry Pi).
- Recursos computacionales limitados.
- No se requiere alta concurrencia masiva.
- No se requiere alta disponibilidad distribuida.

---

## 5. Supuestos de Uso

- Número reducido de propiedades.
- Volumen moderado de transacciones mensuales.
- Uso doméstico o pequeña escala.
- Los usuarios no son técnicos avanzados en contabilidad.

---

## 6. No Objetivos

El sistema no pretende:

- Ser un ERP generalista.
- Gestionar múltiples empresas independientes.
- Ofrecer multi-tenancy SaaS.
- Sustituir asesoría fiscal profesional.
- Implementar un sistema contable completo de doble partida.

---

## 7. Relación con la Arquitectura

Este documento define el entorno y restricciones externas.

Las decisiones técnicas derivadas de estas restricciones se formalizan exclusivamente en los ADR.