-- Script de configuración de la base de datos para el sistema de detección de placas

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS placas;

-- Usar la base de datos
USE placas;

-- Crear la tabla para el registro de placas
CREATE TABLE IF NOT EXISTS registro_placas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    origen VARCHAR(50) DEFAULT 'Cámara IP',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento de las consultas
CREATE INDEX idx_placa ON registro_placas(placa);
CREATE INDEX idx_fecha ON registro_placas(fecha);

-- Añadir usuario de aplicación (opcional - ajustar según necesidades)
-- CREATE USER 'placas_app'@'localhost' IDENTIFIED BY 'password_seguro';
-- GRANT SELECT, INSERT, UPDATE ON placas.* TO 'placas_app'@'localhost';
-- FLUSH PRIVILEGES; 